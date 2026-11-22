#!/usr/bin/env python3
"""Generate web configuration reference from the checked-out ConfigProperties.kt.

This deliberately supports only the literal metadata expressions used by Gameyfin.
New Kotlin expressions must be supported explicitly; unsupported syntax fails the
build instead of publishing incomplete or guessed defaults.
"""

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess


SOURCE = Path("app/src/main/kotlin/org/gameyfin/app/config/ConfigProperties.kt")
FIELDS = ("type", "key", "name", "description", "default", "allowedValues", "min", "max", "step")
CONSTRUCTOR = (
    "val type: KClass<T>", "val key: String", "val name: String", "val description: String",
    "val default: T? = null", "val allowedValues: List<T>? = null",
    "val min: Number? = null", "val max: Number? = null", "val step: Number? = null",
)
# Spring Boot's public LogLevel enum. All other enums must be defined in the source.
EXTERNAL_ENUMS = {"LogLevel": ["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL", "OFF"]}


class MetadataError(ValueError):
    """The source no longer fits the supported metadata grammar."""


@dataclass(frozen=True)
class Token:
    kind: str
    text: str


def tokenize(source):
    pattern = re.compile(
        r'(?P<space>\s+)|(?P<comment>//[^\n]*|/\*[\s\S]*?\*/)'
        r'|(?P<raw>"""[\s\S]*?""")|(?P<string>"(?:\\.|[^"\\])*\")'
        r'|(?P<number>\d+)|(?P<word>[A-Za-z_][A-Za-z_0-9]*)|(?P<symbol>.)'
    )
    tokens = []
    for match in pattern.finditer(source):
        kind = match.lastgroup
        if kind not in ("space", "comment"):
            tokens.append(Token(kind, match.group()))
    return tokens


def split_arguments(tokens):
    result, current, depth = [], [], 0
    for token in tokens:
        if token.text in ("(", "[", "<"):
            depth += 1
        elif token.text in (")", "]", ">"):
            depth -= 1
        if token.text == "," and depth == 0:
            if not current:
                raise MetadataError("Empty argument")
            result.append(current)
            current = []
        else:
            current.append(token)
    if depth != 0:
        raise MetadataError("Unbalanced metadata expression")
    if current:
        result.append(current)
    return result


def decode_string(token):
    if token.kind == "raw":
        value = token.text[3:-3]
        if "$" in value:
            raise MetadataError("String interpolation is unsupported")
        return value
    value = token.text[1:-1]
    result, index = [], 0
    escapes = {"t": "\t", "b": "\b", "n": "\n", "r": "\r", "f": "\f", '"': '"', "'": "'", "\\": "\\", "$": "$"}
    while index < len(value):
        char = value[index]
        if char == "$":
            raise MetadataError("String interpolation is unsupported")
        if char != "\\":
            result.append(char)
            index += 1
            continue
        index += 1
        if index >= len(value):
            raise MetadataError("Incomplete string escape")
        char = value[index]
        if char == "u":
            digits = value[index + 1:index + 5]
            if not re.fullmatch(r"[0-9a-fA-F]{4}", digits):
                raise MetadataError("Invalid Unicode escape")
            result.append(chr(int(digits, 16)))
            index += 5
        elif char in escapes:
            result.append(escapes[char])
            index += 1
        else:
            raise MetadataError(f"Unsupported Kotlin escape: \\{char}")
    return "".join(result)


