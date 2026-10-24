# Much More Dungeons

![Much More Dungeons 2.0](marketing/images/banner.png)

Four handcrafted dungeons and six procedural labyrinths for Minecraft, each with its own biomes, loot tier, themed
spawners and a named guardian. Vaults hold a treasure map to a dungeon of the next tier, from the Smuggler's Villa
(tier 1) to the Soulfire Crypt and the Abyssal Halls (tier 4).

**2.0 "The Labyrinth Update"** rebuilds the mod around its dungeons and adds the labyrinths: see the [2.0.0 notes](patchnotes/2.0.0.md) and the
[design notes](docs/DESIGN-2.0.md).

## Which jar do I download?

Jar names are `muchmoredungeons-{loader}-{minecraft}-{modVersion}.jar`. Match **both** the Minecraft version and the
loader.

| Minecraft | Java | Fabric jar (needs Fabric API) | NeoForge / Forge jar |
|-----------|------|-------------------------------|----------------------|
| 1.20.1 | 17+ | `…-fabric-1.20.1-….jar` | `…-forge-1.20.1-….jar` (Forge 47) |
| 1.21.1 | 21+ | `…-fabric-1.21.1-….jar` | `…-neoforge-1.21.1-….jar` |
| 26.1.2 | 25+ | `…-fabric-26.1.2-….jar` | `…-neoforge-26.1.2-….jar` |
| 26.2 | 25+ | `…-fabric-26.2-….jar` | `…-neoforge-26.2-….jar` |
| 26.3 | 25+ | `…-fabric-26.3-….jar` | `…-neoforge-26.3-….jar` |

Install it on the server and on clients (single player generates its world on the client).

## The dungeons

| Dungeon (id) | Tier | Biomes | Spawners | Guardian |
|--------------|------|--------|----------|----------|
| Smuggler's Villa (`outdoor_villa`) | 1 | plains, sunflower plains, meadows, flower forests, savannas | pillager | Smuggler Chief (vindicator) |
| Arcane Spire (`tower_dungeon`) | 2 | `#minecraft:is_forest`, `#minecraft:is_taiga` | zombie, skeleton, spider, witch | Spire Illusionist (illusioner) |
| Cursed Keep (`dungeon_t2`) | 3 | deserts, badlands, jungles, swamps, savannas | named zombies, husk and witch, skeleton | Keep Warlord (zombie) |
| Soulfire Crypt (`soulfire_crypt`) | 4 | snowy and cold biomes | wither skeleton, blaze | Cinder Warden (wither skeleton) |

## The labyrinths

Underground mazes assembled by the vanilla jigsaw system from fifteen generated pieces per theme (entrance shaft or
hub, corridors, corners, junctions, crossings, stairs, two spawner rooms, storeroom, library, pillared hall, shrine,
dead end, loot alcove, and the vault chamber with two vault chests, two spawners and the guardian, which is always
placed). Every labyrinth is laid out differently. Pieces are buried like ancient cities, so water and lava stay out.

| Labyrinth (id) | Tier | Where | Spawners | Guardian |
|----------------|------|-------|----------|----------|
| Forgotten Catacombs (`catacombs`) | 2 | under plains, meadows and forests | skeleton, zombie | Bone Warden (skeleton) |
| Sunscorched Tomb (`sandstone_tomb`) | 2 | under deserts and badlands | husk, skeleton | Tomb King (husk) |
| Verdant Warrens (`overgrown_warrens`) | 2 | under jungles, swamps and lush caves | spider, cave spider, zombie | Broodmother (spider) |
| Rimefrost Vaults (`frost_vaults`) | 3 | under snowy biomes | stray, skeleton | Frost Lich (stray) |
| Abyssal Halls (`deepslate_halls`) | 4 | deep under any Overworld biome (y -28) | zombie, skeleton, cave spider | Abyssal Knight (wither skeleton) |
| Infernal Bastille (`nether_bastille`) | 4 | the Nether (y 40) | blaze, wither skeleton, magma cube | Brute Overseer (piglin brute) |

## Shared by all ten

- **Loot**: every chest draws from its dungeon's table (`chests/<id>`), the guarded vault from `chests/<id>_vault`.
  Enchantment levels rise from 5-15 in tier 1 to 30-39 in tier 4. Labyrinths add their theme's own items.
- **Treasure maps**: each Overworld vault below tier 4 has a map to a dungeon or labyrinth of the next tier (tags
  `on_tier2_maps` to `on_tier4_maps`), and regular chests sometimes do.
