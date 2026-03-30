# Much More Dungeons

A Minecraft mod that adds immersive and rewarding dungeons to the game world, encouraging exploration with balanced structure generation and valuable loot.

## Building the Mod

**Requirements:**
- Java 17 or higher
- Gradle (uses included wrapper)

**Build Steps:**
1. Clone the repository
2. Run `./gradlew build` (or `gradlew.bat build` on Windows)
3. The compiled mod JARs will be in `fabric/build/libs/` and `forge/build/libs/`

## Project Structure

This is a MultiLoader mod supporting both Fabric and Forge with a shared common module:

```
1.20.1/
├── common/                    # Shared code and resources
│   └── src/main/
│       ├── java/com/nightbeam/muchmoredungeons/
│       │   ├── CommonClass.java      # Shared mod initialization
│       │   ├── Constants.java        # Mod constants (ID, name, logger)
│       │   ├── platform/             # Platform abstraction for loader-specific features
│       │   ├── mixin/                # Shared mixins
│       │   └── world/structure/      # Structure registration and implementation
│       └── resources/
│           ├── data/muchmoredungeons/
│           │   ├── loot_tables/      # Loot table definitions
│           │   ├── structures/       # NBT structure files
│           │   └── worldgen/         # Structure set and biome configurations
│           └── muchmoredungeons.mixins.json
│
├── fabric/                    # Fabric-specific code
│   ├── src/main/java/com/nightbeam/muchmoredungeons/
│   │   ├── MuchMoreDungeons.java     # Fabric mod entry point
│   │   └── platform/                 # Fabric platform helper
│   └── src/main/resources/
│       ├── fabric.mod.json           # Fabric metadata
│       └── muchmoredungeons.fabric.mixins.json
│
└── forge/                     # Forge-specific code
    ├── src/main/java/com/nightbeam/muchmoredungeons/
    │   ├── MuchMoreDungeons.java     # Forge mod entry point
    │   └── platform/                 # Forge platform helper
    └── src/main/resources/META-INF/
        ├── mods.toml                 # Forge metadata
        └── muchmoredungeons.forge.mixins.json
```

## Features

### Tower Dungeon Structure
- **Name:** tower_dungeon
- **Spawning:**
  - Biomes: Plains, Forest, Taiga, Birch Forest, Dark Forest, Windswept Plains, Windswept Forest
  - Frequency: Spacing of 30 chunks, separation of 10 chunks
  - Generate on surface with proper terrain adaptation
- **Loot:** Balanced chest loot including iron, gold, diamonds, emeralds, and enchanted books

## Mod Metadata

| Field | Value |
|-------|-------|
| Mod ID | muchmoredungeons |
| Display Name | Much More Dungeons |
| Package | com.nightbeam.muchmoredungeons |
| Author | nightbeam |
| Website | https://nightbeam.cloud |
| Version | 1.0.0 |
| Minecraft Version | 1.20.1 |

## Development

### Adding New Features
1. Common code goes in `common/src/main/java/com/nightbeam/muchmoredungeons/`
2. Loader-specific code goes in `fabric/` or `forge/` directories respectively
3. Shared resources go in `common/src/main/resources/`
4. Update build.gradle files if adding new dependencies

### Logging
All logging uses SLF4J via `Constants.LOG`:
```java
Constants.LOG.info("Message with mod name in logger");
Constants.LOG.debug("Debug information");
Constants.LOG.error("Error message", exception);
```

### Platform Services
Use the ServiceLoader-based platform abstraction to access loader-specific APIs:
```java
if (Services.PLATFORM.isDevelopmentEnvironment()) {
    // Dev environment specific code
}
String platformName = Services.PLATFORM.getPlatformName(); // "Fabric" or "Forge"
```

## License

CC0-1.0 (Public Domain)

## Support

For issues and support, visit: https://nightbeam.cloud
