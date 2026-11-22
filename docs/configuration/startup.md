---
icon: material/tune
---

# Startup settings

Most users only need `APP_KEY`, a persistent Gameyfin folder, and a game-folder mount.
Use the [Docker guide](../installation/docker.md) first.
These advanced settings are applied when Gameyfin starts; restart the container after changing its environment.
They are separate from the database-backed [web configuration](reference.md).

## Application and container

| Variable | Default | Purpose |
| --- | --- | --- |
| `APP_KEY` | Required | Base64-encoded AES key for encrypted settings. Preserve it across updates and restores. |
| `APP_URL` | Unset | External setup URL printed in first-run logs. Notification links use the request URL. |
| `PUID`, `PGID` | Container user/group | Optional user and group IDs for filesystem access. |
| `JAVA_OPTS` | Unset | Append flags to the container's JVM defaults. |
| `JAVA_OPTS_OVERRIDE` | Unset | Replace the container's JVM defaults. |

## Database overrides

Prefer the database selector during setup or **Administration → System**.
Advanced deployments can manage the datasource through Spring Boot configuration instead:

| Variable | Example |
| --- | --- |
| `SPRING_DATASOURCE_URL` | `jdbc:postgresql://db:5432/gameyfin_db` |
| `SPRING_DATASOURCE_USERNAME` | `gfadmin` |
| `SPRING_DATASOURCE_PASSWORD` | Your database password |
| `SPRING_DATASOURCE_DRIVERCLASSNAME` | `org.postgresql.Driver` |

An externally configured datasource takes precedence over database settings saved in the UI.
Do not change the URL to migrate an existing installation: changing a connection string alone does not transfer its data.
Use the database switch workflow or a backup and restore.
UI database connection settings are stored outside the database, in `./db/database.json` by default.
Override that path with `GAMEYFIN_DATABASE_SETTINGSFILE` if necessary, and persist its directory.

## Storage and marketplace

Spring Boot maps property names to environment variables by replacing dots with underscores, removing hyphens, and using uppercase.
For example, `gameyfin.plugins.install-directory` becomes `GAMEYFIN_PLUGINS_INSTALLDIRECTORY`.

| Property | Default | Purpose |
| --- | --- | --- |
| `gameyfin.database.settings-file` | `./db/database.json` | Persisted database connection settings. |
| `gameyfin.backup.directory` | `./backups` | Backup archive storage. |
| `spring.content.fs.filesystem-root` | `./data/` | Downloaded artwork and other stored media. |
| `gameyfin.plugins.install-directory` | `plugins` | Installed plugin JARs, relative to the working directory. |
| `gameyfin.plugins.marketplace.official-url` | `https://github.com/gameyfin/plugin-marketplace` | Official marketplace source. |
| `gameyfin.plugins.marketplace.connect-timeout` | `10s` | Marketplace connection timeout. |
| `gameyfin.plugins.marketplace.request-timeout` | `2m` | Marketplace request timeout. |
| `gameyfin.plugins.marketplace.cache-ttl` | `1h` | Marketplace index cache lifetime. |
| `gameyfin.plugins.marketplace.allow-insecure-urls` | `false` | Permit HTTP marketplace URLs. Keep disabled for normal installations. |

Docker's working directory is `/opt/gameyfin`. Keep configured storage paths within a persistent mount.
An alternate plugin install directory does not move all plugin state; keep the whole persistent folder for recovery.

## Bounded background executor

These settings control the bounded executor used for background work. They are not the per-scan concurrency setting in **Games**.
Leave the defaults unless you have measured a need to tune them.

| Property | Default |
| --- | --- |
| `gameyfin.async.bounded.core-pool-size` | `4` |
| `gameyfin.async.bounded.max-pool-size` | `16` |
| `gameyfin.async.bounded.queue-capacity` | `100` |
