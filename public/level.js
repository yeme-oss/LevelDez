// Level model, geometry, analysis and the action ("button") registry. Pure logic - no THREE here.
import { CATALOG, STYLES, variantFor, replacementFor, packTypes, listPacks } from './catalog.js';
import { THEMES, TYPE_THEMES, resolveTheme } from './themes.js';

export const WT = 0.12; // wall thickness
export const WALLS = {
  N: { inward: [0, 1], tan: [1, 0], rot: 0, opp: 'S' },
  S: { inward: [0, -1], tan: [-1, 0], rot: 180, opp: 'N' },
  W: { inward: [1, 0], tan: [0, -1], rot: 90, opp: 'E' },
  E: { inward: [-1, 0], tan: [0, 1], rot: -90, opp: 'W' },
};
export const ROOM_TYPES = ['living', 'bedroom', 'dining', 'kitchen', 'office', 'bathroom', 'hall', 'library', 'laboratory', 'crypt', 'chapel', 'corridor', 'classroom', 'dormitory', 'ritual'];
const rad = d => d * Math.PI / 180;
const deg = r => r * 180 / Math.PI;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const r2 = v => Math.round(v * 100) / 100;

let _n = 1;
export const uid = p => `${p}${(_n++).toString(36)}${Math.random().toString(36).slice(2, 4)}`;
export const newLevel = () => ({ version: 1, meta: { name: 'Untitled level', units: 'm' }, style: 'modern', pack: null, rooms: [], openings: [], props: [] });
export const getRoom = (L, id) => L.rooms.find(r => r.id === id);
export const roomProps = (L, r) => L.props.filter(p => p.room === r.id);
export const roomOpenings = (L, r) => L.openings.filter(o => o.room === r.id);
export const defOf = t => CATALOG[t] || { size: [0.5, 0.5, 0.5], place: 'floor', tags: [], cat: 'decor' };
export const propSize = p => { const s = defOf(p.type).size, k = p.scale || 1; return [s[0] * k, s[1] * k, s[2] * k]; };
export const hasTag = (p, t) => defOf(p.type).tags.includes(t);
export const isFloorBlocker = p => defOf(p.type).place === 'floor' && !hasTag(p, 'flat');

export function addRoom(L, { type = 'living', x = 0, z = 0, w = 5, d = 4, h = 2.8, name } = {}) {
  const r = { id: uid('r'), name: name || `${type[0].toUpperCase() + type.slice(1)} ${L.rooms.length + 1}`, type, x, z, w, d, h, wallColor: null, floorColor: null };
  L.rooms.push(r); return r;
}
export function addOpening(L, room, wall, type = 'door', t = 0, extra = {}) {
  const o = { id: uid('o'), room: room.id, wall, type, t, w: type === 'door' ? 0.95 : 1.4, h: type === 'door' ? 2.1 : 1.2, sill: type === 'door' ? 0 : 0.9, ...extra };
  L.openings.push(o); return o;
}
export function addProp(L, room, type, x, z, rot = 0, extra = {}) {
  if (L.pack && !extra.noSwap && defOf(type).place !== 'floor') type = replacementFor(type, L.pack, type + x + z + _n) || type; // pack stand-ins for lamps, art...
  const def = defOf(type);
  const p = { id: uid('p'), type, room: room.id, x: r2(x), z: r2(z), y: def.place === 'ceiling' ? r2(room.h - def.size[2]) : def.place === 'wall' ? def.y : 0, rot: r2(rot), scale: 1, color: null, ...extra };
  const v = L.pack ? variantFor(type, L.pack, p.id) : null; if (v) p.variant = v;
  delete p.noSwap;
  L.props.push(p); return p;
}
export const removeProp = (L, id) => { L.props = L.props.filter(p => p.id !== id && p.host !== id); };

// ---- wall math --------------------------------------------------------------
export const wallLen = (r, wall) => (wall === 'N' || wall === 'S') ? r.w : r.d;
export function wallBase(r, wall) {
  return wall === 'N' ? [r.x, r.z - r.d / 2] : wall === 'S' ? [r.x, r.z + r.d / 2] : wall === 'W' ? [r.x - r.w / 2, r.z] : [r.x + r.w / 2, r.z];
}
export function wallPoint(r, wall, t, dist = 0) {
  const [bx, bz] = wallBase(r, wall), W = WALLS[wall];
  return [bx + W.tan[0] * t + W.inward[0] * dist, bz + W.tan[1] * t + W.inward[1] * dist];
}
export const faceRot = (fx, fz) => deg(Math.atan2(fx, fz));
export const faceTo = (from, to) => faceRot(to[0] - from[0], to[1] - from[1]);
const loc2w = (rotDeg, lx, lz) => { const a = rad(rotDeg), c = Math.cos(a), s = Math.sin(a); return [lx * c + lz * s, -lx * s + lz * c]; };

// oriented rectangle {cx,cz,hw,hd,rot}
export function rectOf(p) { const [w, d] = propSize(p); return { cx: p.x, cz: p.z, hw: w / 2, hd: d / 2, rot: p.rot || 0 }; }
function corners(R) { return [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([a, b]) => { const [x, z] = loc2w(R.rot, a * R.hw, b * R.hd); return [R.cx + x, R.cz + z]; }); }
export function rectsOverlap(A, B, margin = 0) {
  const axes = [rad(A.rot), rad(B.rot)].flatMap(a => [[Math.cos(a), -Math.sin(a)], [Math.sin(a), Math.cos(a)]]);
  const ca = corners(A), cb = corners(B);
  for (const [ax, az] of axes) {
    const pa = ca.map(c => c[0] * ax + c[1] * az), pb = cb.map(c => c[0] * ax + c[1] * az);
    if (Math.max(...pa) + margin <= Math.min(...pb) || Math.max(...pb) + margin <= Math.min(...pa)) return false;
  }
  return true;
}
const inRoom = (r, R, inset = 0.005) => corners(R).every(([x, z]) => Math.abs(x - r.x) <= r.w / 2 - inset && Math.abs(z - r.z) <= r.d / 2 - inset);

// no-go rectangles: space in front of doors, and in front of windows for tall things
export function zones(L, r) {
  return roomOpenings(L, r).map(o => {
    const [x, z] = wallPoint(r, o.wall, o.t, o.type === 'door' ? 0.7 : 0.32);
    return { R: { cx: x, cz: z, hw: (o.w + (o.type === 'door' ? 0.5 : 0.35)) / 2, hd: o.type === 'door' ? 0.7 : 0.32, rot: WALLS[o.wall].rot }, door: o.type === 'door' };
  });
}
export function placementProblem(L, r, p, ignore = new Set()) {
  const R = rectOf(p), def = defOf(p.type);
  if (!inRoom(r, R)) return 'out-of-bounds';
  if (hasTag(p, 'flat')) return null; // rugs may run under doors
  const tall = def.size[2] * (p.scale || 1) > 0.95;
  for (const z of zones(L, r)) if ((z.door || tall) && rectsOverlap(R, z.R)) return z.door ? 'blocks-door' : 'blocks-window';
  if (hasTag(p, 'flat')) return null;
  for (const q of roomProps(L, r)) {
    if (q.id === p.id || ignore.has(q.id) || !isFloorBlocker(q)) continue;
    if (rectsOverlap(R, rectOf(q), 0.02)) return 'collides:' + q.type;
  }
  return null;
}
// place only when valid; returns prop or null
export function tryPlace(L, r, type, x, z, rot, extra = {}) {
  const sub = L.pack && !extra.noSwap && defOf(type).place === 'floor' ? replacementFor(type, L.pack, type + x + z + _n) : null;
  for (const t of sub ? [sub, type] : [type]) {
    const p = addProp(L, r, t, x, z, rot, extra);
    if (defOf(t).place === 'floor' && placementProblem(L, r, p)) { L.props.pop(); continue; }
    return p;
  }
  return null;
}

// ---- spot search ------------------------------------------------------------
// positions where an item of `type` can sit flush against `wall`, ordered by distance from t0
export function wallSpots(L, r, wall, type, t0 = 0, scale = 1) {
  const def = defOf(type), W = WALLS[wall], len = wallLen(r, wall), hw = def.size[0] * scale / 2, dep = def.size[1] * scale / 2 + 0.02;
  const out = []; for (let t = -len / 2 + hw + 0.05; t <= len / 2 - hw - 0.05; t += 0.1) out.push(t);
  out.sort((a, b) => Math.abs(a - t0) - Math.abs(b - t0));
  return out.map(t => { const [x, z] = wallPoint(r, wall, t, dep); return { x, z, rot: W.rot, wall, t }; });
}
export function putOnWall(L, r, type, wall, t0 = 0, extra = {}) {
  const order = [wall, ...wallsByFreeLength(L, r).filter(w => w !== wall)]; // fall back to the other walls
  for (const w of order) for (const s of wallSpots(L, r, w, type, w === wall ? t0 : 0, extra.scale || 1)) { const p = tryPlace(L, r, type, s.x, s.z, s.rot, extra); if (p) return p; }
  return null;
}
export function wallsByFreeLength(L, r) {
  return Object.keys(WALLS).map(w => ({ w, free: wallLen(r, w) - roomOpenings(L, r).filter(o => o.wall === w).reduce((a, o) => a + o.w + 0.6, 0) - roomProps(L, r).filter(p => isFloorBlocker(p) && wallDist(r, p) < 0.15 && nearestWall(r, p) === w).reduce((a, p) => a + propSize(p)[0], 0) }))
    .sort((a, b) => b.free - a.free).map(o => o.w);
}
export function nearestWall(r, p) {
  const ds = { N: p.z - (r.z - r.d / 2), S: r.z + r.d / 2 - p.z, W: p.x - (r.x - r.w / 2), E: r.x + r.w / 2 - p.x };
  return Object.keys(ds).sort((a, b) => ds[a] - ds[b])[0];
}
function wallDist(r, p) { const [w, d] = propSize(p); const ext = Math.max(Math.abs(Math.cos(rad(p.rot))) * 0 + Math.max(w, d) / 2, 0); const W = nearestWall(r, p); const dd = { N: p.z - (r.z - r.d / 2), S: r.z + r.d / 2 - p.z, W: p.x - (r.x - r.w / 2), E: r.x + r.w / 2 - p.x }[W]; return dd - Math.min(w, d) / 2 - 0.02 + (ext * 0); }
// best free spot for an item anywhere (wall-hugging types -> along walls; others -> interior grid); spreads items out
export function findFreeSpot(L, r, type, { preferWall = null } = {}) {
  const def = defOf(type), hug = preferWall ?? def.tags.includes('wall-hug'), cands = [];
  const others = roomProps(L, r).filter(isFloorBlocker);
  const score = (x, z) => Math.min(2, ...others.map(q => Math.hypot(q.x - x, q.z - z)), 2);
  const test = (x, z, rot) => { const p = { id: '_t', type, room: r.id, x, z, rot, scale: 1, y: 0 }; return !placementProblem(L, r, p); };
  if (hug) for (const w of Object.keys(WALLS)) for (const s of wallSpots(L, r, w, type, 0).filter((_, i) => i % 4 === 0)) { if (test(s.x, s.z, s.rot)) cands.push({ ...s, s: score(s.x, s.z) }); }
  else for (let x = r.x - r.w / 2 + 0.4; x < r.x + r.w / 2 - 0.3; x += 0.3) for (let z = r.z - r.d / 2 + 0.4; z < r.z + r.d / 2 - 0.3; z += 0.3) {
    const rot = defOf(type).tags.includes('faces-center') ? faceTo([x, z], [r.x, r.z]) : 0; if (test(x, z, rot)) cands.push({ x, z, rot, s: score(x, z) });
  }
  cands.sort((a, b) => b.s - a.s); return cands[0] || null;
}

