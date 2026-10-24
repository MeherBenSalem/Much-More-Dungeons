#!/usr/bin/env python3
"""Generate the soulfire_crypt.nbt structure template for every workspace.

Run from anywhere: python3 tools/generate_soulfire_crypt.py (needs nbtlib)."""

from pathlib import Path

from nbtlib import Byte, Compound, Double, File, Float, Int, List, Long, Short, String

W0, H0, D0 = 21, 10, 25  # the crypt itself (x, y, z)
OX, OZ = 2, 4  # margin for the buttresses and the entrance portico (the portico is on the z = 0 side)
W, H, D = W0 + 2 * OX, H0 + 3, D0 + OZ + 2
VOID = -1  # no block in the template: the ground is left as it is


def block(name, **props):
    c = Compound({"Name": String(name)})
    if props:
        c["Properties"] = Compound({k: String(v) for k, v in props.items()})
    return c


PALETTE = [
    block("minecraft:air"),  # 0
    block("minecraft:deepslate_bricks"),  # 1
    block("minecraft:cracked_deepslate_bricks"),  # 2
    block("minecraft:blackstone"),  # 3
    block("minecraft:polished_blackstone_bricks"),  # 4
    block("minecraft:soul_sand"),  # 5
    block("minecraft:soul_soil"),  # 6
    block("minecraft:crying_obsidian"),  # 7
    block("minecraft:soul_fire"),  # 8
    block("minecraft:soul_lantern", hanging="false"),  # 9
    block("minecraft:chain"),  # 10
    block("minecraft:deepslate_brick_stairs", facing="east", half="bottom", shape="straight", waterlogged="false"),  # 11
    block("minecraft:deepslate_brick_stairs", facing="west", half="bottom", shape="straight", waterlogged="false"),  # 12
    block("minecraft:deepslate_brick_stairs", facing="south", half="bottom", shape="straight", waterlogged="false"),  # 13
    block("minecraft:deepslate_brick_stairs", facing="north", half="bottom", shape="straight", waterlogged="false"),  # 14
    block("minecraft:iron_bars"),  # 15
    block("minecraft:spawner"),  # 16
    block("minecraft:chest", facing="south", type="single", waterlogged="false"),  # 17
    block("minecraft:chest", facing="north", type="single", waterlogged="false"),  # 18
    block("minecraft:structure_block", mode="data"),  # 19 — data markers
    block("minecraft:polished_blackstone_brick_wall", east="none", north="none", south="none", up="true", west="none", waterlogged="false"),  # 20
    block("minecraft:deepslate_tile_slab", type="bottom", waterlogged="false"),  # 21
    block("minecraft:soul_lantern", hanging="true"),  # 22
    block("minecraft:deepslate_tiles"),  # 23
    block("minecraft:cracked_deepslate_tiles"),  # 24
    block("minecraft:polished_blackstone_brick_stairs", facing="south", half="bottom", shape="straight", waterlogged="false"),  # 25
    block("minecraft:polished_blackstone_brick_slab", type="bottom", waterlogged="false"),  # 26
    block("minecraft:chiseled_polished_blackstone"),  # 27
    block("minecraft:soul_campfire", facing="south", lit="true", signal_fire="false", waterlogged="false"),  # 28
    block("minecraft:polished_blackstone_brick_stairs", facing="north", half="top", shape="straight", waterlogged="false"),  # 29
    block("minecraft:deepslate_brick_stairs", facing="west", half="top", shape="straight", waterlogged="false"),  # 30
    block("minecraft:deepslate_brick_stairs", facing="east", half="top", shape="straight", waterlogged="false"),  # 31
    block("minecraft:cobbled_deepslate"),  # 32
]

