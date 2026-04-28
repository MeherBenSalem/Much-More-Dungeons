---
description: "Use when editing mod code or resources in the versioned common, fabric, forge, or neoforge source trees. Enforces the Much More Dungeons multiloader separation between shared code and loader-specific adapters."
name: "Multiloader Separation"
applyTo:
  - "*/common/src/**"
  - "*/fabric/src/**"
  - "*/forge/src/**"
  - "*/neoforge/src/**"
---

# Multiloader Separation

- Treat each version folder as a multiloader project split into `common/` plus loader modules.
- Put shared gameplay logic, shared registrations, shared mixins, and shared data resources in `common/src/`.
- Put only loader-specific entrypoints, metadata, platform adapters, and loader API integrations in `fabric/src/`, `forge/src/`, or `neoforge/src/`.
- Do not import Fabric, Forge, or NeoForge APIs into `common/` code.
- When shared code needs loader-specific behavior, add or use a platform service abstraction in `common/` and implement it in each supported loader module.
- If a platform service, loader contract, or shared abstraction changes, update every supported loader module for that version in the same change.
- Prefer changing shared behavior once in `common/` and only mirror the minimum required wiring in loader modules.
- Keep resource placement aligned with the project structure: shared mod data in `common/src/main/resources/`, loader metadata in the matching loader module resources.