# QA record: 2.0.0

`tools/qa/run_matrix.sh` (see [CONTRIBUTING](../CONTRIBUTING.md#testing-in-game)) on a fresh world per build: a dev
server and a real game client under Xvfb, driven over RCON by `tools/qa/dungeon_checks.py`. The jars in `releases/`
were built from the same commit's sources.

| Build | Checks | Failures |
|-------|--------|----------|
| 1.20.1 Fabric | 211 | 0 |
| 1.20.1 Forge | 211 | 0 |
| 1.21.1 Fabric | 211 | 0 |
| 1.21.1 NeoForge | 211 | 0 |
| 26.1.2 Fabric | 211 | 0 |
| 26.1.2 NeoForge | 211 | 0 |
| 26.2 Fabric | 211 | 0 |
| 26.2 NeoForge | 211 | 0 |
| 26.3 Fabric | 211 | 0 |
| 26.3 NeoForge | 211 | 0 |

The 211 checks of each build, for all ten structures (four dungeons, six labyrinths, the Infernal Bastille in the
Nether):

| Group | Checks | What |
|-------|--------|------|
| locate | 12 | `/locate structure` finds each one, and the `#muchmoredungeons:dungeons` and `#muchmoredungeons:labyrinths` tags work |
| natural | 68 | The located one generates and holds: chests on its own loot table, its vault on the vault table, loot rolled into them, a treasure map to the next tier where it has one, spawners with the expected mobs, its guardian alive |
| place, placed | 78 | `/place structure` places another one elsewhere, inspected the same way |
| loot | 20 | Every loot table (regular and vault) rolls |
| client | 31 | A real client walks into each one (discovery advancement), defeats its guardian (guardian advancement, and the guardian's weapon drops), then has Dungeon Delver and Into Every Maze |
| log | 2 | The server log has no errors about the mod, its loot, advancements or structures, and no errors at all |

## Found and fixed by this QA

* Labyrinth guardians lost their weapon (the Abyssal Knight held a stone sword): jigsaw runs `finalizeSpawn` on template
  mobs. The mod now gives the weapon back when the guardian first joins the world.
* `/muchmoredungeons inspect` could report a labyrinth's vault as the vault of a dungeon above it.
* 26.2 NeoForge granted no kill advancements on its first beta build (26.2.0.1-beta); the 26.2 jar now builds
  against 26.2.0.93.
* Current NeoForge versions deprecate `logoFile`; the NeoForge jars now also declare `iconFile`.
