# Gameyfin documentation

The site uses Zensical.
`docs/configuration/reference.md` is generated from Gameyfins code (do not edit that reference by hand).

## Build locally

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run:

```sh
git submodule update --init --recursive
uv sync --locked
python3 scripts/generate_configuration.py
cp external/gameyfin/app/src/test/resources/openapi/v1.json docs/api/openapi.json
GAMEYFIN_SOURCE_ROOT=external/gameyfin python3 -m unittest discover -s tests -v
uv run zensical build --clean
```

For local preview, generate the configuration reference and copy the API contract first, then run
`uv run zensical serve`.
To compare against another Gameyfin checkout:

```sh
python3 scripts/generate_configuration.py --source-root ../gameyfin
```