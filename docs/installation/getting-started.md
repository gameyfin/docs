---
title: Getting Started
description: From your first login to your first game library
icon: material/rocket-launch
---

# Getting started

Open Gameyfin in your browser after [installation](docker.md).

## 1. Complete the setup wizard

1. Choose your theme.
2. Keep **H2 (embedded)** for a simple installation, or configure and test a PostgreSQL connection.
3. Create your administrator account with a username, email address, and password of at least eight characters.
4. Finish the wizard and log in with that account. A database change may restart Gameyfin first.

If you are moving an existing installation, the welcome screen also offers **Restore from backup**.
Read [Backup and restore](../configuration/system.md) before restoring.

## 2. Install plugins

After your first administrator login, **Choose your plugins** opens the marketplace as the final setup step.
Gameyfin ships **without pre-installed plugins**.

1. Install a metadata plugin, such as IGDB or Steam, to find game descriptions and artwork.
2. Install a download provider, such as Direct Download, if users should download games through Gameyfin.
3. Wait for each installation to complete. The task popover shows progress and history.
4. Click **Finish setup**.
5. Open **Administration → Plugins → Installed**, review each plugin's configuration, and enable it. Some providers require credentials from an external service.

You can finish without installing anything and return through **Administration → Plugins** later.
A library scan requires at least one enabled metadata provider. Installing a plugin does not replace configuring and enabling it.

For more detail, see [Managing plugins](../configuration/plugins.md).

## 3. Add your first library

1. Open your avatar menu and select **Administration → Games**.
2. Use **Add new library**, enter a name, and add the folder containing your games.
3. With Docker, use the path **inside the container**, such as `/games`, rather than the host path `/srv/games`.
4. Start a quick scan. Follow progress in the task popover.
5. Open the home page to browse the matched games.

For example, `/games/My Game/` can contain the files for one game.
Check [Libraries and collections](../configuration/libraries.md) if paths remain unmatched.
Automatic filesystem watching is disabled by default; configure it under **Games → Scanning**, or schedule scans under **Tasks**.

## 4. Check access and backups

Access without login is disabled by default. Keep it disabled unless you intend to share your library publicly.
Create accounts through **Users**, and enable self-registration only if you want it.

Set up [backups](../configuration/system.md) and keep your `APP_KEY` safe before adding more users.
See [Troubleshooting](../faq/index.md) if setup, matching, or downloads fail.
