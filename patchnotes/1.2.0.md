# Much More Dungeons v1.2.0

### New Features
* Added **Soulfire Crypt** — a cold-biome soul-fire crypt with blackstone / deepslate architecture, soul lanterns, and crying-obsidian altar
* Crypt includes wither skeleton and blaze spawners, ambient wither skeletons / strays, and a named **Cinder Warden**
* New chest loot table `muchmoredungeons:chests/soulfire_crypt` (soul lanterns, netherite scrap, wither skull chance, enchanted gear)

### Improvements
* Switched project licensing to **Apache License 2.0** with standard OSS contributor docs
* Fixed 1.21+ loot table path (`loot_table` singular) so chest loot loads correctly
* Removed accidental nested 26.1.2 workspace copies and committed build jars from git

### Compatibility
* Drop-in update from **1.1.3** for remaining lines
* Loaders:
  * `1.20.1` — Fabric + Forge
  * `1.21.1` / `26.1.2` / `26.2` — Fabric + NeoForge
* Java: 17 (1.20.1), 21 (1.21.1), 25 (26.1.2 / 26.2)

### Upgrade Notes
1. Remove any previous Much More Dungeons jar for your Minecraft / loader line
2. Install the matching `1.2.0` jar
3. Restart the client or server; locate with `/locate structure muchmoredungeons:soulfire_crypt`
