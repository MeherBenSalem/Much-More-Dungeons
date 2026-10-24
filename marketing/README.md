# Marketing

Listing copy and artwork for CurseForge and Modrinth.

| Path | What it is |
|------|------------|
| `curseforge/description.md` | The project description (Markdown; also works on Modrinth). Images load from this repo's `main` branch. |
| `curseforge/summary.txt` | The one-line summary (under 250 characters). |
| `images/banner.png` | 1800×600 header banner. |
| `images/icon.png` | 512×512 project icon (also the mod's in-jar `logo.png`). |
| `images/card-*.png` | 1600×900 feature cards used in the description and as gallery images. |
| `images/header-*.png`, `images/divider.png` | Transparent section headers and a divider for the description. |
| `images/screenshots/*.jpg` | Real in-game captures (Minecraft 26.3, Fabric) used by the cards and the gallery. |
| `source/render.cjs` | Renders every PNG above from the screenshots and the bundled fonts. |
| `source/fonts/` | Cinzel and Alegreya Sans, both under the SIL Open Font License (licence files included). |

The look: torch-lit stone, amber gold for titles, a dashed treasure-map line ending in a red X, and one colour per
dungeon tier (Villa green, Spire violet, Keep ember, Crypt soul cyan) used for frames, tags and the divider.

## Regenerating the images

Needs Node.js and Playwright with Chromium:

```bash
NODE_PATH="$(npm root -g)" node marketing/source/render.cjs             # everything
NODE_PATH="$(npm root -g)" node marketing/source/render.cjs card-trail  # one asset
```

The release name and the supported Minecraft versions and loaders are at the top of `render.cjs`, with the four
dungeons' names, tiers and colours. Supporting a new Minecraft version means adding one line there, plus one row to the
download table in `description.md`. After changing the icon, copy `images/icon.png` to every workspace's
`common/src/main/resources/logo.png`.

## Retaking the screenshots

`tools/qa/marketing_shots.py` captures every screenshot from a dev client (see `tools/qa/` and `CONTRIBUTING.md`): a
1920×1080 window under Xvfb, on a 26.3 Fabric dev server whose `server.properties` uses `level-name=showcase`,
`level-type=minecraft:normal`, the seed given at the top of the script, `broadcast-rcon-to-ops=false` and
`view-distance=12`:

```bash
tools/qa/devrun.sh prepare-server 26.3 fabric showcase minecraft:normal <seed>
sed -i 's/view-distance=8/view-distance=12/' 26.3/fabric/runs/server/server.properties
tools/qa/devrun.sh start-server 26.3 fabric && tools/qa/devrun.sh start-client 26.3 fabric
python3 tools/qa/rcon.py "op Builder"
python3 tools/qa/marketing_shots.py              # or a few: villa spire_inside vault
```

Every dungeon in the pictures is the naturally generated one `/locate` finds from spawn; camera angles per dungeon
are at the top of the script. Every screenshot is a single unedited frame.

| Screenshot | Scene |
|------------|-------|
| `villa.jpg`, `spire.jpg`, `keep.jpg`, `crypt.jpg` | Each dungeon from outside, in its biome |
| `villa_inside.jpg`, `spire_inside.jpg`, `keep_inside.jpg`, `crypt_inside.jpg` | Inside each dungeon, from its guardian towards the vault |
| `guardian.jpg` | A guardian with its name shown |
| `vault.jpg` | A vault opened in survival, with its loot |
| `map.jpg` | A treasure map from the Villa's vault, in hand |
| `advancements.jpg` | The Much More Dungeons advancement tab |