AIR, BRICK, CRACK, BLACK, PBLACK, SSAND, SSOIL, COBS, SFIRE, SLAN, CHAIN = range(11)
STAIR_E, STAIR_W, STAIR_S, STAIR_N, BARS, SPAWNER, CHEST_S, CHEST_N, SBLOCK, WALL, SLAB = range(11, 22)
HANG, TILES, CTILES, PSTAIR_S, PSLAB, CHISEL, CAMPFIRE, PSTAIR_N_TOP, STAIR_W_TOP, STAIR_E_TOP, COBBLED = range(22, 33)

grid = [[[VOID for _ in range(D)] for _ in range(H)] for _ in range(W)]
block_nbt = {}  # (x,y,z) -> Compound
entities = []


def fill_abs(x0, y0, z0, x1, y1, z1, state):
    for x in range(min(x0, x1), max(x0, x1) + 1):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            for z in range(min(z0, z1), max(z0, z1) + 1):
                if 0 <= x < W and 0 <= y < H and 0 <= z < D:
                    grid[x][y][z] = state


def set_abs(x, y, z, state):
    fill_abs(x, y, z, x, y, z, state)


# The crypt's own coordinates (0..20, 0..9, 0..24), shifted into the margin.
def fill(x0, y0, z0, x1, y1, z1, state):
    fill_abs(x0 + OX, y0, z0 + OZ, x1 + OX, y1, z1 + OZ, state)


def setb(x, y, z, state):
    set_abs(x + OX, y, z + OZ, state)


def spawner_nbt(entity_id: str) -> Compound:
    spawn = Compound({
        "entity": Compound({"id": String(entity_id)}),
    })
    # 1.20.1 uses SpawnData; keep both-compatible fields used by modern spawners
    return Compound({
        "SpawnData": spawn,
        "spawn_data": spawn,
        "MinSpawnDelay": Short(200),
        "MaxSpawnDelay": Short(600),
        "SpawnCount": Short(2),
        "MaxNearbyEntities": Short(4),
        "RequiredPlayerRange": Short(16),
        "SpawnRange": Short(4),
        "Delay": Short(20),
    })


def chest_nbt(table: str = "soulfire_crypt") -> Compound:
    return Compound({
        "LootTable": String(f"muchmoredungeons:chests/{table}"),
        "id": String("minecraft:chest"),
    })


def structure_marker(name: str) -> Compound:
    return Compound({
        "mode": String("DATA"),
        "name": String(name),
        "metadata": String(name),
        "posX": Int(0),
        "posY": Int(0),
        "posZ": Int(0),
        "sizeX": Int(0),
        "sizeY": Int(0),
        "sizeZ": Int(0),
        "rotation": String("NONE"),
        "mirror": String("NONE"),
        "ignoreEntities": Byte(0),
        "powered": Byte(0),
        "showair": Byte(0),
        "showboundingbox": Byte(0),
        "integrity": nbt_float(1.0),
        "seed": Long(0),
        "author": String("muchmoredungeons"),
    })


def nbt_float(v: float):
    return Float(v)


# --- Build layout ---
# Floor and walls for vestibule (z 0-5), nave (z 5-15), relic chamber (z 15-24)

# Exterior shell
fill(0, 0, 0, W - 1, 0, D - 1, BRICK)  # floor
fill(0, H - 1, 0, W - 1, H - 1, D - 1, PBLACK)  # roof
fill(0, 1, 0, 0, H - 2, D - 1, BRICK)  # west wall
fill(W - 1, 1, 0, W - 1, H - 2, D - 1, BRICK)  # east wall
fill(0, 1, 0, W - 1, H - 2, 0, BRICK)  # south entrance wall
fill(0, 1, D - 1, W - 1, H - 2, D - 1, BRICK)  # north wall

# Hollow interior
fill(1, 1, 1, W - 2, H - 2, D - 2, AIR)

# Entrance doorway
fill(9, 1, 0, 11, 3, 0, AIR)
setb(9, 1, 0, STAIR_S)
setb(11, 1, 0, STAIR_S)

# Vestibule soul accents
for x, z in ((3, 2), (17, 2), (3, 4), (17, 4)):
    setb(x, 1, z, SSAND)
    setb(x, 2, z, SFIRE)
    setb(x, 1, z + 1, COBS)

