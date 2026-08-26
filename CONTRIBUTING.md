# Contributing

Thanks for contributing to Much More Dungeons.

## How to contribute

1. Fork the repository and create a branch from `main`.
2. Make your change in the correct MultiLoader workspace (`1.20.1`, `1.21.1`, `26.1.2`, or `26.2`).
3. Keep shared gameplay logic in `common/`. Put loader-specific code only in `fabric/`, `forge/`, or `neoforge/`.
4. Build the workspace you touched (`./gradlew build` or `gradlew.bat build` inside that folder).
5. Open a pull request with a short description of what changed and why.

## Expectations

- Prefer small, focused changes.
- Do not commit build outputs (`dist/`, `**/build/`), IDE files, or secrets.
- Match existing naming and package structure (`com.nightbeam.muchmoredungeons`).
- If you change shared behavior, update every loader module for that Minecraft version in the same PR when needed.

## Licensing

Unless you state otherwise, contributions are submitted under the [Apache License 2.0](LICENSE).
