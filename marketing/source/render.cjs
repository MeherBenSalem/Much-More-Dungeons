// Renders the listing artwork in marketing/images/ from real in-game captures (marketing/images/screenshots/) and the
// bundled OFL fonts. Usage (from the repository root): NODE_PATH="$(npm root -g)" node marketing/source/render.cjs [name...]
// Requires the `playwright` package with a Chromium build available.
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

// The release and the supported Minecraft versions. Adding a version is one line here
// (plus one row in the download table of curseforge/description.md).
const RELEASE = { version: '2.0', name: 'The Labyrinth Update' };
const VERSIONS = [
  { minecraft: '1.20.1', loaders: ['Fabric', 'Forge'] },
  { minecraft: '1.21.1', loaders: ['Fabric', 'NeoForge'] },
  { minecraft: '26.1.2', loaders: ['Fabric', 'NeoForge'] },
  { minecraft: '26.2', loaders: ['Fabric', 'NeoForge'] },
  { minecraft: '26.3', loaders: ['Fabric', 'NeoForge'] },
];
const LOADERS = ['Fabric', 'Forge', 'NeoForge'].filter((loader) => VERSIONS.some((v) => v.loaders.includes(loader)));

// The four dungeons, in trail order. Colours are the tier colours used everywhere in the artwork.
const DUNGEONS = [
  { key: 'villa', name: 'Smuggler’s Villa', tier: 1, color: '#9ccc65', biome: 'Plains, meadows, savannas', guardian: 'Smuggler Chief' },
  { key: 'spire', name: 'Arcane Spire', tier: 2, color: '#c58cff', biome: 'Forests and taigas', guardian: 'Spire Illusionist' },
  { key: 'keep', name: 'Cursed Keep', tier: 3, color: '#ff7a59', biome: 'Deserts, badlands, jungles, swamps', guardian: 'Keep Warlord' },
  { key: 'crypt', name: 'Soulfire Crypt', tier: 4, color: '#5fe3e6', biome: 'Snowy and cold lands', guardian: 'Cinder Warden' },
];

// The six labyrinths: procedural underground dungeons, a new layout every time.
const LABYRINTHS = [
  { key: 'catacombs', name: 'Forgotten Catacombs', tier: 2, color: '#d8ccb0', where: 'Under plains and forests', guardian: 'Bone Warden' },
  { key: 'tomb', name: 'Sunscorched Tomb', tier: 2, color: '#f0c46a', where: 'Under deserts and badlands', guardian: 'Tomb King' },
  { key: 'warrens', name: 'Verdant Warrens', tier: 2, color: '#8fd16a', where: 'Under jungles and swamps', guardian: 'Broodmother' },
  { key: 'frost', name: 'Rimefrost Vaults', tier: 3, color: '#a8e8ff', where: 'Under snowy lands', guardian: 'Frost Lich' },
  { key: 'abyss', name: 'Abyssal Halls', tier: 4, color: '#59d3c6', where: 'Deep below everything', guardian: 'Abyssal Knight' },
  { key: 'bastille', name: 'Infernal Bastille', tier: 4, color: '#ff6a3d', where: 'In the Nether', guardian: 'Brute Overseer' },
];

const root = path.resolve(__dirname, '..', '..');
const out = path.join(root, 'marketing', 'images');
const shots = path.join(out, 'screenshots');
const fonts = path.join(__dirname, 'fonts');
const url = (file) => 'file://' + file;
const shot = (name) => url(path.join(shots, name));

