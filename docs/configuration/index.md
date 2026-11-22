---
title: Configuration
description: Configure Gameyfin through the administration interface
icon: material/cog
---

# Configuration

Log in as an administrator and open **Administration** from your avatar menu.
Most settings are saved in Gameyfin's database through this interface.
They are separate from the [startup settings](startup.md) passed to Docker or Spring Boot.

Start with [Getting started](../installation/getting-started.md) if this is your first installation.

## Administration guide

- [Libraries and collections](libraries.md): add folders, scan games, and manage unmatched paths.
- [Game requests](requests.md): let users request additions to your library.
- [Downloads](downloads.md): manage downloads and per-user bandwidth limits.
- [Users](users.md): accounts, registration, and approval.
- [Security and SSO](sso.md): public access, API documentation, and identity providers.
- [API keys](api.md): credentials for integrations.
- [Messages](messages.md): email notifications and templates.
- [Plugins](plugins.md): marketplace installation, configuration, and priority.
- [Tasks](tasks.md): schedules, background work, progress, and history.
- [Logs](logs.md): troubleshooting and log retention.
- [System](system.md): backups, restore, database changes, and restart.

## Complete settings reference

The [Configuration reference](reference.md) is generated from `ConfigProperties.kt` in the same Gameyfin checkout used for the Docker examples.
It lists every declared web setting with its key, type, description, default, and declared constraints.
Plugin settings and task settings come from their own definitions and are described in their respective interfaces.
Use the administration guides for workflows; use the reference to look up exact values.