# Nave columns and soul fire braziers
for x in (4, 16):
    for z in (7, 10, 13):
        fill(x, 1, z, x, 5, z, PBLACK)
        setb(x, 6, z, WALL)
        setb(x, 7, z, SLAN)

for x, z in ((7, 8), (13, 8), (7, 12), (13, 12)):
    setb(x, 1, z, SSOIL)
    setb(x, 2, z, SFIRE)

# Side alcove west — wither skeleton spawner
fill(1, 1, 9, 3, 4, 12, AIR)
fill(1, 1, 9, 3, 1, 12, BLACK)
setb(2, 1, 10, SPAWNER)
block_nbt[(2, 1, 10)] = spawner_nbt("minecraft:wither_skeleton")
setb(2, 2, 11, BARS)
setb(1, 3, 10, SLAN)

# Side alcove east — blaze spawner
fill(17, 1, 9, 19, 4, 12, AIR)
fill(17, 1, 9, 19, 1, 12, BLACK)
setb(18, 1, 10, SPAWNER)
block_nbt[(18, 1, 10)] = spawner_nbt("minecraft:blaze")
setb(18, 2, 11, BARS)
setb(19, 3, 10, SLAN)

# Loot crypt (side chamber south-east of nave)
fill(14, 1, 3, 18, 4, 6, AIR)
fill(14, 1, 3, 18, 1, 6, CRACK)
setb(16, 1, 4, CHEST_S)
block_nbt[(16, 1, 4)] = chest_nbt()
setb(15, 2, 3, COBS)
setb(17, 2, 3, COBS)

# Second loot chest in west loot nook
fill(2, 1, 3, 6, 4, 6, AIR)
fill(2, 1, 3, 6, 1, 6, CRACK)
setb(4, 1, 4, CHEST_S)
block_nbt[(4, 1, 4)] = chest_nbt()

# Relic chamber arch
fill(6, 1, 15, 14, 6, 15, BRICK)
fill(8, 1, 15, 12, 4, 15, AIR)
fill(6, 1, 16, 14, 6, 23, AIR)
fill(6, 1, 16, 14, 1, 23, SSOIL)
for x in range(7, 14):
    for z in range(17, 23):
        if (x + z) % 3 == 0:
            setb(x, 1, z, SSAND)

# Crying obsidian altar
fill(9, 1, 20, 11, 1, 21, COBS)
setb(10, 2, 20, SFIRE)
setb(9, 2, 21, SLAN)
setb(11, 2, 21, SLAN)

# Boss chest behind altar
setb(10, 1, 22, CHEST_N)
block_nbt[(10, 1, 22)] = chest_nbt("soulfire_crypt_vault")

# Guardian marker: the mod spawns the Cinder Warden here when the crypt generates.
setb(10, 1, 19, SBLOCK)
block_nbt[(10, 1, 19)] = structure_marker("guardian")

# Corner cracked accents
for x, z in ((1, 1), (W - 2, 1), (1, D - 2), (W - 2, D - 2)):
    setb(x, 0, z, CRACK)
    setb(x, H - 1, z, COBS)

# Ceiling chains + hanging lanterns in nave
for x, z in ((10, 9), (10, 11), (10, 13)):
    setb(x, H - 2, z, CHAIN)
    setb(x, H - 3, z, HANG)

# --- Exterior ---
# Weathering: a fixed pattern of cracked bricks and tiles in the outer walls.
for x in range(W0):
    for y in range(1, H0 - 1):
        for z in range(D0):
            if (x in (0, W0 - 1) or z in (0, D0 - 1)) and grid[x + OX][y][z + OZ] == BRICK:
                h = (x * 73856093 ^ y * 19349663 ^ z * 83492791) % 11
                if h == 0:
                    setb(x, y, z, CRACK)
                elif h in (1, 2):
                    setb(x, y, z, TILES)
                elif h == 3:
                    setb(x, y, z, CTILES)

