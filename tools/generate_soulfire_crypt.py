#!/usr/bin/env python3
"""Generate soulfire_crypt.nbt structure template for Much More Dungeons."""

from pathlib import Path

from nbtlib import Byte, Compound, Double, File, Float, Int, List, Long, Short, String

W, H, D = 21, 10, 25  # x, y, z


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
]

AIR, BRICK, CRACK, BLACK, PBLACK, SSAND, SSOIL, COBS, SFIRE, SLAN, CHAIN = range(11)
STAIR_E, STAIR_W, STAIR_S, STAIR_N, BARS, SPAWNER, CHEST_S, CHEST_N, SBLOCK, WALL, SLAB = range(11, 22)

grid = [[[AIR for _ in range(D)] for _ in range(H)] for _ in range(W)]
block_nbt = {}  # (x,y,z) -> Compound
entities = []


def fill(x0, y0, z0, x1, y1, z1, state):
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                if 0 <= x < W and 0 <= y < H and 0 <= z < D:
                    grid[x][y][z] = state


def setb(x, y, z, state):
    if 0 <= x < W and 0 <= y < H and 0 <= z < D:
        grid[x][y][z] = state


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


def chest_nbt() -> Compound:
    return Compound({
        "LootTable": String("muchmoredungeons:chests/soulfire_crypt"),
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
setb(16, 1, 5, SBLOCK)
block_nbt[(16, 1, 5)] = structure_marker("chest")
setb(15, 2, 3, COBS)
setb(17, 2, 3, COBS)

# Second loot chest in west loot nook
fill(2, 1, 3, 6, 4, 6, AIR)
fill(2, 1, 3, 6, 1, 6, CRACK)
setb(4, 1, 4, CHEST_S)
block_nbt[(4, 1, 4)] = chest_nbt()
setb(4, 1, 5, SBLOCK)
block_nbt[(4, 1, 5)] = structure_marker("chest")

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
block_nbt[(10, 1, 22)] = chest_nbt()
setb(10, 2, 22, SBLOCK)
block_nbt[(10, 2, 22)] = structure_marker("chest")

# Guardian marker (structure block) + embedded entity for 1.20.1 jigsaw
setb(10, 1, 19, SBLOCK)
block_nbt[(10, 1, 19)] = structure_marker("guardian")

# Named Cinder Warden entity (works for jigsaw + template placement)
entities.append(Compound({
    "pos": List[Double]([Double(10.5), Double(2.0), Double(19.5)]),
    "blockPos": List[Int]([Int(10), Int(2), Int(19)]),
    "nbt": Compound({
        "id": String("minecraft:wither_skeleton"),
        "CustomName": String('{"text":"Cinder Warden","color":"dark_red","bold":true}'),
        "CustomNameVisible": Byte(1),
        "PersistenceRequired": Byte(1),
        "Health": Float(40.0),
        "HandItems": List[Compound]([
            Compound({"id": String("minecraft:stone_sword"), "Count": Byte(1)}),
            Compound({}),
        ]),
        "ArmorItems": List[Compound]([
            Compound({}),
            Compound({}),
            Compound({"id": String("minecraft:chainmail_chestplate"), "Count": Byte(1)}),
            Compound({}),
        ]),
    }),
}))

# Corner cracked accents
for x, z in ((1, 1), (W - 2, 1), (1, D - 2), (W - 2, D - 2)):
    setb(x, 0, z, CRACK)
    setb(x, H - 1, z, COBS)

# Ceiling chains + hanging lanterns in nave
PALETTE.append(block("minecraft:soul_lantern", hanging="true"))  # 22
HANG = 22
for x, z in ((10, 9), (10, 11), (10, 13)):
    setb(x, H - 2, z, CHAIN)
    setb(x, H - 3, z, HANG)

blocks = []
for x in range(W):
    for y in range(H):
        for z in range(D):
            state = grid[x][y][z]
            if state == AIR:
                continue
            entry = Compound({
                # Must be List[Int], not IntArray — otherwise Minecraft loads an empty template
                "pos": List[Int]([Int(x), Int(y), Int(z)]),
                "state": Int(state),
            })
            if (x, y, z) in block_nbt:
                entry["nbt"] = block_nbt[(x, y, z)]
            blocks.append(entry)

repo = Path(__file__).resolve().parents[1]
targets = [
    (repo / "1.20.1/common/src/main/resources/data/muchmoredungeons/structures/soulfire_crypt.nbt", 3465),
    (repo / "1.21.1/common/src/main/resources/data/muchmoredungeons/structure/soulfire_crypt.nbt", 3955),
    (repo / "26.1.2/common/src/main/resources/data/muchmoredungeons/structure/soulfire_crypt.nbt", 3955),
    (repo / "26.2/common/src/main/resources/data/muchmoredungeons/structure/soulfire_crypt.nbt", 3955),
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