const css = `
@font-face { font-family: Display; src: url('${url(path.join(fonts, 'cinzel.woff2'))}'); font-weight: 400 900; }
@font-face { font-family: Body; font-weight: 500; src: url('${url(path.join(fonts, 'alegreya-sans-500.woff2'))}'); }
@font-face { font-family: Body; font-weight: 800; src: url('${url(path.join(fonts, 'alegreya-sans-800.woff2'))}'); }
:root { --text:#f3ead9; --dim:#b9a98f; --gold:#f2b45a; --ember:#ff7a3d; --bg:#100d0c; --stone:#2a2420; }
* { box-sizing: border-box; }
html, body { margin: 0; background: var(--bg); color: var(--text); font-family: Body, sans-serif; font-weight: 500; }
.stage { position: relative; overflow: hidden; background: radial-gradient(ellipse at 28% 45%, #2b1f17 0%, #100d0c 72%); }
.display { font-family: Display, serif; font-weight: 900; letter-spacing: .02em; }
.title { background: linear-gradient(180deg, #fff6e2 0%, #ffd88a 45%, #f2b45a 70%, #b8742c 100%);
         -webkit-background-clip: text; background-clip: text; color: transparent; }
.glow { filter: drop-shadow(0 0 20px rgba(242,180,90,.32)) drop-shadow(0 3px 0 rgba(0,0,0,.75)); }
.kicker { font-weight: 800; color: var(--gold); letter-spacing: .24em; font-size: 22px; text-transform: uppercase; }
.trail { height: 0; border-top: 4px dashed rgba(242,180,90,.85); }
.x { display: inline-block; position: relative; width: 22px; height: 22px; }
.x::before, .x::after { content: ''; position: absolute; left: 9px; top: -2px; width: 5px; height: 26px; background: #e2402c; border-radius: 2px;
                        box-shadow: 0 0 8px rgba(226,64,44,.7); }
.x::before { transform: rotate(45deg); } .x::after { transform: rotate(-45deg); }
.frame { position: relative; overflow: hidden; background: #000; border: 3px solid #6b5640; border-radius: 6px;
         box-shadow: 0 0 0 3px #1a1310, 0 0 0 5px rgba(242,180,90,.45), 0 28px 70px rgba(0,0,0,.75); }
.frame > img, .frame > div > img { display: block; }
.frame::after { content: ''; position: absolute; inset: 0; box-shadow: inset 0 0 40px rgba(0,0,0,.55); pointer-events: none; }
.rivet { position: absolute; width: 12px; height: 12px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #ffe0a0, #9a6a2c 70%);
         box-shadow: 0 1px 2px #000; z-index: 3; }
.vignette { position: absolute; inset: 0; background: radial-gradient(ellipse at center, rgba(0,0,0,0) 38%, rgba(0,0,0,.82) 100%); }
.backdrop { position: absolute; inset: -40px; background-size: cover; background-position: center; filter: blur(12px) brightness(.3) saturate(1.1) sepia(.25); }
.bricks { position: absolute; inset: 0; opacity: .07;
          background-image: linear-gradient(#000 2px, transparent 2px), linear-gradient(90deg, #000 2px, transparent 2px);
          background-size: 64px 32px, 64px 64px; }
.pill { display: inline-block; border-radius: 4px; border: 2px solid rgba(242,180,90,.7); padding: 6px 18px 4px; margin-right: 12px;
        font-weight: 800; font-size: 20px; letter-spacing: .1em; color: #fff3d8; background: rgba(16,13,12,.7); text-transform: uppercase; }
.tag { display: inline-flex; align-items: center; gap: 10px; font-weight: 800; font-size: 19px; letter-spacing: .12em; text-transform: uppercase;
       padding: 6px 14px 5px; border-radius: 4px; background: rgba(16,13,12,.88); }
ul.points { list-style: none; padding: 0; margin: 0; }
ul.points li { position: relative; padding-left: 34px; margin: 0 0 14px; font-size: 28px; line-height: 1.28; }
ul.points li::before { content: ''; position: absolute; left: 4px; top: 11px; width: 11px; height: 11px; background: var(--gold);
                       transform: rotate(45deg); box-shadow: 0 0 10px rgba(242,180,90,.7); }
b.hi { color: #fff; font-weight: 800; }
.stats { display: flex; margin-top: 22px; border: 2px solid rgba(242,180,90,.4); border-radius: 6px; background: rgba(16,13,12,.86);
         box-shadow: 0 18px 50px rgba(0,0,0,.55); }
.stats > div { flex: 1; padding: 12px 22px 10px; border-left: 2px solid rgba(242,180,90,.18); }
.stats > div:first-child { border-left: 0; }
.stats .t { font-weight: 800; font-size: 16px; letter-spacing: .18em; color: var(--dim); text-transform: uppercase; }
.stats .v { font-family: Display, serif; font-weight: 900; font-size: 30px; color: #fff3d8; margin-top: 2px; white-space: nowrap; }
`;

