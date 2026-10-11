// Prop catalog: procedural builders (origin = floor centre, front = +z). GLBs in /assets override these by type.
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { detailTexture } from './surfaces.js';

export const STYLES = {
  modern:     { wall: '#e9e6df', floor: '#b89f7d', wood: '#8b6b4a', fabric: '#5d6b7a', accent: '#d9822b', metal: '#2b2d31', plant: '#3f7d4a', light: '#fff1d6' },
  scandi:     { wall: '#f3f1ec', floor: '#d9c3a0', wood: '#d8b98a', fabric: '#9fb3bd', accent: '#e0a3a0', metal: '#4a4a4a', plant: '#5c9460', light: '#fff4e0' },
  rustic:     { wall: '#d8c7a8', floor: '#6b4a2f', wood: '#6e4a2c', fabric: '#8a4b3a', accent: '#b7791f', metal: '#2a2522', plant: '#4a6b32', light: '#ffd9a0' },
  industrial: { wall: '#8d9096', floor: '#5a5d62', wood: '#5b4636', fabric: '#3d4a55', accent: '#c0562b', metal: '#1b1c1e', plant: '#3d6b4b', light: '#ffe2b8' },
  gothic:     { wall: '#34343e', floor: '#26262b', wood: '#2a1a12', fabric: '#6e0f1f', accent: '#7a3fb0', metal: '#2b2b30', plant: '#2f4a3a', light: '#ff9d4d', floorPattern: 'stone', pack: 'gothic' },
  scifi:      { wall: '#cfd8e0', floor: '#323a46', wood: '#2a3038', fabric: '#1f7a96', accent: '#e0457b', metal: '#2b2f36', plant: '#2e9b6a', light: '#bfe8ff', floorPattern: 'diamond', pack: 'scifi' },
  luxe:       { wall: '#2e3340', floor: '#3b2f2a', wood: '#2b1d17', fabric: '#7b2d4f', accent: '#d4af37', metal: '#c9a24b', plant: '#2f6b4f', light: '#ffe6b0' },
};

const matCache = new Map();
export function mat(color, { r = 0.7, m = 0, emissive = null } = {}) {
  const k = `${color}|${r}|${m}|${emissive}`;
  if (!matCache.has(k)) {
    const o = { color, roughness: r, metalness: m };
    if (emissive) { o.emissive = emissive; o.emissiveIntensity = 0.9; }
    const mm = new THREE.MeshStandardMaterial(o);
    mm.name = 'm_' + color.replace('#', '') + (emissive ? '_glow' : '');
    matCache.set(k, mm);
  }
  return matCache.get(k);
}
const geoCache = new Map();
function geo(key, make) { if (!geoCache.has(key)) geoCache.set(key, make()); return geoCache.get(key); }

function rng(seed) { let s = 0; for (const c of String(seed)) s = (s * 31 + c.charCodeAt(0)) >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }

// y = bottom of the box
function bx(g, m, w, h, d, x = 0, y = 0, z = 0, name) {
  const me = new THREE.Mesh(geo(`b${w},${h},${d}`, () => new THREE.BoxGeometry(w, h, d)), m);
  me.position.set(x, y + h / 2, z); me.castShadow = me.receiveShadow = true; if (name) me.name = name; g.add(me); return me;
}
function cy(g, m, rt, rb, h, x = 0, y = 0, z = 0, name, seg = 20) {
  const me = new THREE.Mesh(geo(`c${rt},${rb},${h},${seg}`, () => new THREE.CylinderGeometry(rt, rb, h, seg)), m);
  me.position.set(x, y + h / 2, z); me.castShadow = me.receiveShadow = true; if (name) me.name = name; g.add(me); return me;
}
function sp(g, m, r, x, y, z, sx = 1, sy = 1, sz = 1, name) {
  const me = new THREE.Mesh(geo(`s${r}`, () => new THREE.SphereGeometry(r, 14, 10)), m);
  me.position.set(x, y, z); me.scale.set(sx, sy, sz); me.castShadow = true; if (name) me.name = name; g.add(me); return me;
}
const legs4 = (g, m, w, d, h, t = 0.05, inset = 0.05) => {
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) bx(g, m, t, h, t, sx * (w / 2 - inset), 0, sz * (d / 2 - inset), 'leg');
};
const BOOK = ['#8c2f39', '#2f5d8c', '#c9a227', '#3d7a4a', '#e6e1d6', '#5a3d7a', '#d9822b'];

