#!/usr/bin/env python3
"""Applies the 2.0 data fixes to the hand-built templates and copies them to every workspace.

The fixes are idempotent, so running this again is harmless:
  * every chest draws from the dungeon's own loot table (the old fixed contents and vanilla tables are dropped);
    the highest chest is the vault and draws from the vault table;
  * empty spawners get a mob;
  * a `guardian` data marker is placed next to the vault, where the mod spawns the dungeon's guardian;
  * the Smuggler's Villa's walls of empty chests become barrels, apart from its loot chests.

  python3 tools/templates.py            (needs nbtlib; the Soulfire Crypt comes from generate_soulfire_crypt.py)
"""
from __future__ import annotations

import math
import shutil
from pathlib import Path

from nbtlib import Byte, Compound, Float, Int, List, Long, Short, String, load

REPO = Path(__file__).resolve().parents[1]
SOURCE = REPO / '1.21.1/common/src/main/resources/data/muchmoredungeons/structure'
WORKSPACES = {'1.20.1': 'structures', '1.21.1': 'structure', '26.1.2': 'structure', '26.2': 'structure', '26.3': 'structure'}
NS = 'muchmoredungeons'

# Mobs for the template's empty spawners, from the lowest spawner up.
SPAWNERS = {
    'outdoor_villa': ['minecraft:pillager'],
    'tower_dungeon': ['minecraft:zombie', 'minecraft:skeleton', 'minecraft:spider', 'minecraft:witch'],
    'dungeon_t2': ['minecraft:skeleton'],
}
# Villa: the chests that keep their chest (and get loot); the rest of the chest walls become barrels.
VILLA_CHESTS = {(5, 1, 4), (8, 1, 4), (11, 1, 4), (5, 1, 8), (8, 1, 8), (11, 1, 8)}
VILLA_GUARDIAN = (5, 1, 6)
SOLID_SKIP = ('air', 'cave_air', 'void_air', 'water', 'lava', 'fire', 'torch', 'carpet', 'snow', 'grass', 'fern', 'flower')


def name(palette, block):
    return str(palette[int(block['state'])]['Name'])


def state_index(palette, block_name, **props):
    for i, entry in enumerate(palette):
        if str(entry['Name']) != block_name:
            continue
        have = {k: str(v) for k, v in entry.get('Properties', {}).items()}
        if have == props:
            return i
    entry = Compound({'Name': String(block_name)})
    if props:
        entry['Properties'] = Compound({k: String(v) for k, v in props.items()})
    palette.append(entry)
    return len(palette) - 1


def marker(kind):
    return Compound({
        'id': String('minecraft:structure_block'), 'mode': String('DATA'), 'name': String(kind), 'metadata': String(kind),
        'posX': Int(0), 'posY': Int(0), 'posZ': Int(0), 'sizeX': Int(0), 'sizeY': Int(0), 'sizeZ': Int(0),
        'rotation': String('NONE'), 'mirror': String('NONE'), 'ignoreEntities': Byte(1), 'powered': Byte(0),
        'showair': Byte(0), 'showboundingbox': Byte(0), 'integrity': Float(1.0), 'seed': Long(0), 'author': String(NS),
    })


def fix(dungeon: str):
    path = SOURCE / f'{dungeon}.nbt'
    nbt = load(path)
    palette = nbt['palette']
    blocks = nbt['blocks']
    at = {tuple(int(v) for v in b['pos']): b for b in blocks}

    if dungeon == 'outdoor_villa':
        for pos, b in at.items():
            if name(palette, b) in ('minecraft:chest', 'minecraft:barrel') and pos[1] <= 4 and pos not in VILLA_CHESTS:
                facing = 'south' if pos[2] <= 4 else 'north'
                b['state'] = Int(state_index(palette, 'minecraft:barrel', facing=facing, open='false'))
                b.pop('nbt', None)
        for pos in VILLA_CHESTS:
            facing = 'south' if pos[2] <= 4 else 'north'
            at[pos]['state'] = Int(state_index(palette, 'minecraft:chest', facing=facing, type='single', waterlogged='false'))

    chests = sorted((pos for pos, b in at.items() if name(palette, b) == 'minecraft:chest'), key=lambda p: (p[1], p))
    vault = chests[-1]
    for pos in chests:
        table = f'{NS}:chests/{dungeon}' + ('_vault' if pos == vault else '')
        at[pos]['nbt'] = Compound({'id': String('minecraft:chest'), 'LootTable': String(table)})

    mobs = SPAWNERS.get(dungeon, [])
    empty = sorted((pos for pos, b in at.items() if name(palette, b) == 'minecraft:spawner'
                    and not str(b.get('nbt', {}).get('SpawnData', {}).get('entity', {}).get('id', ''))), key=lambda p: (p[1], p))
    for i, pos in enumerate(empty):
        entity = Compound({'entity': Compound({'id': String(mobs[min(i, len(mobs) - 1)])})})
        spawner = at[pos].setdefault('nbt', Compound({'id': String('minecraft:mob_spawner'), 'Delay': Short(20),
                                                     'MinSpawnDelay': Short(200), 'MaxSpawnDelay': Short(800),
                                                     'SpawnCount': Short(3), 'MaxNearbyEntities': Short(6),
                                                     'RequiredPlayerRange': Short(16), 'SpawnRange': Short(4)}))
        spawner['SpawnData'] = entity
        spawner['SpawnPotentials'] = List[Compound]([Compound({'weight': Int(1), 'data': entity})])

    if not any(name(palette, b) == 'minecraft:structure_block' for b in at.values()):
        spot = VILLA_GUARDIAN if dungeon == 'outdoor_villa' else standable_near(at, palette, vault, nbt)
        entry = at.get(spot)
        if entry is None:
            entry = Compound({'pos': List[Int]([Int(v) for v in spot]), 'state': Int(0)})
            blocks.append(entry)
            at[spot] = entry
        entry['state'] = Int(state_index(palette, 'minecraft:structure_block', mode='data'))
        entry['nbt'] = marker('guardian')
        print(f'  {dungeon}: guardian marker at {spot}')
    print(f'  {dungeon}: {len(chests)} chests (vault at {vault}), {len(empty)} empty spawners filled')
    nbt.save(path, gzipped=True)
    return path


def standable_near(at, palette, target, nbt):
    """The nearest air block, on the vault's floor or the one above it, with a solid block under it and air above."""
    size = [int(v) for v in nbt['size']]

    def kind(pos):
        b = at.get(pos)
        return name(palette, b).split(':')[1] if b is not None else 'void'

    best = None
    tx, ty, tz = target
    for y in (ty, ty + 1):
        for x in range(max(0, tx - 6), min(size[0], tx + 7)):
            for z in range(max(0, tz - 6), min(size[2], tz + 7)):
                pos = (x, y, z)
                if pos == target or kind(pos) != 'air' or kind((x, y + 1, z)) != 'air':
                    continue
                below = kind((x, y - 1, z))
                if below in ('void',) or any(s in below for s in SOLID_SKIP) or 'chest' in below:
                    continue
                d = math.dist(pos, target)
                if d >= 2 and (best is None or d < best[0]):
                    best = (d, pos)
    if best is None:
        raise SystemExit(f'no spot for a guardian near {target}')
    return best[1]


def main():
    for dungeon in ('outdoor_villa', 'tower_dungeon', 'dungeon_t2'):
        src = fix(dungeon)
        for ws, folder in WORKSPACES.items():
            dst = REPO / ws / 'common/src/main/resources/data' / NS / folder / src.name
            if dst != src:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)


if __name__ == '__main__':
    main()
