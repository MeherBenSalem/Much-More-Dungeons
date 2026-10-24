# Contributing

Thanks for helping improve Much More Dungeons.

## How to contribute

1. Fork the repository and create a feature branch from `main`.
2. Make focused changes in the relevant Minecraft version workspace (`1.20.1/`, `1.21.1/`, `26.1.2/`, `26.2/` or
   `26.3/`). A gameplay change usually belongs in all five: the `common/` code is nearly identical between them, and
   only version-specific APIs differ.
3. Build the workspace you changed (`./gradlew build` from that folder, with Java 17 for 1.20.1, 21 for 1.21.1 and 25
   for 26.x). This also runs the unit tests.
4. Open a pull request describing the change and how you tested it.

## Layout

Each workspace is a MultiLoader Gradle build:

- `common/`: everything that matters. `dungeon/` holds the Minecraft-free parts (the dungeon definitions and the
  terrain decision, unit-tested), `world/` the structure, piece, guardian and registration code, `config/` the config
  file, `command/` the inspect command.
- `fabric/` and `neoforge/` (`forge/` on 1.20.1): entry points that register the structure and piece types and the
  command, and give common code the config folder.

Data is generated, not edited by hand:

```bash
pip install nbtlib
python3 tools/datagen.py                   # loot tables, advancements, tags, structures, structure sets, language
python3 tools/templates.py                 # villa, spire and keep templates (idempotent fixes), copied to all workspaces
python3 tools/generate_soulfire_crypt.py   # the crypt template
```

`tools/datagen.py` knows each version's data format (folder names, predicate and loot function syntax); change the
tables at its top and run it, then rebuild.

## Testing in game

`tools/qa/` drives dev servers over RCON and a real client under Xvfb (software rendering). It needs `xdotool` and
ImageMagick (`import`) and an X server on `:1` (`Xvfb :1 -screen 0 1920x1080x24 &`).

```bash
tools/qa/devrun.sh prepare-server 26.3 fabric     # eula, RCON on 25575 (password qa), a fresh normal world
tools/qa/devrun.sh start-server 26.3 fabric
tools/qa/devrun.sh start-client 26.3 fabric       # joins localhost:25565 as "Builder"
python3 tools/qa/rcon.py "op Builder"
python3 tools/qa/dungeon_checks.py --log /tmp/mmd-qa/fabric-server.log --client --shots /tmp/mmd-qa/shots
tools/qa/devrun.sh stop-client; tools/qa/devrun.sh stop-server 26.3
```

`dungeon_checks.py` locates every dungeon, generates the located one and inspects it (chests on the right loot tables,
the loot rolls including a treasure map, spawner mobs, the guardian), places another with `/place structure` and
inspects that, rolls every loot table, and with `--client` walks into each dungeon, defeats its guardian and checks the
advancements and the weapon drop. It ends by scanning the server log for errors.

`tools/qa/run_matrix.sh` does all of that on a fresh world for every build (ten: five versions, two loaders each):

```bash
tools/qa/run_matrix.sh                       # all builds; results in /tmp/mmd-qa/results/
tools/qa/run_matrix.sh 26.3:fabric 1.20.1:forge
```

`prepare-server` writes `advertiseDedicatedServerToLan = false` to `forge/runs/server/defaultconfigs/forge-server.toml`
for the 1.20.1 Forge dev server (otherwise Forge's LAN advertiser loads a client-only class and the server stops).
`tools/qa/rarity.py` measures how far the nearest of each dungeon is from a grid of points, to check spacing changes.

If you change gameplay or data, run the checks on every workspace you touched, for both loaders.

## Coding expectations

- Prefer small, reviewable PRs over large mixed changes.
- Keep ids stable: structure, structure type, piece, template and loot table ids are what saved worlds refer to.
- Keep logic Minecraft-free where it can be, and test it in `common/src/test`.
- Match existing naming, package layout, and MultiLoader patterns.
- Do not commit build output, run directories, IDE metadata, or local secrets.
- When fixing a bug, say which versions and loaders you verified.

## Issues

Use GitHub Issues for bugs and feature requests. Include the Minecraft version, mod loader, mod version, other
worldgen mods, and steps to reproduce when reporting bugs.

## Licensing

By contributing, you agree that your contributions are licensed under the Apache License, Version 2.0, unless you
state otherwise in the pull request.
