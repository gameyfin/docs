---
title: Plugins
description: Extend Gameyfin through the plugin marketplace
icon: material/power-plug
---

# Plugins

Gameyfin ships without pre-installed plugins. Install the features you need from the marketplace during setup or under **Administration → Plugins**.

## What plugins provide

- **Game metadata:** descriptions, platforms, artwork, and other information from sources such as IGDB and Steam.
- **Downloads:** browser downloads or alternative transfer methods such as torrents.
- **Game stores:** store product lookup, version/build information, DLC, and edition suggestions.
- **Background tasks:** scheduled or manually started work, with progress and logs.
- **Notifications and actions:** messages to users and optional actions handled by a plugin.

One plugin can implement several extension points.
Marketplace installation, updates, and removal load or unload plugins at runtime without restarting the whole application.

## For administrators

Follow [Managing plugins](../configuration/plugins.md) to install, configure, enable, and prioritize providers.
Read [Plugin security](security.md) before installing third-party code.

## For developers

Start with the [tutorial](tutorial.md), then use the [API guide](info-for-devs.md) for the available extension points and host services.