// Embers drifting up from the bottom of a card. Deterministic.
const embers = (count = 40, seed = 7) => `<canvas style="position:absolute;inset:0;width:100%;height:100%"></canvas><script>
(() => { const c = document.currentScript.previousElementSibling; const r = c.getBoundingClientRect();
  c.width = r.width; c.height = r.height; const g = c.getContext('2d'); let s = ${seed};
  const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  for (let i = 0; i < ${count}; i++) { const x = rnd() * c.width, y = c.height * (.35 + rnd() * .65), r = 1 + rnd() * 2.6, a = .15 + rnd() * .5;
    g.fillStyle = 'rgba(255,' + Math.round(140 + rnd() * 80) + ',80,' + a + ')'; g.shadowColor = 'rgba(255,150,60,.9)'; g.shadowBlur = 10;
    g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill(); } })();
</script>`;

const page = (width, height, body, transparent = false) => `<!doctype html><html><head><meta charset="utf-8"><style>${css}
body { width: ${width}px; height: ${height}px; } .stage { width: ${width}px; height: ${height}px; }
${transparent ? 'html, body, .stage { background: transparent; }' : ''}</style></head>
<body><div class="stage">${body}</div></body></html>`;

const rivets = () => ['left:8px;top:8px', 'right:8px;top:8px', 'left:8px;bottom:8px', 'right:8px;bottom:8px']
  .map((p) => `<span class="rivet" style="${p}"></span>`).join('');
// An exact region (x, y, w, h in 1920x1080 pixels) of a capture, scaled to W pixels wide, in a riveted frame.
const region = (file, x, y, w, h, W) => `<div style="position:relative;width:${W}px;height:${Math.round(W * h / w)}px;overflow:hidden">
    <img src="${shot(file)}" style="position:absolute;max-width:none;width:${W * 1920 / w}px;left:${-x * W / w}px;top:${-y * W / w}px"></div>`;
const framed = (inner, style = '') => `<div class="frame" style="${style}">${inner}${rivets()}</div>`;
const tierTag = (d, extra = '') => `<span class="tag" style="border:2px solid ${d.color};color:${d.color};${extra}">
  <span style="display:inline-block;width:10px;height:10px;background:${d.color};transform:rotate(45deg);box-shadow:0 0 8px ${d.color}"></span>Tier ${d.tier} · ${d.name}</span>`;
const stats = (items) => `<div class="stats">${items.map(([t, v, flex]) =>
  `<div${flex ? ` style="flex:${flex}"` : ''}><div class="t">${t}</div><div class="v">${v}</div></div>`).join('')}</div>`;

// A feature card: copy on the left, artwork on the right.
const card = ({ kicker, title, points, art, width = 1600, height = 900, artWidth = 940, backdrop = 'spire.jpg', color }) => page(width, height, `
  <div class="backdrop" style="background-image:url('${shot(backdrop)}')"></div>
  <div class="bricks"></div><div class="vignette"></div>${embers()}
  <div style="position:absolute;left:80px;top:0;bottom:0;width:${width - artWidth - 150}px;display:flex;flex-direction:column;justify-content:center">
    <div class="kicker" style="${color ? `color:${color}` : ''}">${kicker}</div>
    <div class="display title glow" style="font-size:66px;line-height:1.04;margin:14px 0 22px">${title}</div>
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:30px"><div class="trail" style="flex:1"></div><span class="x"></span></div>
    <ul class="points">${points.map((point) => `<li>${point.replace(/ (\S+)$/, '&nbsp;$1')}</li>`).join('')}</ul>
  </div>
  <div style="position:absolute;right:62px;top:50%;transform:translateY(-50%);width:${artWidth}px">${art}</div>`);

const versionText = VERSIONS.map((v) => v.minecraft).join(' · ');

