---
title: Plugins
description: Gameyfin Plugin Development Guide
icon: material/power-plug
---

## How Gameyfin Plugins work

Gameyfin plugins are designed to extend the functionality of the application by allowing developers to create custom features or integrate with external services.
Plugins can be used to fetch game metadata, provide download capabilities, or add new features to the Gameyfin ecosystem.

Plugins can be enabled or disabled in the Admin UI at runtime, but Gameyfin has to be restarted if after you (un)install a plugin.

### Types of Plugins

Gameyfin currently supports two types of plugins:

- **Game Metadata Plugins**: These plugins are used to fetch metadata for games from external sources.
- **Download Provider Plugins**: These plugins are used to provide download functionality for games.

## Bundled Plugins

Gameyfin comes with several bundled plugins that provide essential functionality:

- **IGDB Metadata Plugin**: This plugin fetches game metadata from IGDB.
- **Steam Metadata Plugin**: This plugin fetches game metadata from Steam using <em>undocumented</em> APIs.
- **SteamGridDB Metadata Plugin**: This plugin fetches only covers from SteamGridDB.
- **Direct Download Plugin**: This plugin allows your users to directly download games in their web browser.