# Much More Dungeons v1.1.3

### New Features
* Added Minecraft **26.2** MultiLoader workspace (Fabric + NeoForge)

### Improvements
* Fixed **26.1.2** toolchain so `gradle.properties` targets Minecraft **26.1.2** (was still on 26.1.1 deps)
* Refreshed 26.1.2 Fabric API / Fabric Loader / NeoForge / NeoForm to current 26.1.2 releases
* Aligned shared mod version to **1.1.3** across all kept workspaces

### Bug Fixes
* Updated 26.2 example mixins for Minecraft API change: `getVersionType()` → `getLaunchedVersion()`

### Configuration
* MultiLoader matrix trimmed to: `1.20.1`, `1.21.1`, `26.1.2`, `26.2`
* Removed workspaces: `1.21.5`, `1.21.8`, `1.21.11`

### Compatibility
* Drop-in update from **1.1.2** for remaining lines
* Loaders:
  * `1.20.1` — Fabric + Forge
  * `1.21.1` / `26.1.2` / `26.2` — Fabric + NeoForge
* Java: 17 (1.20.1), 21 (1.21.1), 25 (26.1.2 / 26.2)

### Upgrade Notes
1. Remove any previous Much More Dungeons jar for your Minecraft / loader line
2. Install the matching `1.1.3` jar from `dist/`
3. Restart the client or server and confirm the mod loads on the intended Minecraft version