// An excerpt of the config file the mod writes on first start (comments and values as generated).
const configPanel = () => {
  const c = (text) => `<span style="color:#8c7c66">${text}</span>`;
  const k = (text) => `<span style="color:#ffd88a">"${text}"</span>`;
  const v = (text) => `<span style="color:#9ccc65">${text}</span>`;
  const lines = [
    c('// Much More Dungeons. Changes apply after a restart and only to chunks generated afterwards.'),
    c('// Spacing, separation and biomes are datapack data: see the README on GitHub.'),
    '{',
    `  ${c('// Spawn each dungeon’s named guardian when the dungeon generates.')}`,
    `  ${k('guardians')}: ${v('true')},`,
    '',
    `  ${c('// Per dungeon: "enabled" turns it off entirely (it can then not be located either), "chance"')}`,
    `  ${c('// (0 to 1) is the share of valid spots that get one; 0.5 halves how many generate.')}`,
    `  ${k('dungeons')}: {`,
    `    ${k('outdoor_villa')}: { ${k('enabled')}: ${v('true')}, ${k('chance')}: ${v('1.0')} },`,
    `    ${k('tower_dungeon')}: { ${k('enabled')}: ${v('true')}, ${k('chance')}: ${v('1.0')} },`,
    `    ${k('dungeon_t2')}: { ${k('enabled')}: ${v('true')}, ${k('chance')}: ${v('1.0')} },`,
    `    ${k('soulfire_crypt')}: { ${k('enabled')}: ${v('true')}, ${k('chance')}: ${v('1.0')} }`,
    '  }',
    '}',
  ];
  return `<pre style="margin:0;padding:22px 24px;font-size:16px;line-height:1.55;color:#eadfca;white-space:pre;font-family:'DejaVu Sans Mono',monospace">${lines.join('\n')}</pre>`;
};

// The trail: four dungeons linked by a dashed map line, each with its tier colour.
const trailStrip = (size = 200) => `<div style="position:relative;display:flex;justify-content:space-between;align-items:center">
  <div class="trail" style="position:absolute;left:${size / 2}px;right:${size / 2}px;top:${size / 2}px"></div>
  ${DUNGEONS.map((d) => `<div style="position:relative;display:flex;flex-direction:column;align-items:center;width:${size}px">
    <div class="frame" style="width:${size}px;height:${size}px;border-color:${d.color};border-radius:50%">
      <img src="${shot(d.key + '.jpg')}" style="width:${size * 1.9}px;margin-left:-${size * .45}px;margin-top:-${size * .1}px"></div>
    <div class="display" style="font-size:${Math.round(size / 8.5)}px;color:${d.color};margin-top:12px;text-align:center;line-height:1.15;min-height:2.3em;text-shadow:0 2px 0 #000">${d.name}</div>
    <div style="font-size:${Math.round(size / 11)}px;color:var(--dim);font-weight:800;letter-spacing:.12em;margin-top:4px">TIER ${d.tier}</div></div>`).join('')}</div>`;

const header = (title) => page(1400, 120, `
  <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:22px">
    <div class="trail" style="width:250px"></div>
    <span style="display:inline-block;width:16px;height:16px;background:var(--gold);transform:rotate(45deg);box-shadow:0 0 12px rgba(242,180,90,.8)"></span>
    <div class="display title glow" style="font-size:56px;white-space:nowrap">${title}</div>
    <span style="display:inline-block;width:16px;height:16px;background:var(--gold);transform:rotate(45deg);box-shadow:0 0 12px rgba(242,180,90,.8)"></span>
    <div class="trail" style="width:250px"></div>
  </div>`, true);

const divider = () => page(1400, 44, `
  <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:18px">
    <div class="trail" style="width:400px;opacity:.75"></div>
    ${DUNGEONS.map((d) => `<span style="display:inline-block;width:13px;height:13px;background:${d.color};transform:rotate(45deg);box-shadow:0 0 10px ${d.color}"></span>`).join('')}
    <span class="x" style="margin-left:6px"></span>
    <div class="trail" style="width:400px;opacity:.75"></div>
  </div>`, true);