// ---- analysis ---------------------------------------------------------------
const TOP = { tv_unit: 0.5, bookshelf: 1.9 };
export const topY = p => (TOP[p.type] ?? defOf(p.type).size[2]) * (p.scale || 1);
export function analyze(L, r) {
  const props = roomProps(L, r), floor = props.filter(isFloorBlocker), area = r.w * r.d;
  const counts = {}, cats = {}; props.forEach(p => { counts[p.type] = (counts[p.type] || 0) + 1; const c = defOf(p.type).cat; cats[c] = (cats[c] || 0) + 1; });
  const fp = floor.reduce((a, p) => a + propSize(p)[0] * propSize(p)[1], 0);
  const problems = props.map(p => ({ p, why: defOf(p.type).place === 'floor' ? placementProblem(L, r, p) : null })).filter(x => x.why);
  const hostIds = new Set(props.filter(p => p.host).map(p => p.host));
  const hosts = props.filter(p => hasTag(p, 'holds-decor') && defOf(p.type).place === 'floor');
  const ops = roomOpenings(L, r), windows = ops.filter(o => o.type === 'window');
  const curtained = windows.filter(w => props.some(p => hasTag(p, 'curtain') && Math.hypot(...[p.x, p.z].map((v, i) => v - wallPoint(r, w.wall, w.t)[i])) < 0.8));
  const corners = [['N', 'W'], ['N', 'E'], ['S', 'W'], ['S', 'E']].map(([a, b]) => {
    const sx = b === 'W' ? -1 : 1, sz = a === 'N' ? -1 : 1, x = r.x + sx * (r.w / 2 - 0.4), z = r.z + sz * (r.d / 2 - 0.4);
    const R = { cx: x, cz: z, hw: 0.3, hd: 0.3, rot: 0 };
    return { name: a + b, x, z, free: !floor.some(q => rectsOverlap(R, rectOf(q))) && !zones(L, r).some(zn => rectsOverlap(R, zn.R)) };
  });
  // largest free square (0.25m grid)
  const N = 0.25, nx = Math.floor(r.w / N), nz = Math.floor(r.d / N), occ = [];
  for (let i = 0; i < nx; i++) { occ[i] = []; for (let j = 0; j < nz; j++) { const R = { cx: r.x - r.w / 2 + (i + .5) * N, cz: r.z - r.d / 2 + (j + .5) * N, hw: N / 2, hd: N / 2, rot: 0 }; occ[i][j] = floor.some(q => rectsOverlap(R, rectOf(q))); } }
  let best = 0; for (let i = 0; i < nx; i++) for (let j = 0; j < nz; j++) { let s = 0; outer: while (i + s < nx && j + s < nz) { for (let a = 0; a <= s; a++) if (occ[i + s][j + a] || occ[i + a][j + s]) break outer; s++; } best = Math.max(best, s); }
  const wallArt = props.filter(p => defOf(p.type).place === 'wall' && !hasTag(p, 'curtain') && !hasTag(p, 'light')).length;
  const lights = props.filter(p => defOf(p.type).cat === 'light' || hasTag(p, 'light')).length;
  const plants = props.filter(p => hasTag(p, 'plant')).length;
  const decor = props.filter(p => p.host).length;
  const arch = props.filter(p => hasTag(p, 'arch')).length, clutter = props.filter(p => hasTag(p, 'decor') && defOf(p.type).place === 'floor').length;
  const wallSpan = Object.keys(WALLS).reduce((a, w) => a + wallLen(r, w), 0);
  const f = {
    area: r2(area), fill: r2(fp / area), counts, cats, problems, collisions: problems.filter(x => x.why.startsWith('collides') || x.why === 'out-of-bounds').length, doorBlocked: problems.filter(x => x.why === 'blocks-door').length,
    hasRug: !!counts.rug, lights, plants, wallArt, decor, hostsBare: hosts.filter(h => !hostIds.has(h.id)).length, windows: windows.length, windowsBare: windows.length - curtained.length,
    freeCorners: corners.filter(c => c.free), corners, freeSquare: r2(best * N), seating: (cats.seating || 0), hasBed: !!counts.bed, nightstands: counts.nightstand || 0, beds: counts.bed || 0,
    arch, clutter, packActive: !!L.pack,
    composed: 0,
    wallArtTarget: Math.max(1, Math.round(wallSpan / 6)), furnishedItems: floor.length, doors: ops.filter(o => o.type === 'door').length,
  };
  f.composed = r.composed || 0; f.score = score(f); return f;
}
export function score(f) {
  let s = 0; const fillPts = 1 - Math.min(1, Math.abs(f.fill - 0.24) / 0.24); s += fillPts * 30;
  s += Math.min(1, Object.keys(f.cats).length / 6) * 15 + (f.hasRug ? 10 : 0) + Math.min(1, f.lights / Math.max(1, Math.round(f.area / 10))) * 10;
  s += Math.min(1, f.wallArt / f.wallArtTarget) * 10 + Math.min(1, f.plants / Math.max(1, Math.round(f.area / 12))) * 10 + Math.min(1, f.decor / Math.max(2, f.furnishedItems / 2)) * 15;
  if (f.packActive) s += Math.min(1, f.arch / Math.max(3, f.area / 5)) * 10 + Math.min(1, f.clutter / Math.max(2, f.area / 7)) * 5;
  s -= f.collisions * 8 + f.doorBlocked * 10 + f.windowsBare * 2; return Math.round(clamp(s, 0, 100));
}
// compact record handed to Decision-1 as `state`
export function describe(L, r) {
  const f = analyze(L, r);
  return { room: `${r.name} (${r.type}, ${r.w}x${r.d} m, ceiling ${r.h} m)`, style: L.style, furniture: f.counts, floor_coverage_percent: Math.round(f.fill * 100), largest_free_floor_square_m: f.freeSquare,
    has_rug: f.hasRug, light_sources: f.lights, wall_art: f.wallArt, plants: f.plants, decor_items_on_surfaces: f.decor, bare_surfaces: f.hostsBare, windows: f.windows, windows_without_curtains: f.windowsBare,
    free_corners: f.freeCorners.map(c => c.name), overlapping_or_blocking_items: f.problems.map(x => `${x.p.type}: ${x.why}`), doors: f.doors, richness_score_0_100: f.score,
    asset_pack: L.pack || 'none', gothic_architecture_pieces: f.arch, floor_clutter_items: f.clutter };
}

// ---- actions ---------------------------------------------------------------
const pick = (arr, rnd) => arr[Math.floor(rnd() * arr.length)];
const near = (p, a, b, d) => Math.hypot(p.x - a, p.z - b) < d;
const out = (msg, n = 1) => ({ msg, n });


// ---- asset-pack helpers: pack-only types feed the fill/decor/art/light buttons ------------------
const packPool = (L, pred) => L.pack ? packTypes(L.pack, pred) : [];
const withPack = (L, pred, prob, rnd) => { const ex = packPool(L, pred); return ex.length && rnd() < prob ? pick(ex, rnd) : null; };
const isFloorItem = d => d.place === 'floor' && !d.tags.includes('flat') && !d.tags.includes('arch');
export function reskinLevel(L) {
  let n = 0;
  for (const p of L.props) { const v = L.pack ? variantFor(p.type, L.pack, p.id) : null; if ((v || null) !== (p.variant || null)) { if (v) p.variant = v; else delete p.variant; n++; } }
  return n;
}
function hangAt(L, r, type, wall, t) {
  const d = defOf(type), len = wallLen(r, wall); if (Math.abs(t) > len / 2 - d.size[0] / 2 - 0.1) return null;
  const tOf = a => (a.x - r.x) * WALLS[wall].tan[0] + (a.z - r.z) * WALLS[wall].tan[1];
  if (roomProps(L, r).some(a => defOf(a.type).place === 'wall' && nearestWall(r, a) === wall && Math.abs(tOf(a) - t) < (d.size[0] + propSize(a)[0]) / 2 + 0.2)) return null;
  if (roomOpenings(L, r).some(o => o.wall === wall && Math.abs(o.t - t) < (o.w + d.size[0]) / 2 + 0.15)) return null;
  const [x, z] = wallPoint(r, wall, t, d.size[1] / 2 + 0.005); return addProp(L, r, type, x, z, WALLS[wall].rot);
}
function packFloor(L, r, rnd, n, pred = () => true) {
  let c = 0; const pool = packPool(L, d => isFloorItem(d) && pred(d)); if (!pool.length) return 0;
  for (let i = 0; i < n; i++) { const t = pick(pool, rnd), s = findFreeSpot(L, r, t); if (s && tryPlace(L, r, t, s.x, s.z, s.rot)) c++; }
  return c;
}
function furnishLibrary(L, r, rnd) {
  let n = 0;
  for (const w of wallsByFreeLength(L, r)) { const len = wallLen(r, w); for (let t = -len / 2 + 0.55; t < len / 2 - 0.45; t += 1.0) if (tryPlace(L, r, 'bookshelf', ...wallPoint(r, w, t, 0.18), WALLS[w].rot)) n++; }
  const s = findFreeSpot(L, r, 'desk', { preferWall: false }); if (s && tryPlace(L, r, 'desk', s.x, s.z, 0)) n++;
  const a = findFreeSpot(L, r, 'armchair'); if (a && tryPlace(L, r, 'armchair', a.x, a.z, a.rot)) n++;
  return n;
}
function furnishLab(L, r, rnd) {
  let n = 0; const ws = wallsByFreeLength(L, r);
  if (tryPlace(L, r, 'dining_table', r.x, r.z, r.w >= r.d ? 0 : 90)) n++;
  if (putOnWall(L, r, 'desk', ws[0])) n++;
  if (putOnWall(L, r, 'bookshelf', ws[1] || ws[0])) n++;
  return n + packFloor(L, r, rnd, 3);
}
function furnishCrypt(L, r, rnd) { const n = packFloor(L, r, rnd, Math.max(3, Math.round(r.w * r.d / 6))); return n || furnishHall(L, r); }
function furnishChapel(L, r, rnd) {
  let n = 0; const altar = packTypes(L.pack || '', d => d.tags.includes('altar'))[0] || null;
  if (altar && putOnWall(L, r, altar, 'N', 0)) n++;
  const rows = Math.max(1, Math.floor((r.d - 3.2) / 1.1)), cols = r.w >= 5 ? [-1.2, 1.2] : [0];
  for (let i = 0; i < rows; i++) for (const cx of cols) if (tryPlace(L, r, 'bench', r.x + cx, r.z - r.d / 2 + 2.6 + i * 1.1, 180)) n++;
  return n + (n ? 0 : packFloor(L, r, rnd, 3));
}

