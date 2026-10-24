#!/usr/bin/env python3
"""Writes the mod's data files (loot tables, advancements, tags, structures, structure sets, language) into every
workspace, each in the format of its Minecraft version. Edit the tables here, not the generated JSON.

  python3 tools/datagen.py

Format differences handled here (checked against each version's vanilla data):
  1.20.1   plural folders (loot_tables, advancements), "function" lists, {"item": id} icons, "structure" in location
           predicates, exploration map destination without '#', enchant_with_levels "treasure"
  1.21.1   singular folders, {"id": id} icons, "structures", "options" instead of "treasure", texture backgrounds
  26.x     asset-id advancement backgrounds
  26.2+    namespaced entity sub-predicates ("minecraft:location")
  26.3     loot "modifier" (with "type") instead of "functions" (with "function"), "condition" instead of
           "conditions", map destination as a '#tag', spawn override "count" instead of minCount/maxCount,
           exploration maps fill the item they are given (filled_map, dropped when nothing is found)
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from labyrinths import ENDS, HALLS, THEMES  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
NS = 'muchmoredungeons'
VERSIONS = ['1.20.1', '1.21.1', '26.1.2', '26.2', '26.3']

DUNGEONS = ['outdoor_villa', 'tower_dungeon', 'dungeon_t2', 'soulfire_crypt']
TITLES = {
    'outdoor_villa': "Smuggler's Villa",
    'tower_dungeon': 'Arcane Spire',
    'dungeon_t2': 'Cursed Keep',
    'soulfire_crypt': 'Soulfire Crypt',
}
GUARDIANS = {
    'outdoor_villa': 'Smuggler Chief',
    'tower_dungeon': 'Spire Illusionist',
    'dungeon_t2': 'Keep Warlord',
    'soulfire_crypt': 'Cinder Warden',
}
# Loot tiers. Each dungeon's treasure maps lead to a dungeon of the next tier (in the Overworld).
TIER = {'outdoor_villa': 1, 'tower_dungeon': 2, 'dungeon_t2': 3, 'soulfire_crypt': 4}
TIER.update({k: t['tier'] for k, t in THEMES.items()})
TIER_BASE = {1: 'outdoor_villa', 2: 'tower_dungeon', 3: 'dungeon_t2', 4: 'soulfire_crypt'}
ROMAN = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}
OVERWORLD = [k for k in TIER if THEMES.get(k, {}).get('dimension') != 'nether']
LABYRINTHS = list(THEMES)
ALL = DUNGEONS + LABYRINTHS
TITLES.update({k: t['name'] for k, t in THEMES.items()})
GUARDIANS.update({k: t['guardian'][1] for k, t in THEMES.items()})
# Labyrinth placement: spacing, separation, salt.
LABYRINTH_SETS = {
    'catacombs': (22, 8, 31001), 'sandstone_tomb': (22, 8, 31002), 'overgrown_warrens': (22, 8, 31003),
    'frost_vaults': (24, 8, 31004), 'deepslate_halls': (20, 7, 31005), 'nether_bastille': (18, 6, 31006),
}

# Placement: spacing and separation in chunks, salt, and how many chunks to keep clear of villages.
SETS = {
    'outdoor_villa': (24, 8, 65432),
    'tower_dungeon': (34, 12, 12345),
    'dungeon_t2': (28, 10, 54321),
    'soulfire_crypt': (28, 10, 884422),
}
VILLAGE_CLEARANCE = 4

# Biomes. Vanilla tags such as #minecraft:is_forest already include most modded biomes; the conventional tags are
# optional entries, so a missing tag never breaks loading.
BIOMES = {
    'outdoor_villa': (['minecraft:plains', 'minecraft:sunflower_plains', 'minecraft:meadow', 'minecraft:flower_forest',
                       'minecraft:savanna', 'minecraft:savanna_plateau'], ['plains']),
    'tower_dungeon': (['#minecraft:is_forest', '#minecraft:is_taiga'], []),
    'dungeon_t2': (['minecraft:desert', '#minecraft:is_badlands', 'minecraft:swamp', 'minecraft:mangrove_swamp',
                    '#minecraft:is_jungle', '#minecraft:is_savanna'], ['desert']),
    'soulfire_crypt': (['minecraft:snowy_plains', 'minecraft:snowy_taiga', 'minecraft:ice_spikes', 'minecraft:grove',
                        'minecraft:snowy_slopes', 'minecraft:taiga', 'minecraft:old_growth_pine_taiga',
                        'minecraft:old_growth_spruce_taiga', 'minecraft:windswept_hills',
                        'minecraft:windswept_gravelly_hills', 'minecraft:windswept_forest'], ['snowy']),
}
# Conventional tag names per version for the optional entries above.
CONVENTIONAL = {
    'legacy': lambda name: [f'#c:{name}', f'#forge:is_{name}'],
    'modern': lambda name: [f'#c:is_{name}'],
}

SPAWN_OVERRIDES = {
    'soulfire_crypt': {'monster': {'bounding_box': 'piece', 'spawns': [
        {'type': 'minecraft:wither_skeleton', 'weight': 80, 'minCount': 1, 'maxCount': 2},
        {'type': 'minecraft:stray', 'weight': 60, 'minCount': 1, 'maxCount': 3},
    ]}},
}


# Loot ----------------------------------------------------------------------------------------------------------------
# An entry is (item, weight, count or (min, max) or None, extras) where extras is 'enchant', ('levels', lo, hi) or
# ('treasure', lo, hi) for enchanted gear and books.

def e(item, weight, count=None, extra=None):
    return (item, weight, count, extra)


SUPPLIES = {
    'outdoor_villa': [
        e('bread', 12, (2, 5)), e('wheat', 10, (3, 9)), e('potato', 8, (2, 6)), e('carrot', 8, (2, 6)),
        e('leather', 8, (1, 4)), e('string', 8, (2, 6)), e('arrow', 8, (4, 12)), e('iron_nugget', 8, (3, 9)),
        e('iron_ingot', 6, (1, 3)), e('emerald', 5, (1, 3)), e('gold_nugget', 6, (2, 7)), e('torch', 6, (4, 12)),
    ],
    'tower_dungeon': [
        e('bread', 8, (2, 4)), e('apple', 8, (2, 5)), e('iron_ingot', 12, (2, 6)), e('gold_ingot', 8, (1, 4)),
        e('redstone', 8, (3, 9)), e('lapis_lazuli', 8, (3, 9)), e('arrow', 8, (6, 16)), e('bone', 8, (2, 6)),
        e('string', 6, (2, 5)), e('ender_pearl', 3, (1, 2)), e('emerald', 5, (1, 4)), e('experience_bottle', 4, (1, 3)),
    ],
    'dungeon_t2': [
        e('gold_ingot', 10, (2, 6)), e('iron_ingot', 10, (2, 6)), e('obsidian', 6, (1, 4)), e('arrow', 8, (8, 20)),
        e('gunpowder', 8, (2, 6)), e('bone', 8, (3, 8)), e('ender_pearl', 5, (1, 3)), e('emerald', 6, (2, 6)),
        e('experience_bottle', 5, (2, 5)), e('cooked_beef', 6, (2, 5)), e('blaze_powder', 4, (1, 3)),
    ],
    'soulfire_crypt': [
        e('soul_lantern', 8, (1, 3)), e('soul_sand', 8, (2, 8)), e('coal', 10, (3, 10)), e('bone', 10, (3, 8)),
        e('blaze_rod', 8, (1, 3)), e('gold_ingot', 8, (2, 5)), e('crying_obsidian', 5, (1, 3)),
        e('experience_bottle', 6, (2, 6)), e('magma_cream', 5, (1, 3)), e('quartz', 6, (3, 9)),
    ],
}
VALUABLES = {
    'outdoor_villa': [
        e('crossbow', 6, None, ('levels', 5, 15)), e('iron_sword', 5, None, ('levels', 5, 15)),
        e('leather_horse_armor', 4), e('saddle', 4), e('name_tag', 3), e('book', 4, None, ('levels', 5, 15)),
        e('golden_apple', 2), e('lead', 4), e('diamond', 1),
    ],
    'tower_dungeon': [
        e('iron_sword', 5, None, ('levels', 15, 25)), e('bow', 5, None, ('levels', 15, 25)),
        e('iron_chestplate', 4, None, ('levels', 15, 25)), e('iron_helmet', 4, None, ('levels', 15, 25)),
        e('book', 6, None, ('levels', 15, 25)), e('golden_apple', 4), e('diamond', 3, (1, 2)),
        e('iron_horse_armor', 3), e('name_tag', 3),
    ],
    'dungeon_t2': [
        e('diamond', 6, (1, 3)), e('diamond_sword', 3, None, ('levels', 20, 30)),
        e('diamond_pickaxe', 3, None, ('levels', 20, 30)), e('iron_chestplate', 4, None, ('levels', 20, 30)),
        e('book', 6, None, ('levels', 20, 30)), e('golden_apple', 5), e('diamond_horse_armor', 2),
        e('netherite_upgrade_smithing_template', 1),
    ],
    'soulfire_crypt': [
        e('diamond', 6, (1, 3)), e('netherite_scrap', 4), e('wither_skeleton_skull', 2),
        e('diamond_sword', 3, None, ('levels', 30, 39)), e('bow', 3, None, ('levels', 30, 39)),
        e('book', 6, None, ('levels', 30, 39)), e('golden_apple', 5), e('netherite_upgrade_smithing_template', 2),
    ],
}
VAULT = {
    'outdoor_villa': [
        e('emerald', 8, (4, 10)), e('iron_ingot', 8, (3, 8)), e('gold_ingot', 6, (2, 5)), e('diamond', 4, (1, 2)),
        e('crossbow', 5, None, ('levels', 10, 20)), e('iron_chestplate', 4, None, ('levels', 10, 20)),
        e('golden_apple', 4), e('book', 4, None, ('levels', 10, 20)),
    ],
    'tower_dungeon': [
        e('diamond', 8, (1, 3)), e('emerald', 6, (4, 10)), e('ender_pearl', 6, (2, 4)), e('golden_apple', 6, (1, 2)),
        e('diamond_sword', 3, None, ('levels', 15, 25)), e('bow', 4, None, ('levels', 20, 30)),
        e('book', 5, None, ('treasure', 20, 30)), e('experience_bottle', 5, (4, 8)),
    ],
    'dungeon_t2': [
        e('diamond', 8, (2, 5)), e('emerald_block', 4, (1, 2)), e('golden_apple', 6, (1, 3)),
        e('enchanted_golden_apple', 1), e('diamond_chestplate', 3, None, ('treasure', 25, 35)),
        e('diamond_sword', 3, None, ('treasure', 25, 35)), e('netherite_upgrade_smithing_template', 3),
        e('totem_of_undying', 2), e('book', 5, None, ('treasure', 25, 35)),
    ],
    'soulfire_crypt': [
        e('netherite_ingot', 2), e('netherite_scrap', 6, (1, 3)), e('diamond', 8, (3, 6)),
        e('enchanted_golden_apple', 2), e('wither_skeleton_skull', 4), e('diamond_axe', 3, None, ('treasure', 30, 39)),
        e('diamond_chestplate', 3, None, ('treasure', 30, 39)), e('book', 6, None, ('treasure', 30, 39)),
        e('netherite_upgrade_smithing_template', 4),
    ],
}
ROLLS = {  # supplies, valuables
    'outdoor_villa': ((3, 6), (1, 2)),
    'tower_dungeon': ((3, 6), (1, 2)),
    'dungeon_t2': ((4, 7), (1, 3)),
    'soulfire_crypt': ((4, 7), (2, 3)),
}


class Dialect:
    def __init__(self, version):
        self.v = version
        self.legacy = version == '1.20.1'
        self.v26 = version.startswith('26.')
        # 26.2 moved entity sub-predicates into a registry with namespaced keys ("minecraft:location").
        self.namespaced_predicates = version in ('26.2', '26.3')
        self.modifier = version == '26.3'

    # Folders
    def loot_dir(self):
        return 'loot_tables' if self.legacy else 'loot_table'

    def advancement_dir(self):
        return 'advancements' if self.legacy else 'advancement'

    # Loot
    def fn(self, fname, **fields):
        key = 'type' if self.modifier else 'function'
        return {key: f"minecraft:{fname}", **fields}

    def with_functions(self, entry, functions):
        if functions:
            entry['modifier' if self.modifier else 'functions'] = functions if len(functions) > 1 or not self.modifier else functions[0]
        return entry

    @staticmethod
    def uniform(lo, hi):
        return {'type': 'minecraft:uniform', 'min': lo, 'max': hi}

    def enchant(self, kind, lo, hi):
        if kind == 'enchant':
            return self.fn('enchant_randomly')
        f = self.fn('enchant_with_levels', levels=self.uniform(lo, hi))
        if kind == 'treasure' and self.legacy:
            f['treasure'] = True
        return f

    def item(self, entry):
        item, weight, count, extra = entry
        out = {'type': 'minecraft:item', 'name': f'minecraft:{item}', 'weight': weight}
        functions = []
        if isinstance(count, tuple):
            functions.append(self.fn('set_count', count=self.uniform(*count)))
        elif count:
            functions.append(self.fn('set_count', count=count))
        if extra:
            functions.append(self.enchant(*((extra,) if isinstance(extra, str) else extra)))
        return self.with_functions(out, functions)

    def treasure_map(self, tier, weight=1):
        tag = f'{NS}:on_tier{tier}_maps'
        destination = f'#{tag}' if self.modifier else tag
        decoration = 'red_x' if self.legacy else 'minecraft:red_x'
        name = {'translate': f'item.{NS}.map.tier{tier}', 'fallback': f'Dungeon Map: Tier {ROMAN[tier]}'}
        set_name = self.fn('set_name', name=name)
        if not self.legacy:
            set_name['target'] = 'item_name'
        functions = [self.fn('exploration_map', destination=destination, decoration=decoration, zoom=2,
                             search_radius=12, skip_existing_chunks=True)]
        item = 'minecraft:map'
        if self.modifier:
            # 26.3 writes the map data onto the item it is given instead of turning an empty map into a filled
            # one; like vanilla, drop the map when no dungeon was found.
            item = 'minecraft:filled_map'
            functions.append(self.fn('filtered', item_filter={'predicates': {'minecraft:map_id': {}}},
                                     on_fail=self.fn('discard')))
        functions.append(set_name)
        return self.with_functions({'type': 'minecraft:item', 'name': item, 'weight': weight}, functions)

    @staticmethod
    def pool(rolls, entries):
        return {'rolls': Dialect.uniform(*rolls) if isinstance(rolls, tuple) else rolls, 'entries': entries}

    def spawn_overrides(self, overrides):
        """26.3 replaced minCount/maxCount with an int provider under "count"."""
        if not self.modifier:
            return overrides
        out = json.loads(json.dumps(overrides))
        for category in out.values():
            for spawn in category['spawns']:
                lo, hi = spawn.pop('minCount'), spawn.pop('maxCount')
                spawn['count'] = lo if lo == hi else {'type': 'minecraft:uniform', 'min_inclusive': lo, 'max_inclusive': hi}
        return out

    # Advancements
    def icon(self, item):
        return {'item': f'minecraft:{item}'} if self.legacy else {'id': f'minecraft:{item}'}

    def background(self):
        if self.v26:
            return 'minecraft:block/mossy_stone_bricks'
        return 'minecraft:textures/block/mossy_stone_bricks.png'

    def sub(self, name):
        return f'minecraft:{name}' if self.namespaced_predicates else name

    def entity_properties(self, predicate):
        if self.modifier:
            return {'type': 'minecraft:entity_properties', 'entity': 'this', 'predicate': predicate}
        return [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': predicate}]

    def in_structure(self, dungeon):
        key = 'structure' if self.legacy else 'structures'
        return {'trigger': 'minecraft:location', 'conditions': {'player': self.entity_properties(
            {self.sub('location'): {key: f'{NS}:{dungeon}'}})}}

    def killed_guardian(self, dungeon):
        tag = f'{NS}.guardian.{dungeon}'
        if self.modifier:
            predicate = {'minecraft:entity_tags': {'any_of': [tag]}}
        else:
            predicate = {self.sub('nbt'): '{Tags:["%s"]}' % tag}
        return {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': self.entity_properties(predicate)}}


def text(key, fallback):
    return {'translate': key, 'fallback': fallback}


ICONS = {'outdoor_villa': 'barrel', 'tower_dungeon': 'amethyst_shard', 'dungeon_t2': 'iron_bars',
         'soulfire_crypt': 'soul_lantern', 'catacombs': 'bone', 'sandstone_tomb': 'chiseled_sandstone',
         'overgrown_warrens': 'moss_block', 'frost_vaults': 'blue_ice', 'deepslate_halls': 'sculk',
         'nether_bastille': 'nether_bricks'}
GUARDIAN_ICONS = {'outdoor_villa': 'iron_axe', 'tower_dungeon': 'bow', 'dungeon_t2': 'diamond_sword',
                  'soulfire_crypt': 'wither_skeleton_skull', 'catacombs': 'skeleton_skull',
                  'sandstone_tomb': 'golden_sword', 'overgrown_warrens': 'spider_eye', 'frost_vaults': 'snowball',
                  'deepslate_halls': 'netherite_sword', 'nether_bastille': 'golden_axe'}
DISCOVER = {
    'outdoor_villa': ('Contraband', "Find a Smuggler's Villa"),
    'tower_dungeon': ('Spellbound Heights', 'Find an Arcane Spire'),
    'dungeon_t2': ('Cursed Ground', 'Enter a Cursed Keep'),
    'soulfire_crypt': ('Cold Fire', 'Enter a Soulfire Crypt'),
    'catacombs': ('Rest in Pieces', 'Enter the Forgotten Catacombs'),
    'sandstone_tomb': ('Sealed Away', 'Enter a Sunscorched Tomb'),
    'overgrown_warrens': ('Into the Green', 'Enter the Verdant Warrens'),
    'frost_vaults': ('Cold Storage', 'Enter the Rimefrost Vaults'),
    'deepslate_halls': ('Bottom of the World', 'Enter the Abyssal Halls'),
    'nether_bastille': ('Hot Property', 'Enter an Infernal Bastille'),
}
SLAY = {
    'outdoor_villa': ('Chief Out', 'Defeat the Smuggler Chief', 50),
    'tower_dungeon': ('Illusions Shattered', 'Defeat the Spire Illusionist', 100),
    'dungeon_t2': ('Warlord Fallen', 'Defeat the Keep Warlord', 150),
    'soulfire_crypt': ('Ashes to Ashes', 'Defeat the Cinder Warden', 250),
    'catacombs': ('Bone Dry', 'Defeat the Bone Warden', 100),
    'sandstone_tomb': ('Dethroned', 'Defeat the Tomb King', 100),
    'overgrown_warrens': ('Exterminator', 'Defeat the Broodmother', 100),
    'frost_vaults': ('Thaw', 'Defeat the Frost Lich', 150),
    'deepslate_halls': ('Knight Fall', 'Defeat the Abyssal Knight', 250),
    'nether_bastille': ('Overseen', 'Defeat the Brute Overseer', 250),
}


def advancements(d: Dialect):
    out = {}
    lang = {}

    def display(name, item, title, desc, frame='task', root=False):
        lang[f'advancements.{NS}.{name}.title'] = title
        lang[f'advancements.{NS}.{name}.description'] = desc
        shown = {'icon': d.icon(item), 'title': text(f'advancements.{NS}.{name}.title', title),
                 'description': text(f'advancements.{NS}.{name}.description', desc), 'frame': frame,
                 'show_toast': not root, 'announce_to_chat': not root and frame != 'task'}
        if root:
            shown['background'] = d.background()
        return shown

    out['root'] = {
        'display': display('root', 'map', 'Much More Dungeons', 'Find one of the dungeons and follow its treasure map',
                           root=True),
        'criteria': {k: d.in_structure(k) for k in ALL},
        'requirements': [ALL[:]],
    }
    for k in ALL:
        title, desc = DISCOVER[k]
        out[f'discover_{k}'] = {
            'parent': f'{NS}:root', 'display': display(f'discover_{k}', ICONS[k], title, desc),
            'criteria': {'entered': d.in_structure(k)}, 'requirements': [['entered']],
        }
        title, desc, xp = SLAY[k]
        out[f'slay_{k}_guardian'] = {
            'parent': f'{NS}:discover_{k}', 'display': display(f'slay_{k}_guardian', GUARDIAN_ICONS[k], title, desc, 'goal'),
            'criteria': {'killed': d.killed_guardian(k)}, 'requirements': [['killed']], 'rewards': {'experience': xp},
        }
    out['all_dungeons'] = {
        'parent': f'{NS}:root',
        'display': display('all_dungeons', 'filled_map', 'Dungeon Delver', 'Enter all four dungeons', 'challenge'),
        'criteria': {k: d.in_structure(k) for k in DUNGEONS}, 'requirements': [[k] for k in DUNGEONS],
        'rewards': {'experience': 300},
    }
    out['all_labyrinths'] = {
        'parent': f'{NS}:root',
        'display': display('all_labyrinths', 'recovery_compass', 'Into Every Maze', 'Enter all six labyrinths', 'challenge'),
        'criteria': {k: d.in_structure(k) for k in LABYRINTHS}, 'requirements': [[k] for k in LABYRINTHS],
        'rewards': {'experience': 500},
    }
    return out, lang


def has_map(k):
    return TIER[k] < 4 and k in OVERWORLD


def loot_tables(d: Dialect):
    """The four dungeons have their own lists; a labyrinth uses its tier's lists plus its own flavour items."""
    tables = {}
    for k in ALL:
        base = TIER_BASE[TIER[k]]
        flavour = [e(item, 8, (1, 4)) for item in THEMES[k]['flavour']] if k in THEMES else []
        supplies, valuables = ROLLS[base]
        pools = [d.pool(supplies, [d.item(x) for x in SUPPLIES[base] + flavour]),
                 d.pool(valuables, [d.item(x) for x in VALUABLES[base]])]
        if has_map(k):
            pools.append(d.pool(1, [d.treasure_map(TIER[k] + 1), {'type': 'minecraft:empty', 'weight': 3}]))
        tables[f'chests/{k}'] = {'type': 'minecraft:chest', 'pools': pools}
        vault = [d.pool((3, 5), [d.item(x) for x in VAULT[base]]), d.pool((2, 4), [d.item(x) for x in SUPPLIES[base] + flavour])]
        if has_map(k):
            vault.append(d.pool(1, [d.treasure_map(TIER[k] + 1)]))
        tables[f'chests/{k}_vault'] = {'type': 'minecraft:chest', 'pools': vault}
    return tables


