---
title: Information for Developers
description: Plugin API, lifecycle, configuration, and publishing reference
icon: material/code-braces
---

# Developing plugins

Gameyfin uses [PF4J](https://pf4j.org/) to load JVM plugins. A plugin contains a wrapper class and one or more extensions.
Use the [tutorial](tutorial.md) for a complete metadata plugin.

This reference follows Gameyfin **2.7.1**. The current source builds with Java 25 and Kotlin 2.4.21.
Depend on `org.gameyfin:plugin-api` using `compileOnly`, and select a version compatible with your target Gameyfin installation.
The API is published on [Maven Central](https://central.sonatype.com/artifact/org.gameyfin/plugin-api).
When developing against an unreleased Gameyfin checkout, publish its API locally with `./gradlew :plugin-api:publishToMavenLocal`.
Add `mavenLocal()` to your plugin's repositories for that case.

!!! warning "API compatibility"

    Do not assume every API release is binary compatible. Rebuild and test your plugin against supported Gameyfin versions.
    Declare the supported Gameyfin versions in `Plugin-Requires` and in your marketplace release metadata.

## Packaging and manifest

The JAR must contain `META-INF/MANIFEST.MF` and a PF4J extension index, `META-INF/extensions.idx`.
Generate the index with an annotation processor suitable for your language, or maintain it explicitly as shown in the tutorial.
Annotate extension classes with `org.pf4j.Extension`. They need public no-argument constructors; do not use Kotlin `inner` classes.

| Manifest attribute | Purpose |
| --- | --- |
| `Plugin-Id` | Stable unique ID. Use a domain or GitHub identity you own; `org.gameyfin.*` is reserved for the Gameyfin team. |
| `Plugin-Version` | Plugin release version in SemVer format. |
| `Plugin-Class` | Fully qualified wrapper class name. |
| `Plugin-Requires` | Supported Gameyfin versions, for example `>=2.7.1 & <3.0.0`. |
| `Plugin-Name` | Display name. |
| `Plugin-Description` | Markdown description. Use `<br>` for line breaks; manifest continuation lines begin with a space. |
| `Plugin-Author` | Author name or comma-separated author names. |
| `Plugin-Short-Description` | Optional plain-text description for compact UI elements. |
| `Plugin-Url` | Optional project URL. |
| `Plugin-License` | Optional license identifier, such as `MIT` or `AGPL-3.0-only`. |
| `Plugin-Dependencies` | Optional PF4J plugin dependencies. See the [PF4J documentation](https://pf4j.org/doc/plugins.html). |

Do not bundle `plugin-api` or PF4J into your JAR. Package any additional runtime dependencies your plugin needs.
A logo named `logo.png`, `logo.jpg`, `logo.jpeg`, `logo.gif`, `logo.svg`, or `logo.webp` can be placed at the classpath root.

## Wrapper, context, and lifecycle

Extend `GameyfinPlugin`, or `ConfigurableGameyfinPlugin` when configuration is needed.
Declare a public constructor accepting `PluginContext`:

```kotlin
class ExamplePlugin(context: PluginContext) : GameyfinPlugin(context)
```

The context supplies `pluginId`, `pluginVersion`, `dataDirectory`, `dataService`, and `notificationService`.
The wrapper also exposes `dataDirectory`, `dataService`, `stateFile`, and a Jackson 3 `ObjectMapper`.
Use the context and public API rather than depending on application implementation classes.

Override PF4J `start()` and `stop()` when needed. Release threads, network clients, and other resources in `stop()`.
Plugins can be stopped and restarted when configuration changes or administrators disable, update, or uninstall them.
Marketplace operations load and unload plugins at runtime. A manually copied JAR requires an application restart for discovery.
Constructors should not perform work that requires an enabled plugin.

### State and files

`dataDirectory` is dedicated to the plugin, but it may not exist yet. Create directories before writing files.
`saveState(state)` writes JSON to `state.json`; `loadState<T>()` returns `null` when the file is missing, empty, or unreadable.
Handle missing or incompatible state explicitly. Coordinate concurrent access yourself; these helpers do not provide transactions or locking.
Use configuration fields for credentials rather than writing secrets into state files.

## Configuration

`ConfigurableGameyfinPlugin` implements `Configurable`. Declare `configMetadata: PluginConfigMetadata`, a list of `ConfigMetadata` entries.
Each entry has a stable `key`, Java `type`, `label`, `description`, optional `default`, `isRequired` (default `true`), and `isSecret` (default `false`).
Enums supply dropdown choices automatically.

```kotlin
import org.gameyfin.pluginapi.core.config.ConfigMetadata
import org.gameyfin.pluginapi.core.config.PluginConfigMetadata
import org.gameyfin.pluginapi.core.wrapper.ConfigurableGameyfinPlugin
import org.gameyfin.pluginapi.core.wrapper.PluginContext

class ExamplePlugin(context: PluginContext) : ConfigurableGameyfinPlugin(context) {
    override val configMetadata: PluginConfigMetadata = listOf(
        ConfigMetadata(
            key = "apiKey",
            type = String::class.java,
            label = "API key",
            description = "Access key issued by the metadata service.",
            isSecret = true
        )
    )
}
```

Read values with `config<T>(key)` or `optionalConfig<T>(key)`. Defaults apply when a stored value is absent.
The required accessor throws `PluginConfigError` for missing values; both accessors can throw for invalid values or unknown keys.
The base class supports strings, numeric primitives, strict booleans, enums, and types exposing a suitable static `valueOf(String)` or `parse(String)` method.

Override `validateConfig(config: Map<String, String?>)` for custom checks.
Call `super.validateConfig(config)` first and return its errors when invalid; it checks required values and types.
Return `PluginConfigValidationResult.VALID` or `PluginConfigValidationResult.INVALID(mapOf("apiKey" to "Explanation"))`.
Do not read the wrapper's currently loaded values when validating a proposed configuration; use the supplied map and account for defaults.

Gameyfin generates the configuration UI and encrypts stored plugin configuration values in its database.
`isSecret` masks a field in the UI; it does not sandbox the plugin. Never log credentials.
Saving configuration restarts the plugin to apply it. Invalid configuration prevents the plugin from starting.

## Metadata providers

Implement `GameMetadataProvider`:

- `supportedPlatforms` declares the platforms the provider supports.
- `fetchByTitle(gameTitle, platformFilter, maxResults)` returns best matches first. Respect platform filters and result limits.
- `fetchById(id)` returns one game or `null` when no match exists.

`GameMetadata` requires `originalId` and `title`. Keep source IDs stable.
Optional fields include `platforms`, `description`, `coverUrls`, `headerUrls`, `release`, `userRating`, `criticRating`,
`developedBy`, `publishedBy`, `genres`, `themes`, `keywords`, `screenshotUrls`, `videoUrls`, `features`, and `perspectives`.
Image and video fields use `Set<URI>`; `release` uses `Instant`. Ratings use the 0–100 scale.
Return an empty list when a title search finds nothing. Use network timeouts for external requests.

## Download providers

Implement `DownloadProvider.download(path: Path)` and return either:

- `FileDownload(data, fileExtension, size, fileName)`, with an `InputStream` and optional metadata.
- `LinkDownload(url)`, for a download hosted elsewhere.

`name`, `description`, and `shortDescription` optionally describe an individual provider; otherwise Gameyfin uses its plugin's manifest.
`describe(path)` can return `DownloadMetadata(fileExtension, size)` without generating a body, for example for HTTP HEAD requests.
Return `null` when this information cannot be obtained cheaply. A `null` size means unknown length.

### Resumable downloads

Override `prepareRangeDownload(path)` when the resource supports byte ranges. Otherwise its default `null` falls back to a full download.
The returned `RangeDownload` provides metadata, a quoted strong HTTP `etag`, and `openStream(offset, length)`.
Open a bounded stream without reading preceding bytes. Closing the stream must close the range resource.
The caller owns the range resource and must close it even when no response body is sent.
Document how your provider keeps bytes stable if underlying files change; the same strong ETag must not identify different content.

### Selected files

Implement `SelectiveDownloadProvider.downloadSelection(root, relativeFiles)` to support downloads of selected files within a game directory.
Gameyfin supplies a canonical root and distinct, validated relative paths.
For one file, return that file directly and set `FileDownload.fileName` to its basename.
For multiple files, return a ZIP preserving relative paths.
Files can change after validation: do not follow a replacement symlink when opening a selected file.

## Store providers

`GameStoreProvider` is independent of metadata providers. A plugin can implement either or both.
It supplies product search, available builds, DLC, and edition suggestions.

Define a constant `store: GameStoreInfo`:

- `id` must remain stable because Gameyfin persists store links with it. Use lower-case letters, digits, and dashes.
- `displayName` names the store.
- `productIdPattern` must match a complete product ID.
- `urlPatterns` extract product IDs from URLs using the first capture group.
- `caseInsensitiveIds` enables lower-case normalization.

`GameStoreInfo.parseProductId(input)` accepts IDs or matching URLs, normalizes them, and returns `null` for invalid input.

Implement the operations your source supports:

| Operation | Result |
| --- | --- |
| `search(query)` | `GameStoreProduct` base games, best matches first. Set `supportsSearch = false` if unsupported. |
| `fetchVersions(productId)` | `GameStoreVersion` entries, newest first. `buildId` is opaque, not a semantic version. |
| `fetchDlc(productId)` | `GameStoreDlc` entries classified as `DLC`, `EDITION_UPGRADE`, or `BONUS`. |
| `suggestEditions(productId)` | Edition names. |

Default methods return empty lists. Throw when version lookup fails because the source is unreachable or the product is unknown.
Multiple plugins may describe the same store ID. Gameyfin uses plugin priority for search and version fallbacks;
it merges DLC and edition names without duplicates. Return empty lists for capabilities your source does not provide.

## Read-only host data

`PluginContext.dataService` and `GameyfinPlugin.dataService` provide `GameyfinDataService`:

- `getGames()`, `getGames(ids)`, `getGame(id)`, and `getGamesOfLibrary(libraryId)`.
- `getLibraries()` and `getLibrary(id)`.
- `getCollections()` and `getCollection(id)`.

Results are snapshots; later host changes are not reflected. Unknown game IDs in a batch are ignored; single-item lookups return `null`.
`GameInfo` includes IDs, title, path, file size, platforms, and release/creation/update timestamps.
`LibraryInfo` includes its ID, name, directories, and platforms. `CollectionInfo` includes its ID, name, description, and game IDs.
These objects do not provide write access to Gameyfin.

## Background tasks

Implement `GameyfinTask` as an indexed `@Extension`. Tasks appear on the administration **Tasks** page while the plugin is started.
They are removed when the plugin stops, and running tasks receive cancellation requests.

Use a stable `key`, unique within the plugin, because schedules and settings persist under that key.
Set a readable `name` and `description`. `defaultSchedule` uses [Spring cron syntax](https://docs.spring.io/spring-framework/reference/integration/scheduling.html#scheduling-cron-expression),
including a seconds field, or macros such as `@daily`. `null` means manual execution by default.
`scheduledByDefault` controls whether the default schedule starts enabled. Administrators can change schedules.

Declare `settings` and `parameters` with `ConfigMetadata`:

- `context.setting<T>(key)` reads persisted settings, falling back to defaults.
- `context.parameter<T>(key)` reads values for one manual run. Scheduled runs use parameter defaults.
- Use `GameSelection` to display a game picker. Resolve its `gameIds` through the data service.

`execute(context)` returns `TaskResult(summary)` or `null`. Exceptions mark a run failed.
Only one run of a given task executes at a time. `TaskContext` includes `runId` and `trigger` (`MANUAL`, `SCHEDULE`, `SYSTEM`, or `WATCHER`).
Report progress with `progress(description, current, total)`.
SLF4J logs on the execution thread appear in the run log. Wrap work on other threads with `context.wrap(Runnable)` or `context.wrap(Callable<T>)`.

Cancellation is cooperative. Use `context.forEachItem(items) { ... }`, `throwIfCancelled()`, or `isCancellationRequested` between units of work.
Check at least every few seconds and bound blocking I/O with timeouts. Do not swallow `TaskCancelledException`.
Wrapped work checks cancellation before it starts. Return `cancellable = false` only when the task cannot honor this contract.

## Notifications and actions

Use `context.notificationService.publish(NotificationRequest(...))` to publish an in-app notification and retain its returned ID.
Notifications survive plugin restarts. `resolve(id)` removes a notification published by that plugin, including archived entries.

A request contains a `title`, `body`, severity (`INFO`, `SUCCESS`, `WARNING`, or `ERROR`), recipients, and optional actions.
The default audience is `ADMINS`. `ALL_USERS` snapshots existing accounts at publication time;
`USERS` requires an explicit set of user IDs.

Actions have a unique `key` within the notification, a `label`, and a type:

- `LINK` opens its `url`.
- `RESTART` requests an application restart, subject to administrator authorization.
- `PLUGIN` calls an indexed `@Extension` implementing `NotificationActionHandler` with the same key.

A handler is available while its plugin is started. Its default `permission` is `ADMIN`;
use `RECIPIENT` only when each recipient should be allowed to run it.
`NotificationActionContext` contains `actorId`, `notificationId`, `executionId`, and server-stored `parameters`.
The browser cannot replace these parameters. Validate their values and use timeouts for blocking I/O.
A successful callback consumes server actions for that inbox. Failed or interrupted actions may be retried explicitly.
Use `executionId` as an idempotency key for external effects; the host cannot atomically commit an external effect and its execution receipt.

## Publishing and updates

Publish an immutable JAR at an HTTPS URL and submit its metadata to the
[official marketplace](https://github.com/gameyfin/plugin-marketplace#submitting-a-plugin-plugin-developers).
The marketplace guide covers its JSON schema, SHA-512 checksums, releases, and custom indexes.
Gameyfin verifies checksums, manifest ID/version, and version compatibility before installation.

Community plugins should be **unsigned**. Gameyfin classifies them as third-party and requires an administrator to enable them.
A JAR signed with an unrecognized key is untrusted and cannot be started.
The official marketplace can list community plugins; listing there does not give them an official signature.
See [plugin security](security.md) for the trust model.
