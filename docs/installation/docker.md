---
title: Docker Installation
description: How to install Gameyfin using Docker
icon: simple/docker
---

# Docker Installation

Docker is the recommended way to run Gameyfin, as it simplifies the installation process and reduces the likelihood of issues related to dependencies and environment configuration.

The Gameyfin Docker image is currently available on [Docker Hub](https://hub.docker.com/r/grimsi/gameyfin).

## Docker Compose
You can use Docker Compose to run Gameyfin.

#### Environment Variables
Contrary to Gameyfin v1 almost no configuration via environment variables is required to run Gameyfin.  

##### APP_KEY
The only required environment variable is `APP_KEY`, which Gameyfin uses to encrypt sensitive data in the database.  
The app key  must be a 16, 24 or 32 byte long Base64 encoded string, which can be generated using the following command:

```bash
openssl rand -base64 32
```

##### APP_URL
If you are using Gameyfin with a reverse proxy, you should also set the `APP_URL` environment variable to the URL of your Gameyfin instance (e.g. `https://gameyfin.example.com`).

##### PUID & PGID
If you want to run Gameyfin with a specific user and group ID, you can set the `PUID` and `PGID` environment variables.

#### Volumes and Ports
The volumes for the database, data, and logs should be mounted to the host system to persist data across container restarts.  
Additionally, you have to mount your library folder(s) to the container, so Gameyfin can access your media files.  
Finally if you want to use the included torrent plugin, you need to expose the necessary ports (6969 for the tracker and 6881 for the torrent client).
The ports can be changed if needed (either by mapping to another port on your host or by changing the plugin configuration), but the default ports are recommended for compatibility with other applications.

#### Compose File
You can use the following `docker-compose.yml` file to run Gameyfin:

```yaml title="docker-compose.yml"
--8<-- "external/gameyfin/docker/docker-compose.example.yml"
```

Start Gameyfin using Docker Compose with the following command:

```bash
docker-compose up -d
```

Observe the logs to ensure that Gameyfin starts correctly:

```bash
docker-compose logs -f gameyfin
```
The logs should contain the message `Loaded plugins: <list of plugins>` when the application is ready.  
You should now be able to access Gameyfin at `http://<docker-host-ip-or-hostname>:8080` (or `APP_URL` if it's behind a reverse proxy) in your web browser.

## First steps

Proceed to the [Getting Started](getting-started.md) guide to learn how to configure Gameyfin and add your media library.