# A plinth course around the base and buttresses every four blocks along the long walls.
for x in range(-1, W0 + 1):
    for z in (-1, D0):
        setb(x, 0, z, COBBLED)
for z in range(-1, D0 + 1):
    for x in (-1, W0):
        setb(x, 0, z, COBBLED)
for z in range(2, D0 - 1, 4):
    for x, top in ((-1, STAIR_W), (W0, STAIR_E)):
        fill(x, 0, z, x, 5, z, PBLACK)
        setb(x, 6, z, top)
for x in range(4, W0 - 3, 4):
    if 8 <= x <= 12:
        continue
    setb(x, 0, D0, PBLACK)
    fill(x, 1, D0, x, 5, D0, PBLACK)
    setb(x, 6, D0, STAIR_N)

# Parapet and corner posts with soul lanterns on the roof.
for x in range(W0):
    for z in range(D0):
        if x in (0, W0 - 1) or z in (0, D0 - 1):
            setb(x, H0, z, WALL if (x + z) % 2 == 0 else PSLAB)
for x, z in ((0, 0), (W0 - 1, 0), (0, D0 - 1), (W0 - 1, D0 - 1)):
    fill(x, H0, z, x, H0 + 1, z, PBLACK)
    setb(x, H0 + 2, z, SLAN)
# A raised ridge of tiles over the relic chamber.
fill(7, H0, 16, 13, H0, 23, TILES)
fill(9, H0 + 1, 18, 11, H0 + 1, 21, PSLAB)

# Entrance portico: two pillars, a lintel with hanging lanterns, soul campfires and a path.
for x in (7, 13):
    fill(x, 0, -3, x, 4, -3, PBLACK)
    setb(x, 5, -3, CHISEL)
    setb(x, 0, -1, CAMPFIRE)
fill(7, 5, -2, 13, 5, -1, PBLACK)
fill(8, 5, -3, 12, 5, -3, PSTAIR_N_TOP)
fill(7, 6, -3, 13, 6, -1, PSLAB)
setb(10, 6, -2, CHISEL)
for x in (9, 11):
    setb(x, 4, -2, HANG)
fill(8, 0, -4, 12, 0, -1, SSOIL)
fill(9, 0, -4, 11, 0, -1, CRACK)
fill(8, 1, -3, 12, 4, -1, AIR)
fill(9, 1, 0, 11, 3, 0, AIR)

blocks = []
for x in range(W):
    for y in range(H):
        for z in range(D):
            # Air is stored too, so the crypt clears the ground it is dug into; the margin is left to the terrain.
            state = grid[x][y][z]
            if state == VOID:
                continue
            entry = Compound({
                # Must be List[Int], not IntArray — otherwise Minecraft loads an empty template
                "pos": List[Int]([Int(x), Int(y), Int(z)]),
                "state": Int(state),
            })
            if (x - OX, y, z - OZ) in block_nbt:
                entry["nbt"] = block_nbt[(x - OX, y, z - OZ)]
            blocks.append(entry)

repo = Path(__file__).resolve().parents[1]
targets = [(repo / "1.20.1/common/src/main/resources/data/muchmoredungeons/structures/soulfire_crypt.nbt", 3465)] + [
    (repo / f"{ws}/common/src/main/resources/data/muchmoredungeons/structure/soulfire_crypt.nbt", 3955)
    for ws in ("1.21.1", "26.1.2", "26.2", "26.3")
]

for path, data_version in targets:
    root = Compound({
        "size": List[Int]([Int(W), Int(H), Int(D)]),
        "palette": List[Compound](PALETTE),
        "blocks": List[Compound](blocks),
        "entities": List[Compound](entities),
        "DataVersion": Int(data_version),
    })
    path.parent.mkdir(parents=True, exist_ok=True)
    File(root).save(path, gzipped=True)
    print(f"Wrote {path} ({path.stat().st_size} bytes, DataVersion={data_version})")