def evaluate(tokens, enums):
    texts = [token.text for token in tokens]
    if len(tokens) == 1:
        token = tokens[0]
        if token.kind in ("string", "raw"):
            return decode_string(token)
        if token.kind == "number":
            return int(token.text)
        if token.text in ("true", "false", "null"):
            return {"true": True, "false": False, "null": None}[token.text]
    if len(tokens) == 2 and texts[0] == "-" and tokens[1].kind == "number":
        return -int(texts[1])
    if len(tokens) == 5 and tokens[0].kind in ("string", "raw") and texts[1:] == [".", "trimMargin", "(", ")"]:
        lines = decode_string(tokens[0]).splitlines()
        if lines and not lines[0].strip():
            lines.pop(0)
        if lines and not lines[-1].strip():
            lines.pop()
        return "\n".join(re.sub(r"^\s*\|", "", line) for line in lines)
    if len(tokens) >= 3 and texts[0:2] == ["arrayOf", "("] and texts[-1] == ")":
        return [evaluate(argument, enums) for argument in split_arguments(tokens[2:-1])]
    if len(tokens) == 3 and texts[1] == "." and texts[0] in enums:
        values = enums[texts[0]]
        if texts[2] == "entries":
            return list(values)
        if texts[2] in values:
            return texts[2]
    raise MetadataError("Unsupported metadata expression: " + " ".join(texts))


def closing(tokens, start, opener, closer):
    depth = 0
    for index in range(start, len(tokens)):
        if tokens[index].text == opener:
            depth += 1
        elif tokens[index].text == closer:
            depth -= 1
            if depth == 0:
                return index
    raise MetadataError(f"Missing closing {closer}")


def validate_constructor(tokens):
    declarations = [index for index in range(len(tokens) - 1)
                    if [token.text for token in tokens[index:index + 2]] == ["class", "ConfigProperties"]]
    if len(declarations) != 1:
        raise MetadataError("Expected exactly one ConfigProperties constructor declaration")
    index = declarations[0] + 2
    if [token.text for token in tokens[index:index + 5]] != ["<", "T", ":", "Serializable", ">"]:
        raise MetadataError("Unsupported ConfigProperties type parameter declaration")
    start = index + 5
    if start >= len(tokens) or tokens[start].text != "(":
        raise MetadataError("Missing ConfigProperties constructor")
    end = closing(tokens, start, "(", ")")
    arguments = split_arguments(tokens[start + 1:end])
    actual = [[token.text for token in argument] for argument in arguments]
    expected = [[token.text for token in tokenize(argument)] for argument in CONSTRUCTOR]
    if actual != expected:
        raise MetadataError("ConfigProperties constructor schema changed; update the parser before generating documentation")


def parse_properties(source):
    tokens = tokenize(source)
    validate_constructor(tokens)
    enums = dict(EXTERNAL_ENUMS)
    for index in range(len(tokens) - 3):
        if [token.text for token in tokens[index:index + 2]] == ["enum", "class"]:
            if tokens[index + 3].text != "{":
                raise MetadataError("Only literal enum declarations are supported")
            end = closing(tokens, index + 3, "{", "}")
            body = tokens[index + 4:end]
            if any(token.kind != "word" and token.text != "," for token in body):
                raise MetadataError("Only literal enum entries are supported")
            values = [part[0].text for part in split_arguments(body) if len(part) == 1]
            if len(values) != len(split_arguments(body)):
                raise MetadataError("Unsupported enum entry")
            enums[tokens[index + 2].text] = values

    entries, keys = [], set()
    inherited_count = sum(
        [token.text for token in tokens[index:index + 3]] == [":", "ConfigProperties", "<"]
        for index in range(len(tokens) - 2)
    )
    for index in range(len(tokens) - 2):
        if [token.text for token in tokens[index:index + 2]] != ["data", "object"]:
            continue
        if [token.text for token in tokens[index + 3:index + 6]] != [":", "ConfigProperties", "<"]:
            raise MetadataError("Unsupported configuration object declaration")
        end_type = closing(tokens, index + 5, "<", ">")
        type_name = "".join(token.text for token in tokens[index + 6:end_type])
        if type_name not in ("Boolean", "Int", "String", "Array<String>") and type_name not in enums:
            raise MetadataError(f"Unsupported configuration type: {type_name}")
        if end_type + 1 >= len(tokens) or tokens[end_type + 1].text != "(":
            raise MetadataError("Expected metadata constructor")
        end = closing(tokens, end_type + 1, "(", ")")
        entry, named, seen_fields = {"type": type_name}, False, set()
        arguments = split_arguments(tokens[end_type + 2:end])
        for position, argument in enumerate(arguments):
            if len(argument) > 2 and argument[1].text == "=":
                named = True
                field, expression = argument[0].text, argument[2:]
            else:
                if named or position >= len(FIELDS):
                    raise MetadataError("Invalid positional metadata argument")
                field, expression = FIELDS[position], argument
            if field not in FIELDS or field in seen_fields:
                raise MetadataError(f"Unknown or duplicate metadata field: {field}")
            seen_fields.add(field)
            if field == "type":
                if "".join(token.text for token in expression) != type_name + "::class":
                    raise MetadataError("Metadata type does not match configuration type")
            else:
                entry[field] = evaluate(expression, enums)
        if "type" not in seen_fields:
            raise MetadataError("Missing metadata type")
        for field in ("key", "name", "description"):
            if not isinstance(entry.get(field), str) or not entry[field]:
                raise MetadataError(f"Missing string metadata field: {field}")
        if not re.fullmatch(r"[a-z0-9]+(?:[.-][a-z0-9]+)*", entry["key"]):
            raise MetadataError(f"Unsupported configuration key: {entry['key']}")
        if entry["key"] in keys:
            raise MetadataError(f"Duplicate configuration key: {entry['key']}")
        keys.add(entry["key"])
        entries.append(entry)
    if not entries or len(entries) != inherited_count:
        raise MetadataError("Some configuration declarations were not parsed")
    anchors = [entry["key"].replace(".", "-") for entry in entries]
    if len(anchors) != len(set(anchors)):
        raise MetadataError("Configuration keys produce duplicate documentation anchors")
    return entries


