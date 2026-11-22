---
icon: material/bookshelf
---

# Libraries and collections

Open **Administration → Games** to manage libraries, collections, and scanning.
A library points to one or more folders on the server. A collection groups games for browsing without changing their folders.

## Add a library

Use **Add new library**, give it a name, and add at least one source path.
Docker paths must match the container side of your volume mapping, such as `/games`.
Gameyfin needs permission to read the folder and its files.

Install, configure, and enable a metadata plugin before scanning. Set provider priorities under [Plugins](plugins.md).
Use quick scans to find new games; full scans also refresh existing games while preserving fields edited by users.
Scheduled scans are configured under [Tasks](tasks.md).

## Scanning settings

Automatic filesystem watching defaults to **off**. Enable it to scan affected folders when files change.
Choose which file extensions count as games and whether empty directories should be scanned.
Optional Java-compatible regular expressions can remove release tags from filenames before matching.
The title matching ratio compares results from different metadata providers; lowering it can merge unrelated games.

Scan concurrency defaults to **4**, with a declared range of **1–16**.
Lower it if scans use too much memory. Changes apply to new scans.
See the [generated reference](reference.md#library-scan-enable-filesystem-watcher) for all scanning settings and defaults.

## Manage games and unmatched paths

Open a library's configuration to edit its details, manage games, and review unmatched paths.
You can correct a game's metadata or match it manually.
Removing a game from the library adds its path to the unmatched paths list so later scans do not immediately re-add it.
Removing a user-generated unmatched-path entry lets a future scan try that path again.
Plugin-generated unmatched paths are retried by later scans automatically.

See [Matching troubleshooting](../faq/index.md#how-can-i-improve-the-matching-accuracy) for help with filenames and providers.

## Collections

Create collections from the **Collections** section of **Games** and add games to group them for your users.
The library and collection order controls change their display order.

## Minimum ratio for title matching {#minimum-ratio-for-title-matching}

This setting lives under **Games → Scanning**. See the [reference](reference.md#library-scan-title-match-min-ratio) for its default and declared bounds.

## Upload games

Administrators can use **Upload** in the Games administration page to add files through the browser.
Choose the destination library and directory, select metadata, and review the upload before starting.
The destination must be writable by Gameyfin; a Docker library mounted with `:ro` cannot accept uploads.
