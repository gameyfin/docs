---
title: FAQ
description: Troubleshoot setup, matching, and downloads
icon: material/help-circle
---

# Frequently asked questions

## Gameyfin doesn't start because of permission issues

The container user needs read and directory traversal access to game folders, plus write access to its persistent Gameyfin folder.
Check [PUID and PGID](../installation/docker.md#puid-pgid) and the ownership of your mounted directories.
Read the first error in `docker compose logs gameyfin` to find the affected path.

## Why does a library folder not appear in Docker?

Docker can only see mounted folders. Map a host folder such as `/srv/games` to a container path such as `/games`.
Enter `/games` in Gameyfin. Check permissions if the mount exists but cannot be read.

## Why are there no plugins after installation?

Gameyfin ships without pre-installed plugins.
Install them from **Choose your plugins** after your first administrator login, or through **Administration → Plugins**.
Configure and enable at least one metadata provider before scanning. Install a download provider for downloads.

## Why can I browse games but not download them?

Install and enable a download provider, such as Direct Download, in **Administration → Plugins**.
Read its configuration instructions and check that Gameyfin can read the game files.
Torrent downloads require the plugin's network ports in addition to the web interface port.

## Library scan progress and/or application logs are not shown in the UI

Gameyfin uses WebSockets for live updates.
Check that your reverse proxy forwards WebSocket connections and that the browser or network does not block them.
Inspect task run logs under **Administration → Tasks** as well as application logs.

## How does Gameyfin match my video games?

1. Gameyfin scans the library's folders for game files and directories.
2. It derives a title from each new path, applying your title-extraction regex if enabled.
3. Enabled metadata providers supporting the selected platforms search for that title concurrently.
4. Gameyfin takes each provider's best result and compares normalized titles, including Roman numeral normalization.
5. It filters incompatible matches and merges metadata according to provider priority.

The title matching ratio compares results across metadata sources. A lower ratio can merge unrelated games.
Configure it under [Games → Scanning](../configuration/libraries.md#minimum-ratio-for-title-matching).

Manual metadata searches request up to ten results per provider.
Results are grouped by normalized title and release year so you can choose the correct match.

## How can I improve the matching accuracy?

- Use clear game titles for filenames or folders. Remove unrelated release tags, or configure a title-extraction regex.
- Select the correct platforms for the library.
- Check that metadata providers are enabled, configured, and reachable. More providers can fill missing metadata.
- Correct a match manually from the game's metadata search if automatic matching picks the wrong game.
- Review provider priority when sources disagree.

## What's the difference between "quick scan" and "full scan"?

A quick scan finds new games. A full scan also refreshes existing games and their metadata.
Both can revisit paths that metadata plugins previously failed to match.
A full scan preserves metadata fields edited by users.

Choosing a result through **Search for metadata** replaces metadata with the selected result and can overwrite manual edits.

## What are "ignored paths" and how do they work?

Gameyfin tracks why a path is unmatched or excluded:

- **Plugin-generated:** no metadata match was found, or processing failed. Later scans retry these paths.
- **User-generated:** a user removed a game from the library. Scans keep that path excluded.

Review unmatched paths in the library's administration page.
Remove a user-generated entry if you want a later scan to consider that path again.

## Where are periodic metadata refresh settings?

Scheduled library scans are managed in **Administration → Tasks**.
This replaces the old periodic metadata-refresh controls under Libraries.
See [Tasks](../configuration/tasks.md) for schedules, settings, progress, and run history.
