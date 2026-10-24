# Much More Dungeons 2.0: audit, market gaps and plan

This document records what 1.2.0 actually did, what players expect from a dungeon or structure mod today, where 1.2.0
fell short, and what 2.0 changes. Every 2.0 claim below is implemented and checked in game by
`tools/qa/dungeon_checks.py` on all ten builds (see [CONTRIBUTING](../CONTRIBUTING.md)).

## 1. Audit of 1.2.0

| Area | What the code and data did |
|------|----------------------------|
| Loot | Only the Soulfire Crypt used one of the mod's loot tables. The Tower's chests held **fixed items** saved in the template (every tower gave the same loot), the Dungeon T2 used vanilla `simple_dungeon` and `end_city_treasure`, and the Villa had no loot table at all. `chests/tower_dungeon` and `chests/dungeon_t2` existed but nothing used them. |
| Spawners | All four Tower spawners, the Villa's spawner and one Dungeon T2 spawner were **empty** (no mob). |
| Villa | 145 chests stacked into walls, all empty. |
| Crypt | Each loot chest stood next to a data marker that placed a second chest on top of or beside it; the Cinder Warden was both embedded in the template and spawned by the marker code (two wardens possible). |
| 1.20.1 | A different implementation: plain vanilla jigsaw structures, so the crypt's markers, guardian and loot did nothing. |
| Placement | The template's corner was put at the chunk centre (dungeons were off-centre) at whatever height the centre column had: no check for water, slopes or cliffs, so dungeons could float, hang off hills or stand in lakes. |
| Rarity | Spacing 80 to 100 chunks: the nearest dungeon was often 3,000 to 6,000 blocks away. |
| Biomes | The Villa and Dungeon T2 shared one biome list (swamp, jungle, desert, savanna, badlands); vanilla biome ids only, so biomes from other worldgen mods were never used. |
| Progression | None: no tiers, no advancements, nothing pointing from one dungeon to the next. |
| Config | None. |
| Code | MultiLoader template leftovers (example mixins logging "Hello from Common init", a log line printing the diamond's id), a wrong `sources` URL in `fabric.mod.json`, a 1.21.1 `pack.mcmeta` with format 8. |
| Tooling | No tests, no QA scripts, no release jars in the repo; the publish workflow guessed the Minecraft version and required an unrelated library. |

## 2. What players expect from a dungeon mod

Gathered from the comment sections, issue trackers and reviews of the popular structure and dungeon mods, and from
long-running community wishes (dungeons "are just a cobblestone room", "the loot is rotten flesh and horse armor",
"once you've seen one you've seen them all"). Recurring expectations:

1. **Control over frequency and biomes**, ideally both a simple config and datapack overrides (the larger mods
   moved spacing and biome lists to datapack JSON; players still ask for an on/off switch per structure).
2. **Loot worth the trip, scaled to difficulty**: early structures give early-game help, late ones give late-game
   items; no fixed or copy-pasted chests.
3. **Something to fight**: themed spawners and a named mini-boss at the end.
4. **Visual quality and terrain fit**: no floating buildings, no structures cut in half by cliffs or standing in water.
5. **Compatibility** with other worldgen mods (modded biomes through tags) and datapacks; no overlap with villages.
6. **`/locate` support** and ways to find structures in survival: explorer or treasure maps.
7. **Advancements** for finding and clearing structures.
8. **No worldgen lag**, server-side safety in multiplayer, and stable ids so existing worlds keep working.

## 3. Gap table

| Expectation | 1.2.0 | 2.0 |
|-------------|-------|-----|
| Loot per dungeon | 1 of 4 dungeons used its own table | Every chest of every dungeon draws from that dungeon's table (8 tables: regular + vault per dungeon) |
| Loot progression | none | Four tiers: Smuggler's Villa (early) → Arcane Spire → Cursed Keep → Soulfire Crypt (late); enchantment levels 5-15 up to 30-39, netherite at the end |
| Fixed / duplicated loot | Tower chests identical in every world | Rolled per chest from a seeded table |
| Spawners | 6 empty | All have mobs, themed per dungeon |
| Variety | 4 fixed buildings | 4 handcrafted dungeons **plus 6 procedural labyrinths** whose layout is assembled differently every time |
| Mini-boss | Crypt only (sometimes two) | A named guardian in every dungeon and labyrinth (10), tougher than their kind, persistent, weapon always drops |
| Treasure maps | none | A **dungeon trail**: loot can hold a map to a dungeon of the next tier, and vaults always do |
| Advancements | none | 23: a tab, one per discovery, one per guardian (with XP), Dungeon Delver (all four dungeons) and Into Every Maze (all six labyrinths) |
| Dimensions | Overworld | Overworld and the Nether |
| `/locate` | per structure | per structure, `#muchmoredungeons:dungeons` for any and `#muchmoredungeons:labyrinths` for a labyrinth |
| Terrain fit | centre column only | 16 samples over the footprint: no water, a slope limit per dungeon, never below sea level, centred on its chunk |
| Rarity | nearest often 3k-6k blocks | measured median nearest: Villa ~550, Spire ~770, Crypt ~1,200, Keep ~1,500 blocks |
| Biomes | vanilla ids, two dungeons shared one list | Per-dungeon lists using vanilla biome tags (`#minecraft:is_forest`...) that modded biomes join, plus optional conventional tags (`#c:is_snowy`...) |
| Villages | could overlap | Kept 4 chunks away from village placements |
| Config | none | `config/muchmoredungeons.json`: enable/disable each dungeon, spawn chance per dungeon, guardians on/off |
| Datapacks | spacing/biomes via JSON | same, documented; loot tables, advancements and templates all overridable |
| 1.20.1 | separate jigsaw implementation | identical behaviour to every other version |
| Versions | 1.20.1, 1.21.1, 26.1.2, 26.2 | + 26.3 |
| Admin tooling | none | `/muchmoredungeons inspect` lists a dungeon's chests, spawners and guardian |
| Tests / QA | none | JUnit for placement and config; in-game QA script run on all 10 builds |

## 4. The plan as built

### The unique part: labyrinths

The market gap that stands out most is that dungeon mods ship **fixed** buildings: once you have seen one, you have
seen them all (the most common complaint about vanilla structures too). Procedural, multi-room dungeons exist but are
rarely themed to the land above them, linked to a loot progression or available on every loader and version.

2.0 adds six **labyrinths**: underground dungeons assembled by vanilla's jigsaw system from a generated set of 16
pieces per theme (an entrance shaft or a hub, corridors, corners, tees, crossings, stairs going down, two spawner
rooms, a storeroom, a library, a pillared hall, a shrine, dead ends, alcoves, a vault approach and a vault chamber with
the guardian). Every labyrinth is a different maze, built from its theme's palette, mobs and loot:

| Id | Name | Tier | Where | Guardian |
|----|------|------|-------|----------|
| `catacombs` | Forgotten Catacombs | 2 | under plains, meadows and forests | Bone Warden (skeleton) |
| `sandstone_tomb` | Sunscorched Tomb | 2 | under deserts and badlands | Tomb King (husk) |
| `overgrown_warrens` | Verdant Warrens | 2 | under jungles, swamps and lush caves | Broodmother (spider) |
| `frost_vaults` | Rimefrost Vaults | 3 | under snowy biomes | Frost Lich (stray) |
| `deepslate_halls` | Abyssal Halls | 4 | deep under any Overworld biome (y -28) | Abyssal Knight (wither skeleton) |
| `nether_bastille` | Infernal Bastille | 4 | in the Nether (y 40) | Brute Overseer (piglin brute) |

Because they are standard jigsaw structures, datapacks can add pieces to any pool, and the pieces are generated by
`tools/labyrinths.py`, so a new theme is a palette and a few lines.

### Dungeons and tiers

| Id (unchanged) | Name | Tier | Biomes | Guardian |
|----------------|------|------|--------|----------|
| `outdoor_villa` | Smuggler's Villa | 1 | plains, sunflower plains, meadow, flower forest, savanna | Smuggler Chief (vindicator, iron axe) |
| `tower_dungeon` | Arcane Spire | 2 | `#minecraft:is_forest`, `#minecraft:is_taiga` | Spire Illusionist (illusioner, bow) |
| `dungeon_t2` | Cursed Keep | 3 | desert, badlands, swamps, jungles, savannas | Keep Warlord (zombie, diamond sword) |
| `soulfire_crypt` | Soulfire Crypt | 4 | snowy and cold biomes | Cinder Warden (wither skeleton, diamond axe) |

Structure, structure type, piece type, template and loot table ids are those of 1.2.0, so saved worlds load and keep
their dungeons. Chunks generated after the update use the new placement and spacing.

### Code

* `common/` holds everything: `Dungeon` (MC-free definitions), `Placement` (MC-free terrain decision), the config,
  one `DungeonStructure` and `DungeonPiece` class serving all four dungeons, `Guardians` and the inspect command.
  Loader modules only register the types, the command and the config folder.
* Data files are generated by `tools/datagen.py` in each Minecraft version's own format (folder names, predicate and
  loot function syntax changed several times between 1.20.1 and 26.3).
* Templates are fixed by `tools/templates.py`; the crypt is generated by `tools/generate_soulfire_crypt.py`.

### Out of scope for 2.0

* Cartographer trades for the maps: loader-specific trade events on every version for little gain over the loot trail.
* Boss bars and custom guardian AI: the guardians are vanilla mobs with better stats and gear.
* The config's on/off switch, chance and guardian toggle apply to the four handcrafted dungeons; labyrinths are
  standard jigsaw structures controlled by their structure set and pools (datapack data).
