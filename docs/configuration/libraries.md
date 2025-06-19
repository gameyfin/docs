# Libraries

## Permissions

### Allow access to game libraries without login
Default: `false`  
This option allows users to access game libraries without logging in (great if you want to share your game library with friends or family).

## Scanning

### Enable automatic scanning using file system watchers
Default: `true`  
This option enables automatic scanning of game libraries using file system watchers. This way Gameyfin will automatically detect changes in your game libraries and update the database accordingly.

### Scan empty directories
Default: `false`  
This option allows Gameyfin to scan empty directories in your game libraries. This is useful if you want to keep track of directories that do not contain any games, but it may slow down the scanning process.

### Minimum ratio for title matching
Default: `90`  
Range: `0-100`  
This option filters the results of the title matching algorithm. If the ratio is below this value, the title will not be matched.  
Lowering this value may result in more matches, but it may also result in more false matches.

### File extensions to consider as games
Default: `zip,tar,gz,rar,7z,bz2,xz,iso,jar,tgz,exe,bat,cmd,com,msi,bin,run,app,dmg,elf`  
This option allows you to specify which file extensions should be considered as games.

## Metadata

### Enable periodic refresh of video game metadata
Default: `true`  
This option enables periodic refresh of video game metadata.  
Gameyfin will automatically update the metadata of your games based on the configured sources.

### Schedule for periodic metadata refresh
Default: `0 0 * * 0` (every Sunday at midnight)  
This option allows you to configure the schedule for periodic metadata refresh.  
The format is a cron expression.

## Libraries
This section allows you to manage your game libraries in Gameyfin.
Add a new library, scan a library for games or open the administration page of a library.

### Library administration

#### Details
This section allows you to manage the details of your game library, such as the name and file system paths of library.  
You can also delete the library from here.

#### Games
This section allows you to manage the games in your library.  
You can edit the details of a game, delete a game or match a game manually.  
If you delete a game, its path will be added as "unmatched path", effectively excluding it from future scans.

#### Unmatched paths
This section allows you to manage the unmatched paths in your library.  
If you delete an unmatched path, it will be included in future scans again.