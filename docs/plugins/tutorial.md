---
title: Plugin Development Tutorial
description: Build and test a complete metadata plugin
icon: material/school
---

# Build your first plugin

This tutorial creates a Kotlin metadata plugin for Gameyfin **2.7.1**.
It returns one hardcoded game so you can test discovery and metadata lookup without API credentials.
See the [developer reference](info-for-devs.md) for configuration, tasks, downloads, stores, and notifications.

## Requirements

- JDK 25.
- Gradle supporting Java 25, such as the version used by Gameyfin's Gradle wrapper.
- A running test installation of Gameyfin and write access to its plugin directory.
- An IDE or text editor.

Use a test library rather than your production library: this provider deliberately returns sample metadata.

## Create the project

Create these files:

```text
hello-gameyfin/
├── settings.gradle.kts
├── build.gradle.kts
└── src/main/
    ├── kotlin/com/example/gameyfin/HelloPlugin.kt
    └── resources/META-INF/extensions.idx
```

In `settings.gradle.kts`:

```kotlin
rootProject.name = "hello-gameyfin"
```

In `build.gradle.kts`:

```kotlin
plugins {
    kotlin("jvm") version "2.4.21"
}

group = "com.example"
version = "1.0.0"

repositories {
    mavenCentral()
}

kotlin {
    jvmToolchain(25)
}

dependencies {
    compileOnly("org.gameyfin:plugin-api:2.7.1")
}

tasks.jar {
    archiveBaseName.set("hello-gameyfin")
    manifest {
        attributes(
            "Plugin-Id" to "com.example.gameyfin.hello",
            "Plugin-Version" to project.version.toString(),
            "Plugin-Class" to "com.example.gameyfin.HelloPlugin",
            "Plugin-Requires" to ">=2.7.1 & <3.0.0",
            "Plugin-Name" to "Hello Gameyfin",
            "Plugin-Description" to "A minimal example metadata provider.",
            "Plugin-Author" to "Your name",
            "Plugin-License" to "MIT"
        )
    }
    // Include the Kotlin runtime; compileOnly keeps the host API out of the JAR.
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE
    from(configurations.runtimeClasspath.get().map { zipTree(it) }) {
        exclude("META-INF/*.SF", "META-INF/*.DSA", "META-INF/*.RSA")
    }
}
```

Match the API version to the Gameyfin version you support.
If you are working against an unreleased checkout, run `./gradlew :plugin-api:publishToMavenLocal` in Gameyfin first,
then add `mavenLocal()` to this project's `repositories` block.
Replace the example ID with an identity you own before publishing. Do not use the reserved `org.gameyfin.*` namespace.

## Implement the wrapper and extension

In `src/main/kotlin/com/example/gameyfin/HelloPlugin.kt`:

```kotlin
package com.example.gameyfin

import org.gameyfin.pluginapi.core.wrapper.GameyfinPlugin
import org.gameyfin.pluginapi.core.wrapper.PluginContext
import org.gameyfin.pluginapi.gamemetadata.GameMetadata
import org.gameyfin.pluginapi.gamemetadata.GameMetadataProvider
import org.gameyfin.pluginapi.gamemetadata.Platform
import org.pf4j.Extension

class HelloPlugin(context: PluginContext) : GameyfinPlugin(context)

@Extension
class HelloMetadataProvider : GameMetadataProvider {
    override val supportedPlatforms: Set<Platform> = Platform.entries.toSet()

    override fun fetchByTitle(
        gameTitle: String,
        platformFilter: Set<Platform>,
        maxResults: Int
    ): List<GameMetadata> {
        if (maxResults <= 0) return emptyList()
        return listOf(exampleGame(platformFilter))
    }

    override fun fetchById(id: String): GameMetadata? =
        if (id == "hello-world") exampleGame(emptySet()) else null

    private fun exampleGame(platforms: Set<Platform>) = GameMetadata(
        originalId = "hello-world",
        title = "Hello World Game",
        platforms = platforms.takeIf { it.isNotEmpty() },
        description = "Metadata returned by the tutorial plugin."
    )
}
```

The wrapper receives the host context. The separate extension has a public no-argument constructor, which PF4J uses to instantiate it.
The example reports support for every platform and returns sample metadata for any title.
A real provider must search the supplied title, honor the platform filter, and return best matches first, up to `maxResults`.
Return an empty list for no matches and `null` for an unknown source ID.

## Register the extension

Put this single line in `src/main/resources/META-INF/extensions.idx`, followed by a newline:

```text
com.example.gameyfin.HelloMetadataProvider
```

This is PF4J's extension index. The tutorial maintains it explicitly so no Kotlin annotation processor is needed.
Add every extension class to the index. For larger plugins, use compatible annotation processing to generate this file instead.
The wrapper class does not belong in this index.

## Build and check the JAR

From the plugin project, create a Gradle wrapper if needed, then build:

```shell
gradle wrapper
./gradlew build
jar tf build/libs/hello-gameyfin-1.0.0.jar
```

On Windows use `gradlew.bat` instead of `./gradlew`.
The JAR listing must include `META-INF/MANIFEST.MF`, `META-INF/extensions.idx`, and both compiled plugin classes.
Do not sign community plugin JARs with your own key: Gameyfin rejects signatures it does not recognize.

## Install and test

1. Stop your test Gameyfin installation.
2. Copy `build/libs/hello-gameyfin-1.0.0.jar` into its persistent `plugins` directory.
   With Docker, use the host directory mounted at `/opt/gameyfin/plugins`, not a temporary file inside the container.
3. Start Gameyfin. Manual JAR discovery requires an application restart.
4. Open **Administration > Plugins > Installed**. Find **Hello Gameyfin** and enable it.
   An unsigned local plugin is third-party and is not enabled automatically.
5. Disable other metadata providers in this test installation.
6. Add a test library source containing a game folder or file, then scan it.
7. Confirm that Gameyfin displays **Hello World Game**.

If the plugin does not appear, check the application logs for loading errors and verify the manifest, extension index, and API version.
If it appears but cannot start, check its trust status and the logs.
When replacing a manually installed test JAR, stop Gameyfin first and remove the old JAR to avoid duplicate versions.

## Publish the plugin

For normal distribution, use the marketplace so administrators can install and update your plugin from the UI.
Follow the [marketplace submission guide](https://github.com/gameyfin/plugin-marketplace#submitting-a-plugin-plugin-developers)
to publish a release and checksum. Test each supported Gameyfin version before broadening `Plugin-Requires`.