function furnishLiving(L, r, rnd) {
  const tv = putOnWall(L, r, 'tv_unit', wallsByFreeLength(L, r)[0]); if (!tv) return 0; let n = 1; const tvW = nearestWall(r, tv);
  const W = WALLS[tvW], opp = WALLS[W.opp], ext = (tvW === 'N' || tvW === 'S') ? r.d : r.w;
  for (const f of [0.66, 0.58, 0.5]) {
    const d = ext * f; const [sx, sz] = wallPoint(r, tvW, 0, d); const sofa = tryPlace(L, r, 'sofa', sx, sz, opp.rot);
    if (sofa) { n++; const [cx, cz] = wallPoint(r, tvW, 0, d * 0.5 + 0.1); if (tryPlace(L, r, 'coffee_table', cx, cz, opp.rot)) n++; break; }
  }
  const side = WALLS[tvW].tan; const ar = tryPlace(L, r, 'armchair', ...wallPoint(r, tvW, (tvW === 'N' || tvW === 'S' ? r.w : r.d) * 0.32, ext * 0.42), 0) ;
  if (ar) { ar.rot = r2(faceTo([ar.x, ar.z], [r.x, r.z])); if (placementProblem(L, r, ar)) removeProp(L, ar.id); else n++; }
  const sh = wallsByFreeLength(L, r).find(w => w !== tvW); if (sh && putOnWall(L, r, 'bookshelf', sh, 0)) n++;
  return n;
}
function furnishBedroom(L, r) {
  const ws = wallsByFreeLength(L, r); let n = 0;
  if (putOnWall(L, r, 'bed', ws[0])) n++; else return 0;
  if (ws[1] && putOnWall(L, r, 'wardrobe', ws[1], 0.5)) n++;
  const w3 = ws.find(w => w !== ws[0]); if (w3 && putOnWall(L, r, 'dresser', w3, -0.6)) n++;
  return n;
}
function furnishDining(L, r) {
  const along = r.w >= r.d ? 0 : 90, tbl = tryPlace(L, r, 'dining_table', r.x, r.z, along); if (!tbl) return 0; let n = 1;
  const L2 = 0.95; // chairs on both long sides + ends
  for (const [lx, lz] of [[-.5, -.8], [.5, -.8], [-.5, .8], [.5, .8], [-1.22, 0], [1.22, 0]]) {
    const [wx, wz] = loc2w(along, lx, lz); const rot = faceTo([r.x + wx, r.z + wz], [r.x, r.z]); if (tryPlace(L, r, 'dining_chair', r.x + wx, r.z + wz, rot)) n++;
  }
  const w = wallsByFreeLength(L, r)[0]; if (w && putOnWall(L, r, 'dresser', w)) n++;
  return n;
}
function furnishKitchen(L, r) {
  const ws = wallsByFreeLength(L, r); let n = 0, w = ws[0], len = wallLen(r, w);
  for (let t = -len / 2 + 0.65; t < len / 2 - 1.5; t += 1.22) { if (tryPlace(L, r, 'kitchen_counter', ...wallPoint(r, w, t, 0.33), WALLS[w].rot)) n++; }
  if (tryPlace(L, r, 'fridge', ...wallPoint(r, w, len / 2 - 0.4, 0.37), WALLS[w].rot)) n++;
  const w2 = ws[1]; if (w2) for (let t = -wallLen(r, w2) / 2 + 0.9; t < wallLen(r, w2) / 2 - 0.9; t += 1.22) if (tryPlace(L, r, 'kitchen_counter', ...wallPoint(r, w2, t, 0.33), WALLS[w2].rot)) n++;
  return n;
}
function furnishOffice(L, r) {
  const ws = wallsByFreeLength(L, r); const d = putOnWall(L, r, 'desk', ws[0]); if (!d) return 0; let n = 1;
  const opp = WALLS[WALLS[nearestWall(r, d)].opp]; if (tryPlace(L, r, 'office_chair', ...loc2w(d.rot, -0.1, 0.8).map((v, i) => v + [d.x, d.z][i]), d.rot + 180 + 15)) n++;
  for (const w of ws.slice(1, 3)) if (putOnWall(L, r, 'bookshelf', w)) n++;
  return n;
}
function furnishBath(L, r) {
  const ws = wallsByFreeLength(L, r); let n = 0;
  if (putOnWall(L, r, 'bathtub', ws[0], 0)) n++;
  const v = ws.slice(1).find(w => putOnWall(L, r, 'sink_vanity', w, -0.4)); if (v) { n++; }
  if (ws.slice(1).find(w => putOnWall(L, r, 'toilet', w, 0.6))) n++;
  return n;
}
function furnishCorridor(L, r, rnd) {
  const longWalls = r.w >= r.d ? ['N', 'S'] : ['W', 'E'], len = Math.max(r.w, r.d); let n = 0;
  const pool = L.pack ? packPool(L, d => d.place === 'floor' && !d.tags.includes('flat') && !d.tags.includes('arch') && (d.tags.includes('decor') || d.tags.includes('light') || d.tags.includes('seating')) && d.size[0] <= 1.3) : ['bench', 'plant'];
  longWalls.forEach((w, wi) => { for (let t = -len / 2 + 1.4 + wi * 1.2; t < len / 2 - 1.0; t += 2.6 + rnd() * 1.4) {
    const type = pick(pool, rnd); for (const sp of wallSpots(L, r, w, type, t).slice(0, 8)) { if (Math.abs(sp.t - t) > 0.9) break; if (tryPlace(L, r, type, sp.x, sp.z, sp.rot)) { n++; break; } } } });
  return n;
}
function furnishHall(L, r) { return putOnWall(L, r, 'bench', wallsByFreeLength(L, r)[0]) ? 1 : 0; }

const FILL = {
  living: ['armchair', 'side_table', 'ottoman', 'bookshelf', 'bench'], bedroom: ['bench', 'armchair', 'dresser', 'side_table'], dining: ['dresser', 'bench', 'side_table'],
  kitchen: ['kitchen_counter', 'bench'], office: ['bookshelf', 'armchair', 'side_table'], bathroom: ['bench'], hall: ['bench', 'side_table', 'dresser'],
  library: ['bookshelf', 'armchair', 'side_table', 'desk'], laboratory: ['bookshelf', 'side_table', 'desk'], crypt: ['bench', 'side_table'], chapel: ['bench', 'side_table'], corridor: ['bench', 'plant'], classroom: ['bookshelf', 'side_table'], dormitory: ['side_table', 'bench'], ritual: ['side_table', 'bench'],
};
const DECOR_FOR = {
  nightstand: ['table_lamp', 'books'], coffee_table: ['books', 'vase', 'plant_small'], side_table: ['table_lamp', 'plant_small', 'vase'], dining_table: ['vase'], desk: ['table_lamp', 'books', 'plant_small'],
  dresser: ['vase', 'plant_small', 'table_lamp'], kitchen_counter: ['plant_small', 'vase'], tv_unit: ['vase', 'plant_small'], sink_vanity: ['plant_small', 'vase'], bookshelf: ['plant_small'],
};
const ART_FOR = { sofa: 'painting', bed: 'painting', desk: 'wall_shelf', dresser: 'mirror', sink_vanity: 'mirror', tv_unit: null, bench: 'mirror', dining_table: null };

const roomsOf = (ctx) => ctx.room ? [ctx.room] : ctx.level.rooms;
function each(ctx, fn) { let msgs = [], n = 0; for (const r of roomsOf(ctx)) { const o = fn(r, analyze(ctx.level, r)); if (o && o.n) { n += o.n; msgs.push(`${r.name}: ${o.msg}`); } } return { n, msg: msgs.join('; ') || 'nothing to do' }; }