def display(value):
    if value is None:
        return "Not set"
    if isinstance(value, list):
        return ", ".join(display(item) for item in value)
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def render(entries, revision="main"):
    base = f"https://github.com/gameyfin/gameyfin/blob/{revision}/{SOURCE.as_posix()}"
    lines = ["---", "title: Configuration reference", "icon: material/book-open-variant", "---", "", "# Configuration reference", "", "<!-- Generated by scripts/generate_configuration.py. Do not edit manually. -->", "",
             "These settings are configured in the administration interface, not through environment variables.", "",
             f"Defaults and descriptions come from [Gameyfin's configuration definitions]({base}).", "",
             "Paths such as `/swagger-ui.html` refer to your Gameyfin instance, not this documentation site.", ""]
    for entry in entries:
        lines.extend([f'## {entry["name"]} {{ #{entry["key"].replace(".", "-")} }}', "", f'**Key:** `{entry["key"]}`  ',
                      f'**Type:** `{entry["type"]}`  ', f'**Default:** `{display(entry.get("default"))}`', ""])
        if entry.get("allowedValues") is not None:
            lines.extend(["**Allowed values:** " + ", ".join(f"`{display(value)}`" for value in entry["allowedValues"]), ""])
        constraints = [f"{field}: `{entry[field]}`" for field in ("min", "max", "step") if entry.get(field) is not None]
        if constraints:
            lines.extend(["**Constraints:** " + "; ".join(constraints), ""])
        lines.extend([entry["description"].replace("[Swagger UI](/swagger-ui.html)", "`/swagger-ui.html`"), ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=Path("external/gameyfin"))
    parser.add_argument("--output", type=Path, default=Path("docs/configuration/reference.md"))
    args = parser.parse_args()
    try:
        entries = parse_properties((args.source_root / SOURCE).read_text(encoding="utf-8"))
        revision = subprocess.run(["git", "-C", str(args.source_root), "rev-parse", "HEAD"],
                                  check=True, capture_output=True, text=True).stdout.strip()
        result = render(entries, revision)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
    except (OSError, MetadataError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Configuration generation failed: {error}\n")
    print(f"Generated {len(entries)} configuration options: {args.output}")


if __name__ == "__main__":
    main()
