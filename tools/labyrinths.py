#!/usr/bin/env python3
"""The labyrinths: underground dungeons assembled by vanilla jigsaw from generated rooms, corridors and stairs, so no
two are alike. This module defines the themes (used by datagen.py too) and, run as a script, writes every theme's
structure templates into every workspace:

  python3 tools/labyrinths.py            (needs nbtlib)

Every theme uses the same set of pieces, built from its own palette:
  entrance   a shaft from the surface down to a landing (themes with an entrance)
  hub        a pillared hall, the start of themes without an entrance (deep and Nether labyrinths)
  corridor, corner, tee, cross, stairs                         -> pool <theme>/halls
  spawner_a, spawner_b, storeroom, library, pillar_hall, shrine -> pool <theme>/halls
  dead_end, alcove                                              -> pool <theme>/ends (the fallback)
  vault      an antechamber and the guarded vault chamber with the guardian; it is the start's only neighbour, so it
             is always placed, and the maze grows from the antechamber's two side doors
Pieces meet at jigsaw blocks named muchmoredungeons:door in the middle of 3x3 doorways.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

NS = 'muchmoredungeons'
REPO = Path(__file__).resolve().parents[1]
WORKSPACES = {'1.20.1': 'structures', '1.21.1': 'structure', '26.1.2': 'structure', '26.2': 'structure', '26.3': 'structure'}
DATA_VERSION = 3465  # 1.20.1: every newer version upgrades the templates when it loads them

# id: name, tier, guardian (entity, name, health, armor, attack, mainhand, helmet), spawner mobs, biomes
# (entries and optional conventional tag names), how deep the corridors are (relative to the surface, or an absolute
# y with no entrance), palette, flavour loot added to the tier's tables.
THEMES = {
    'catacombs': dict(
        name='Forgotten Catacombs', tier=2,
        guardian=('minecraft:skeleton', 'Bone Warden', 80, 8, 6, 'minecraft:bow', 'minecraft:iron_helmet'),
        mobs=['minecraft:skeleton', 'minecraft:zombie'],
        biomes=(['minecraft:plains', 'minecraft:sunflower_plains', 'minecraft:meadow', '#minecraft:is_forest'], ['plains']),
        depth=-14,
        palette=dict(wall=[('stone_bricks', 6), ('mossy_stone_bricks', 3), ('cracked_stone_bricks', 2)],
                     floor=[('stone_bricks', 4), ('cobblestone', 2), ('mossy_cobblestone', 1)], ceiling=[('stone_bricks', 1)],
                     pillar='chiseled_stone_bricks', trim='polished_andesite', light='lantern', glow='glowstone',
                     decor=['skeleton_skull', 'bone_block', 'cobweb', 'candle'], stairs='stone_brick_stairs',
                     shelf='bookshelf'),
        flavour=['bone', 'arrow', 'candle']),
    'sandstone_tomb': dict(
        name='Sunscorched Tomb', tier=2,
        guardian=('minecraft:husk', 'Tomb King', 90, 10, 7, 'minecraft:golden_sword', 'minecraft:golden_helmet'),
        mobs=['minecraft:husk', 'minecraft:skeleton'],
        biomes=(['minecraft:desert', '#minecraft:is_badlands'], ['desert']),
        depth=-14,
        palette=dict(wall=[('sandstone', 5), ('cut_sandstone', 3), ('smooth_sandstone', 2)],
                     floor=[('smooth_sandstone', 4), ('orange_terracotta', 1)], ceiling=[('cut_sandstone', 1)],
                     pillar='chiseled_sandstone', trim='orange_terracotta', light='lantern', glow='glowstone',
                     decor=['skeleton_skull', 'decorated_pot', 'cobweb', 'sand'], stairs='sandstone_stairs',
                     shelf='bookshelf'),
        flavour=['gold_ingot', 'gold_nugget', 'sand']),
    'overgrown_warrens': dict(
        name='Verdant Warrens', tier=2,
        guardian=('minecraft:spider', 'Broodmother', 80, 6, 7, '', ''),
        mobs=['minecraft:spider', 'minecraft:cave_spider', 'minecraft:zombie'],
        biomes=(['#minecraft:is_jungle', 'minecraft:swamp', 'minecraft:mangrove_swamp', 'minecraft:lush_caves'], ['swamp']),
        depth=-14,
        palette=dict(wall=[('mossy_cobblestone', 4), ('mud_bricks', 3), ('moss_block', 2)],
                     floor=[('moss_block', 3), ('mud_bricks', 2), ('rooted_dirt', 1)], ceiling=[('mud_bricks', 1)],
                     pillar='jungle_log', trim='packed_mud', light='lantern', glow='ochre_froglight',
                     decor=['moss_carpet', 'azalea', 'cobweb', 'flowering_azalea'], stairs='mud_brick_stairs',
                     shelf='bookshelf'),
        flavour=['string', 'spider_eye', 'slime_ball']),
    'frost_vaults': dict(
        name='Rimefrost Vaults', tier=3,
        guardian=('minecraft:stray', 'Frost Lich', 110, 10, 7, 'minecraft:bow', 'minecraft:diamond_helmet'),
        mobs=['minecraft:stray', 'minecraft:skeleton'],
        biomes=(['minecraft:snowy_plains', 'minecraft:snowy_taiga', 'minecraft:ice_spikes', 'minecraft:grove',
                 'minecraft:snowy_slopes', 'minecraft:frozen_peaks'], ['snowy']),
        depth=-14,
        palette=dict(wall=[('packed_ice', 4), ('stone_bricks', 3), ('snow_block', 2), ('blue_ice', 1)],
                     floor=[('polished_diorite', 3), ('packed_ice', 2)], ceiling=[('packed_ice', 1)],
                     pillar='blue_ice', trim='polished_diorite', light='lantern', glow='sea_lantern',
                     decor=['skeleton_skull', 'snow_block', 'cobweb', 'ice'], stairs='stone_brick_stairs',
                     shelf='bookshelf'),
        flavour=['snowball', 'blue_ice', 'arrow']),
    'deepslate_halls': dict(
        name='Abyssal Halls', tier=4,
        guardian=('minecraft:wither_skeleton', 'Abyssal Knight', 150, 14, 12, 'minecraft:netherite_sword',
                  'minecraft:netherite_helmet'),
        mobs=['minecraft:zombie', 'minecraft:skeleton', 'minecraft:cave_spider'],
        biomes=(['#minecraft:is_overworld'], []),
        depth=('absolute', -28),
        palette=dict(wall=[('deepslate_bricks', 5), ('deepslate_tiles', 3), ('cracked_deepslate_bricks', 2)],
                     floor=[('polished_deepslate', 3), ('deepslate_tiles', 2)], ceiling=[('deepslate_tiles', 1)],
                     pillar='chiseled_deepslate', trim='polished_basalt', light='soul_lantern', glow='shroomlight',
                     decor=['sculk', 'candle', 'cobweb', 'skeleton_skull'], stairs='deepslate_brick_stairs',
                     shelf='bookshelf'),
        flavour=['echo_shard', 'amethyst_shard', 'sculk']),
    'nether_bastille': dict(
        name='Infernal Bastille', tier=4, dimension='nether',
        guardian=('minecraft:piglin_brute', 'Brute Overseer', 150, 14, 12, 'minecraft:golden_axe', 'minecraft:netherite_helmet'),
        mobs=['minecraft:blaze', 'minecraft:wither_skeleton', 'minecraft:magma_cube'],
        biomes=(['#minecraft:is_nether'], []),
        depth=('absolute', 40),
        palette=dict(wall=[('nether_bricks', 5), ('red_nether_bricks', 3), ('cracked_nether_bricks', 2), ('blackstone', 1)],
                     floor=[('polished_blackstone_bricks', 4), ('magma_block', 1)], ceiling=[('nether_bricks', 1)],
                     pillar='chiseled_polished_blackstone', trim='polished_blackstone', light='lantern', glow='shroomlight',
                     decor=['wither_skeleton_skull', 'nether_wart_block', 'gold_block', 'soul_sand'],
                     stairs='nether_brick_stairs', shelf='bookshelf'),
        flavour=['blaze_rod', 'gold_ingot', 'magma_cream', 'quartz']),
}

HALLS = [('corridor', 6), ('corner', 2), ('tee', 2), ('cross', 1), ('stairs', 2), ('spawner_a', 2), ('spawner_b', 1),
         ('storeroom', 2), ('library', 1), ('pillar_hall', 1), ('shrine', 1)]
ENDS = [('dead_end', 3), ('alcove', 1)]


class Piece:
    """A template under construction: blocks by position, a palette of block states, block entity data, entities."""

    def __init__(self, theme, sx, sy, sz, seed):
        self.t, self.p = theme, theme['palette']
        self.size = (sx, sy, sz)
        self.blocks = {}
        self.entities = []
        self.rng = random.Random(seed)

    def set(self, x, y, z, name, props=None, nbt=None):
        if 0 <= x < self.size[0] and 0 <= y < self.size[1] and 0 <= z < self.size[2]:
            self.blocks[(x, y, z)] = (name if ':' in name else 'minecraft:' + name, tuple(sorted((props or {}).items())), nbt)

    def fill(self, x1, y1, z1, x2, y2, z2, name, props=None):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    self.set(x, y, z, name, props)

    def pick(self, kind):
        entries = self.p[kind]
        return self.rng.choices([e[0] for e in entries], [e[1] for e in entries])[0]

    def shell(self, x1, y1, z1, x2, y2, z2):
        """A hollow box: floor, ceiling and walls from the palette, air inside."""
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if y == y1:
                        self.set(x, y, z, self.pick('floor'))
                    elif y == y2:
                        self.set(x, y, z, self.pick('ceiling'))
                    elif x in (x1, x2) or z in (z1, z2):
                        self.set(x, y, z, self.pick('wall'))
                    else:
                        self.set(x, y, z, 'air')

    def door(self, side, pool, y=1, name=f'{NS}:door', target=f'{NS}:door', at=None):
        """A 3x3 doorway in the middle of a side (or centred on `at` along it), with a jigsaw in its bottom middle
        facing out of the piece."""
        sx, _, sz = self.size
        cx, cz = (at, at) if at is not None else (sx // 2, sz // 2)
        cells = {'north': [(cx + d, 0) for d in (-1, 0, 1)], 'south': [(cx + d, sz - 1) for d in (-1, 0, 1)],
                 'west': [(0, cz + d) for d in (-1, 0, 1)], 'east': [(sx - 1, cz + d) for d in (-1, 0, 1)]}[side]
        for x, z in cells:
            for dy in range(3):
                self.set(x, y + dy, z, 'air')
        jx, jz = cells[1]
        self.set(jx, y, jz, 'jigsaw', {'orientation': f'{side}_up'}, {
            'id': 'minecraft:jigsaw', 'name': name, 'target': target, 'pool': pool,
            'joint': 'rollable', 'final_state': 'minecraft:air'})

    def light(self, x, y, z):
        """A light block set into the ceiling."""
        self.set(x, y, z, self.p['glow'])

    def lantern(self, x, y, z):
        self.set(x, y, z, self.p['light'], {'hanging': 'false', 'waterlogged': 'false'})

    def decor(self, x, y, z):
        d = self.rng.choice(self.p['decor'])
        if d == 'candle':
            self.set(x, y, z, 'candle', {'candles': str(self.rng.randint(1, 4)), 'lit': 'true', 'waterlogged': 'false'})
        elif d.endswith('skull'):
            self.set(x, y, z, d, {'rotation': str(self.rng.randint(0, 15))})
        elif d == 'decorated_pot':
            self.set(x, y, z, d, {'facing': 'north', 'waterlogged': 'false'})
        else:
            self.set(x, y, z, d)

    def chest(self, x, y, z, table, facing='north'):
        self.set(x, y, z, 'chest', {'facing': facing, 'type': 'single', 'waterlogged': 'false'},
                 {'id': 'minecraft:chest', 'LootTable': f'{NS}:chests/{table}'})

    def spawner(self, x, y, z, mob):
        entity = {'entity': {'id': mob}}
        self.set(x, y, z, 'spawner', None, {
            'id': 'minecraft:mob_spawner', 'SpawnData': entity, 'SpawnPotentials': [{'weight': 1, 'data': entity}],
            'Delay': ('short', 20), 'MinSpawnDelay': ('short', 200), 'MaxSpawnDelay': ('short', 700),
            'SpawnCount': ('short', 3), 'MaxNearbyEntities': ('short', 6), 'RequiredPlayerRange': ('short', 16),
            'SpawnRange': ('short', 4)})

    def guardian(self, x, y, z, theme_id):
        entity, name, health, armor, attack, mainhand, helmet = self.t['guardian']
        tag = f'{NS}.guardian'
        nbt = {
            'id': entity, 'CustomName': '{"text":"%s"}' % name, 'CustomNameVisible': ('byte', 1),
            'PersistenceRequired': ('byte', 1), 'Health': ('float', float(health)),
            'Attributes': [{'Name': 'minecraft:generic.max_health', 'Base': ('double', float(health))},
                           {'Name': 'minecraft:generic.armor', 'Base': ('double', float(armor))},
                           {'Name': 'minecraft:generic.attack_damage', 'Base': ('double', float(attack))},
                           {'Name': 'minecraft:generic.knockback_resistance', 'Base': ('double', 0.5)}],
            'HandItems': [{'id': mainhand, 'Count': ('byte', 1)} if mainhand else {}, {}],
            'HandDropChances': [('float', 2.0 if mainhand else 0.0), ('float', 0.0)],
            'ArmorItems': [{}, {}, {}, {'id': helmet, 'Count': ('byte', 1)} if helmet else {}],
            'ArmorDropChances': [('float', 0.0)] * 4,
            'Tags': [tag, f'{tag}.{theme_id}'],
        }
        if entity == 'minecraft:piglin_brute':
            nbt['IsImmuneToZombification'] = ('byte', 1)
        self.entities.append(((x + 0.5, float(y), z + 0.5), (x, y, z), nbt))


# Pieces ---------------------------------------------------------------------------------------------------------------

def halls(tid):
    return f'{NS}:labyrinth/{tid}/halls'


def corridor(t, tid, seed, length=9, far_pool=None):
    p = Piece(t, 5, 6, length, seed)
    p.shell(0, 0, 0, 4, 5, length - 1)
    for z in (0, length - 1):
        p.fill(1, 1, z, 3, 4, z, 'air')
    p.door('north', halls(tid))
    p.door('south', far_pool or halls(tid))
    p.light(2, 5, length // 2)
    if p.rng.random() < 0.6:
        p.decor(p.rng.choice((1, 3)), 1, p.rng.randint(2, length - 3))
    return p


def junction(t, tid, seed, sides):
    p = Piece(t, 5, 6, 5, seed)
    p.shell(0, 0, 0, 4, 5, 4)
    for side in sides:
        p.door(side, halls(tid))
    p.light(2, 5, 2)
    return p


def stairs(t, tid, seed):
    """Nine long, going down four blocks: in at the top (north), out at the bottom (south)."""
    p = Piece(t, 5, 10, 9, seed)
    p.shell(0, 0, 0, 4, 9, 8)
    for z in range(9):
        floor = max(0, min(4, 6 - z))
        p.fill(1, 1, z, 3, floor, z, p.pick('floor'))
        if 1 <= z <= 5 and floor > 0:
            p.fill(1, floor, z, 3, floor, z, p.p['stairs'], {'facing': 'north', 'half': 'bottom', 'shape': 'straight', 'waterlogged': 'false'})
    p.door('north', halls(tid), y=5)
    p.door('south', halls(tid), y=1)
    p.light(2, 9, 4)
    return p


def room(t, tid, seed, kind):
    size = 13 if kind == 'pillar_hall' else 11
    p = Piece(t, size, 7, size, seed)
    p.shell(0, 0, 0, size - 1, 6, size - 1)
    for side in ('north', 'south', 'east', 'west'):
        p.door(side, halls(tid))
    c, m = size // 2, size - 2
    for x, z in ((1, 1), (1, m), (m, 1), (m, m)):
        p.fill(x, 1, z, x, 5, z, p.p['pillar'])
    p.light(c, 6, c)
    mobs = t['mobs']
    if kind in ('spawner_a', 'spawner_b'):
        mob = mobs[0] if kind == 'spawner_a' else mobs[1 % len(mobs)]
        p.fill(c - 1, 1, c - 1, c + 1, 1, c + 1, p.p['trim'])
        p.spawner(c, 2, c, mob)
        for x, z in ((2, 2), (m - 1, m - 1)):
            p.decor(x, 1, z)
    elif kind == 'storeroom':
        p.chest(2, 1, 2, tid, 'south')
        p.chest(m - 1, 1, m - 1, tid, 'north')
        for x, z in ((m - 1, 2), (2, m - 1), (3, 2), (m - 2, m - 1)):
            p.set(x, 1, z, 'barrel', {'facing': 'up', 'open': 'false'})
        p.lantern(c, 1, c)
    elif kind == 'library':
        for z in range(2, m):
            if abs(z - c) > 1:
                p.fill(1, 1, z, 1, 4, z, p.p['shelf'])
                p.fill(m, 1, z, m, 4, z, p.p['shelf'])
        p.set(c, 1, c, 'lectern', {'facing': 'south', 'has_book': 'false', 'powered': 'false'})
        p.chest(c, 1, 2, tid, 'south')
        p.lantern(2, 1, 2)
    elif kind == 'pillar_hall':
        for x, z in ((4, 4), (4, m - 3), (m - 3, 4), (m - 3, m - 3)):
            p.fill(x, 1, z, x, 5, z, p.p['pillar'])
        p.spawner(c, 1, c, mobs[-1])
        p.chest(c, 1, 2, tid, 'south')
        p.decor(2, 1, m - 1)
    elif kind == 'shrine':
        p.fill(c - 1, 1, c - 1, c + 1, 1, c + 1, p.p['trim'])
        p.set(c, 2, c, p.p['pillar'])
        p.chest(c, 1, c + 2, tid, 'south')
        for x, z in ((c - 2, c - 2), (c + 2, c - 2)):
            p.lantern(x, 1, z)
        p.decor(c, 3, c)
    return p


def end(t, tid, seed, alcove):
    p = Piece(t, 5, 6, 3 if not alcove else 5, seed)
    sz = p.size[2]
    p.shell(0, 0, 0, 4, 5, sz - 1)
    p.door('north', halls(tid))
    p.fill(1, 1, sz - 1, 3, 4, sz - 1, p.pick('wall'))
    if alcove:
        p.chest(2, 1, sz - 2, tid, 'north')
    else:
        p.decor(2, 1, 1)
    return p


def vault(t, tid, seed):
    """An antechamber and the vault chamber behind it. It is the start piece's only neighbour, so it is always placed;
    the maze grows from the antechamber's side doors."""
    a = 9  # antechamber depth
    p = Piece(t, 15, 9, a + 15, seed)
    p.shell(0, 0, 0, 14, 6, a - 1)
    p.door('north', halls(tid))
    p.door('west', halls(tid), at=a // 2)
    p.door('east', halls(tid), at=a // 2)
    for x in (3, 11):
        p.fill(x, 1, 2, x, 5, 2, p.p['pillar'])
        p.fill(x, 1, a - 3, x, 5, a - 3, p.p['pillar'])
    p.light(7, 6, a // 2)
    p.decor(1, 1, 1)
    p.decor(13, 1, 1)
    # The chamber, through a doorway in the antechamber's back wall.
    o = a - 1
    p.shell(0, 0, o, 14, 8, o + 15)
    p.fill(6, 1, o, 8, 3, o, 'air')
    for x, z in ((3, 4), (11, 4), (3, 11), (11, 11)):
        p.fill(x, 1, o + z, x, 7, o + z, p.p['pillar'])
    p.fill(5, 1, o + 11, 9, 1, o + 14, p.p['trim'])
    p.chest(6, 2, o + 13, f'{tid}_vault', 'north')
    p.chest(8, 2, o + 13, f'{tid}_vault', 'north')
    p.spawner(1, 1, o + 14, t['mobs'][0])
    p.spawner(13, 1, o + 14, t['mobs'][-1])
    for x, z in ((7, 4), (3, 8), (11, 8)):
        p.light(x, 8, o + z)
    p.lantern(5, 2, o + 11)
    p.lantern(9, 2, o + 11)
    for x, z in ((1, 2), (13, 2), (2, 7), (12, 7)):
        p.decor(x, 1, o + z)
    p.guardian(7, 1, o + 9, tid)
    return p


def entrance(t, tid, seed):
    """A 7x7 shaft from the surface (ground level at y = 14) down to a landing, ladder on the north, closed by a hatch."""
    p = Piece(t, 7, 19, 7, seed)
    p.shell(0, 0, 0, 6, 6, 6)
    for y in range(6, 17):
        for x in range(7):
            for z in range(7):
                p.set(x, y, z, p.pick('wall') if x in (0, 6) or z in (0, 6) else 'air')
    p.door('east', f'{NS}:labyrinth/{tid}/vault')
    for y in range(1, 16):
        p.set(3, y, 1, 'ladder', {'facing': 'south', 'waterlogged': 'false'})
    # A closed hatch over the shaft keeps rain and rivers out; open it to climb down.
    for x in range(1, 6):
        for z in range(1, 6):
            p.set(x, 16, z, 'spruce_trapdoor', {'facing': 'north', 'half': 'top', 'open': 'false', 'powered': 'false',
                                                'waterlogged': 'false'})
    # Corner posts with lanterns mark the shaft on the surface.
    for x, z in ((0, 0), (6, 0), (0, 6), (6, 6)):
        p.set(x, 17, z, p.p['pillar'])
        p.lantern(x, 18, z)
    p.lantern(5, 1, 5)
    return p


def hub(t, tid, seed):
    p = Piece(t, 9, 7, 9, seed)
    p.shell(0, 0, 0, 8, 6, 8)
    p.door('east', f'{NS}:labyrinth/{tid}/vault')
    for x, z in ((1, 1), (1, 7), (7, 1), (7, 7)):
        p.fill(x, 1, z, x, 5, z, p.p['pillar'])
    p.light(4, 6, 4)
    p.lantern(4, 1, 4)
    return p


def pieces(tid, t):
    seed = sum(map(ord, tid))
    out = {
        'corridor': corridor(t, tid, seed + 1),
        'corner': junction(t, tid, seed + 2, ('north', 'east')),
        'tee': junction(t, tid, seed + 3, ('north', 'east', 'west')),
        'cross': junction(t, tid, seed + 4, ('north', 'east', 'west', 'south')),
        'stairs': stairs(t, tid, seed + 5),
        'dead_end': end(t, tid, seed + 6, False),
        'alcove': end(t, tid, seed + 7, True),
        'vault': vault(t, tid, seed + 8),
    }
    for i, kind in enumerate(('spawner_a', 'spawner_b', 'storeroom', 'library', 'pillar_hall', 'shrine')):
        out[kind] = room(t, tid, seed + 10 + i, kind)
    out['start'] = hub(t, tid, seed + 20) if isinstance(t['depth'], tuple) else entrance(t, tid, seed + 20)
    return out


# NBT ------------------------------------------------------------------------------------------------------------------

def to_nbt(value):
    from nbtlib import Byte, Compound, Double, Float, Int, List, Short, String
    if isinstance(value, tuple) and len(value) == 2 and isinstance(value[0], str):
        kind, v = value
        return {'byte': Byte, 'short': Short, 'float': Float, 'double': Double, 'int': Int}[kind](v)
    if isinstance(value, dict):
        return Compound({k: to_nbt(v) for k, v in value.items()})
    if isinstance(value, list):
        items = [to_nbt(v) for v in value]
        return List[type(items[0])](items) if items else List[Compound]([])
    if isinstance(value, bool):
        return Byte(int(value))
    if isinstance(value, int):
        return Int(value)
    if isinstance(value, float):
        return Double(value)
    return String(value)


def save(piece: Piece, path: Path):
    from nbtlib import Compound, Double, File, Int, List, String
    palette, index, blocks = [], {}, []
    for pos, (name, props, nbt) in sorted(piece.blocks.items()):
        key = (name, props)
        if key not in index:
            index[key] = len(palette)
            entry = Compound({'Name': String(name)})
            if props:
                entry['Properties'] = Compound({k: String(v) for k, v in props})
            palette.append(entry)
        block = Compound({'pos': List[Int]([Int(v) for v in pos]), 'state': Int(index[key])})
        if nbt:
            block['nbt'] = to_nbt(nbt)
        blocks.append(block)
    entities = [Compound({'pos': List[Double]([Double(v) for v in p]), 'blockPos': List[Int]([Int(v) for v in b]),
                          'nbt': to_nbt(n)}) for p, b, n in piece.entities]
    root = Compound({'size': List[Int]([Int(v) for v in piece.size]), 'palette': List[Compound](palette),
                     'blocks': List[Compound](blocks), 'entities': List[Compound](entities),
                     'DataVersion': Int(DATA_VERSION)})
    path.parent.mkdir(parents=True, exist_ok=True)
    File(root).save(path, gzipped=True)


def main():
    count = 0
    for tid, t in THEMES.items():
        for name, piece in pieces(tid, t).items():
            for ws, folder in WORKSPACES.items():
                save(piece, REPO / ws / 'common/src/main/resources/data' / NS / folder / 'labyrinth' / tid / f'{name}.nbt')
            count += 1
    print(f'wrote {count} templates for {len(THEMES)} labyrinths into {len(WORKSPACES)} workspaces')
    return 0


if __name__ == '__main__':
    sys.exit(main())