// Each def: label, cat, size [w,d,h], place ('floor'|'wall'|'ceiling'|'surface'), y (mount height), tags, build(c, rnd) -> fills group.
// c = palette colours (c.main overrides the primary material colour).
export const CATALOG = {
  bed: { label: 'Bed', cat: 'sleep', size: [1.7, 2.15, 1.0], place: 'floor', tags: ['bed', 'headwall'], build(g, c) {
    bx(g, mat(c.wood), 1.6, 0.3, 2.1, 0, 0, 0, 'frame'); bx(g, mat('#f2efe8'), 1.5, 0.25, 1.95, 0, 0.3, 0.02, 'mattress');
    bx(g, mat(c.main || c.fabric), 1.52, 0.06, 1.25, 0, 0.5, 0.4, 'blanket');
    for (const s of [-1, 1]) bx(g, mat('#fbfaf6', { r: 0.9 }), 0.62, 0.13, 0.36, s * 0.38, 0.55, -0.78, 'pillow');
    bx(g, mat(c.wood), 1.7, 1.0, 0.08, 0, 0, -1.07, 'headboard'); } },
  nightstand: { label: 'Nightstand', cat: 'storage', size: [0.45, 0.4, 0.5], place: 'floor', tags: ['holds-decor', 'beside'], build(g, c) {
    bx(g, mat(c.main || c.wood), 0.45, 0.5, 0.4, 0, 0, 0, 'body'); bx(g, mat(c.metal, { m: 0.6 }), 0.1, 0.02, 0.02, 0, 0.32, 0.21, 'knob'); bx(g, mat('#3a3a3a'), 0.4, 0.01, 0.01, 0, 0.25, 0.201, 'seam'); } },
  sofa: { label: 'Sofa', cat: 'seating', size: [2.1, 0.95, 0.85], place: 'floor', tags: ['seating', 'faces-center'], build(g, c) {
    const f = mat(c.main || c.fabric, { r: 0.95 }); bx(g, f, 2.1, 0.4, 0.95, 0, 0.1, 0, 'base'); bx(g, f, 2.1, 0.45, 0.25, 0, 0.4, -0.35, 'back');
    for (const s of [-1, 1]) bx(g, f, 0.2, 0.3, 0.95, s * 0.95, 0.4, 0, 'arm');
    for (const s of [-1, 1]) bx(g, mat(c.main || c.fabric, { r: 0.95 }), 0.86, 0.14, 0.7, s * 0.43, 0.5, 0.08, 'cushion');
    legs4(g, mat(c.wood), 2.0, 0.85, 0.1); } },
  armchair: { label: 'Armchair', cat: 'seating', size: [0.85, 0.85, 0.85], place: 'floor', tags: ['seating', 'faces-center'], build(g, c) {
    const f = mat(c.accent, { r: 0.95 }); bx(g, f, 0.85, 0.38, 0.85, 0, 0.1, 0, 'base'); bx(g, f, 0.85, 0.45, 0.2, 0, 0.4, -0.32, 'back');
    for (const s of [-1, 1]) bx(g, f, 0.14, 0.28, 0.85, s * 0.35, 0.4, 0, 'arm'); bx(g, f, 0.55, 0.12, 0.6, 0, 0.48, 0.07, 'cushion'); legs4(g, mat(c.wood), 0.8, 0.8, 0.1); } },
  ottoman: { label: 'Ottoman', cat: 'seating', size: [0.6, 0.6, 0.4], place: 'floor', tags: ['seating'], build(g, c) {
    cy(g, mat(c.accent, { r: 0.95 }), 0.3, 0.3, 0.38, 0, 0.02, 0, 'body'); } },
  coffee_table: { label: 'Coffee table', cat: 'table', size: [1.0, 0.6, 0.42], place: 'floor', tags: ['table', 'holds-decor', 'center'], build(g, c) {
    bx(g, mat(c.main || c.wood), 1.0, 0.05, 0.6, 0, 0.37, 0, 'top'); legs4(g, mat(c.metal, { m: 0.6 }), 1.0, 0.6, 0.37, 0.04, 0.06); } },
  side_table: { label: 'Side table', cat: 'table', size: [0.45, 0.45, 0.55], place: 'floor', tags: ['table', 'holds-decor', 'beside'], build(g, c) {
    cy(g, mat(c.main || c.wood), 0.23, 0.23, 0.04, 0, 0.5, 0, 'top'); cy(g, mat(c.metal, { m: 0.6 }), 0.025, 0.025, 0.5, 0, 0, 0, 'stem'); cy(g, mat(c.metal, { m: 0.6 }), 0.16, 0.16, 0.02, 0, 0, 0, 'foot'); } },
  dining_table: { label: 'Dining table', cat: 'table', size: [1.8, 0.95, 0.75], place: 'floor', tags: ['table', 'holds-decor', 'center'], build(g, c) {
    bx(g, mat(c.main || c.wood), 1.8, 0.05, 0.95, 0, 0.7, 0, 'top'); legs4(g, mat(c.wood), 1.8, 0.95, 0.7, 0.07, 0.07); } },
  dining_chair: { label: 'Dining chair', cat: 'seating', size: [0.45, 0.47, 0.9], place: 'floor', tags: ['seating', 'chair'], build(g, c) {
    bx(g, mat(c.main || c.fabric, { r: 0.9 }), 0.45, 0.05, 0.45, 0, 0.44, 0, 'seat'); legs4(g, mat(c.wood), 0.45, 0.45, 0.44, 0.04, 0.02); bx(g, mat(c.wood), 0.45, 0.4, 0.04, 0, 0.5, -0.215, 'back'); } },
  desk: { label: 'Desk', cat: 'table', size: [1.4, 0.7, 0.75], place: 'floor', tags: ['table', 'holds-decor', 'wall-hug', 'desk'], build(g, c) {
    bx(g, mat(c.main || c.wood), 1.4, 0.04, 0.7, 0, 0.71, 0, 'top'); bx(g, mat(c.wood), 0.4, 0.6, 0.6, 0.45, 0.1, 0, 'drawers'); for (const s of [-1, 1]) bx(g, mat(c.metal, { m: 0.6 }), 0.04, 0.7, 0.04, -0.65, 0, s * 0.3, 'leg'); } },
  office_chair: { label: 'Office chair', cat: 'seating', size: [0.6, 0.6, 1.0], place: 'floor', tags: ['seating', 'chair'], build(g, c) {
    cy(g, mat(c.metal, { m: 0.6 }), 0.28, 0.28, 0.03, 0, 0.05, 0, 'base'); cy(g, mat(c.metal, { m: 0.6 }), 0.03, 0.03, 0.4, 0, 0.05, 0, 'stem');
    bx(g, mat(c.fabric), 0.5, 0.08, 0.5, 0, 0.45, 0, 'seat'); bx(g, mat(c.fabric), 0.46, 0.5, 0.07, 0, 0.5, -0.24, 'back'); } },
  bookshelf: { label: 'Bookshelf', cat: 'storage', size: [0.95, 0.32, 1.9], place: 'floor', tags: ['storage', 'wall-hug', 'holds-decor'], build(g, c, r) {
    const w = mat(c.main || c.wood); for (const s of [-1, 1]) bx(g, w, 0.04, 1.9, 0.32, s * 0.455, 0, 0, 'side'); bx(g, w, 0.95, 1.9, 0.02, 0, 0, -0.15, 'back');
    for (let i = 0; i <= 5; i++) bx(g, w, 0.9, 0.03, 0.32, 0, i * 0.37, 0, 'shelf');
    for (let i = 0; i < 5; i++) { let x = -0.42; while (x < 0.4) { const bw = 0.03 + r() * 0.04; if (r() < 0.2) { x += 0.12; continue; } bx(g, mat(BOOK[(r() * BOOK.length) | 0], { r: 0.8 }), bw, 0.22 + r() * 0.08, 0.2, x + bw / 2, i * 0.37 + 0.03, 0, 'book'); x += bw + 0.002; } } } },
  wardrobe: { label: 'Wardrobe', cat: 'storage', size: [1.3, 0.62, 2.1], place: 'floor', tags: ['storage', 'wall-hug', 'tall'], build(g, c) {
    bx(g, mat(c.main || c.wood), 1.3, 2.1, 0.62, 0, 0, 0, 'body'); for (const s of [-1, 1]) { bx(g, mat(c.wood), 0.62, 2.0, 0.02, s * 0.32, 0.05, 0.315, 'door'); bx(g, mat(c.metal, { m: 0.7 }), 0.02, 0.2, 0.03, s * 0.06, 1.0, 0.33, 'handle'); } } },
  dresser: { label: 'Dresser', cat: 'storage', size: [1.2, 0.46, 0.85], place: 'floor', tags: ['storage', 'wall-hug', 'holds-decor'], build(g, c) {
    bx(g, mat(c.main || c.wood), 1.2, 0.75, 0.46, 0, 0.1, 0, 'body'); legs4(g, mat(c.wood), 1.2, 0.46, 0.1, 0.05, 0.05);
    for (let i = 0; i < 3; i++) { bx(g, mat('#2a2a2a'), 1.1, 0.01, 0.01, 0, 0.3 + i * 0.22, 0.231, 'seam'); bx(g, mat(c.metal, { m: 0.7 }), 0.12, 0.02, 0.03, 0, 0.18 + i * 0.22 + 0.03, 0.245, 'pull'); } } },
  tv_unit: { label: 'TV unit', cat: 'media', size: [1.6, 0.42, 1.1], place: 'floor', tags: ['media', 'wall-hug', 'faces-center', 'focal'], build(g, c) {
    bx(g, mat(c.main || c.wood), 1.6, 0.45, 0.42, 0, 0.05, 0, 'stand'); bx(g, mat('#0c0d10', { r: 0.2, m: 0.3 }), 1.25, 0.7, 0.04, 0, 0.5, -0.05, 'tv'); bx(g, mat(c.metal), 0.3, 0.02, 0.15, 0, 0.5, -0.05, 'tvfoot'); } },
  floor_lamp: { label: 'Floor lamp', cat: 'light', size: [0.38, 0.38, 1.6], place: 'floor', tags: ['light', 'corner', 'glow'], light: 1, build(g, c) {
    cy(g, mat(c.metal, { m: 0.7 }), 0.14, 0.14, 0.03, 0, 0, 0, 'base'); cy(g, mat(c.metal, { m: 0.7 }), 0.012, 0.012, 1.3, 0, 0, 0, 'pole');
    cy(g, mat(c.light, { emissive: c.light }), 0.14, 0.19, 0.3, 0, 1.3, 0, 'shade'); } },
  table_lamp: { label: 'Table lamp', cat: 'light', size: [0.24, 0.24, 0.42], place: 'surface', tags: ['light', 'glow', 'decor'], light: 0.5, build(g, c) {
    cy(g, mat(c.accent, { r: 0.4 }), 0.07, 0.09, 0.2, 0, 0, 0, 'base'); cy(g, mat(c.light, { emissive: c.light }), 0.09, 0.13, 0.2, 0, 0.2, 0, 'shade'); } },
  ceiling_light: { label: 'Pendant light', cat: 'light', size: [0.5, 0.5, 0.45], place: 'ceiling', tags: ['light', 'glow'], light: 1.4, build(g, c) {
    cy(g, mat(c.metal, { m: 0.6 }), 0.008, 0.008, 0.25, 0, 0.2, 0, 'cord'); cy(g, mat(c.light, { emissive: c.light }), 0.1, 0.25, 0.2, 0, 0, 0, 'shade'); } },
  plant: { label: 'Potted plant', cat: 'decor', size: [0.55, 0.55, 1.2], place: 'floor', tags: ['plant', 'corner', 'decor'], build(g, c, r) {
    cy(g, mat('#b5654a', { r: 0.9 }), 0.17, 0.12, 0.3, 0, 0, 0, 'pot'); const lm = mat(c.plant, { r: 0.8 });
    for (let i = 0; i < 9; i++) { const a = r() * 6.28, rad = 0.05 + r() * 0.15; sp(g, lm, 0.16, Math.cos(a) * rad, 0.5 + r() * 0.6, Math.sin(a) * rad, 1, 1.5, 1, 'leaf'); } } },
  plant_small: { label: 'Small plant', cat: 'decor', size: [0.2, 0.2, 0.32], place: 'surface', tags: ['plant', 'decor'], build(g, c, r) {
    cy(g, mat('#e6e1d6', { r: 0.9 }), 0.07, 0.05, 0.1, 0, 0, 0, 'pot'); for (let i = 0; i < 4; i++) sp(g, mat(c.plant), 0.07, (r() - 0.5) * 0.08, 0.17 + r() * 0.1, (r() - 0.5) * 0.08, 1, 1.4, 1, 'leaf'); } },
  vase: { label: 'Vase', cat: 'decor', size: [0.16, 0.16, 0.34], place: 'surface', tags: ['decor'], build(g, c) {
    cy(g, mat(c.accent, { r: 0.3 }), 0.05, 0.08, 0.26, 0, 0, 0, 'body'); cy(g, mat(c.accent, { r: 0.3 }), 0.035, 0.05, 0.08, 0, 0.26, 0, 'neck'); } },
  books: { label: 'Book stack', cat: 'decor', size: [0.26, 0.2, 0.14], place: 'surface', tags: ['decor'], build(g, c, r) {
    let y = 0; for (let i = 0; i < 3; i++) { const h = 0.03 + r() * 0.02; bx(g, mat(BOOK[(r() * BOOK.length) | 0], { r: 0.8 }), 0.24 - i * 0.015, h, 0.17, (r() - 0.5) * 0.02, y, 0, 'book'); y += h; } } },
  rug: { label: 'Rug', cat: 'rug', size: [2.6, 1.8, 0.02], place: 'floor', tags: ['rug', 'flat', 'center'], build(g, c) {
    bx(g, mat(c.main || c.accent, { r: 1 }), 2.6, 0.015, 1.8, 0, 0.001, 0, 'rug'); bx(g, mat('#f1ede4', { r: 1 }), 2.3, 0.017, 1.5, 0, 0.001, 0, 'rug_inner'); bx(g, mat(c.main || c.accent, { r: 1 }), 1.9, 0.019, 1.1, 0, 0.001, 0, 'rug_core'); } },
  painting: { label: 'Painting', cat: 'wallart', size: [0.9, 0.05, 0.65], place: 'wall', y: 1.45, tags: ['wallart', 'decor'], build(g, c, r) {
    bx(g, mat(c.wood), 0.9, 0.65, 0.04, 0, 0, 0, 'frame'); bx(g, mat('#f5f2ea'), 0.8, 0.55, 0.012, 0, 0.05, 0.022, 'mat');
    for (let i = 0; i < 3; i++) bx(g, mat([c.accent, c.fabric, c.plant][i]), 0.2 + r() * 0.3, 0.1 + r() * 0.25, 0.01, (r() - 0.5) * 0.3, 0.12 + r() * 0.15, 0.03, 'art'); } },
  mirror: { label: 'Wall mirror', cat: 'wallart', size: [0.6, 0.05, 1.2], place: 'wall', y: 0.9, tags: ['wallart', 'decor'], build(g, c) {
    bx(g, mat(c.metal, { m: 0.7 }), 0.6, 1.2, 0.04, 0, 0, 0, 'frame'); bx(g, mat('#9fb4bd', { r: 0.2, m: 0.1 }), 0.54, 1.14, 0.01, 0, 0.03, 0.022, 'glass'); } },
  wall_shelf: { label: 'Wall shelf', cat: 'wallart', size: [0.9, 0.2, 0.25], place: 'wall', y: 1.4, tags: ['wallart', 'decor', 'holds-decor'], build(g, c, r) {
    bx(g, mat(c.wood), 0.9, 0.04, 0.2, 0, 0, 0.1, 'board'); for (let i = 0; i < 4; i++) bx(g, mat(BOOK[(r() * BOOK.length) | 0]), 0.04, 0.2, 0.14, -0.3 + i * 0.05, 0.04, 0.1, 'book'); } },
  curtains: { label: 'Curtains', cat: 'wallart', size: [1.8, 0.14, 2.4], place: 'wall', y: 0.05, tags: ['curtain'], build(g, c) {
    const f = mat(c.fabric, { r: 1 }); for (const s of [-1, 1]) for (let i = 0; i < 4; i++) bx(g, f, 0.17, 2.3, 0.1, s * (0.5 + i * 0.12), 0, 0.03 + (i % 2) * 0.03, 'fold'); cy(g, mat(c.metal, { m: 0.7 }), 0.015, 0.015, 1.9, 0, 2.3 - 0.95, 0.03, 'rod').rotation.z = Math.PI / 2; } },
  kitchen_counter: { label: 'Kitchen counter', cat: 'kitchen', size: [1.2, 0.62, 0.92], place: 'floor', tags: ['kitchen', 'wall-hug', 'holds-decor', 'run'], build(g, c) {
    bx(g, mat(c.wood), 1.2, 0.86, 0.6, 0, 0, 0, 'cabinet'); bx(g, mat('#d9d6cf', { r: 0.3 }), 1.22, 0.05, 0.64, 0, 0.86, 0.01, 'top'); bx(g, mat(c.metal, { m: 0.7 }), 0.4, 0.02, 0.02, 0, 0.7, 0.31, 'handle'); } },
  fridge: { label: 'Fridge', cat: 'kitchen', size: [0.72, 0.7, 1.85], place: 'floor', tags: ['kitchen', 'wall-hug', 'tall'], build(g, c) {
    bx(g, mat('#c9ced3', { r: 0.3, m: 0.6 }), 0.72, 1.85, 0.7, 0, 0, 0, 'body'); bx(g, mat('#6b7075'), 0.68, 0.01, 0.01, 0, 1.15, 0.351, 'seam'); for (const y of [1.3, 0.6]) bx(g, mat(c.metal, { m: 0.8 }), 0.03, 0.4, 0.03, 0.28, y, 0.37, 'handle'); } },
  sink_vanity: { label: 'Vanity sink', cat: 'bath', size: [0.8, 0.5, 0.9], place: 'floor', tags: ['bath', 'wall-hug', 'holds-decor'], build(g, c) {
    bx(g, mat(c.wood), 0.8, 0.8, 0.5, 0, 0, 0, 'cabinet'); bx(g, mat('#f5f5f5', { r: 0.2 }), 0.82, 0.05, 0.52, 0, 0.8, 0, 'top'); bx(g, mat('#e8eef2', { r: 0.1 }), 0.4, 0.02, 0.3, 0, 0.84, 0.02, 'basin'); cy(g, mat(c.metal, { m: 0.9 }), 0.012, 0.012, 0.18, 0, 0.85, -0.17, 'tap'); } },
  toilet: { label: 'Toilet', cat: 'bath', size: [0.4, 0.7, 0.8], place: 'floor', tags: ['bath', 'wall-hug'], build(g, c) {
    const p = mat('#f7f7f5', { r: 0.15 }); bx(g, p, 0.38, 0.4, 0.2, 0, 0.0, -0.25, 'tank'); bx(g, p, 0.38, 0.4, 0.5, 0, 0, 0.0, 'bowl'); bx(g, p, 0.4, 0.04, 0.44, 0, 0.4, 0.04, 'seat'); bx(g, p, 0.38, 0.4, 0.2, 0, 0.4, -0.25, 'tankTop'); } },
  bathtub: { label: 'Bathtub', cat: 'bath', size: [1.7, 0.78, 0.58], place: 'floor', tags: ['bath', 'wall-hug', 'long'], build(g, c) {
    bx(g, mat('#f7f7f5', { r: 0.15 }), 1.7, 0.55, 0.78, 0, 0, 0, 'shell'); bx(g, mat('#cfe6f2', { r: 0.05 }), 1.5, 0.02, 0.6, 0, 0.545, 0, 'water'); cy(g, mat(c.metal, { m: 0.9 }), 0.015, 0.015, 0.25, -0.8, 0.55, 0, 'tap'); } },
  bench: { label: 'Bench', cat: 'seating', size: [1.2, 0.4, 0.45], place: 'floor', tags: ['seating', 'wall-hug'], build(g, c) {
    bx(g, mat(c.main || c.wood), 1.2, 0.06, 0.4, 0, 0.39, 0, 'seat'); legs4(g, mat(c.metal, { m: 0.6 }), 1.2, 0.4, 0.39, 0.04, 0.04); } },
};
export const TYPES = Object.keys(CATALOG);