- **Guardians** spawn once when the structure generates: named, persistent, stronger than their kind, and their weapon
  always drops.
- **Advancements**: a Much More Dungeons tab with one advancement per dungeon found, one per guardian defeated (with
  experience), Dungeon Delver for entering all four dungeons and Into Every Maze for all six labyrinths.
- **Placement**: handcrafted dungeons are centred on a chunk, only on dry ground at or above sea level with a limited
  slope. Dungeons and Overworld labyrinths keep four chunks from village placements. Find them with
  `/locate structure muchmoredungeons:<id>`, `#muchmoredungeons:dungeons` (all ten) or `#muchmoredungeons:labyrinths`.

## Configuration

`config/muchmoredungeons.json` is written on first start, with comments. It covers the four handcrafted dungeons;
labyrinths are standard jigsaw structures, configured with datapacks.

| Key | What it does |
|-----|--------------|
| `guardians` | Spawn each dungeon's guardian (default `true`) |
| `dungeons.<id>.enabled` | Generate this dungeon at all (default `true`) |
| `dungeons.<id>.chance` | Share of valid spots that get the dungeon, 0 to 1 (default `1.0`) |

Changes apply after a restart, to newly generated chunks. Everything else is datapack data under
`data/muchmoredungeons/`:

| File | Controls |
|------|----------|
| `worldgen/structure_set/<id>_set.json` | spacing, separation, salt, village clearance |
| `tags/worldgen/biome/has_structure/<id>.json` | biomes |
| `worldgen/structure/<id>.json` | terrain adaptation, spawn overrides |
| `loot_table/chests/<id>.json`, `<id>_vault.json` (`loot_tables/` on 1.20.1) | loot |
| `advancement/` (`advancements/` on 1.20.1) | advancements |
| `worldgen/template_pool/labyrinth/<id>/` | a labyrinth's pools (`start`, `halls`, `ends`, `vault`): add your own rooms |
| `structure/<id>.nbt`, `structure/labyrinth/<id>/` (`structures/` on 1.20.1) | the templates; a `guardian` data marker places the guardian, `chest` and `vault` markers place a loot chest |

`/muchmoredungeons inspect [pos] [fill]` (permission level 2) reports what the dungeon at a position holds: chests by
loot table, spawners by mob, its guardian and where its vault is.

## Upgrading from 1.x

Structure, structure type, piece, template and loot table ids are unchanged, so dungeons already generated stay in
your world. Newly generated chunks use the 2.0 placement and spacing, so dungeons may appear in different places than
1.x would have put them.

## Building

Each Minecraft version is a separate MultiLoader Gradle workspace (`common/`, `fabric/` and `neoforge/`, or `forge/` on
1.20.1). Gradle needs the workspace's Java version: 17 for 1.20.1, 21 for 1.21.1, 25 for 26.x.

```bash
cd 26.3
./gradlew build          # jars in fabric/build/libs and neoforge/build/libs; runs the unit tests
```

Prebuilt release jars go in `releases/` for the publish workflow. Release notes for a version live in
`patchnotes/<version>.md`.

## Tools

- [`tools/datagen.py`](tools/datagen.py): writes loot tables, advancements, tags, structures and structure sets into
  every workspace in that version's format. Edit the tables there, not the JSON.
- [`tools/labyrinths.py`](tools/labyrinths.py): generates every labyrinth piece from its theme (palette, mobs,
  guardian); add a theme there.
- [`tools/templates.py`](tools/templates.py) and [`tools/generate_soulfire_crypt.py`](tools/generate_soulfire_crypt.py):
  fix and generate the structure templates.
- [`tools/qa/`](tools/qa): dev servers and a real game client under Xvfb. `dungeon_checks.py` checks locating,
  natural generation, `/place`, loot tables, spawners, guardians, advancements and the logs; `run_matrix.sh` runs it on
  every build; `marketing_shots.py` captures the listing screenshots; `rarity.py` measures how far the nearest dungeons
  are.
- [`marketing/`](marketing): the CurseForge/Modrinth description, listing images and how to regenerate them.

## Links

- [Discord](https://discord.gg/SAmd9fhNhr)
- [Modrinth](https://modrinth.com/mod/much-more-dungeons)
- [Source and issues](https://github.com/MeherBenSalem/Much-More-Dungeons)
- [Support us](https://nightbeam.dev/support)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

See [.github/SECURITY.md](.github/SECURITY.md).

## License

[Apache License 2.0](LICENSE).