export const ACTIONS = [
  { id: 'furnish_core', group: 'Layout', label: 'Furnish core', desc: 'Place the essential furniture for the room type', keywords: ['furnish', 'fill', 'populate', 'set up', 'equip'],
    run: ctx => each(ctx, (r, f) => { if (f.furnishedItems) return null; const fn = { living: furnishLiving, bedroom: furnishBedroom, dining: furnishDining, kitchen: furnishKitchen, office: furnishOffice, bathroom: furnishBath, hall: furnishHall, library: furnishLibrary, laboratory: furnishLab, crypt: furnishCrypt, chapel: furnishChapel, corridor: furnishCorridor, classroom: furnishKits, dormitory: furnishKits, ritual: furnishKits }[r.type] || furnishHall; const n = fn(ctx.level, r, ctx.rnd); return { n, msg: `placed ${n} core pieces` }; }) },
  { id: 'compose_room', group: 'Layout', label: 'Compose room', desc: 'Add cohesive themed setups (reading nook, altar arrangement, workbench group, crypt row, lounge, bed suite...) so the room feels designed',
    keywords: ['compose', 'setup', 'arrangement', 'nook', 'cohesive', 'themed', 'richer', 'denser', 'more furniture', 'fuller', 'less empty', 'populate'],
    run: ctx => each(ctx, r => { const n = composeRoom(ctx.level, r, ctx.rnd); return { n, msg: `${n} pieces in ${r.composed || 0} setups` }; }) },
  { id: 'fill_empty', group: 'Layout', label: 'Fill empty space', desc: 'Add secondary furniture where the floor is bare', keywords: ['empty', 'sparse', 'bare', 'more furniture', 'fuller'],
    run: ctx => each(ctx, (r, f) => { let n = 0; const pool = FILL[r.type] || FILL.hall; for (let i = 0; i < 2; i++) { const t = withPack(ctx.level, isFloorItem, 0.65, ctx.rnd) || pick(pool, ctx.rnd), s = findFreeSpot(ctx.level, r, t); if (s && tryPlace(ctx.level, r, t, s.x, s.z, s.rot)) n++; } return { n, msg: `added ${n} pieces` }; }) },
  { id: 'declutter', group: 'Layout', label: 'Declutter', desc: 'Remove the least important items from a crowded room', keywords: ['declutter', 'cramped', 'crowded', 'too much', 'remove clutter', 'tidy', 'less'],
    run: ctx => each(ctx, (r) => { const order = ['books', 'vase', 'plant_small', 'ottoman', 'bench', 'side_table', 'armchair', 'plant']; let n = 0; for (const t of order) { const p = ctx.level.props.find(q => q.room === r.id && q.type === t); if (p && n < 3) { removeProp(ctx.level, p.id); n++; } } return { n, msg: `removed ${n} items` }; }) },
  { id: 'fix_problems', group: 'Layout', label: 'Fix overlaps', desc: 'Relocate or remove items that collide, stick out of the room, or block doors', keywords: ['overlap', 'collide', 'clipping', 'blocking', 'fix', 'stuck', 'intersect'],
    run: ctx => each(ctx, (r, f) => { let n = 0; for (const { p } of f.problems) { const s = findFreeSpot(ctx.level, r, p.type, { preferWall: hasTag(p, 'wall-hug') }); if (s) { p.x = r2(s.x); p.z = r2(s.z); p.rot = r2(s.rot); n++; } else { removeProp(ctx.level, p.id); n++; } } return { n, msg: `resolved ${n} problems` }; }) },
  { id: 'snap_walls', group: 'Layout', label: 'Snap to walls', desc: 'Push wall-type furniture flush against the nearest wall', keywords: ['snap', 'wall', 'flush', 'against the wall', 'align'],
    run: ctx => each(ctx, r => { let n = 0; for (const p of roomProps(ctx.level, r).filter(p => hasTag(p, 'wall-hug') && defOf(p.type).place === 'floor')) { const w = nearestWall(r, p), len = wallLen(r, w); const t = clamp(((p.x - r.x) * WALLS[w].tan[0] + (p.z - r.z) * WALLS[w].tan[1]), -len / 2, len / 2); const [x, z] = wallPoint(r, w, t, propSize(p)[1] / 2 + 0.02); const old = [p.x, p.z, p.rot]; p.x = r2(x); p.z = r2(z); p.rot = WALLS[w].rot; if (placementProblem(ctx.level, r, p)) [p.x, p.z, p.rot] = old; else n++; } return { n, msg: `snapped ${n}` }; }) },
  { id: 'face_focus', group: 'Layout', label: 'Face seating', desc: 'Rotate seating toward the TV or the room centre', keywords: ['face', 'rotate', 'orient', 'toward', 'turn'],
    run: ctx => each(ctx, r => { const tv = roomProps(ctx.level, r).find(p => p.type === 'tv_unit'), tgt = tv ? [tv.x, tv.z] : [r.x, r.z]; let n = 0; for (const p of roomProps(ctx.level, r).filter(p => hasTag(p, 'faces-center') && p.type !== 'tv_unit')) { const old = p.rot; p.rot = r2(faceTo([p.x, p.z], tgt)); if (placementProblem(ctx.level, r, p)) p.rot = old; else n++; } return { n, msg: `oriented ${n}` }; }) },
  { id: 'add_rug', group: 'Furnish', label: 'Add rug', desc: 'Anchor the seating or bed area with a rug', keywords: ['rug', 'carpet', 'cozy', 'cosy', 'warm', 'soft'],
    run: ctx => each(ctx, (r, f) => {
      if (f.hasRug) return null; const ps = roomProps(ctx.level, r);
      if (r.type === 'corridor') { const sc = clamp((Math.min(r.w, r.d) - 0.55) / 1.8, 0.4, 1.2); addProp(ctx.level, r, 'rug', r.x, r.z, r.w >= r.d ? 0 : 90, { scale: r2(sc) }); return { n: 1, msg: 'runner rug added' }; } const anchor = ps.find(p => p.type === 'bed') || ps.find(p => p.type === 'coffee_table') || ps.find(p => p.type === 'dining_table') || ps.find(p => p.type === 'desk');
      let x = r.x, z = r.z, rot = 0, sc = 1; if (anchor) { x = anchor.x; z = anchor.z; rot = anchor.rot; const [w, d] = propSize(anchor); sc = clamp(Math.max((w + 1.2) / 2.6, (d + 1.2) / 1.8), 0.7, 1.6);
        if (anchor.type === 'bed') { [x, z] = loc2w(rot, 0, 0.6).map((v, i) => v + [anchor.x, anchor.z][i]); } }
      sc = Math.min(sc, (r.w - 0.5) / 2.6, (r.d - 0.5) / 1.8); const p = addProp(ctx.level, r, 'rug', x, z, rot, { scale: r2(sc), color: null }); return { n: 1, msg: 'rug added' }; }) },
  { id: 'add_nightstands', group: 'Furnish', label: 'Bedside tables', desc: 'Flank every bed with nightstands', keywords: ['nightstand', 'bedside', 'bed table'],
    run: ctx => each(ctx, r => { let n = 0; for (const b of roomProps(ctx.level, r).filter(p => p.type === 'bed')) for (const s of [-1, 1]) { const [wx, wz] = loc2w(b.rot, s * (propSize(b)[0] / 2 + 0.26), -propSize(b)[1] / 2 + 0.3); const x = b.x + wx, z = b.z + wz; if (roomProps(ctx.level, r).some(p => p.type === 'nightstand' && near(p, x, z, 0.3))) continue; if (tryPlace(ctx.level, r, 'nightstand', x, z, b.rot)) n++; } return { n, msg: `added ${n} nightstands` }; }) },
  { id: 'add_decor', group: 'Furnish', label: 'Style surfaces', desc: 'Put lamps, books, vases and small plants on bare surfaces', keywords: ['decor', 'decorate', 'accessor', 'knick', 'vase', 'books', 'lived-in', 'details', 'surface'],
    run: ctx => each(ctx, r => { let n = 0; const ps = roomProps(ctx.level, r); const hosted = new Set(ps.filter(p => p.host).map(p => p.host));
      for (const h of ps.filter(p => hasTag(p, 'holds-decor') && defOf(p.type).place === 'floor' && !hosted.has(p.id))) { const pool = DECOR_FOR[h.type] || ['vase']; const cnt = h.type === 'bookshelf' || h.type === 'dining_table' ? 1 : 2;
        const [hw, hd] = propSize(h); for (let i = 0; i < cnt; i++) { const t = withPack(ctx.level, d => d.place === 'surface', 0.85, ctx.rnd) || pool[(i + Math.floor(ctx.rnd() * pool.length)) % pool.length]; const lx = cnt === 1 ? 0 : (i ? 1 : -1) * Math.min(hw * 0.28, 0.35), lz = h.type === 'tv_unit' ? 0.02 : 0; const [wx, wz] = loc2w(h.rot, lx, lz);
          addProp(ctx.level, r, t, h.x + wx, h.z + wz, h.rot + (ctx.rnd() - 0.5) * 40, { y: r2(topY(h)), host: h.id }); n++; } }
      return { n, msg: `${n} decor pieces` }; }) },
  { id: 'add_wall_art', group: 'Furnish', label: 'Hang wall art', desc: 'Paintings, mirrors, banners and shelves above furniture and on bare walls', keywords: ['art', 'painting', 'picture', 'mirror', 'wall', 'bare walls', 'frame', 'hang', 'banner', 'tapestry'],
    run: ctx => each(ctx, (r, f) => { let n = 0; const L = ctx.level, ps = roomProps(L, r);
      const artType = base => withPack(L, d => d.place === 'wall' && !d.tags.includes('light') && !d.tags.includes('curtain'), 0.55, ctx.rnd) || base;
      const hang = (type, wall, t) => { const p = hangAt(L, r, type, wall, t); if (p) n++; return !!p; };
      for (const p of ps) { const t = ART_FOR[p.type]; if (!t || wallDist(r, p) > 0.25 || f.wallArt + n >= f.wallArtTarget + 2) continue; const w = nearestWall(r, p); if (!hasTag(p, 'wall-hug') && p.type !== 'bed' && p.type !== 'sofa') continue; hang(artType(t), w, (p.x - r.x) * WALLS[w].tan[0] + (p.z - r.z) * WALLS[w].tan[1]); }
      for (const w of Object.keys(WALLS)) { if (f.wallArt + n >= f.wallArtTarget + 1) break; if (!ps.some(p => isFloorBlocker(p) && wallDist(r, p) < 0.25 && nearestWall(r, p) === w && propSize(p)[2] > 1.4)) hang(artType(pick(['painting', 'mirror'], ctx.rnd)), w, wallLen(r, w) * 0.2 * (ctx.rnd() < 0.5 ? -1 : 1)) || hang('painting', w, 0); }
      return { n, msg: `hung ${n}` }; }) },
  { id: 'add_architecture', group: 'Furnish', label: 'Gothic architecture', desc: 'Pillars, wall pilasters, window and door surrounds, ceiling vaults, cobwebs and floor sigils from the asset pack', keywords: ['architecture', 'pillar', 'column', 'arch', 'vault', 'gothic', 'window frame', 'door frame', 'cobweb', 'ceiling', 'cathedral', 'crypt look'],
    run: ctx => each(ctx, (r, f) => {
      const L = ctx.level, rnd = ctx.rnd; if (!L.pack) return null; let n = 0;
      const tagged = tag => packPool(L, d => d.tags.includes(tag)), onRoom = tag => roomProps(L, r).some(p => hasTag(p, tag));
      // 1. surrounds for windows and doors
      for (const o of roomOpenings(L, r)) {
        const tag = o.type === 'window' ? 'window-deco' : 'door-deco', pool = tagged(tag), [wx, wz] = wallPoint(r, o.wall, o.t);
        if (!pool.length || roomProps(L, r).some(p => hasTag(p, tag) && near(p, wx, wz, 0.5))) continue;
        const type = pick(pool, rnd), d = defOf(type), y0 = o.type === 'window' ? o.sill - 0.02 : 0;
        const sc = clamp(Math.min((o.w + 0.15) / (o.type === 'window' ? 1.55 : 1.1) / 1.0, (r.h - 0.08 - y0) / d.size[2]), 0.5, 1.6);
        const [x, z] = wallPoint(r, o.wall, o.t, d.size[1] * sc / 2 + 0.01); addProp(L, r, type, x, z, WALLS[o.wall].rot, { scale: r2(sc), y: r2(y0), noSwap: true }); n++;
      }
      // 2. corner pillars (one style per room)
      const pillars = tagged('pillar').filter(t => !t.includes('broken'));
      if (pillars.length && r.w >= 4.2 && r.d >= 4.2 && !onRoom('pillar')) {
        const type = pick(pillars, rnd), sc = clamp((r.h - 0.12) / defOf(type).size[2], 0.6, 1.2);
        for (const [sx, sz] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) if (tryPlace(L, r, type, r.x + sx * (r.w / 2 - 0.45), r.z + sz * (r.d / 2 - 0.45), 0, { scale: r2(sc), noSwap: true })) n++;
      }
      // 3. pilasters between openings along the walls (one style per room)
      const pil = tagged('pilaster');
      if (pil.length && !onRoom('pilaster')) {
        const type = pick(pil, rnd), sc = Math.min(1, (r.h - 0.06) / defOf(type).size[2]);
        for (const w of Object.keys(WALLS)) { const len = wallLen(r, w); for (let t = -len / 2 + 0.3; t <= len / 2 - 0.25; t += Math.max(2.0, len / Math.max(2, Math.round(len / 2.3)))) { const p = hangAt(L, r, type, w, t); if (p) { p.scale = r2(sc); p.y = 0; n++; } } }
      }
      // 4. ceiling vault over the middle of the room
      const vault = tagged('ceiling-decor'); if (vault.length && !onRoom('ceiling-decor')) { addProp(L, r, pick(vault, rnd), r.x, r.z, 0, { noSwap: true }); n++; }
      // 5. cobwebs in the upper corners
      const webs = tagged('cobweb');
      if (webs.length && !onRoom('cobweb')) for (const [sx, sz] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) if (rnd() < 0.7) {
        const type = pick(webs, rnd), d = defOf(type), cx = r.x + sx * (r.w / 2 - 0.05), cz = r.z + sz * (r.d / 2 - 0.05), dx = -sx * 0.32, dz = -sz * 0.32;
        addProp(L, r, type, cx + dx, cz + dz, faceTo([cx, cz], [r.x, r.z]), { y: r2(r.h - d.size[2]), noSwap: true }); n++;
      }
      // 6. a floor sigil / grate if there is space
      const decals = tagged('decal'); if (decals.length && f.freeSquare >= 1.2 && !onRoom('decal')) { const s = findFreeSpot(L, r, pick(decals, rnd), { preferWall: false }); if (s) { addProp(L, r, pick(decals, rnd), s.x, s.z, 0, { noSwap: true }); n++; } }
      return { n, msg: `${n} architectural pieces` }; }) },
  { id: 'add_clutter', group: 'Furnish', label: 'Add clutter', desc: 'Lived-in floor clutter from the asset pack: barrels, crates, bone heaps, statues, cages', keywords: ['clutter', 'messy', 'lived-in', 'barrels', 'crates', 'junk', 'ossuary', 'statues', 'dusty'],
    run: ctx => each(ctx, (r, f) => {
      const L = ctx.level; if (!L.pack) return null; let n = 0;
      const want = Math.max(2, Math.round(f.area / 6)) - f.clutter;
      for (let i = 0; i < Math.min(5, Math.max(0, want)); i++) { const t = withPack(L, d => isFloorItem(d) && d.tags.includes('decor'), 1, ctx.rnd); if (!t) break; const s = findFreeSpot(L, r, t, { preferWall: true }); if (s && tryPlace(L, r, t, s.x, s.z, s.rot, { noSwap: true })) n++; }
      return { n, msg: `${n} clutter pieces` }; }) },
  { id: 'add_plants', group: 'Furnish', label: 'Add plants', desc: 'Greenery in empty corners', keywords: ['plant', 'green', 'nature', 'fresh', 'botanical', 'jungle', 'life'],
    run: ctx => each(ctx, (r, f) => { let n = 0; const want = Math.max(1, Math.round(f.area / 9)) - f.plants; for (const c of f.freeCorners) { if (n >= want) break; if (tryPlace(ctx.level, r, 'plant', c.x, c.z, faceTo([c.x, c.z], [r.x, r.z]), { scale: r2(0.85 + ctx.rnd() * 0.35) })) n++; } return { n, msg: `${n} plants` }; }) },
  { id: 'add_lighting', group: 'Furnish', label: 'Add lighting', desc: 'Ceiling pendants and floor lamps beside seating', keywords: ['light', 'lamp', 'dark', 'bright', 'illuminat', 'ambient', 'glow'],
    run: ctx => each(ctx, (r, f) => { let n = 0; const want = Math.max(1, Math.round(f.area / 12));
      if (r.type === 'corridor' && !roomProps(ctx.level, r).some(p => defOf(p.type).place === 'ceiling')) {
        const len = Math.max(r.w, r.d), k = Math.max(1, Math.round(len / 4.5)), ct = () => withPack(ctx.level, d => d.place === 'ceiling' && d.tags.includes('light'), 1, ctx.rnd) || 'ceiling_light';
        for (let i = 0; i < k; i++) { const u = (-len / 2) + len * (i + 0.5) / k; addProp(ctx.level, r, ct(), r.w >= r.d ? r.x + u : r.x, r.w >= r.d ? r.z : r.z + u, 0, { noSwap: true }); n++; }
      } else if (!roomProps(ctx.level, r).some(p => defOf(p.type).place === 'ceiling')) { const ct = () => withPack(ctx.level, d => d.place === 'ceiling', 1, ctx.rnd) || 'ceiling_light'; addProp(ctx.level, r, ct(), r.x, r.z, 0); n++; if (want > 1) { addProp(ctx.level, r, ct(), r.x + r.w * 0.25, r.z + r.d * 0.25, 0); n++; } }
      const seat = roomProps(ctx.level, r).find(p => p.type === 'sofa' || p.type === 'armchair'); if (seat && !roomProps(ctx.level, r).some(p => p.type === 'floor_lamp')) { for (const s of [1, -1]) { const [wx, wz] = loc2w(seat.rot, s * (propSize(seat)[0] / 2 + 0.3), -0.3); if (tryPlace(ctx.level, r, 'floor_lamp', seat.x + wx, seat.z + wz, 0)) { n++; break; } } }
      else if (!seat && f.freeCorners[0] && !f.lights) { const c = f.freeCorners[0]; if (tryPlace(ctx.level, r, 'floor_lamp', c.x, c.z, 0)) n++; }
      if (ctx.level.pack) {
        const wl = packPool(ctx.level, d => d.place === 'wall' && d.tags.includes('light')), fl = packPool(ctx.level, d => d.place === 'floor' && d.tags.includes('light'));
        const sconces = () => roomProps(ctx.level, r).filter(p => defOf(p.type).place === 'wall' && hasTag(p, 'light')).length;
        if (wl.length) for (const w of Object.keys(WALLS)) { const len = wallLen(r, w); for (const t of [-len * 0.3, len * 0.3]) if (sconces() < Math.max(2, Math.round(f.area / 7)) && hangAt(ctx.level, r, pick(wl, ctx.rnd), w, t)) n++; }
        if (fl.length) for (const c of f.freeCorners.slice(0, 2)) if (tryPlace(ctx.level, r, pick(fl, ctx.rnd), c.x, c.z, faceTo([c.x, c.z], [r.x, r.z]))) n++;
      }
      return { n, msg: `${n} lights` }; }) },
  { id: 'add_curtains', group: 'Furnish', label: 'Add curtains', desc: 'Dress every bare window', keywords: ['curtain', 'drape', 'window dressing', 'blind'],
    run: ctx => each(ctx, r => { let n = 0; for (const o of roomOpenings(ctx.level, r).filter(o => o.type === 'window')) { const [x, z] = wallPoint(r, o.wall, o.t); if (roomProps(ctx.level, r).some(p => hasTag(p, 'curtain') && near(p, x, z, 0.9))) continue; const sc = clamp((o.w + 0.6) / 1.8, 0.7, 1.4) , k = Math.min(sc, (r.h - 0.15) / 2.45); const [px, pz] = wallPoint(r, o.wall, o.t, 0.1 * k); addProp(ctx.level, r, 'curtains', px, pz, WALLS[o.wall].rot, { scale: r2(k) }); n++; } return { n, msg: `${n} curtains` }; }) },
  { id: 'add_window', group: 'Structure', label: 'Add window', desc: 'Cut a window into the longest free wall', keywords: ['window', 'daylight', 'natural light', 'sunlight'],
    run: ctx => each(ctx, r => { const w = wallsByFreeLength(ctx.level, r).find(x => wallIsExterior(ctx.level, r, x)); if (!w) return null; for (const t of [0, 1, -1, 2, -2].map(v => v * 1.2)) { const win = { t, w: 1.4 }; if (!roomOpenings(ctx.level, r).some(o => o.wall === w && Math.abs(o.t - t) < (o.w + 1.4) / 2 + 0.2) && Math.abs(t) < wallLen(r, w) / 2 - 0.9) { addOpening(ctx.level, r, w, 'window', t); return { n: 1, msg: `window on ${w}` }; } } return null; }) },
  { id: 'add_door', group: 'Structure', label: 'Add door', desc: 'Add another door', keywords: ['door', 'entrance', 'exit', 'entry'],
    run: ctx => each(ctx, r => { const w = wallsByFreeLength(ctx.level, r)[1] || 'S'; const len = wallLen(r, w); for (const t of [0.35, -0.35, 0, 0.2, -0.2].map(v => v * len)) if (!roomOpenings(ctx.level, r).some(o => o.wall === w && Math.abs(o.t - t) < (o.w + 0.95) / 2 + 0.1)) { addOpening(ctx.level, r, w, 'door', r2(t)); return { n: 1, msg: `door on ${w}` }; } return null; }) },
  { id: 'resize_room', group: 'Structure', label: 'Resize room', desc: 'Make the room larger or smaller', keywords: ['bigger', 'larger', 'smaller', 'resize', 'enlarge', 'shrink', 'expand', 'wider'],
    params: [{ key: 'dir', criteria: { bigger: 'make the room larger', smaller: 'make the room smaller' }, def: 'bigger' }],
    run: (ctx, a) => each(ctx, r => { const k = a.dir === 'smaller' ? 0.85 : 1.18, nw = r2(clamp(r.w * k, 2.2, 14)), nd = r2(clamp(r.d * k, 2.2, 14)); const kx = nw / r.w, kz = nd / r.d; for (const p of roomProps(ctx.level, r)) { p.x = r2(r.x + (p.x - r.x) * kx); p.z = r2(r.z + (p.z - r.z) * kz); } for (const o of roomOpenings(ctx.level, r)) o.t = r2(o.t * (o.wall === 'N' || o.wall === 'S' ? kx : kz)); r.w = nw; r.d = nd; return { n: 1, msg: `now ${nw}x${nd}` }; }) },
  { id: 'generate_layout', scope: 'level', group: 'Structure', label: 'Generate layout', desc: 'REPLACE the level with a generated floor plan: a main corridor, side corridors, big end halls and many rooms of varying sizes',
    keywords: ['layout', 'floor plan', 'corridor', 'corridors', 'complex', 'map', 'dungeon', 'mansion', 'maze', 'generate level', 'whole building', 'academy layout'],
    params: [{ key: 'size', criteria: { small: 'a small compact layout with only a few rooms', medium: 'a medium layout with around ten rooms', large: 'a large sprawling complex layout with many rooms and several corridors' }, def: 'medium' }],
    run: (ctx, a) => { const n = generateLayout(ctx.level, { size: a.size || 'medium', seed: Math.floor(ctx.rnd() * 1e9) }); return { n, msg: `generated ${n} rooms (${a.size || 'medium'})` }; } },
  { id: 'add_room', scope: 'level', group: 'Structure', label: 'Add adjoining room', desc: 'Add one or more NEW rooms to the level (bedroom, library, laboratory, crypt, chapel, kitchen...) attached next to the existing ones', keywords: ['add room', 'new room', 'another room', 'extend', 'connect', 'next to'],
    params: [{ key: 'type', multi: true, criteria: { living: 'a living room', bedroom: 'a bedroom', dining: 'a dining room', kitchen: 'a kitchen', office: 'a home office', bathroom: 'a bathroom', hall: 'a hallway', corridor: 'a corridor', classroom: 'a classroom', dormitory: 'a dormitory', ritual: 'a ritual chamber', library: 'a library', laboratory: 'a laboratory', crypt: 'a crypt', chapel: 'a chapel' }, def: 'bedroom' }],
    run: (ctx, a) => { const L = ctx.level, last = L.rooms.reduce((m, r) => !m || r.x + r.w / 2 > m.x + m.w / 2 ? r : m, null); const type = a.type || 'bedroom', w = { bathroom: 2.6, hall: 2.4, kitchen: 4, crypt: 5.5, chapel: 5.5, library: 5, laboratory: 5, corridor: 8, classroom: 6.5, dormitory: 6, ritual: 6.5 }[type] || 4.2, d = type === 'corridor' ? 2.2 : last ? last.d : 4; const nr = addRoom(L, { type, w, d, x: last ? last.x + last.w / 2 + 2 * WT + w / 2 : 0, z: last ? last.z : 0 });
      if (last) { addOpening(L, last, 'E', 'door', 0); addOpening(L, nr, 'W', 'door', 0); } addOpening(L, nr, 'N', 'window', 0); assignThemes(L, { only: nr }); return out(`added ${nr.name}`); } },
  { id: 'restyle', scope: 'level', group: 'Style', label: 'Restyle', desc: 'Switch the whole palette and material style', keywords: ['style', 'restyle', 'theme', 'look', 'vibe', 'mood', 'rustic', 'modern', 'industrial', 'luxe', 'scandi', 'cozy', 'luxury', 'elegant'],
    params: [{ key: 'style', criteria: { modern: 'clean neutral modern', gothic: 'dark gothic necromancer crypt, candlelit, bone, iron, crimson, haunted', scandi: 'light airy scandinavian pastel', rustic: 'warm earthy rustic wood cabin', industrial: 'dark concrete metal loft', luxe: 'dark opulent luxurious gold velvet', scifi: 'futuristic sci-fi spaceship, cyberpunk neon, hull panels, holograms' }, def: 'modern' }],
    run: (ctx, a) => { const old = ctx.level.style; ctx.level.style = a.style in STYLES ? a.style : 'modern'; const np = STYLES[ctx.level.style].pack, op = STYLES[old]?.pack; if (np && listPacks().includes(np)) ctx.level.pack = np; else if (!np && op && ctx.level.pack === op) ctx.level.pack = null; reskinLevel(ctx.level); ctx.level.rooms.forEach(r => { r.wallColor = null; r.floorColor = null; }); assignThemes(ctx.level, { reroll: true, rnd: ctx.rnd }); ctx.level.props.forEach(p => { if (p.type !== 'rug') p.color = null; }); return out(`style -> ${ctx.level.style}`); } },
  { id: 'reskin', group: 'Style', label: 'Apply asset pack', desc: 'Swap furniture for the active asset pack models (set the pack in the header)', keywords: ['asset pack', 'reskin', 'swap models', 'use the gothic', 'gothic assets', 'custom assets', 'blender assets'],
    run: ctx => { const n = reskinLevel(ctx.level); return { n, msg: n ? `${n} props re-skinned (pack: ${ctx.level.pack || 'none'})` : `already up to date (pack: ${ctx.level.pack || 'none'})` }; } },
  { id: 'vary_surfaces', group: 'Style', label: 'Vary surfaces', desc: 'Give each room its own wallpaper or stone, floor, wainscot and mood lighting so rooms stop looking alike', keywords: ['wallpaper', 'texture', 'textures', 'walls', 'floors', 'floor', 'surface', 'finish', 'variety', 'varied', 'uniform', 'monotone', 'same'],
    run: ctx => { const rs = ctx.room ? [ctx.room] : ctx.level.rooms; rs.forEach(r => assignThemes(ctx.level, { reroll: true, only: r, rnd: ctx.rnd })); return { n: rs.length, msg: `re-themed ${rs.length} room(s)` }; } },
  { id: 'mirror_layout', group: 'Style', label: 'Mirror layout', desc: 'Flip the room left-to-right', keywords: ['mirror', 'flip', 'reverse', 'swap sides'],
    run: ctx => each(ctx, r => { for (const p of roomProps(ctx.level, r)) { p.x = r2(2 * r.x - p.x); p.rot = r2(-p.rot); } for (const o of roomOpenings(ctx.level, r)) { if (o.wall === 'E') o.wall = 'W'; else if (o.wall === 'W') o.wall = 'E'; else o.t = -o.t; } return { n: 1, msg: 'flipped' }; }) },
  { id: 'clear_room', group: 'Layout', label: 'Clear room', desc: 'Remove all furniture', keywords: ['clear', 'empty the room', 'remove everything', 'wipe', 'start over', 'reset'],
    run: ctx => each(ctx, r => { const n = roomProps(ctx.level, r).length; ctx.level.props = ctx.level.props.filter(p => p.room !== r.id); return { n, msg: `removed ${n}` }; }) },
];
export const ACTION = Object.fromEntries(ACTIONS.map(a => [a.id, a]));