def labyrinth_data(d: Dialect, data: Path):
    """Template pools, jigsaw structures, structure sets and biome tags of the labyrinths."""
    def element(tid, piece):
        return {'element_type': 'minecraft:single_pool_element', 'location': f'{NS}:labyrinth/{tid}/{piece}',
                'projection': 'rigid', 'processors': 'minecraft:empty'}

    def pool(tid, name, pieces, fallback='minecraft:empty'):
        write(data / 'worldgen/template_pool/labyrinth' / tid / f'{name}.json',
              {'fallback': fallback, 'elements': [{'weight': w, 'element': element(tid, p)} for p, w in pieces]})

    for tid, t in THEMES.items():
        ends = f'{NS}:labyrinth/{tid}/ends'
        pool(tid, 'start', [('start', 1)])
        pool(tid, 'halls', HALLS, ends)
        pool(tid, 'ends', ENDS)
        pool(tid, 'vault', [('vault', 1)], ends)
        structure = {'type': 'minecraft:jigsaw', 'biomes': f'#{NS}:has_structure/{tid}', 'step': 'underground_structures',
                     'spawn_overrides': {}, 'terrain_adaptation': 'bury', 'start_pool': f'{NS}:labyrinth/{tid}/start',
                     'size': 6, 'max_distance_from_center': 80, 'use_expansion_hack': False}
        if isinstance(t['depth'], tuple):
            structure['start_height'] = {'absolute': t['depth'][1]}
        else:
            structure['start_height'] = {'absolute': t['depth']}
            structure['project_start_to_heightmap'] = 'WORLD_SURFACE_WG'
        write(data / 'worldgen/structure' / f'{tid}.json', structure)
        spacing, separation, salt = LABYRINTH_SETS[tid]
        placement = {'type': 'minecraft:random_spread', 'spacing': spacing, 'separation': separation, 'salt': salt}
        if t.get('dimension') != 'nether':
            placement['exclusion_zone'] = {'other_set': 'minecraft:villages', 'chunk_count': VILLAGE_CLEARANCE}
        write(data / 'worldgen/structure_set' / f'{tid}_set.json',
              {'structures': [{'structure': f'{NS}:{tid}', 'weight': 1}], 'placement': placement})
        values, conventional = t['biomes']
        entries = list(values)
        for name in conventional:
            for tag in CONVENTIONAL['legacy' if d.legacy else 'modern'](name):
                entries.append({'id': tag, 'required': False})
        write(data / 'tags/worldgen/biome/has_structure' / f'{tid}.json', {'values': entries})