// ---- external GLB assets (assets/**.glb, packs = sub-folders) -----------------
// Entry fields (manifest.json): file, as (base type this is a variant of), label, cat, size [w,d,h], place, y, tags,
// tint (palette key recolouring materials named tint*), light (intensity), lightColor, lightY (m above base), pack.
const ext = new Map();      // asset key -> { scene, entry }
const VARIANTS = {};        // base type -> [asset keys with entry.as]
const REPLACERS = {};       // base type -> [pack-only types with entry.replaces] (e.g. candelabra replaces floor_lamp)
export const PACKS = new Set();
const hashStr = x => { let h = 0; for (const c of String(x)) h = (h * 31 + c.charCodeAt(0)) >>> 0; return h; };
const LIGHT_RE = /candle|torch|sconce|chandelier|lamp|brazier|lantern|flame|fire|cauldron|crystal|orb/i;
const WALL_RE = /sconce|banner|tapestry|painting|mirror|shield|rack|window_deco|plaque/i;
const CEIL_RE = /chandelier|hanging|ceiling|pendant/i;
const SURF_RE = /skull|candle|book|goblet|chalice|crystal|orb|flask|bottle|vase|dagger|scroll|potion|bone_pile/i;
const nice = k => k.replace(/^[a-z0-9]+_/i, m => m).replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
function guessEntry(key, e, sz) {
  const name = key.toLowerCase(), place = CEIL_RE.test(name) ? 'ceiling' : WALL_RE.test(name) ? 'wall' : SURF_RE.test(name) ? 'surface' : 'floor';
  const light = LIGHT_RE.test(name);
  return { label: nice(key.replace(new RegExp('^' + (e.pack || '') + '_'), '')), place, y: place === 'wall' ? 1.6 : undefined,
    tags: [...(place === 'floor' ? ['wall-hug'] : []), ...(light ? ['light', 'glow'] : []), ...(place === 'surface' ? ['decor'] : [])],
    light: light ? 1 : 0, lightColor: light ? '#ff9a3c' : undefined, lightY: Math.round(sz.y * 0.9 * 100) / 100, tint: 'fabric' };
}
export async function loadExternalAssets() {
  let info; try { info = await (await fetch('/api/assets')).json(); } catch { return []; }
  const entries = { ...info.manifest }, listed = new Set(Object.values(entries).map(e => e.file));
  for (const f of info.files) if (!listed.has(f)) { // loose GLB: auto-register (namespaced by pack folder)
    const parts = f.split('/'), pack = parts.length > 1 ? parts[0] : null, base = parts.at(-1).replace(/\.glb$/i, '');
    entries[(pack ? pack + '_' : '') + base] = { file: f, pack, auto: true, bbox: info.looseBBox?.[f] || undefined };
  }
  ext.clear(); PACKS.clear(); for (const k in VARIANTS) delete VARIANTS[k]; for (const k in REPLACERS) delete REPLACERS[k];
  for (const k of Object.keys(CATALOG)) if (CATALOG[k].external) delete CATALOG[k];
  const loader = new GLTFLoader(), loaded = [];
  await Promise.all(Object.entries(entries).map(async ([key, e]) => {
    try {
      let sz, scene = null;
      if (e.bbox) sz = { x: e.bbox[0], z: e.bbox[1], y: e.bbox[2] };       // [w, d, h] from the manifest: no download needed
      else { const gltf = await loader.loadAsync('/assets/' + e.file); scene = gltf.scene; sz = new THREE.Box3().setFromObject(scene).getSize(new THREE.Vector3()); }
      const entry = { ...guessEntry(key, e, sz), ...e };
      ext.set(key, { scene, entry });
      if (entry.pack) PACKS.add(entry.pack);
      if (entry.as) (VARIANTS[entry.as] ||= []).push(key);
      else if (!CATALOG[key]) CATALOG[key] = { external: true, pack: entry.pack, label: entry.label || key, cat: entry.cat || entry.pack || 'decor',
        size: entry.size || [sz.x, sz.z, sz.y].map(v => Math.round(v * 100) / 100), place: entry.place, y: entry.y, tags: entry.tags || [], build() {} };
      if (entry.replaces && CATALOG[key]) (REPLACERS[entry.replaces] ||= []).push(key);
      loaded.push(key);
    } catch (err) { console.warn('asset failed', key, err); }
  }));
  for (const k in VARIANTS) VARIANTS[k].sort();
  return loaded;
}
// GLBs are downloaded on demand: only the assets a level actually uses.
const loading = new Map();
export const neededKeys = props => [...new Set(props.map(assetKeyOf).filter(k => k && ext.get(k).scene === null))];
export function ensureAssets(keys) {
  const loader = new GLTFLoader();
  return Promise.all(keys.map(k => {
    const rec = ext.get(k); if (!rec || rec.scene !== null) return null;
    if (!loading.has(k)) loading.set(k, loader.loadAsync('/assets/' + rec.entry.file).then(g => { rec.scene = g.scene; }).catch(e => { console.warn('asset load failed', k, e); rec.scene = false; }).finally(() => loading.delete(k)));
    return loading.get(k);
  }));
}
export const hasExternal = t => ext.has(t) || (VARIANTS[t] || []).length > 0;
export const listPacks = () => [...PACKS].sort();
export const assetEntry = k => ext.get(k)?.entry;
export function variantFor(base, pack, seed) {
  const c = (VARIANTS[base] || []).filter(k => ext.get(k).entry.pack === pack);
  return c.length ? c[hashStr(seed) % c.length] : null;
}
export function replacementFor(base, pack, seed) {
  const c = (REPLACERS[base] || []).filter(k => CATALOG[k]?.pack === pack).sort();
  return c.length ? c[hashStr(seed) % c.length] : null;
}
export const packTypes = (pack, pred = () => true) => Object.keys(CATALOG).filter(k => CATALOG[k].external && CATALOG[k].pack === pack && pred(CATALOG[k])).sort();
export const assetKeyOf = p => (p.variant && ext.has(p.variant)) ? p.variant : ext.has(p.type) ? p.type : null;
// light emitted by a prop: from asset metadata, else from the procedural definition
export function lightOf(p) {
  const def = CATALOG[p.type], k = assetKeyOf(p), e = k && ext.get(k).entry;
  if (e && e.light) return { i: e.light, color: e.lightColor || null, y: e.lightY ?? def.size[2] * 0.9 };
  if (def?.light && !(e && e.light === 0)) return { i: def.light, color: null, y: def.place === 'ceiling' ? 0.1 : def.size[2] - 0.05 };
  return null;
}