const dungeonCard = (key, points, inside, crop = [160, 60, 1600, 900]) => {
  const d = DUNGEONS.find((x) => x.key === key);
  return card({
    kicker: `Tier ${d.tier} · ${d.biome}`, title: d.name.replace(' ', '<br>'), color: d.color, backdrop: `${key}.jpg`, points,
    art: `<div style="position:relative">${framed(region(`${key}.jpg`, ...crop, 940), `border-color:${d.color}`)}
      <div class="frame" style="position:absolute;right:-24px;bottom:-46px;width:400px;border-color:${d.color}">${region(inside, 240, 135, 1440, 810, 400)}</div>
      <div style="position:absolute;left:18px;top:18px">${tierTag(d)}</div></div>` });
};

const assets = {
  banner: () => page(1800, 600, `
    <img src="${shot('spire.jpg')}" style="position:absolute;right:-260px;top:-170px;width:1500px;-webkit-mask-image:linear-gradient(90deg,transparent 0%,#000 36%);mask-image:linear-gradient(90deg,transparent 0%,#000 36%)">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(16,13,12,.97) 0%,rgba(16,13,12,.9) 33%,rgba(16,13,12,.35) 58%,rgba(16,13,12,0) 80%)"></div>
    <div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(16,13,12,.8) 0%,rgba(16,13,12,0) 34%)"></div>
    <div class="bricks" style="-webkit-mask-image:linear-gradient(90deg,#000 0%,#000 38%,transparent 60%);mask-image:linear-gradient(90deg,#000 0%,#000 38%,transparent 60%)"></div>
    <div class="vignette" style="opacity:.6"></div>${embers(46, 3)}
    <div style="position:absolute;left:82px;top:62px;width:1160px">
      <div class="kicker">${RELEASE.version} · ${RELEASE.name}</div>
      <div class="display title glow" style="display:inline-block;font-size:96px;line-height:1;margin:16px 0 18px;padding-right:10px;white-space:nowrap">Much More Dungeons</div>
      <div style="display:flex;align-items:center;gap:16px;width:720px;margin-bottom:22px">
        ${DUNGEONS.map((d) => `<span style="display:inline-block;width:14px;height:14px;background:${d.color};transform:rotate(45deg);box-shadow:0 0 10px ${d.color}"></span>`).join('<div class="trail" style="flex:1"></div>')}
        <div class="trail" style="flex:1"></div><span class="x"></span></div>
      <div style="font-size:32px;color:#fff3d8;line-height:1.28;font-weight:800">Four handcrafted dungeons, six procedural labyrinths,<br>ten guardians, and treasure maps from one to the next.</div>
      <div style="margin-top:30px">${LOADERS.map((l) => `<span class="pill">${l}</span>`).join('')}
        <span style="font-size:22px;color:var(--dim);margin-left:6px;font-weight:800">${versionText}</span></div>
    </div>`),

  icon: () => page(512, 512, `
    <div style="position:absolute;inset:0;border-radius:92px;overflow:hidden;background:#100d0c">
      <img src="${shot('spire.jpg')}" style="position:absolute;width:1100px;left:-300px;top:-60px;filter:saturate(1.15) contrast(1.05)">
      <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 38%,rgba(16,13,12,0) 30%,rgba(16,13,12,.85) 100%)"></div>
      <div style="position:absolute;left:0;right:0;bottom:0;height:150px;background:linear-gradient(0deg,rgba(16,13,12,.95),rgba(16,13,12,0))"></div>
      <svg width="512" height="512" style="position:absolute;inset:0">
        <path d="M70 430 C 150 380, 230 440, 300 400 S 410 360, 430 410" fill="none" stroke="#f2b45a" stroke-width="9" stroke-dasharray="20 15" stroke-linecap="round" style="filter:drop-shadow(0 0 6px rgba(242,180,90,.8))"/>
        <g transform="translate(430 410)" style="filter:drop-shadow(0 0 8px rgba(226,64,44,.9))">
          <rect x="-7" y="-34" width="14" height="68" rx="4" fill="#e2402c" transform="rotate(45)"/>
          <rect x="-7" y="-34" width="14" height="68" rx="4" fill="#e2402c" transform="rotate(-45)"/></g>
      </svg>
    </div>
    <div style="position:absolute;inset:0;border-radius:92px;border:8px solid #b8742c;box-shadow:inset 0 0 0 4px #1a1310, inset 0 0 50px rgba(242,180,90,.25)"></div>`, true),

  'card-labyrinths': () => card({
    kicker: 'Six labyrinths', title: 'Never the<br>same maze', backdrop: 'catacombs.jpg',
    points: ['Underground dungeons assembled by jigsaw: corridors, stairs, rooms and a vault, in a new layout every time',
      'Spawner rooms, storerooms, libraries, shrines and pillared halls', 'A guardian waits in every vault chamber',
      'Under the Overworld’s biomes, deep below everything, and in the Nether'],
    art: `<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px">
      ${LABYRINTHS.map((d) => `<div style="position:relative">${framed(region(d.key + '.jpg', 240, 135, 1440, 810, 300), `border-color:${d.color}`)}
        <div style="position:absolute;left:26px;bottom:9px"><span class="tag" style="border:2px solid ${d.color};color:${d.color};font-size:13px;padding:4px 9px 3px">${d.name}</span></div></div>`).join('')}</div>
      ${stats([['Labyrinths', '6'], ['Pieces each', '15'], ['Layouts', 'Endless']])}` }),

  'card-cutaway': () => card({
    kicker: 'Procedural', title: 'Every map<br>is new', backdrop: 'cutaway.jpg',
    points: ['A labyrinth seen from above with the ground taken away',
      'Built from its theme’s blocks, mobs and loot', 'Stairs lead further down; dead ends hide loot alcoves',
      'Pieces and pools are datapack data: add your own rooms'],
    art: framed(region('cutaway.jpg', 160, 60, 1600, 900, 940)) }),

  'card-dungeons': () => card({
    kicker: 'Four handcrafted dungeons', title: 'From smugglers<br>to soulfire',
    points: ['Each dungeon has its own biomes, loot tier, spawners and guardian',
      'Hand-built, centred on flat, dry ground: no floating, no flooding',
      'Find them with <b class="hi">/locate</b>, or follow the treasure maps',
      'Ids are unchanged: 1.x worlds keep their dungeons'],
    art: `<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
      ${DUNGEONS.map((d) => `<div style="position:relative">${framed(region(d.key + '.jpg', 240, 135, 1440, 810, 460), `border-color:${d.color}`)}
        <div style="position:absolute;left:12px;bottom:12px">${tierTag(d, 'font-size:15px')}</div></div>`).join('')}</div>` }),

  'card-trail': () => card({
    kicker: 'The dungeon trail', title: 'Follow<br>the map', backdrop: 'map.jpg',
    points: ['Every vault holds a treasure map to a dungeon of the next tier', 'Regular chests may hold one too',
      'Tier I → II → III → IV: the loot gets better at every step',
      'Maps lead to a dungeon in land nobody has explored yet'],
    art: `${framed(region('map.jpg', 160, 60, 1600, 900, 940))}<div style="margin-top:34px">${trailStrip(170)}</div>` }),

  'card-guardians': () => card({
    kicker: 'Guardians', title: 'Something<br>to fight', backdrop: 'guardian.jpg',
    points: DUNGEONS.map((d) => `<b class="hi" style="color:${d.color}">${d.guardian}</b> guards the ${d.name}`).concat(
      ['Six more in the labyrinths, from the Bone Warden to the Brute Overseer',
        'Tougher than their kind, they stay until defeated, and their weapon always drops']),
    art: framed(region('guardian.jpg', 160, 60, 1600, 900, 940)) }),

  'card-loot': () => card({
    kicker: 'Loot', title: 'Four tiers<br>of treasure', backdrop: 'vault.jpg',
    points: ['Every chest rolls from its dungeon’s own loot table', 'One guarded <b class="hi">vault</b> per dungeon with the best of it',
      'Early: iron, emeralds, crossbows. Late: diamonds, netherite, enchanted golden apples',
      'Enchantments scale from level 5 to 39 with the tier', 'All tables can be changed with a datapack'],
    art: `${framed(region('vault.jpg', 360, 150, 1200, 780, 940))}
      ${stats(DUNGEONS.map((d) => [`Tier ${d.tier}`, `<span style="color:${d.color}">${d.name.split(' ').pop()}</span>`]))}` }),

  'card-advancements': () => card({
    kicker: 'Advancements', title: 'A tab of<br>its own', backdrop: 'advancements.jpg',
    points: ['Discover each dungeon and labyrinth', 'Defeat each guardian, with experience as a reward',
      '<b class="hi">Dungeon Delver</b>: all four dungeons', '<b class="hi">Into Every Maze</b>: all six labyrinths',
      '23 advancements in their own tab'],
    art: framed(region('advancements.jpg', 240, 100, 1440, 880, 940)) }),

  'card-worldgen': () => card({
    kicker: 'For servers and modpacks', title: 'Your world,<br>your rules', backdrop: 'keep.jpg',
    points: ['<b class="hi">config/muchmoredungeons.json</b>: switch off or thin out the four dungeons, or skip their guardians',
      'Spacing, biomes, loot and advancements are plain datapack JSON',
      'Modded biomes join through biome tags', 'Kept clear of villages',
      '<b class="hi">/muchmoredungeons inspect</b> shows what a dungeon holds'],
    art: `<div style="display:flex;flex-direction:column;gap:18px">
      ${framed(configPanel(), 'background:#15100d')}
      ${stats([['Loaders', 'Fabric · NeoForge · Forge', 2], ['Versions', '5'], ['Structures', '10']])}</div>` }),

  'card-villa': () => dungeonCard('villa', ['A smugglers’ warehouse of barrels and crates', 'Pillager spawner in the aisle',
    'Guarded by the <b class="hi">Smuggler Chief</b>', 'Iron, emeralds, crossbows and the first map'], 'villa_inside.jpg'),
  'card-spire': () => dungeonCard('spire', ['A towering arcane spire, four floors of spawners', 'Zombies, skeletons, spiders and witches',
    'Guarded by the <b class="hi">Spire Illusionist</b>', 'Enchanted gear, pearls and diamonds'], 'spire_inside.jpg', [240, 0, 1440, 810]),
  'card-keep': () => dungeonCard('keep', ['A dark keep with cursed warriors on every floor', 'Named spawner mobs with gear and effects',
    'Guarded by the <b class="hi">Keep Warlord</b>', 'Diamond gear, totems and upgrade templates'], 'keep_inside.jpg'),
  'card-crypt': () => dungeonCard('crypt', ['A deepslate crypt lit by soul fire', 'Wither skeleton and blaze spawners',
    'Guarded by the <b class="hi">Cinder Warden</b>', 'Netherite, wither skulls and enchanted golden apples'], 'crypt_inside.jpg'),
};