def biome_tag(d: Dialect, k):
    values, conventional = BIOMES[k]
    entries = list(values)
    for name in conventional:
        for tag in CONVENTIONAL['legacy' if d.legacy else 'modern'](name):
            entries.append({'id': tag, 'required': False})
    return {'values': entries}


def write(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def generate(version):
    d = Dialect(version)
    res = REPO / version / 'common/src/main/resources'
    data = res / 'data' / NS
    # Generated folders are rebuilt from scratch; templates (structure/structures) are left alone.
    for folder in (d.loot_dir(), d.advancement_dir(), 'tags', 'worldgen'):
        shutil.rmtree(data / folder, ignore_errors=True)
    for name, table in loot_tables(d).items():
        write(data / d.loot_dir() / f'{name}.json', table)
    advs, lang = advancements(d)
    for name, adv in advs.items():
        write(data / d.advancement_dir() / f'{name}.json', adv)
    for k in DUNGEONS:
        write(data / 'tags/worldgen/biome/has_structure' / f'{k}.json', biome_tag(d, k))
        structure = {'type': f'{NS}:{k}', 'biomes': f'#{NS}:has_structure/{k}', 'step': 'surface_structures',
                     'terrain_adaptation': 'beard_thin', 'spawn_overrides': d.spawn_overrides(SPAWN_OVERRIDES.get(k, {}))}
        write(data / 'worldgen/structure' / f'{k}.json', structure)
        spacing, separation, salt = SETS[k]
        write(data / 'worldgen/structure_set' / f'{k}_set.json', {
            'structures': [{'structure': f'{NS}:{k}', 'weight': 1}],
            'placement': {'type': 'minecraft:random_spread', 'spacing': spacing, 'separation': separation,
                          'salt': salt, 'exclusion_zone': {'other_set': 'minecraft:villages',
                                                           'chunk_count': VILLAGE_CLEARANCE}}})
    labyrinth_data(d, data)
    for tier in (2, 3, 4):
        write(data / 'tags/worldgen/structure' / f'on_tier{tier}_maps.json',
              {'values': [f'{NS}:{k}' for k in OVERWORLD if TIER[k] == tier]})
        lang[f'item.{NS}.map.tier{tier}'] = f'Dungeon Map: Tier {ROMAN[tier]}'
    write(data / 'tags/worldgen/structure/dungeons.json', {'values': [f'{NS}:{k}' for k in ALL]})
    write(data / 'tags/worldgen/structure/labyrinths.json', {'values': [f'{NS}:{k}' for k in LABYRINTHS]})
    write(res / 'assets' / NS / 'lang/en_us.json', dict(sorted(lang.items())))


def main():
    for version in VERSIONS:
        generate(version)
        print('generated', version)


if __name__ == '__main__':
    main()