export function mulberry(seed) { let a = seed >>> 0; return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
export function runAction(L, id, room, params = {}, seed = Date.now()) {
  const a = ACTION[id]; if (!a) return { n: 0, msg: 'unknown action' };
  return a.run({ level: L, room, rnd: mulberry(seed) }, params);
}

// move/rotate a prop; anything hosted on it (lamps on a table...) follows rigidly
export function moveProp(L, id, nx, nz, nrot) {
  const p = L.props.find(q => q.id === id); if (!p) return; const dr = nrot - p.rot, a = rad(dr), c = Math.cos(a), s = Math.sin(a);
  for (const q of L.props.filter(q => q.host === id)) { const dx = q.x - p.x, dz = q.z - p.z; q.x = r2(nx + dx * c + dz * s); q.z = r2(nz - dx * s + dz * c); q.rot = r2(q.rot + dr); }
  p.x = r2(nx); p.z = r2(nz); p.rot = r2(nrot);
}
export function moveRoom(L, r, nx, nz) {
  const dx = nx - r.x, dz = nz - r.z; for (const p of roomProps(L, r)) { p.x = r2(p.x + dx); p.z = r2(p.z + dz); } r.x = r2(nx); r.z = r2(nz);
}


// ---- procedural floor plan: corridors + rooms of varying size on a rigid wall grid ----------------
const SPEC = { // [w min, w max, d min, d max, ceiling height]
  bedroom: [3.2, 4.4, 3.2, 4.4, 2.8], office: [3, 4, 3, 4, 2.8], bathroom: [2.4, 3, 2.4, 3, 2.8], kitchen: [4, 5, 3.5, 4.5, 2.8], dining: [4.5, 6, 4, 5, 3],
  living: [5, 7, 4, 6, 3], library: [5, 7, 4, 6, 3.4], laboratory: [4.5, 6, 4, 5.5, 3.1], crypt: [5, 7, 5, 7, 3.4], chapel: [5, 6.5, 7, 9, 4.2], hall: [6, 9, 5, 7, 3.6], corridor: [2.2, 2.2, 2.2, 2.2, 3], classroom: [6, 8, 5, 6.5, 3.2], dormitory: [5, 7, 4.2, 5.5, 3], ritual: [6, 7.5, 6, 7.5, 3.8],
};
const MIXES = { scifi: ['bedroom', 'bedroom', 'dormitory', 'office', 'office', 'laboratory', 'laboratory', 'kitchen', 'dining', 'living', 'bathroom', 'classroom', 'library', 'hall'], gothic: ['bedroom', 'bedroom', 'bedroom', 'library', 'library', 'laboratory', 'laboratory', 'crypt', 'office', 'dining', 'living', 'bathroom', 'classroom', 'dormitory', 'ritual'], plain: ['bedroom', 'bedroom', 'living', 'kitchen', 'bathroom', 'office', 'dining'] };
const rectOfRoom = r => ({ x0: r.x - r.w / 2, x1: r.x + r.w / 2, z0: r.z - r.d / 2, z1: r.z + r.d / 2 });
const roomsClash = (a, b) => a.x0 - WT < b.x1 + WT - 1e-4 && a.x1 + WT > b.x0 - WT + 1e-4 && a.z0 - WT < b.z1 + WT - 1e-4 && a.z1 + WT > b.z0 - WT + 1e-4;

// attach a new room against `side` of `parent` (walls side by side, 2*WT between interiors) and cut aligned doors through both
function tryAttach(L, parent, side, type, rnd, o = {}) {
  const sp = SPEC[type], rr = (a, b) => Math.round((a + rnd() * (b - a)) * 10) / 10, minO = 1.5, gap = 2 * WT;
  const w = o.w ?? rr(sp[0], sp[1]), d = o.d ?? rr(sp[2], sp[3]), P = rectOfRoom(parent); let x, z;
  if (side === 'N' || side === 'S') {
    z = side === 'N' ? P.z0 - gap - d / 2 : P.z1 + gap + d / 2; const lo = P.x0 - w / 2 + minO, hi = P.x1 + w / 2 - minO; if (hi < lo) return null;
    x = clamp(o.at ?? lo + rnd() * (hi - lo), lo, hi);
  } else {
    x = side === 'W' ? P.x0 - gap - w / 2 : P.x1 + gap + w / 2; const lo = P.z0 - d / 2 + minO, hi = P.z1 + d / 2 - minO; if (hi < lo) return null;
    z = clamp(o.at ?? lo + rnd() * (hi - lo), lo, hi);
  }
  x = Math.round(x * 20) / 20; z = Math.round(z * 20) / 20;
  const cand = { x, z, w, d }, C = rectOfRoom(cand);
  if (L.rooms.some(q => q !== parent && roomsClash(rectOfRoom(q), C))) return null;
  const room = addRoom(L, { type, x, z, w, d, h: o.h ?? sp[4], name: o.name });
  const dw = o.door ?? (type === 'chapel' || type === 'hall' ? 1.5 : 0.95);
  if (side === 'N' || side === 'S') {
    const X = (Math.max(P.x0, C.x0) + Math.min(P.x1, C.x1)) / 2;
    if (side === 'N') { addOpening(L, parent, 'N', 'door', r2(X - parent.x), { w: dw }); addOpening(L, room, 'S', 'door', r2(room.x - X), { w: dw }); }
    else { addOpening(L, parent, 'S', 'door', r2(parent.x - X), { w: dw }); addOpening(L, room, 'N', 'door', r2(X - room.x), { w: dw }); }
  } else {
    const Z = (Math.max(P.z0, C.z0) + Math.min(P.z1, C.z1)) / 2;
    if (side === 'E') { addOpening(L, parent, 'E', 'door', r2(Z - parent.z), { w: dw }); addOpening(L, room, 'W', 'door', r2(room.z - Z), { w: dw }); }
    else { addOpening(L, parent, 'W', 'door', r2(parent.z - Z), { w: dw }); addOpening(L, room, 'E', 'door', r2(Z - room.z), { w: dw }); }
  }
  return room;
}
export const wallIsExterior = (L, r, wall) => {
  const R = rectOfRoom(r), gap = 2 * WT;
  return !L.rooms.some(o => { if (o === r) return false; const O = rectOfRoom(o); const ox = Math.min(R.x1, O.x1) - Math.max(R.x0, O.x0), oz = Math.min(R.z1, O.z1) - Math.max(R.z0, O.z0);
    return (wall === 'N' && Math.abs(R.z0 - O.z1 - gap) < 0.03 && ox > 0.3) || (wall === 'S' && Math.abs(O.z0 - R.z1 - gap) < 0.03 && ox > 0.3) || (wall === 'W' && Math.abs(R.x0 - O.x1 - gap) < 0.03 && oz > 0.3) || (wall === 'E' && Math.abs(O.x0 - R.x1 - gap) < 0.03 && oz > 0.3); });
};

// give every room a wall/floor/wainscot/mood theme suited to its type; neighbours-in-the-level prefer different themes
export function assignThemes(L, { reroll = false, only = null, rnd = Math.random } = {}) {
  const gothic = L.style === 'gothic', pal = STYLES[L.style] || STYLES.modern, table = TYPE_THEMES[L.style] || TYPE_THEMES.plain, used = {};
  const ok = k => THEMES[k] && THEMES[k].styles.includes(L.style);
  for (const r of L.rooms) if (r.theme && !(reroll && (!only || r === only))) used[r.theme.key] = (used[r.theme.key] || 0) + 1;
  for (const r of L.rooms) {
    if (r.theme && !(reroll && (!only || r === only))) continue;
    const cands = (table[r.type] || table.default || Object.keys(THEMES).filter(ok)).filter(ok);
    const pool = cands.length ? cands : Object.keys(THEMES).filter(ok);
    const key = [...pool].sort((a, b) => (used[a] || 0) - (used[b] || 0) + (rnd() - 0.5) * 0.9)[0];
    used[key] = (used[key] || 0) + 1; r.theme = resolveTheme(key, pal, rnd); delete r.wallColor; delete r.floorColor;
  }
}


// ---- composed setups ("kits"): cohesive clusters placed against a wall / in a corner / in the middle ------------------
const packBy = (L, ...prefixes) => L.pack ? Object.keys(CATALOG).filter(k => CATALOG[k].external && CATALOG[k].pack === L.pack && prefixes.some(pf => k.startsWith(`${L.pack}_${pf}`))) : [];
const choose = (L, rnd, prefixes, fallback = null) => { const c = packBy(L, ...prefixes); return c.length ? pick(c, rnd) : fallback; };
const shuffle = (a, rnd) => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const put = (L, r, type, pos, rot, extra) => (type ? tryPlace(L, r, type, pos[0], pos[1], rot, extra) : null);
const rug = (L, r, pos, rot, sc) => { addProp(L, r, 'rug', pos[0], pos[1], rot, { scale: r2(sc) }); return 1; };
const faceC = (r, pos) => faceTo(pos, [r.x, r.z]);

function wallAnchors(r, rnd) { const out = []; for (const w of Object.keys(WALLS)) { const len = wallLen(r, w); for (let t = -len / 2 + 1.0; t <= len / 2 - 1.0; t += 0.7) out.push({ kind: 'wall', wall: w, t, rot: WALLS[w].rot }); } return shuffle(out, rnd); }
const cornerAnchors = (r, rnd) => shuffle([[-1, -1], [1, -1], [-1, 1], [1, 1]].map(([sx, sz]) => ({ kind: 'corner', sx, sz, x0: r.x + sx * r.w / 2, z0: r.z + sz * r.d / 2 })), rnd);
const centerAnchors = (r, rnd) => Array.from({ length: 8 }, () => ({ kind: 'center', x: r.x + (rnd() - 0.5) * Math.max(0, r.w - 5) * 0.6, z: r.z + (rnd() - 0.5) * Math.max(0, r.d - 5) * 0.6, rot: (r.w >= r.d ? 0 : 90) + (rnd() < 0.3 ? 180 : 0) }));
const W = (r, a) => (dt, dd) => wallPoint(r, a.wall, a.t + dt, dd);
const Cn = (a) => (dx, dz) => [a.x0 - a.sx * dx, a.z0 - a.sz * dz];
const Zc = (a) => (lx, lz) => { const [wx, wz] = loc2w(a.rot, lx, lz); return [a.x + wx, a.z + wz]; };
const depthOf = t => defOf(t).size[1] / 2 + 0.02;

const KIT_FN = {
  bedSuite: (L, r, rnd, a) => { const w = W(r, a); if (!put(L, r, 'bed', w(0, 1.1), a.rot)) return 0; let n = 1; for (const s of [-1, 1]) if (put(L, r, 'nightstand', w(s * 1.12, 0.26), a.rot)) n++; if (put(L, r, 'bench', w(0, 2.5), a.rot)) n++; return n + rug(L, r, w(0, 1.8), a.rot, 0.9); },
  wardrobeWall: (L, r, rnd, a) => { const w = W(r, a); if (!put(L, r, 'wardrobe', w(0, 0.34), a.rot)) return 0; let n = 1; if (put(L, r, 'dresser', w(1.45, 0.27), a.rot)) { n++; const m = addProp(L, r, 'mirror', ...w(1.45, 0.04), a.rot); if (m) n++; } if (put(L, r, 'nightstand', w(-1.0, 0.26), a.rot)) n++; return n; },
  readingNook: (L, r, rnd, a) => { const c = Cn(a); const ap = c(0.8, 0.8); if (!put(L, r, 'armchair', ap, faceC(r, ap))) return 0; let n = 1; if (put(L, r, 'side_table', c(0.4, 1.7), 0)) n++; const lamp = choose(L, rnd, ['candelabra', 'grand_candelabra'], 'floor_lamp'); if (put(L, r, lamp, c(1.7, 0.35), 0, { noSwap: true })) n++; return n + rug(L, r, c(1.2, 1.2), 0, 0.55); },
  deskStation: (L, r, rnd, a) => { const w = W(r, a); if (!put(L, r, 'desk', w(0, 0.4), a.rot)) return 0; let n = 1; if (put(L, r, rnd() < 0.5 ? 'dining_chair' : 'throne' in CATALOG ? 'dining_chair' : 'dining_chair', w(0.05, 1.15), a.rot + 180 + (rnd() - 0.5) * 30)) n++; for (const s of [-1, 1]) if (put(L, r, 'bookshelf', w(s * 1.3, 0.18), a.rot)) n++; return n; },
  libraryWall: (L, r, rnd, a) => { const type = choose(L, rnd, ['wall_bookcase'], 'bookshelf'), wd = defOf(type).size[0] + 0.05; let n = 0; for (const i of [0, -1, 1]) if (put(L, r, type, W(r, a)(i * wd, depthOf(type)), a.rot, { noSwap: true })) n++; return n >= 1 ? (n >= 2 || L.pack ? n : 0) : 0; },
  diningSet: (L, r, rnd, a) => { const z = Zc(a); const t = put(L, r, 'dining_table', z(0, 0), a.rot); if (!t) return 0; let n = 1; for (const [lx, lz] of [[-0.5, -0.82], [0.5, -0.82], [-0.5, 0.82], [0.5, 0.82], [-1.25, 0], [1.25, 0]]) { const p = z(lx, lz); if (put(L, r, 'dining_chair', p, faceTo(p, z(0, 0)))) n++; } return n + rug(L, r, z(0, 0), a.rot, 1.3); },
  loungeGroup: (L, r, rnd, a) => { const z = Zc(a); if (!put(L, r, 'sofa', z(0, -1.4), a.rot)) return 0; let n = 1; if (put(L, r, 'coffee_table', z(0, -0.15), a.rot)) n++; if (put(L, r, 'armchair', z(-1.7, -0.1), a.rot + 90)) n++; if (put(L, r, 'armchair', z(1.7, -0.1), a.rot - 90)) n++; return n + rug(L, r, z(0, -0.5), a.rot, 1.15); },
  altarSetup: (L, r, rnd, a) => { const altar = choose(L, rnd, ['altar'], null); if (!altar) return 0; const w = W(r, a); if (!put(L, r, altar, w(0, depthOf(altar)), a.rot, { noSwap: true })) return 0; let n = 1;
    for (const s of [-1, 1]) { if (put(L, r, choose(L, rnd, ['grand_candelabra', 'candelabra'], 'floor_lamp'), w(s * 1.45, 0.4), a.rot, { noSwap: true })) n++; const ban = choose(L, rnd, ['banner'], null); if (ban && hangAt(L, r, ban, a.wall, a.t + s * 1.35)) n++; }
    for (const s of [-1, 1]) if (put(L, r, 'bench', w(s * 0.95, 2.6), a.rot + 180)) n++; const kn = choose(L, rnd, ['kneeler'], null); if (kn && put(L, r, kn, w(0, 1.5), a.rot + 180, { noSwap: true })) n++; return n; },
  labBench: (L, r, rnd, a) => { const w = W(r, a), bench = choose(L, rnd, ['lab_bench'], 'desk'); if (!put(L, r, bench, w(0, depthOf(bench)), a.rot, { noSwap: true })) return 0; let n = 1;
    const cau = choose(L, rnd, ['cauldron'], null); if (cau && put(L, r, cau, w(rnd() < 0.5 ? 1.5 : -1.5, 0.55), a.rot, { noSwap: true })) n++;
    const cab = choose(L, rnd, ['cabinet'], 'wardrobe'); if (put(L, r, cab, w(rnd() < 0.5 ? -1.6 : 1.7, depthOf(cab)), a.rot, { noSwap: true })) n++;
    const st = choose(L, rnd, ['stool'], 'dining_chair'); if (put(L, r, st, w(0.4, 1.15), a.rot + 180, { noSwap: true })) n++; return n; },
  cryptRow: (L, r, rnd, a) => { const type = choose(L, rnd, ['sarcophagus', 'coffin'], null); if (!type) return 0; const w = W(r, a), sp = defOf(type).size[0] + 0.4; let n = 0;
    for (const i of [0, -1, 1]) { if (put(L, r, type, w(i * sp, depthOf(type)), a.rot, { noSwap: true })) { n++; const nc = choose(L, rnd, ['crypt_niche'], null); if (nc && i === 0) hangAt(L, r, nc, a.wall, a.t + i * sp); } }
    if (n) for (const s of [-1, 1]) if (put(L, r, choose(L, rnd, ['brazier', 'candelabra'], 'floor_lamp'), w(s * (sp * 1.7), 0.4), a.rot, { noSwap: true })) n++; return n; },
  shrineCorner: (L, r, rnd, a) => { const c = Cn(a), type = choose(L, rnd, ['statue', 'tombstone', 'lectern'], null); if (!type) return 0; const p = c(0.6, 0.6); if (!put(L, r, type, p, faceC(r, p), { noSwap: true })) return 0; let n = 1;
    for (const pos of [c(1.6, 0.35), c(0.35, 1.6)]) if (put(L, r, choose(L, rnd, ['candelabra', 'brazier'], 'floor_lamp'), pos, 0, { noSwap: true })) n++; return n + rug(L, r, c(1.3, 1.3), 0, 0.5); },
  storageCorner: (L, r, rnd, a) => { const c = Cn(a); let n = 0; const kinds = ['barrel', 'crate', 'sack', 'bone_heap'];
    for (const [dx, dz] of [[0.45, 0.45], [1.25, 0.4], [0.4, 1.25], [1.2, 1.2]]) { const t = choose(L, rnd, [pick(kinds, rnd)], L.pack ? null : 'plant'); if (put(L, r, t, c(dx, dz), rnd() * 360, { noSwap: true })) n++; } return n >= 2 ? n : 0; },
  museumWall: (L, r, rnd, a) => { const w = W(r, a); let n = 0; const cs = choose(L, rnd, ['trophy_case', 'cabinet'], 'wardrobe'); for (const s of [-1, 1]) if (put(L, r, cs, w(s * 1.15, depthOf(cs)), a.rot, { noSwap: true })) n++; const st = choose(L, rnd, ['statue', 'mannequin'], 'plant'); if (n && put(L, r, st, w(0, 0.45), a.rot, { noSwap: true })) n++; return n >= 2 ? n : 0; },
  fireplaceWall: (L, r, rnd, a) => { const fp = choose(L, rnd, ['fireplace'], null); if (!fp) return 0; const w = W(r, a); if (!put(L, r, fp, w(0, depthOf(fp)), a.rot, { noSwap: true })) return 0; let n = 1; const f = w(0, 0.4);
    for (const s of [-1, 1]) { const p = w(s * 1.5, 1.4); if (put(L, r, 'armchair', p, faceTo(p, f))) n++; } return n + rug(L, r, w(0, 1.5), a.rot, 1.0); },
  scholarTable: (L, r, rnd, a) => { const z = Zc(a), t = choose(L, rnd, ['study_furniture_map'], 'dining_table'); if (!put(L, r, t, z(0, 0), a.rot, { noSwap: true })) return 0; let n = 1; for (const [lx, lz] of [[-0.6, 0.9], [0.6, 0.9], [-0.6, -0.9], [0.6, -0.9]]) { const p = z(lx, lz); if (put(L, r, choose(L, rnd, ['stool'], 'dining_chair'), p, faceTo(p, z(0, 0)), { noSwap: true })) n++; } return n; },
  classroomRows: (L, r, rnd, a) => { const w = W(r, a), pod = choose(L, rnd, ['podium'], 'desk'); if (!put(L, r, pod, w(0, depthOf(pod)), a.rot, { noSwap: true })) return 0; let n = 1; const bb = choose(L, rnd, ['blackboard'], null); if (bb && hangAt(L, r, bb, a.wall, a.t)) n++;
    for (let row = 0; row < 3; row++) for (const dt of [-1.9, -0.65, 0.65, 1.9]) { const dsk = choose(L, rnd, ['student_desk'], 'desk'); if (put(L, r, dsk, w(dt, 2.3 + row * 1.25), a.rot + 180, { noSwap: true })) { n++; put(L, r, choose(L, rnd, ['stool'], 'dining_chair'), w(dt, 2.95 + row * 1.25), a.rot, { noSwap: true }); } } return n >= 5 ? n : 0; },
  ritualCircle: (L, r, rnd, a) => { const z = Zc(a); let n = rug(L, r, z(0, 0), a.rot, 1.25); const sig = choose(L, rnd, ['floor_feature_sigil'], null); if (sig) { addProp(L, r, sig, ...z(0, 0), 0, { scale: 2.2, noSwap: true }); n++; }
    for (const ang of [0, 90, 180, 270]) { const [lx, lz] = [2.0 * Math.cos(rad(ang)), 2.0 * Math.sin(rad(ang))]; if (put(L, r, choose(L, rnd, ['candelabra', 'brazier'], 'floor_lamp'), z(lx, lz), 0, { noSwap: true })) n++; } return n >= 3 ? n : 0; },
};
const KITS = {
  bedroom: [['bedSuite', 'wall'], ['wardrobeWall', 'wall'], ['readingNook', 'corner'], ['shrineCorner', 'corner'], ['storageCorner', 'corner']],
  dormitory: [['bedSuite', 'wall'], ['bedSuite', 'wall'], ['bedSuite', 'wall'], ['wardrobeWall', 'wall'], ['storageCorner', 'corner']],
  living: [['loungeGroup', 'center'], ['fireplaceWall', 'wall'], ['readingNook', 'corner'], ['museumWall', 'wall'], ['shrineCorner', 'corner']],
  dining: [['diningSet', 'center'], ['fireplaceWall', 'wall'], ['museumWall', 'wall'], ['storageCorner', 'corner'], ['shrineCorner', 'corner']],
  office: [['deskStation', 'wall'], ['libraryWall', 'wall'], ['readingNook', 'corner'], ['scholarTable', 'center']],
  library: [['libraryWall', 'wall'], ['libraryWall', 'wall'], ['libraryWall', 'wall'], ['scholarTable', 'center'], ['readingNook', 'corner'], ['deskStation', 'wall']],
  classroom: [['classroomRows', 'wall'], ['libraryWall', 'wall'], ['deskStation', 'wall'], ['storageCorner', 'corner']],
  laboratory: [['labBench', 'wall'], ['labBench', 'wall'], ['labBench', 'wall'], ['storageCorner', 'corner'], ['scholarTable', 'center'], ['shrineCorner', 'corner']],
  crypt: [['cryptRow', 'wall'], ['cryptRow', 'wall'], ['shrineCorner', 'corner'], ['storageCorner', 'corner'], ['shrineCorner', 'corner']],
  chapel: [['altarSetup', 'wall'], ['shrineCorner', 'corner'], ['shrineCorner', 'corner'], ['museumWall', 'wall']],
  ritual: [['ritualCircle', 'center'], ['altarSetup', 'wall'], ['shrineCorner', 'corner'], ['shrineCorner', 'corner'], ['storageCorner', 'corner']],
  hall: [['museumWall', 'wall'], ['fireplaceWall', 'wall'], ['shrineCorner', 'corner'], ['loungeGroup', 'center'], ['museumWall', 'wall']],
  kitchen: [['labBench', 'wall'], ['storageCorner', 'corner'], ['storageCorner', 'corner']],
};
// --- layout taste: keep fronts of cabinets/altars/hearths clear, keep walkways between doors open, spread setups out, hug walls ---
function frontClearancePenalty(L, r, added) {
  let pen = 0; const blockers = roomProps(L, r).filter(isFloorBlocker);
  for (const p of added) {
    if (defOf(p.type).place !== 'floor') continue;
    const d = hasTag(p, 'hearth') ? 0.9 : hasTag(p, 'altar') || hasTag(p, 'media') ? 0.8 : (hasTag(p, 'storage') || hasTag(p, 'tall')) ? 0.65 : 0; if (!d) continue;
    const [w, dep] = propSize(p), [ox, oz] = loc2w(p.rot || 0, 0, dep / 2 + d / 2), R = { cx: p.x + ox, cz: p.z + oz, hw: w / 2 * 0.9, hd: d / 2, rot: p.rot || 0 };
    for (const q of blockers) if (q.id !== p.id && !hasTag(q, 'seating') && rectsOverlap(R, rectOf(q), 0)) pen++;
  }
  return pen;
}
function walkwayPenalty(L, r) {
  const doors = roomOpenings(L, r).filter(o => o.type === 'door'); if (!doors.length) return 0;
  const pts = doors.map(o => wallPoint(r, o.wall, o.t, 0.9)), tgts = pts.length > 1 ? pts.slice(1) : [[r.x, r.z]], blockers = roomProps(L, r).filter(isFloorBlocker); let pen = 0;
  for (const tg of tgts) for (let i = 0; i <= 1.001; i += 0.08) { const R = { cx: pts[0][0] + (tg[0] - pts[0][0]) * i, cz: pts[0][1] + (tg[1] - pts[0][1]) * i, hw: 0.32, hd: 0.32, rot: 0 }; if (blockers.some(q => rectsOverlap(R, rectOf(q), 0))) pen++; }
  return pen;
}
function scoreKit(L, r, added, n, base) {
  const fl = added.filter(p => defOf(p.type).place === 'floor' && !hasTag(p, 'flat')); if (!fl.length) return n;
  const cx = fl.reduce((a, p) => a + p.x, 0) / fl.length, cz = fl.reduce((a, p) => a + p.z, 0) / fl.length;
  const others = L.props.slice(0, base).filter(q => q.room === r.id && isFloorBlocker(q)), spread = Math.min(2.6, ...others.map(q => Math.hypot(q.x - cx, q.z - cz)), 2.6);
  const hug = added.filter(p => hasTag(p, 'wall-hug') && wallDist(r, p) < 0.2).length;
  return n + spread * 0.8 + hug * 0.25 - 2.5 * frontClearancePenalty(L, r, added) - 1.0 * walkwayPenalty(L, r);
}
function tryKit(L, r, rnd, fn, kind) {
  const base = L.props.length, anchors = kind === 'corner' ? cornerAnchors(r, rnd) : kind === 'center' ? centerAnchors(r, rnd) : wallAnchors(r, rnd); let best = null;
  for (const a of anchors.slice(0, 10)) {
    const n = fn(L, r, rnd, a);
    if (n >= 2) { const added = L.props.slice(base), sc = scoreKit(L, r, added, n, base); if (!best || sc > best.sc) best = { sc, added, n }; }
    L.props.length = base;
  }
  if (best) { L.props.push(...best.added); return best.n; }
  return 0;
}
// place several cohesive setups appropriate to the room type; returns number of props added
export function composeRoom(L, r, rnd) {
  const kits = KITS[r.type]; if (!kits || !kits.length) return 0;
  const want = clamp(Math.round(r.w * r.d / 9) + 1, 2, 8); let made = 0, n = 0, i = 0; const order = shuffle([...kits], rnd);
  while (made < want && i < want * 3) { const [name, kind] = order[i % order.length]; i++; const c = tryKit(L, r, rnd, KIT_FN[name], kind); if (c) { made++; n += c; } }
  r.composed = (r.composed || 0) + made; return n;
}
function furnishKits(L, r, rnd) { const n = composeRoom(L, r, rnd); return n || furnishHall(L, r); }

export function generateLayout(L, { size = 'medium', seed = Date.now() } = {}) {
  const rnd = mulberry(seed), cfg = { small: { len: 11, br: 0 }, medium: { len: 17, br: 1 }, large: { len: 24, br: 2 } }[size] || { len: 17, br: 1 };
  L.rooms = []; L.openings = []; L.props = [];
  const mix = L.pack ? (MIXES[L.style] || MIXES.gothic) : MIXES.plain, bigs = L.pack ? (L.style === 'scifi' ? ['hall', 'laboratory', 'living', 'library'] : ['chapel', 'crypt', 'library', 'hall']) : ['living', 'dining', 'hall'], pickType = () => mix[Math.floor(rnd() * mix.length)], big = () => bigs[Math.floor(rnd() * bigs.length)];
  const spine = addRoom(L, { type: 'corridor', x: 0, z: 0, w: cfg.len, d: 2.2, h: 3, name: 'Main corridor' });
  const S0 = rectOfRoom(spine), branches = [];
  // side corridors first so the side rooms flow around them
  for (let b = 0; b < cfg.br; b++) {
    const side = b % 2 === 0 ? 'S' : 'N', frac = cfg.br === 1 ? 0.55 : (b === 0 ? 0.3 : 0.7), len = 8 + Math.floor(rnd() * 5);
    const c = tryAttach(L, spine, side, 'corridor', rnd, { w: 2.2, d: len, at: S0.x0 + cfg.len * frac, name: b ? 'North corridor' : 'South corridor' }); if (c) branches.push({ c, side });
  }
  // rooms along the main corridor, both sides, widths and depths varied
  for (const side of ['N', 'S']) {
    let cursor = S0.x0 + 0.1;
    while (cursor < S0.x1 - 2.6) {
      const type = pickType(), sp = SPEC[type], w = Math.round((sp[0] + rnd() * (sp[1] - sp[0])) * 10) / 10;
      const r = tryAttach(L, spine, side, type, rnd, { w, at: cursor + w / 2 });
      cursor += r ? w + 2 * WT + rnd() * 0.15 : 1.2;
    }
  }
  // rooms along each side corridor, plus a large room at its far end
  for (const { c, side } of branches) {
    const C = rectOfRoom(c);
    for (const lat of ['W', 'E']) {
      let cursor = C.z0 + 0.1;
      while (cursor < C.z1 - 2.4) {
        const type = pickType(), sp = SPEC[type], d = Math.round((sp[2] + rnd() * (sp[3] - sp[2])) * 10) / 10;
        const r = tryAttach(L, c, lat, type, rnd, { d, at: cursor + d / 2 });
        cursor += r ? d + 2 * WT + rnd() * 0.15 : 1.2;
      }
    }
    tryAttach(L, c, side, big(), rnd, { at: c.x }) || tryAttach(L, c, side, 'office', rnd, { at: c.x });
  }
  // great rooms at the ends of the main corridor
  tryAttach(L, spine, 'E', big(), rnd, { at: spine.z });
  if (cfg.br) tryAttach(L, spine, 'W', 'hall', rnd, { at: spine.z });
  // name rooms and put windows on exterior walls only
  const counts = {};
  for (const r of L.rooms) { if (r.name === 'Main corridor' || r.name.endsWith('corridor')) continue; counts[r.type] = (counts[r.type] || 0) + 1; r.name = `${r.type[0].toUpperCase() + r.type.slice(1)} ${counts[r.type]}`; }
  for (const r of L.rooms) for (const wall of Object.keys(WALLS)) {
    if (!wallIsExterior(L, r, wall)) continue; const len = wallLen(r, wall); if (len < 2.6) continue;
    const k = r.type === 'crypt' ? 1 : r.type === 'corridor' ? (len > 6 ? 0 : 1) : Math.min(3, Math.floor(len / 3.2));
    for (let i = 0; i < k; i++) { const t = r2((i - (k - 1) / 2) * 3.0); if (!roomOpenings(L, r).some(o => o.wall === wall && Math.abs(o.t - t) < (1.4 + o.w) / 2 + 0.3)) addOpening(L, r, wall, 'window', t); }
  }
  assignThemes(L, { reroll: true, rnd });
  return L.rooms.length;
}
