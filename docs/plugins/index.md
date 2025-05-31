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

## How to create a Plugin
 
The plugin system is based on [PF4J](https://github.com/pf4j/pf4j) which allows you to create plugins in Java or Kotlin.
Depending on the type of plugin you want to create, you will need to implement the appropriate interfaces.

For quick start, you can use the [Gameyfin Plugin Template](https://github.com/gameyfin/plugin-template).
This template provides a basic structure for creating a Gameyfin plugin, including the necessary dependencies and configuration files.

### Structure of a Plugin

A Gameyfin plugin typically consists of the following components:

#### Plugin Manifest

The plugin manifest is a Manifest file that contains metadata about the plugin.
It should be located in the `META-INF/MANIFEST.MF` file of your plugin JAR file.

| Field                          | Description                                                                                                                                                          |
|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Plugin-Version                 | Version of the plugin in [SemVer](https://semver.org) format                                                                                                         |
| Plugin-Class                   | Fully qualified class name of your plugin wrapper class                                                                                                              |
| Plugin-Id                      | Unique ID for your plugin. It is recommended to either use a unique [reverse-DNS](https://en.wikipedia.org/wiki/Reverse_domain_name_notation) identifier or a UUID.  |
| Plugin-Name                    | Name of your plugin                                                                                                                                                  |
| Plugin-Description             | Description of the functionality of your plugin in [Markdown](https://commonmark.org/) format. Use `<br>` for line breaks and start suceeding lines with one space.  |
| Plugin-Author                  | Name(s) of the plugin authors (if the plugin has multiple authors, use a comma-separated string)                                                                     |
| _Plugin-Short-Description[^1]_ | Shorter description of your plugin (not in Markdown). Used primarily for display where in various smaller UI elements (falls back to "Plugin-Description" if empty). |
| _Plugin-Url[^1]_               | URL to the website of your plugin (e.g. the GitHub repository containing the plugin source code)                                                                     |
| _Plugin-License[^1]_           | Name of the license for the plugin (e.g. "MIT", "AGLPv3", ...)                                                                                                       |

[^1]: Optional fields that are not required for the plugin to work, but recommended to be set.

#### Source Code

Currently, Gameyfin plugins are written in Java or Kotlin.
The source code of the plugin should be organized in a way that follows the standard Java/Kotlin project structure.

##### Plugin Wrapper Class

The plugin wrapper class is the main class of your plugin that extends either `GameyfinPlugin` or `ConfigurableGameyfinPlugin` (depending on whether your plugin requires configuration).
Your wrapper class should contain one or more inner classes that implement the necessary interfaces for your plugin type.
These inner classes will be used by Gameyfin to interact with your plugin and should be annotated with `@Extension`.
Depending on the type of plugin, you will need to implement specific methods that Gameyfin will call to interact with your plugin.

##### Configurable Plugins

If your plugin requires configuration, you should extend `ConfigurableGameyfinPlugin` instead of `GameyfinPlugin`.
This also means that your plugin will have a configuration page in the Admin UI.
In order for Gameyfin to be able to display the configuration page, your plugin needs to implement two things:
- A `configMetadata` property that returns a `ConfigMetadata` object containing the metadata for your plugin configuration.
- The `validateConfig` method that validates the configuration and returns a `PluginConfigValidationResult`.

For an example of how to implement plugin configuration, see the [Hello World Plugin](https://github.com/gameyfin/plugin-template/blob/main/src/main/kotlin/de/grimsi/gameyfinplugins/template/HelloWorldPlugin.kt) from the quick start template.

## Plugin Security

Gameyfin plugins run in the same JVM as the main application, which means they have access to the same resources and can potentially cause security issues.
Gameyfin does not currently implement a security sandbox for plugins, so it is important to only use plugins from trusted sources.
However, Gameyfin does separate the plugins into different trust levels (from most trusted to least trusted) to help you make informed decisions about which plugins to use:

- **Bundled Plugins**: These plugins are included with Gameyfin and are considered safe to use if you download Gameyfin from a trusted source.
- **Official Plugins**: These plugins are developed by the Gameyfin team or trusted contributors and are considered safe to use. They are signed with a digital signature to verify their authenticity.
- **Community Plugins**: These plugins are developed by the community. They are not signed and should be used with caution.
- **Untrusted Plugins**: These plugins are signed, but the signature is invalid or not recognized by Gameyfin. They are considered untrusted and should be used with caution.

Gameyfin will display the trust level of a plugin in the Admin UI, and you can choose to enable or disable plugins based on their trust level.
Also, plugins will only be started automatically after the installation if they are bundled with Gameyfin or signed by a trusted source.
