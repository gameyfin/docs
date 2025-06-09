---
title: Security
description: How Gameyfin handles plugin security
---

# Plugin Security
!!! danger "Security Warning"

    Gameyfin plugins run in the same JVM as the main application, which means they have access to the same resources and can potentially cause security issues.


Gameyfin does not currently implement a sandbox for plugins, so it is important to only use plugins from trusted sources.
However, Gameyfin does separate the plugins into different trust levels (from most trusted to least trusted) to help you make informed decisions about which plugins to use:

- **Bundled Plugins**: These plugins are included with Gameyfin and are considered safe to use if you download Gameyfin from a trusted source.
- **Official Plugins**: These plugins are developed by the Gameyfin team or trusted contributors and are considered safe to use. They are signed with a digital signature to verify their authenticity.
- **Community Plugins**: These plugins are developed by the community. They are not signed and should be used with caution.
- **Untrusted Plugins**: These plugins are signed, but the signature is invalid or not recognized by Gameyfin. They are considered untrusted and should not be used.

Gameyfin will display the trust level of a plugin in the Admin UI, but it does not restrict you from using any plugins you wish to use.
Also, plugins will only be started automatically after the installation if they are bundled with Gameyfin or signed by a trusted source.
