# Much More Dungeons

MultiLoader Minecraft mod that adds handcrafted dungeon structures with balanced loot for Fabric, Forge, and NeoForge.

## Features

- Tower dungeon, outdoor villa, dungeon T2, and Soulfire Crypt structures
- Soulfire Crypt: cold-biome crypt with spawners, themed hostiles, and a Cinder Warden
- Natural worldgen placement with biome tags and structure sets
- Chest loot tuned for survival progression
- Shared `common` code with loader-specific Fabric / Forge / NeoForge modules

## Requirements

| Workspace | Loaders | Java |
|-----------|---------|------|
| `1.20.1` | Fabric, Forge | 17 |
| `1.21.1` | Fabric, NeoForge | 21 |
| `26.1.2` | Fabric, NeoForge | 25 |
| `26.2` | Fabric, NeoForge | 25 |

Shared mod version: **1.2.0**

## Building

Build one workspace:

```powershell
cd 1.20.1
.\gradlew.bat build
```

Build all workspaces and collect jars into `dist/`:

```powershell
.\build-all.ps1
```

Jars land in each workspace under `fabric/build/libs/`, `forge/build/libs/`, or `neoforge/build/libs/`, and in `dist/` after `build-all.ps1`.

## Project layout

```
/
├── 1.20.1/   # Fabric + Forge
├── 1.21.1/   # Fabric + NeoForge
├── 26.1.2/   # Fabric + NeoForge
├── 26.2/     # Fabric + NeoForge
└── build-all.ps1
```

Each version folder is a MultiLoader project: shared logic in `common/`, loader entrypoints in `fabric/`, `forge/`, or `neoforge/`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Security

See [.github/SECURITY.md](.github/SECURITY.md).

## License

Licensed under the [Apache License 2.0](LICENSE).
