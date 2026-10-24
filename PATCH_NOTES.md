# Patch notes

## 2.0.0 — The Dungeon Trail

Four tiers of loot with a guarded vault per dungeon, a named guardian in each dungeon, treasure maps leading from one
dungeon to the next, ten advancements, terrain-aware placement (no floating or flooded dungeons), more frequent
dungeons with per-dungeon biomes, a config file and `/muchmoredungeons inspect`. Available for Minecraft 1.20.1
(Fabric, Forge), 1.21.1, 26.1.2, 26.2 and 26.3 (Fabric, NeoForge). Ids are unchanged; 1.x worlds keep their dungeons.

Full notes: [patchnotes/2.0.0.md](patchnotes/2.0.0.md).

## 1.2.0

- Added **Soulfire Crypt** — cold-biome soul-fire crypt with wither skeleton / blaze spawners, ambient hostiles, and a named Cinder Warden
- New chest loot table `muchmoredungeons:chests/soulfire_crypt`
- Fixed 1.21+ loot data path (`loot_table`) so crypt chests fill correctly
- Licensed under Apache-2.0; OSS cleanup (NOTICE, CONTRIBUTING, SECURITY, clutter removal)

## 1.1.3

- Added Minecraft 26.2 MultiLoader workspace (Fabric + NeoForge)
- Fixed 26.1.2 toolchain targeting (Minecraft 26.1.2 dependencies)
- Aligned shared mod version to 1.1.3 across workspaces
- MultiLoader matrix: `1.20.1`, `1.21.1`, `26.1.2`, `26.2`
- Dropped workspaces: `1.21.5`, `1.21.8`, `1.21.11`