const HEADERS = {
  'header-whats-new': 'What’s New in 2.0', 'header-dungeons': 'The Dungeons', 'header-labyrinths': 'The Labyrinths',
  'header-trail': 'The Dungeon Trail',
  'header-guardians': 'Guardians', 'header-loot': 'Loot', 'header-advancements': 'Advancements',
  'header-config': 'For Servers and Modpacks', 'header-compatibility': 'Downloads', 'header-faq': 'FAQ', 'header-gallery': 'Gallery',
};
for (const [name, title] of Object.entries(HEADERS)) {
  assets[name] = () => header(title);
}
assets.divider = divider;

(async () => {
  const wanted = process.argv.slice(2);
  const names = wanted.length ? wanted : Object.keys(assets);
  const browser = await chromium.launch();
  const context = await browser.newContext({ deviceScaleFactor: 1 });
  for (const name of names) {
    if (!assets[name]) {
      console.error('unknown asset', name);
      continue;
    }
    const html = assets[name]();
    const file = path.join(__dirname, `.render-${name}.html`);
    fs.writeFileSync(file, html);
    const p = await context.newPage();
    await p.goto(url(file));
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(200);
    const { width, height } = await p.evaluate(() => ({ width: document.body.scrollWidth, height: document.body.scrollHeight }));
    await p.setViewportSize({ width, height });
    const transparent = name.startsWith('header') || name === 'divider' || name === 'icon';
    await p.screenshot({ path: path.join(out, `${name}.png`), omitBackground: transparent });
    await p.close();
    fs.unlinkSync(file);
    console.log('rendered', name);
  }
  await browser.close();
})();
