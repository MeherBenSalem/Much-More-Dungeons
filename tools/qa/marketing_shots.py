#!/usr/bin/env python3
"""Captures the listing screenshots from a real dev client (see marketing/README.md).

Run against a 26.3 Fabric dev server whose world is the showcase world (level-name=showcase, level-type
minecraft:normal, level-seed SEED below, broadcast-rcon-to-ops=false, view-distance=12), with the QA client online:

  python3 tools/qa/marketing_shots.py [shot...]

Every dungeon is the naturally generated one /locate finds from spawn. Each shot is one unedited frame; the HUD is
hidden (F1) except where it is part of the picture (the vault, the map, the advancements).
"""
from __future__ import annotations

import argparse
import math
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from client import Session, PLAYER  # noqa: E402

SEED = '7214950366214'
NS = 'muchmoredungeons'
OUT = Path(__file__).resolve().parents[2] / 'marketing' / 'images' / 'screenshots'

# Camera per exterior shot: horizontal angle around the dungeon (degrees, 0 = from the south), distance as a multiple
# of the dungeon's size, height above its floor as a multiple of its height, and where to aim (share of its height).
EXTERIOR = {
    'outdoor_villa': dict(angle=35, dist=1.5, up=0.9, aim=0.3, time=1500),
    'tower_dungeon': dict(angle=210, dist=1.05, up=0.55, aim=0.45, time=1500),
    'dungeon_t2': dict(angle=140, dist=1.3, up=0.45, aim=0.4, time=1500),
    'soulfire_crypt': dict(angle=0, dist=1.6, up=0.9, aim=0.25, time=1500),
}
NAMES = {'outdoor_villa': 'villa', 'tower_dungeon': 'spire', 'dungeon_t2': 'keep', 'soulfire_crypt': 'crypt'}
# Labyrinths: one shot each inside the vault chamber, past the guardian.
LABYRINTHS = {'catacombs': 'catacombs', 'sandstone_tomb': 'tomb', 'overgrown_warrens': 'warrens',
              'frost_vaults': 'frost', 'deepslate_halls': 'abyss', 'nether_bastille': 'bastille'}
DIMENSION = {'nether_bastille': 'minecraft:the_nether'}


