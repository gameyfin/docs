---
title: Security
description: Plugin trust, signatures, and runtime access
icon: material/shield-check
---

# Plugin security

!!! danger "Plugins run with Gameyfin's permissions"

    Plugins run in the same JVM as Gameyfin. There is no plugin sandbox.
    They can access resources available to the application, including files and network services.
    Install code only from developers and marketplaces you trust.

Gameyfin checks plugin signatures and displays their trust level:

- **Official:** signed with a key trusted by Gameyfin.
- **Bundled:** used for plugins during development and testing. Not for production use.
- **Third-party:** unsigned community code. Review the source and publisher before enabling it.
- **Untrusted:** signed, but the signature is invalid or the signing key is not trusted. Proceed with caution.
- **Unknown:** verification could not establish a usable trust status. Proceed with caution.

A marketplace listing or checksum does not by itself establish that a plugin is safe.
Unsigned third-party plugins require explicit enablement after installation; review their configuration first.
