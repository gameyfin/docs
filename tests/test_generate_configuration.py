"""Regression checks for configuration metadata extraction and rejected syntax."""

import importlib.util
import os
from pathlib import Path
import sys
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/generate_configuration.py"
SPEC = importlib.util.spec_from_file_location("generate_configuration", SCRIPT)
generator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = generator
SPEC.loader.exec_module(generator)


SCHEMA = '''sealed class ConfigProperties<T : Serializable>(
    val type: KClass<T>,
    val key: String,
    val name: String,
    val description: String,
    val default: T? = null,
    val allowedValues: List<T>? = null,
    val min: Number? = null,
    val max: Number? = null,
    val step: Number? = null
) {}
'''


def definition(default='false', type_name="Boolean", extra=""):
    return SCHEMA + f'''data object Example : ConfigProperties<{type_name}>(
        {type_name}::class, "test.example", "Example", "Description"{", " + default if default else ""}{extra}
    )'''


class ConfigurationGeneratorTest(unittest.TestCase):
    def test_literals_and_absent_default(self):
        self.assertFalse(generator.parse_properties(definition())[0]["default"])
        entry = generator.parse_properties(definition("", "String"))[0]
        self.assertNotIn("default", entry)
        self.assertIn("**Default:** `Not set`", generator.render([entry]))

    def test_escape_sequences_and_regex(self):
        source = definition(r'"^[^\\[]+\n\t\u0041\$"', "String")
        self.assertEqual("^[^\\[]+\n\tA$", generator.parse_properties(source)[0]["default"])

    def test_multiline_trim_margin(self):
        source = definition('''"""
            |First line.
            |Second line.
        """.trimMargin()''', "String")
        self.assertEqual("First line.\nSecond line.", generator.parse_properties(source)[0]["default"])

    def test_arrays_and_named_constraints(self):
        entry = generator.parse_properties(definition('arrayOf("zip", "tar",)', "Array<String>"))[0]
        self.assertEqual(["zip", "tar"], entry["default"])
        entry = generator.parse_properties(definition("default = 4", "Int", ", min = 1, max = 16, step = 1"))[0]
        self.assertEqual((4, 1, 16, 1), tuple(entry[field] for field in ("default", "min", "max", "step")))

    def test_local_and_external_enum_values(self):
        source = 'enum class MatchUsersBy { username, email }\n' + definition("MatchUsersBy.username", "MatchUsersBy", ", MatchUsersBy.entries")
        entry = generator.parse_properties(source)[0]
        self.assertEqual(["username", "email"], entry["allowedValues"])
        entry = generator.parse_properties(definition("LogLevel.INFO", "LogLevel", ", LogLevel.entries"))[0]
        self.assertEqual(["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL", "OFF"], entry["allowedValues"])

    def test_fail_closed_for_unknown_expressions_and_types(self):
        for expression in ('computeDefault()', '42L', '"hello $name"', '"\\q"', 'arrayOf("zip") + extra', 'listOf("zip")'):
            with self.subTest(expression=expression), self.assertRaises(generator.MetadataError):
                generator.parse_properties(definition(expression, "String"))
        with self.assertRaises(generator.MetadataError):
            generator.parse_properties(definition("true", "NewType"))

    def test_duplicate_and_unsupported_declarations(self):
        for source in (definition() + definition().replace(SCHEMA, ""), definition().replace("data object", "object"),
                       definition() + '\nobject Another : ConfigProperties<Boolean>(Boolean::class)',
                       definition().replace('"Description"', '"Description", surprise = true'),
                       definition().replace('"Description"', '"Description", default = true, default = false')):
            with self.subTest(source=source), self.assertRaises(generator.MetadataError):
                generator.parse_properties(source)

    def test_changed_constructor_schema_and_defaults_fail(self):
        for source in (
            definition().replace("val name: String,\n    val description: String,", "val description: String,\n    val name: String,"),
            definition().replace("val min: Number? = null", "val min: Number? = 0"),
            definition().replace("val default: T? = null", "val default: T? = computeDefault()"),
            definition().replace("val name: String", "val name: CharSequence"),
            definition().replace("val step: Number? = null", "val step: Number? = null, val extra: Boolean = false"),
            definition().replace(SCHEMA, ""),
        ):
            with self.subTest(source=source), self.assertRaises(generator.MetadataError):
                generator.parse_properties(source)

    def test_anchor_collisions_fail(self):
        first = definition().replace('"test.example"', '"test.a-b"')
        second = definition().replace(SCHEMA, "").replace('"test.example"', '"test-a.b"')
        with self.assertRaisesRegex(generator.MetadataError, "duplicate documentation anchors"):
            generator.parse_properties(first + second)

    def test_truncated_declarations_fail_cleanly(self):
        for body in ("data object Example : ConfigProperties<Boolean>",
                     "data object Example : ConfigProperties<Boolean>(",
                     "data object Example : ConfigProperties<",
                     "data object Example"):
            with self.subTest(body=body), self.assertRaises(generator.MetadataError):
                generator.parse_properties(SCHEMA + body)

    def test_generated_anchors_and_revision(self):
        rendered = generator.render(generator.parse_properties(definition()), "deadbeef")
        self.assertIn("{ #test-example }", rendered)
        self.assertIn("/blob/deadbeef/", rendered)

    def test_real_gameyfin_source(self):
        source_root = Path(os.environ.get("GAMEYFIN_SOURCE_ROOT", "external/gameyfin"))
        source_path = source_root / generator.SOURCE
        if not source_path.is_file():
            self.fail("Initialize external/gameyfin or set GAMEYFIN_SOURCE_ROOT to run the source integration test")
        source = source_path.read_text(encoding="utf-8")
        entries = generator.parse_properties(source)
        self.assertEqual(source.count("data object "), len(entries))
        properties = {entry["key"]: entry for entry in entries}
        self.assertFalse(properties["library.scan.enable-filesystem-watcher"]["default"])
        self.assertEqual(4, properties["library.scan.max-concurrency"]["default"])
        self.assertEqual(["openid", "profile", "email", "roles"], properties["sso.oidc.oauth-scopes"]["default"])
        self.assertEqual(len(entries), generator.render(entries).count("**Key:**"))


if __name__ == "__main__":
    unittest.main()
