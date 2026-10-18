---
title: Information for Developers
description: Specific information for developers who want to understand how to work with the plugin system
---

!!! example "Unstable Feature"

    Gameyfin's plugin API is currently in an **unstable** state.
    Expect breaking changes until the release of `2.0.0` (probably even after that).
    Gameyfin `2.5.0` introduces breaking changes in the plugin API.  
    Update existing plugins to the new interfaces before compiling them against the latest `plugin-api` artifact.

# How to create a Plugin

The plugin system is based on [PF4J](https://github.com/pf4j/pf4j) which allows you to create plugins in Java or Kotlin.
Depending on the type of plugin you want to create, you will need to implement the appropriate interfaces.  
The Gameyfin Plugin API is published as a Maven artifact
on [Maven Central](https://central.sonatype.com/artifact/org.gameyfin/plugin-api), so you can easily include it in your
project.

For a quick start, you can follow the [tutorial](tutorial.md).

## Structure of a Plugin

A Gameyfin plugin typically consists of the following components:

### Plugin Manifest

The plugin manifest is a Manifest file that contains metadata about the plugin.
It should be located in the `META-INF/MANIFEST.MF` file of your plugin JAR file.

| Field                          | Description                                                                                                                                                         |
|--------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Plugin-Version                 | Version of the plugin in [SemVer](https://semver.org) format                                                                                                        |
| Plugin-Class                   | Fully qualified class name of your plugin wrapper class                                                                                                             |
| Plugin-Id                      | Unique ID for your plugin. It is recommended to either use a unique [reverse-DNS](https://en.wikipedia.org/wiki/Reverse_domain_name_notation) identifier or a UUID. |
| Plugin-Name                    | Name of your plugin                                                                                                                                                 |
| Plugin-Description             | Description of the functionality of your plugin in [Markdown](https://commonmark.org/) format. Use `<br>` for line breaks and start suceeding lines with one space. |
| Plugin-Author                  | Name(s) of the plugin authors (if the plugin has multiple authors, use a comma-separated string)                                                                    |
| _Plugin-Short-Description[^1]_ | Shorter description of your plugin (not in Markdown). Used primarily for display in various smaller UI elements (falls back to "Plugin-Description" if empty).      |
| _Plugin-Url[^1]_               | URL to the website of your plugin (e.g. the GitHub repository containing the plugin source code)                                                                    |
| _Plugin-License[^1]_           | Name of the license for the plugin (e.g. "MIT", "AGLPv3", ...)                                                                                                      |

[^1]: Optional fields that are not required for the plugin to work, but recommended to be set.

### Source Code

Gameyfin plugins are written in Java or Kotlin (although any language that compiles to JVM bytecode can be used in
theory).
The source code of the plugin should be organized in a way that follows the standard Java/Kotlin project structure.

#### Plugin Wrapper Class

The plugin wrapper class is the main class of your plugin that extends either `GameyfinPlugin` or
`ConfigurableGameyfinPlugin` (depending on whether your plugin requires configuration).
Your wrapper class should contain one or more inner classes that implement the necessary interfaces for your plugin
type.
These inner classes will be used by Gameyfin to interact with your plugin and should be annotated with `@Extension`.
Depending on the type of plugin, you will need to implement specific methods that Gameyfin will call to interact with
your plugin.

#### Configurable Plugins

If your plugin requires configuration, you should extend `ConfigurableGameyfinPlugin` instead of `GameyfinPlugin`.
This also means that your plugin will have a configuration page in the Admin UI.
In order for Gameyfin to be able to display the configuration page, your plugin needs to implement two things:

- A `configMetadata` property of type `ConfigMetadata` that contains the metadata of your plugin configuration.
- The `validateConfig` method that validates the configuration and returns a `PluginConfigValidationResult`.

For an example of how to implement plugin configuration, take a look at
the [tutorial](tutorial.md#creating-your-first-plugin).

### Reading data from Gameyfin

Gameyfin plugins can read a snapshot of the host application's data through `GameyfinDataService`.
The service is available via `PluginContext.dataService` and `GameyfinPlugin.dataService`, and it exposes read-only
snapshots of games, libraries and collections.

This is especially useful for plugins that register tasks, because tasks can inspect the current host state without
mutating it.
For example, a task can count all games in the installation, filter them by IDs selected in the task UI, or generate
reports based on the configured libraries.

Available methods include:

- `getGames()` / `getGames(ids)` / `getGame(id)`
- `getGamesOfLibrary(libraryId)`
- `getLibraries()` / `getLibrary(id)`
- `getCollections()` / `getCollection(id)`

### Registering Tasks

Starting with Gameyfin `2.5.0`, plugins can contribute background tasks by implementing `GameyfinTask` and annotating
the implementation with `@Extension`.

A task can define:

- a stable `key` that is used for scheduling and persisted settings,
- a human-readable `name` and `description`,
- an optional default cron schedule,
- settings that administrators can change in the UI,
- parameters that admins can pass when manually starting the task,
- and the `execute(context)` method that performs the work.

Task implementations receive a `TaskContext` that provides:

- `setting(key)` and `parameter(key)` accessors,
- cancellation checks via `isCancellationRequested` / `throwIfCancelled()`,
- progress reporting with `progress(...)`,
- and `wrap(...)` helpers to keep logs attached to work done on other threads.

See the [tutorial](tutorial.md) for a small end-to-end example that combines a metadata provider with a task that reads
host data.

