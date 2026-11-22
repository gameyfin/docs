---
title: Docker Installation
description: Install Gameyfin with Docker Compose
icon: simple/docker
---

# Docker installation

Docker Compose is the recommended way to run Gameyfin. Install [Docker Engine with Compose](https://docs.docker.com/engine/install/), or [Docker Desktop](https://docs.docker.com/desktop/), before continuing.
The examples use `ghcr.io/gameyfin/gameyfin:2` and require at least 1 GB of memory for the container.

## 1. Create a configuration folder

Create a folder for Gameyfin and save the Compose file below as `docker-compose.yml` in that folder.
Run all commands on this page from that folder.

## 2. Generate an application key

Run:

```bash
openssl rand -base64 32
```

Replace `<your app key here>` in the Compose file with the output. `APP_KEY` must contain a Base64-encoded 16, 24, or 32-byte AES key.

!!! warning "Keep your application key"

    Gameyfin uses `APP_KEY` to encrypt sensitive settings. Keep a secure copy with your backups.
    Reuse this key when updating, moving, or restoring Gameyfin. A new key cannot decrypt the old settings.

## 3. Mount your game folder

Replace `<mount your library folder(s) here>` with a volume mapping, for example:

```yaml
      - "/srv/games:/games:ro"
```

`/srv/games` is the folder on your Docker host. Change it to your game folder.
`/games` is the path Gameyfin sees inside the container. Use **`/games`** when adding your library in the web interface.
The optional `:ro` makes this mount read-only; omit it if you need Gameyfin to write to the library, such as uploading games.

Keep `./gameyfin:/opt/gameyfin`. It persists the embedded database, settings, images, plugins, plugin data, logs, and backups.
Your game files remain in the separate library mount.

### Compose file: embedded H2 database

H2 needs no separate database server and is recommended for your first setup.
Replace both placeholders before starting:

```yaml title="docker-compose.yml"
--8<-- "external/gameyfin/docker/docker-compose.example.yml"
```

### Optional: PostgreSQL

Use this version if you already want a separate PostgreSQL database. Also replace the database password placeholder.
Starting the `db` service alone does **not** connect Gameyfin to PostgreSQL.
During setup, select **PostgreSQL**, enter host `db`, port `5432`, database `gameyfin_db`, user `gfadmin`, and the same password.
Test the connection before continuing. You can also switch databases later in **Administration → System**.

```yaml title="docker-compose.yml"
--8<-- "external/gameyfin/docker/docker-compose.postgres.example.yml"
```

## 4. Start Gameyfin

```bash
docker compose up -d
docker compose logs -f gameyfin
```

Wait for startup to finish. `Loaded plugins: []` is normal on a new installation: no plugins are pre-installed.
Press `Ctrl+C` to stop following logs; the container keeps running.
Open `http://localhost:8080` on the Docker host, or `http://<server-ip>:8080` from another device on your network.
Continue with [Getting started](getting-started.md).

## Optional environment variables {#environment-variables}

### APP_URL

Set `APP_URL` to your public URL, such as `https://gameyfin.example.com`, when using a reverse proxy.
It controls the setup URL printed in first-run logs. Configure your proxy to forward the original host and protocol, and to support WebSockets.
Notification links use the request URL, so correct proxy headers matter.

### PUID & PGID {#puid-pgid}

Set `PUID` and `PGID` to run Gameyfin with a particular user and group ID.
On Linux, run `id -u` and `id -g` to find your IDs.
That user needs read and directory traversal access to your game folders, and write access to the persistent Gameyfin folder.

### JVM options

`JAVA_OPTS` appends JVM flags to the container defaults.
`JAVA_OPTS_OVERRIDE` replaces all default JVM flags. Leave both unset unless you need to tune the JVM.
See [Startup settings](../configuration/startup.md) for advanced options.

### Torrent ports

If you install and enable the torrent download plugin, uncomment its port mappings in the Compose file.
The example uses `6969` for the tracker and `6881` for peers. These ports are unnecessary for browser downloads.

## Updating

Create and download a [backup](../configuration/system.md) first. Keep your Compose file, `APP_KEY`, persistent folder, and game mounts.
Then run:

```bash
docker compose pull
docker compose up -d
```

Check the logs and open the web interface. Plugin updates are managed separately in the marketplace.