class Shots:
    def __init__(self, s: Session):
        self.s = s
        self.found = {}

    def cmd(self, *c):
        return self.s.cmd(*c)

    def save(self, name, wait=1.5):
        time.sleep(wait)
        png = OUT / (name + '.png')
        self.s.shot(png)
        from PIL import Image
        Image.open(png).convert('RGB').save(OUT / (name + '.jpg'), quality=90)
        png.unlink()
        print('captured', name + '.jpg', flush=True)

    def prepare(self):
        self.cmd('gamerule advance_time false', 'gamerule advance_weather false', 'gamerule spawn_mobs false',
                 'weather clear', 'difficulty normal', f'recipe give {PLAYER} *')
        self.cmd(f'effect give {PLAYER} minecraft:night_vision infinite 0 true')
        time.sleep(6)  # let the recipe toasts pass

    def dungeon(self, dungeon):
        """Locates the dungeon, loads it and returns its piece box and vault position."""
        if dungeon in self.found:
            self.cmd(f'forceload add {self.found[dungeon]["x1"]} {self.found[dungeon]["z1"]} '
                     f'{self.found[dungeon]["x2"]} {self.found[dungeon]["z2"]}')
            return self.found[dungeon]
        dim = DIMENSION.get(dungeon, 'minecraft:overworld')
        out = self.cmd(f'execute in {dim} positioned 0 64 0 run locate structure {NS}:{dungeon}')
        m = re.search(r'\[(-?\d+), ~, (-?\d+)\]', out)
        x, z = int(m.group(1)) // 16 * 16 + 8, int(m.group(2)) // 16 * 16 + 8
        r = 40 if dungeon in NAMES else 96
        self.cmd(f'execute in {dim} run forceload add {x - r} {z - r} {x + r} {z + r}')
        info = ''
        for _ in range(40):
            out = self.cmd(f'execute in {dim} run {NS} inspect {x} 64 {z}')
            m = re.search(rf'MMD inspect id={dungeon} .*?(?=MMD inspect|$)', out, re.S)
            info = m.group(0) if m else ''
            if 'box=' in info and 'guardians=1' in info:
                break
            time.sleep(2)
        b = [int(v) for v in re.search(r'box=(\S+)', info).group(1).split(',')]
        v = re.search(r'vault=(-?\d+),(-?\d+),(-?\d+)', info)
        # A handcrafted dungeon's box includes 12 blocks of terrain adaptation on every side.
        pad = 12 if dungeon in NAMES else 0
        d = dict(x1=b[0] + pad, y1=b[1] + pad, z1=b[2] + pad, x2=b[3] - pad, y2=b[4] - pad, z2=b[5] - pad,
                 vault=tuple(int(g) for g in v.groups()) if v else None, dim=dim)
        self.found[dungeon] = d
        return d

    def look(self, eye, target, dim='minecraft:overworld'):
        dx, dy, dz = target[0] - eye[0], target[1] - (eye[1] + 1.62), target[2] - eye[2]
        yaw = math.degrees(math.atan2(-dx, dz))
        pitch = -math.degrees(math.atan2(dy, math.hypot(dx, dz)))
        self.cmd(f'execute in {dim} run tp {PLAYER} {eye[0]:.2f} {eye[1]:.2f} {eye[2]:.2f} {yaw:.2f} {pitch:.2f}')

    # Shots -----------------------------------------------------------------------------------------------------------

    def exterior(self, dungeon):
        d = self.dungeon(dungeon)
        c = EXTERIOR[dungeon]
        cx, cz = (d['x1'] + d['x2']) / 2 + 0.5, (d['z1'] + d['z2']) / 2 + 0.5
        h = d['y2'] - d['y1']
        size = max(d['x2'] - d['x1'], d['z2'] - d['z1'], h)
        a = math.radians(c['angle'])
        dist = size * c['dist']
        eye = (cx - math.sin(a) * dist, d['y1'] + h * c['up'] + 2, cz + math.cos(a) * dist)
        self.cmd(f'time set {c["time"]}', f'gamemode spectator {PLAYER}')
        self.s.hud(False)
        self.look(eye, (cx, d['y1'] + h * c['aim'], cz))
        self.save(NAMES[dungeon], wait=22)

    def interior(self, dungeon, name=None):
        d = self.dungeon(dungeon)
        self.cmd(f'gamemode spectator {PLAYER}', 'time set 6000')
        self.s.hud(False)
        # Stand a few blocks from the guardian and look past it towards the vault.
        self.cmd(f'execute in {d["dim"]} {self.near(d)} as @e[tag={NS}.guardian.{dungeon},limit=1,sort=nearest] '
                 f'run data merge entity @s {{NoAI:1b}}')
        g = self.guardian_pos(dungeon)
        vx, vy, vz = d['vault'] if d['vault'] else g
        ex, ez = g[0] + (g[0] - vx) * 1.2 + 0.5, g[2] + (g[2] - vz) * 1.2 + 0.5
        if abs(ex - g[0]) + abs(ez - g[2]) < 3:
            ex, ez = g[0] + 4, g[2] + 4
        self.look((ex, g[1] + 0.6, ez), (vx + 0.5, vy + 0.5, vz + 0.5), d['dim'])
        self.save(name or NAMES[dungeon] + '_inside', wait=45)

    def cutaway(self, dungeon='sandstone_tomb'):
        """A labyrinth from above with the ground over it removed: the maze as generated."""
        d = self.dungeon(dungeon)
        floor = d['y2'] - 18  # the entrance's landing: its top (the lanterns) is 18 blocks up
        top = floor + 40
        cut = floor + 5  # the ceilings of the corridors at the landing's level
        for x in range(d['x1'], d['x2'] + 1, 16):
            for y in range(cut, top, 8):
                self.cmd(f'fill {x} {y} {d["z1"]} {min(d["x2"], x + 15)} {min(top, y + 7)} {d["z2"]} minecraft:air')
        self.cmd(f'gamemode spectator {PLAYER}', 'time set 6000')
        self.s.hud(False)
        cx, cz = (d['x1'] + d['x2']) / 2, (d['z1'] + d['z2']) / 2
        span = max(d['x2'] - d['x1'], d['z2'] - d['z1'])
        self.s.tp(cx, cut + span * 0.75, cz + span * 0.45, yaw=180, pitch=62)
        self.save('cutaway', wait=25)

    @staticmethod
    def near(d):
        """Positions a command at the dungeon's vault (or its middle), so @e[sort=nearest] picks its own guardian."""
        x, y, z = d['vault'] or ((d['x1'] + d['x2']) // 2, (d['y1'] + d['y2']) // 2, (d['z1'] + d['z2']) // 2)
        return f'positioned {x} {y} {z}'

    def guardian_pos(self, dungeon):
        d = self.found[dungeon]
        out = self.cmd(f'execute in {d["dim"]} {self.near(d)} run data get entity '
                       f'@e[tag={NS}.guardian.{dungeon},limit=1,sort=nearest] Pos')
        nums = [float(v) for v in re.findall(r'(-?\d+\.?\d*)d', out)]
        return tuple(nums[:3])

    def guardian(self, dungeon='soulfire_crypt'):
        """The guardian, name tag shown, facing the camera."""
        self.dungeon(dungeon)
        self.cmd(f'gamemode spectator {PLAYER}', 'time set 6000')
        self.s.hud(True)
        tag = f'{NS}.guardian.{dungeon}'
        d = self.found[dungeon]
        self.cmd(f'execute {self.near(d)} as @e[tag={tag},limit=1,sort=nearest] run data merge entity @s {{NoAI:1b}}')
        g = self.guardian_pos(dungeon)
        eye = (g[0] + 3.2, g[1] + 1.4, g[2] + 2.2)
        self.cmd(f'execute {self.near(d)} run tp @e[tag={tag},limit=1,sort=nearest] {g[0]} {g[1]} {g[2]} '
                 f'facing {eye[0]} {eye[1]} {eye[2]}')
        self.look(eye, (g[0], g[1] + 1.3, g[2]))
        self.save('guardian', wait=8)

    def vault(self, dungeon='dungeon_t2'):
        """The vault chest opened in survival, with its loot."""
        d = self.dungeon(dungeon)
        vx, vy, vz = d['vault']
        self.cmd(f'kill @e[tag={NS}.guardian.{dungeon}]', f'gamemode survival {PLAYER}', f'clear {PLAYER}', 'time set 6000')
        self.s.hud(True)
        for dx, dz in ((0, 2), (0, -2), (2, 0), (-2, 0)):
            if 'passed' in self.cmd(f'execute if block {vx + dx} {vy} {vz + dz} minecraft:air').lower():
                self.look((vx + dx + 0.5, vy, vz + dz + 0.5), (vx + 0.5, vy + 0.4, vz + 0.5))
                break
        time.sleep(3)
        self.s.click(3)
        self.save('vault', wait=2)
        self.s.key('Escape')

    def treasure_map(self):
        """A treasure map from the villa's vault, held on the way out of the villa."""
        d = self.dungeon('outdoor_villa')
        self.cmd(f'gamemode survival {PLAYER}', f'clear {PLAYER}', 'time set 1500')
        self.cmd(f'loot give {PLAYER} loot {NS}:chests/outdoor_villa_vault')
        # Keep only the map, and hold it.
        for slot in range(36):
            if 'passed' in self.cmd(f'execute if items entity {PLAYER} container.{slot} minecraft:filled_map').lower():
                self.cmd(f'item replace entity {PLAYER} weapon.offhand from entity {PLAYER} container.{slot}')
                break
        for slot in range(36):
            self.cmd(f'item replace entity {PLAYER} container.{slot} with minecraft:air')
        self.cmd(f'item replace entity {PLAYER} hotbar.0 from entity {PLAYER} weapon.offhand',
                 f'item replace entity {PLAYER} weapon.offhand with minecraft:air')
        self.s.hud(False)
        cx = (d['x1'] + d['x2']) / 2
        self.look((cx + 5.5, d['y1'] + 1, d['z2'] + 7.5), (cx, d['y1'] + 3, d['z1']))
        self.s.tp(cx + 5.5, d['y1'] + 1, d['z2'] + 7.5, yaw=200, pitch=38)
        self.save('map', wait=6)

    def advancements(self):
        self.cmd(f'gamemode survival {PLAYER}', f'advancement revoke {PLAYER} everything')
        for k in ('root', 'discover_outdoor_villa', 'slay_outdoor_villa_guardian', 'discover_tower_dungeon',
                  'slay_tower_dungeon_guardian', 'discover_dungeon_t2'):
            self.cmd(f'advancement grant {PLAYER} only {NS}:{k}')
        time.sleep(8)
        self.s.hud(True)
        self.s.key('l', delay=2)
        self.save('advancements', wait=2)
        self.s.key('Escape')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, default=25575)
    ap.add_argument('shots', nargs='*')
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    s = Session(port=args.port)
    shots = Shots(s)
    s.focus()
    shots.prepare()
    wanted = args.shots or ['villa', 'spire', 'keep', 'crypt', 'villa_inside', 'spire_inside', 'keep_inside',
                            'crypt_inside', 'guardian', 'vault', 'map', 'advancements', *LABYRINTHS.values(), 'cutaway']
    by_name = {v: k for k, v in NAMES.items()}
    labyrinths = {v: k for k, v in LABYRINTHS.items()}
    for name in wanted:
        if name in labyrinths:
            shots.interior(labyrinths[name], name)
        elif name in by_name:
            shots.exterior(by_name[name])
        elif name.endswith('_inside'):
            shots.interior(by_name[name[:-7]])
        elif name == 'map':
            shots.treasure_map()
        else:
            getattr(shots, name)()
        shots.cmd('execute in minecraft:overworld run forceload remove all', 'execute in minecraft:the_nether run forceload remove all')
    return 0


if __name__ == '__main__':
    sys.exit(main())
