---
icon: material/puzzle
---

# Managing plugins

Open **Administration → Plugins** to browse the marketplace and manage installed plugins.
New installations contain no pre-installed plugins. The final setup step offers the same marketplace.

## Install and enable

1. Choose a plugin in the marketplace and install it.
2. Follow installation progress in the task popover.
3. Open the installed plugin's configuration and read its provider-specific instructions.
4. Enter required settings, save, and validate the configuration.
5. Enable the plugin.

Metadata providers are needed for library scanning. A download provider is needed for downloads.
Store providers supply product search, version/build information, DLC, and edition suggestions. Plugins may also contribute background tasks.
Installation, updates, and removal through the marketplace do not require a full Gameyfin restart.
Trusted official plugins can start automatically if their configuration is valid. Unsigned third-party plugins require explicit enablement.

## Priorities

Use the priority controls to order providers for each extension type.
Metadata from higher-priority providers takes precedence when results are merged; lower-priority providers fill missing fields.
Download priorities determine the order of available download methods.

## Updates and removal

Use the marketplace to check for updates and install compatible releases.
Before updating or removing a plugin, let its active work finish and keep any data you need.
A plugin's tasks and functionality become unavailable while it is disabled or removed.

## Additional marketplaces and trust

You can add a marketplace by name and URL in the marketplace controls.
Only use repositories and plugins you trust: plugins run inside Gameyfin with the application's access to files and network.
See [Plugin security](../plugins/security.md) for signature checks and trust levels.

If installation fails, check task logs, network access, the release's Gameyfin version requirement, and signature status.
For manually installed development JARs, follow the [developer tutorial](../plugins/tutorial.md).
