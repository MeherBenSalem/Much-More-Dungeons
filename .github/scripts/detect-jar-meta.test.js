#!/usr/bin/env node
'use strict';

const assert = require('assert');
const { detect, detectRequired } = require('./detect-jar-meta.js');

const cases = [
  // Current MultiLoader naming
  ['muchmoredungeons-fabric-1.20.1-2.0.0.jar', 'fabric', '1.20.1'],
  ['muchmoredungeons-forge-1.20.1-2.0.0.jar', 'forge', '1.20.1'],
  ['muchmoredungeons-fabric-1.21.1-2.0.0.jar', 'fabric', '1.21.1'],
  ['muchmoredungeons-neoforge-1.21.1-2.0.0.jar', 'neoforge', '1.21.1'],
  ['muchmoredungeons-fabric-26.2-2.0.0.jar', 'fabric', '26.2'],
  ['muchmoredungeons-neoforge-26.2-2.0.0.jar', 'neoforge', '26.2'],
  ['muchmoredungeons-fabric-26.3-2.0.0.jar', 'fabric', '26.3'],
  ['muchmoredungeons-neoforge-26.3-2.0.0.jar', 'neoforge', '26.3'],
  ['releases/muchmoredungeons-neoforge-26.3-2.0.0.jar', 'neoforge', '26.3'],
  // Calendar versions with a patch number
  ['muchmoredungeons-fabric-26.1.2-2.0.0.jar', 'fabric', '26.1.2'],
  ['muchmoredungeons-neoforge-26.1.2-2.0.0.jar', 'neoforge', '26.1.2'],
  // Older names (mod version first)
  ['muchmoredungeons-1.2.0-forge-1.20.1.jar', 'forge', '1.20.1'],
  ['muchmoredungeons-1.2.0-neoforge-1.21.1.jar', 'neoforge', '1.21.1'],
];

let failed = 0;
for (const [name, loader, gv] of cases) {
  const got = detect(name);
  try {
    assert.strictEqual(got.loader, loader, `${name} loader`);
    assert.strictEqual(got.gv, gv, `${name} gv`);
    console.log('ok', name, '->', got);
  } catch (e) {
    failed += 1;
    console.error('FAIL', name, 'got', got, e.message);
  }
}

// Unparseable names must fail instead of falling back to a default Minecraft version.
try {
  detectRequired('muchmoredungeons-fabric-mystery.jar');
  failed += 1;
  console.error('FAIL expected throw for mystery jar');
} catch (e) {
  console.log('ok refuses default fallback:', e.message.split('\n')[0]);
}

if (failed) {
  console.error(`${failed} case(s) failed`);
  process.exit(1);
}
console.log('all detect-jar-meta cases passed');
