---
icon: material/server
---

# System, backups, and database

Open **Administration → System** for restart, backup and restore, and database management.

## Create a backup

1. Create a backup under **Backup & restore**.
2. Optionally include media files, such as covers and screenshots.
3. Wait for the task to complete, then download the backup to another device.
4. Keep a secure copy of your `APP_KEY` with your recovery materials.

A backup contains database data and optionally images. It does **not** replace a backup of your game files, plugin JARs, or plugin data directories.
Keep a separate copy of your persistent Gameyfin folder and game folders when planning a full recovery.

Enable scheduled backups under [Tasks](tasks.md). Only backups created by that task are deleted according to its retention setting.
Backups kept only on the same disk do not protect against disk failure.

## Restore

Restore a listed backup, or upload one first. A fresh installation also offers **Restore from backup** on the setup welcome screen.

!!! warning "Restoring replaces database data"

    Use the same `APP_KEY` as the instance that created the backup.
    Save a current backup before restoring. Restore replaces the database contents and restarts Gameyfin.
    Users must log in again afterward.

Check the reported restore result after restart. Reinstall missing plugins and restore your game folders separately if moving to another machine.

## Choose or switch databases

H2 is embedded and needs no separate service. PostgreSQL requires a running database server and connection credentials.
You can choose the database during initial setup or switch it here later.
Gameyfin tests the target connection, creates a transfer backup, and restarts to transfer the data.
If the transfer fails, Gameyfin attempts to return to the previous database; check the result shown in System.

!!! warning "Use a dedicated target database"

    Switching can replace existing tables in the target database. Do not use a database containing another application's data.
    Review the test result and overwrite confirmation before continuing.

If database settings are managed through environment variables, the interface reports that they are externally managed.
See [Startup settings](startup.md) for those overrides.
