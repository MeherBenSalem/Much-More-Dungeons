![Much More Dungeons](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/banner.png)

**Four handcrafted dungeons, and a reason to go from one to the next.** Each dungeon has its own biomes, its own
loot tier, themed spawners and a named guardian at the end. Its vault holds a treasure map to the next dungeon:
from a smugglers' villa in the plains to an arcane spire in the forest, a cursed keep in the desert and, last, a
soulfire crypt in the snow.

Fabric and NeoForge (Forge on 1.20.1) · Minecraft 1.20.1, 1.21.1, 26.1.2, 26.2 and 26.3 · install on the server and
clients

![What's new in 2.0](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/header-whats-new.png)

Version 2.0 rebuilds the mod around the four dungeons it already had. Here's what changed from 1.x:

- **Every chest has real loot**: each dungeon has its own loot table and a guarded **vault**, in four tiers from
  early game to late game (1.x towers all had the same fixed chest contents, and most dungeons used vanilla tables)
- **A guardian in every dungeon**: the Smuggler Chief, the Spire Illusionist, the Keep Warlord and the Cinder Warden
- **The dungeon trail**: treasure maps lead from each dungeon to the next
- **10 advancements** in their own tab, with experience for every guardian
- **Better placement**: dungeons are centred, never in water or below sea level, never on steep slopes, and kept
  away from villages
- **More often**: the nearest dungeon is usually within a few hundred to about 1,500 blocks instead of thousands
- Biome tags that **modded biomes** join, a **config file**, and `/muchmoredungeons inspect` for server admins
- Empty spawners fixed, the Villa's walls of empty chests are now barrels, and the Soulfire Crypt has a new exterior
- Now for **Minecraft 26.3** too, and 1.20.1 works exactly like every other version
- Your 1.x worlds keep their dungeons: every id is unchanged

![The dungeons](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/header-dungeons.png)

![Four dungeons](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/card-dungeons.png)

| Dungeon | Tier | Where | Spawners | Guardian |
|---------|------|-------|----------|----------|
| Smuggler's Villa | 1 | plains, sunflower plains, meadows, flower forests, savannas | pillager | Smuggler Chief |
| Arcane Spire | 2 | forests and taigas | zombie, skeleton, spider, witch | Spire Illusionist |
| Cursed Keep | 3 | deserts, badlands, jungles, swamps, savannas | cursed warriors, berserker, shadow mage, rage brute, skeleton | Keep Warlord |
| Soulfire Crypt | 4 | snowy plains and slopes, groves, ice spikes, taigas, windswept hills | wither skeleton, blaze | Cinder Warden |

![Smuggler's Villa](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/card-villa.png)

![Arcane Spire](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/card-spire.png)

![Cursed Keep](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/card-keep.png)

![Soulfire Crypt](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/card-crypt.png)

![The dungeon trail](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/header-trail.png)

![Follow the map](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/card-trail.png)

Every vault holds a treasure map to the next dungeon on the trail, and a regular chest sometimes has one too:

**Smuggler's Villa → Arcane Spire → Cursed Keep → Soulfire Crypt**

The map marks the dungeon with a red X and leads to one in land nobody has explored yet. You can also find
any dungeon with `/locate structure muchmoredungeons:<id>`, or the nearest of the four with
`/locate structure #muchmoredungeons:dungeons`.

![Guardians](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/header-guardians.png)

![Something to fight](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/card-guardians.png)

Each dungeon spawns its guardian once, when it generates. Guardians are vanilla mobs with a name, more health, armour
and damage, and better gear. They never despawn, and the weapon they hold always drops.

| Guardian | Dungeon | Mob | Health | Drops |
|----------|---------|-----|--------|-------|
| Smuggler Chief | Smuggler's Villa | vindicator | 60 | iron axe |
| Spire Illusionist | Arcane Spire | illusioner | 70 | bow |
| Keep Warlord | Cursed Keep | zombie | 100 | diamond sword |
| Cinder Warden | Soulfire Crypt | wither skeleton | 140 | diamond axe |

![Loot](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/header-loot.png)

![Four tiers of treasure](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/card-loot.png)

Every chest rolls from its dungeon's table when it is first opened; the vault (the guarded chest) rolls from a
richer one. Enchanted gear and books scale with the tier:

| Tier | Supplies | Valuables | Vault highlights | Enchantment levels |
|------|----------|-----------|------------------|--------------------|
| 1 · Villa | bread, crops, leather, string, arrows, iron, emeralds | crossbows, iron swords, saddles, name tags | emeralds, diamonds, enchanted iron chestplate | 5-15 (vault 10-20) |
| 2 · Spire | iron, gold, redstone, lapis, pearls, bottles o' enchanting | enchanted iron armour, bows, books, golden apples | diamonds, ender pearls, enchanted diamond sword | 15-25 (vault up to 30) |
| 3 · Keep | gold, iron, obsidian, pearls, blaze powder | diamonds, enchanted diamond tools, upgrade template | emerald blocks, totem of undying, enchanted golden apple | 20-30 (vault 25-35) |
| 4 · Crypt | soul lanterns, blaze rods, quartz, gold, crying obsidian | netherite scrap, wither skulls, enchanted diamond gear | netherite ingot, enchanted golden apples, upgrade templates | 30-39 |

![Advancements](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/header-advancements.png)

![A tab of its own](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/card-advancements.png)

Find each dungeon, defeat each guardian (50 to 250 experience), and enter all four for **Dungeon Delver** (300
experience).

![For servers and modpacks](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/header-config.png)

![Your world, your rules](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/card-worldgen.png)

- **`config/muchmoredungeons.json`**: turn a dungeon off, set the share of valid spots that get one (`chance`, 0 to
  1), or turn guardians off. Applies to newly generated chunks after a restart.
- **Datapacks**: spacing and separation (`worldgen/structure_set`), biomes (`tags/worldgen/biome/has_structure`), loot
  tables, advancements and the structure templates are ordinary data files under the `muchmoredungeons` namespace.
- **Modded biomes**: biome lists use vanilla biome tags such as `#minecraft:is_forest`, which most biome mods add
  their biomes to, plus optional conventional tags such as `#c:is_snowy`.
- **Villages**: dungeons keep four chunks away from village placements.
- **`/muchmoredungeons inspect`** (operators): what the dungeon you stand in holds: its chests by loot table, its
  spawners, its guardian and where its vault is.
- No new blocks, items or entities: dungeons are built from vanilla blocks and stay standing if the mod is removed.

![Downloads](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/header-compatibility.png)

| Minecraft | Fabric | NeoForge / Forge | Java |
|-----------|--------|------------------|------|
| 26.3 | ✔ (Fabric API) | ✔ NeoForge | 25 |
| 26.2 | ✔ (Fabric API) | ✔ NeoForge | 25 |
| 26.1.2 | ✔ (Fabric API) | ✔ NeoForge | 25 |
| 1.21.1 | ✔ (Fabric API) | ✔ NeoForge | 21 |
| 1.20.1 | ✔ (Fabric API) | ✔ Forge | 17 |

Pick the file whose name has your Minecraft version and loader, for example
`muchmoredungeons-fabric-1.21.1-2.0.0.jar`.

![FAQ](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/header-faq.png)

**Do I need to start a new world?** No. Every id is unchanged, so dungeons already in your world stay. New chunks get
the 2.0 placement, loot and guardians.

**Where do I install it?** Wherever worlds are generated: on the server, and on your client for single player. Install
the same version on clients that join a server running it.

**Can I make dungeons rarer or more common?** Rarer: lower `chance` in the config. Either way: change `spacing` and
`separation` in `worldgen/structure_set/<dungeon>_set.json` with a datapack.

**Can I change the loot?** Yes: override `loot_table/chests/<dungeon>.json` and `<dungeon>_vault.json` in a datapack
(`loot_tables/` on 1.20.1).

**How do I find one?** `/locate structure #muchmoredungeons:dungeons`, or open a vault and follow its map.

![Gallery](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/header-gallery.png)

![Arcane Spire](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/screenshots/spire.jpg)

![Cursed Keep](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/screenshots/keep.jpg)

![Soulfire Crypt](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/screenshots/crypt.jpg)

![Smuggler's Villa](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/screenshots/villa.jpg)

![Divider](https://raw.githubusercontent.com/MeherBenSalem/Much-More-Dungeons/main/marketing/images/divider.png)

[Discord](https://discord.gg/SAmd9fhNhr) · [Source and issues](https://github.com/MeherBenSalem/Much-More-Dungeons) · [Support us](https://nightbeam.dev/support) · Made by NightBeam Studio
