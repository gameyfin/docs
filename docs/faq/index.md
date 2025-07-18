---
title: FAQ
description: Gameyfin Installation Guide
icon: material/help-circle
---

!!! example "Beta release"

    The matching algorithm is the heart of Gameyfin and it is not perfect yet.
    Feedback is always welcome, so if you have any issues with the matching process, please open an issue on [GitHub](https://github.com/gameyfin/gameyfin/issues).

# Frequently Asked Questions

## Gameyfin doesn't start because of permission issues

Gameyfin requires access to the filesystem to scan your game libraries and to read the game files.  
If you run Gameyfin as a non-root user, you need to make sure that the user has read access to the game files and directories.  
You can also [configure the user and group](../installation/docker.md#puid-pgid) that Gameyfin should run as in the `docker-compose.yml` file.

## How does Gameyfin match my video games?

The matching algorithm grew a bit more complex compared to the v1 version. Thanks to the new plugin system, Gameyfin can now match games using various sources.  
Since the plugins can have different matching strategies and algorithms, the matching process is now more flexible and can be customized by the user (by using different plugins or by configuring their plugins).  
The matching process for library scans is as follows:  

1. **Filesystem Scan**: Gameyfin scans the filesystem of your libraries for game files and directories.
2. **Filename Extraction**: It extracts the names of all new game files and directories found in the scan.
3. **Result Iteration**: Iterating over the extracted filenames, Gameyfin will try to match each filename using the installed plugins.
    1. The matching process is done in parallel for all plugins so the process takes as long as the slowest plugin to respond (usually IGDB because they enforce rate limits on their API).
4. **Plugin Matching**: Each installed plugin is queried with a filename to match against its own database or API.
    1. The plugins have their own matching strategies, so the result quality may vary depending on the plugin used.
    2. Each plugin returns one result, which is the best match it found for the given filename.
5. **Title Normalization**: The titles of the results are normalized to lowercase and to only include alphanumeric characters and spaces. Roman numerals are converted to Arabic numerals.
    1. This is done to ensure that the titles are consistent and can be matched correctly across different data sources.
6. **Result Filter**: The results from all plugins are filtered based on the normalized game title.
    1. The closest match is determined using fuzzy matching, which allows for minor differences in titles, such as typos or different naming conventions.
    2. All other results that do not match the title with a minimum ratio are discarded.
    3. The filter [can be configured](../configuration/libraries.md#minimum-ratio-for-title-matching).
7. **Result Merging**: The results from each plugin are merged into a single result.
    1. The merging uses the configured plugin priorities to determine which plugin's data to use for each field.
    2. It starts with the first plugin in the priority list and uses its data for all fields. If a field is not set, it will use the next plugin's data in the priority list.
    3. This continues until all fields are filled or all plugins have been checked.
8. **Final Result**: The final result is a game enriched with metadata from the plugins, which is linked to the game file or directory on your filesystem.

The matching process for manual matching via UI is similar, but instead of returning just the top match from each plugin, it returns the top 10 matches from each plugin.
These matches are then grouped based on title (strict matching instead of fuzzy matching) and release year. The user can then select the best match from the list of matches.

## How can I improve the matching accuracy?

There are several ways to improve the matching accuracy:

1. **Use more plugins**: The more plugins you have installed and enabled, the more sources Gameyfin can use to match your games. This increases the chances of finding a match.
2. **Rename your game files**: The closer the game file names are to the actual game titles, the better the matching accuracy.  
   Gameyfin uses fuzzy matching, so even if the file name is not exactly the same as the game title, it can still find a match.

## How will the matching process change in the future?

The matching process is still evolving and will continue to improve over time.  
Jellyfin for example has an [interesting feature](https://jellyfin.org/docs/general/server/media/movies/#metadata-providers) that allows users to include the ID of a game in the file name, which can be used to match the game more accurately.

Again, I am always open to suggestions and feedback, so if you have any ideas on how to improve the matching process, please open an issue on [GitHub](https://github.com/gameyfin/gameyfin/issues).

## What's the difference between "quick scan" and "full scan"?

The "quick scan" only scans for new games while the "full scan" also updates existing games.

This means that the "quick scan" will only add new games to your library, while the "full scan" will also update the metadata of existing games.
Fields that have been modified by a user will **not** be overwritten by the "full scan", so you can safely run it without losing your changes.

If you want to reset the metadata of a game, you can do so by deleting the game from your library (and your unmatched paths) and then running a scan (either type) again.