// identical materials (same name/colour/emissive/opacity/maps) across every prop become one shared instance: smaller GLB, fewer GPU state changes
const sharedMats = new Map();
// [material-name pattern, detail map, scale (1/m), strength]
const DETAIL = [[/^wood/, 'detail_wood', 2.0, 0.85], [/^(stone|brick|moss|ash)/, 'detail_stone', 2.2, 0.9], [/^(marble|obsidian)/, 'detail_stone', 1.4, 0.45], [/^(iron|rust|pewter|copper|silver|gold)/, 'detail_metal', 3.0, 0.7],
  [/^(tint_|cloth|burlap|rope)/, 'detail_fabric', 7.0, 0.7], [/^(leather|book_)/, 'detail_leather', 3.5, 0.75], [/^(bone|ivory)/, 'detail_bone', 3.5, 0.7], [/^(parchment|canvas)/, 'detail_paper', 3.0, 0.6]];
// box-mapped detail (object space, so it scales with the prop) + world-space grime (darker low on walls, blotchy dirt) injected into MeshStandardMaterial
function detailize(m) {
  if (m.userData.detailed || m.emissiveIntensity > 0.01 && (m.emissive?.r + m.emissive?.g + m.emissive?.b) > 0.05 || m.transparent) return;
  const d = DETAIL.find(([re]) => re.test(m.name || '')); const grime = detailTexture('detail_grime'); const tex = d && detailTexture(d[1]);
  m.userData.detailed = true; if (!tex || !grime) return;
  m.onBeforeCompile = sh => {
    sh.uniforms.uDetail = { value: tex }; sh.uniforms.uGrime = { value: grime }; sh.uniforms.uDS = { value: d[2] }; sh.uniforms.uDK = { value: d[3] };
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vOP; varying vec3 vON; varying vec3 vWP; varying vec3 vWN;')
      .replace('#include <begin_vertex>', '#include <begin_vertex>\nvOP = position; vON = normal; vWP = (modelMatrix * vec4(position, 1.0)).xyz; vWN = normalize(mat3(modelMatrix) * normal);');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>
varying vec3 vOP; varying vec3 vON; varying vec3 vWP; varying vec3 vWN; uniform sampler2D uDetail; uniform sampler2D uGrime; uniform float uDS; uniform float uDK;
float triS(sampler2D t, vec3 p, vec3 n) { vec3 w = pow(abs(n), vec3(4.0)); w /= (w.x + w.y + w.z + 1e-4); return texture2D(t, p.yz).r * w.x + texture2D(t, p.zx).r * w.y + texture2D(t, p.xy).r * w.z; }`)
      .replace('#include <color_fragment>', `#include <color_fragment>
float dtl = triS(uDetail, vOP * uDS, normalize(vON));
diffuseColor.rgb *= mix(1.0, clamp(dtl * 2.0, 0.2, 1.8), uDK);
float grm = triS(uGrime, vWP * 0.35, normalize(vWN)); float sideF = 1.0 - abs(vWN.y);
diffuseColor.rgb *= mix(1.0, mix(0.55, 1.0, smoothstep(0.0, 0.55, vWP.y)), sideF) * mix(0.72, 1.12, grm);`)
      .replace('#include <roughnessmap_fragment>', '#include <roughnessmap_fragment>\nroughnessFactor = clamp(roughnessFactor * (0.7 + dtl * 0.6), 0.04, 1.0);');
  };
  m.customProgramCacheKey = () => 'ld-detail'; m.needsUpdate = true;
}
function sharedMaterial(m) {
  if (!m || !m.color) return m;
  const k = [m.name, m.color.getHexString(), m.emissive?.getHexString(), m.emissiveIntensity, m.opacity, m.roughness?.toFixed(2), m.metalness?.toFixed(2), m.map?.uuid || '', m.transparent].join('|');
  if (!sharedMats.has(k)) { sharedMats.set(k, m); detailize(m); }
  return sharedMats.get(k);
}

function fitExternal(key, def, p, style) {
  const { scene, entry } = ext.get(key);
  if (!scene) { // not downloaded yet: ghost box of the right footprint
    const gh = new THREE.Mesh(new THREE.BoxGeometry(def.size[0], def.size[2], def.size[1]), new THREE.MeshStandardMaterial({ color: '#666', transparent: true, opacity: 0.25 }));
    gh.position.y = def.size[2] / 2; const w = new THREE.Group(); w.add(gh); return w;
  }
  const obj = scene.clone(true);
  const box = new THREE.Box3().setFromObject(obj), size = box.getSize(new THREE.Vector3()), ctr = box.getCenter(new THREE.Vector3());
  const native = !entry.as && key !== p.type && !entry.size; // pack-only types keep their modelled size
  // floor items fit the footprint (height is free); wall/ceiling items fit all three axes
  const k = native ? 1 : ((def.place === 'floor' || def.place === 'surface' ? Math.min(def.size[0] / size.x, def.size[1] / size.z) : Math.min(def.size[0] / size.x, def.size[1] / size.z, def.size[2] / size.y)) || 1);
  const wrap = new THREE.Group(); obj.scale.setScalar(k);
  obj.position.set(-ctr.x * k, -box.min.y * k, -ctr.z * k); wrap.add(obj);
  const tint = p.color || (entry.tint && (STYLES[style] || STYLES.modern)[entry.tint]);
  wrap.traverse(o => {
    if (!o.isMesh) return; o.castShadow = o.receiveShadow = true;
    if (tint && o.material?.name?.startsWith('tint')) { o.material = o.material.clone(); o.material.color.set(tint); }
    o.material = sharedMaterial(o.material);
  });
  return wrap;
}

export function buildProp(p, style) {
  const def = CATALOG[p.type]; const g = new THREE.Group();
  g.name = `${p.type}_${p.id}`; g.userData = { propId: p.id, type: p.type };
  if (!def) return g;
  const ak = assetKeyOf(p);
  if (ak && ext.get(ak).scene !== false) g.add(fitExternal(ak, def, p, style));
  else if (def.build) def.build(g, { ...STYLES[style] || STYLES.modern, main: p.color || null }, rng(p.id));
  const s = p.scale || 1; g.scale.setScalar(s);
  g.rotation.y = THREE.MathUtils.degToRad(p.rot || 0);
  g.position.set(p.x, p.y || 0, p.z);
  g.traverse(o => { o.userData.propId = p.id; });
  return g;
}
