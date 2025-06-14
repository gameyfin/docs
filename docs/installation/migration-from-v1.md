---
title: Migration from Gameyfin v1
description: Migration Guide from Gameyfin v1 to v2
---

To keep it short: a straight migration from Gameyfin v1 to v2 is not possible.  
Gameyfin v2 is a complete rewrite of the application (in different programming languages even), and as such, it does not support direct migration of data from Gameyfin v1.  
The database structure has changed significantly and a lot of new fields have been implemented to support the many new features of Gameyfin v2.

Sorry for the inconvenience, but this was necessary to provide a better user experience and to support the new features of Gameyfin v2.  
Depending on the size of your game library, the migration process may take a few minutes, but it is a one-time process (hopefully).

### What to do?

1. **Backup your Gameyfin v1 data**: Make sure to backup your Gameyfin v1 data, especially the database file and any custom configurations you may have.
2. **Install Gameyfin v2**: Follow the [installation guide](../installation/index.md) to install Gameyfin v2.
3. **Reconfigure your settings**: You will need to reconfigure your settings in Gameyfin v2. Some settings may have changed or been removed, so please refer to the documentation for the new settings.
4. **Reimport your data**: Add your game libraries again in Gameyfin v2. You will need to reimport your games and their metadata. Gameyfin v2 supports importing from various sources, so you can choose the one that suits you best.