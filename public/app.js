import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { TransformControls } from 'three/addons/controls/TransformControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { GLTFExporter } from 'three/addons/exporters/GLTFExporter.js';
import { CATALOG, STYLES, TYPES, buildProp, loadExternalAssets, hasExternal, mat, lightOf, listPacks, assetEntry, neededKeys, ensureAssets } from './catalog.js';
import * as LV from './level.js';
import * as DC from './decision.js';
import { surfaceMaterial, loadTextureManifest, whenTexturesReady } from './surfaces.js';
import { THEMES, resolveTheme } from './themes.js';

const { WALLS, WT, ACTIONS, ACTION } = LV;
const $ = s => document.querySelector(s);
const el = (tag, attrs = {}, ...kids) => { const e = document.createElement(tag); for (const [k, v] of Object.entries(attrs)) k === 'class' ? e.className = v : k.startsWith('on') ? e.addEventListener(k.slice(2), v) : e.setAttribute(k, v); for (const c of kids.flat()) e.append(c); return e; };

// ---------------------------------------------------------------- state
const S = { fx: !/fx=0/.test(location.hash + location.search), level: LV.newLevel(), selProp: null, selRoom: null, placing: null, undo: [], redo: [], ceiling: false, cutaway: true, top: false, exporting: false, busy: false };
const saved = (() => { try { return JSON.parse(localStorage.getItem('leveldez.level')); } catch { return null; } })();
if (saved?.rooms?.length) S.level = saved; else {
  const r = LV.addRoom(S.level, { type: 'living', w: 6, d: 4.6, name: 'Living room' }); LV.addOpening(S.level, r, 'S', 'door', 1.6); LV.addOpening(S.level, r, 'N', 'window', -1.5); LV.addOpening(S.level, r, 'N', 'window', 1.5);
}
S.selRoom = S.level.rooms[0]?.id || null;
const L = () => S.level;
const room = () => LV.getRoom(L(), S.selRoom);
const prop = () => L().props.find(p => p.id === S.selProp);
const pal = () => STYLES[L().style] || STYLES.modern;

function snapshot() { S.undo.push(JSON.stringify(L())); if (S.undo.length > 80) S.undo.shift(); S.redo = []; }
function restore(json) { S.level = JSON.parse(json); if (!LV.getRoom(L(), S.selRoom)) S.selRoom = L().rooms[0]?.id || null; if (!prop()) S.selProp = null; refresh(); }
function undo() { if (!S.undo.length) return; S.redo.push(JSON.stringify(L())); restore(S.undo.pop()); }
function redo() { if (!S.redo.length) return; S.undo.push(JSON.stringify(L())); restore(S.redo.pop()); }
function mutate(fn, { snap = true } = {}) { if (snap) snapshot(); const r = fn(); refresh(); return r; }
function toast(msg) { const t = $('#toast'); t.textContent = msg; t.classList.add('show'); clearTimeout(toast.t); toast.t = setTimeout(() => t.classList.remove('show'), 2200); }

// ---------------------------------------------------------------- three.js scene
const view = $('#view');
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: false });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2)); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap; renderer.shadowMap.autoUpdate = false; renderer.shadowMap.needsUpdate = true;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05; renderer.outputColorSpace = THREE.SRGBColorSpace;
view.prepend(renderer.domElement);
const scene = new THREE.Scene(); scene.background = new THREE.Color('#12151c');
const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 200); camera.position.set(9, 9, 11);
// ---- cinematic post stack: MSAA -> ambient occlusion -> bloom -> grade (split-tone, vignette, grain) -> tone map / sRGB ----
const composer = new EffectComposer(renderer, new THREE.WebGLRenderTarget(2, 2, { type: THREE.HalfFloatType, samples: 4 }));
composer.addPass(new RenderPass(scene, camera));
const gtao = new GTAOPass(scene, camera, 2, 2); gtao.output = GTAOPass.OUTPUT.Default;
gtao.updateGtaoMaterial({ radius: 0.55, distanceExponent: 1.5, thickness: 1.2, scale: 1.25, samples: 12, distanceFallOff: 1.0, screenSpaceRadius: false });
gtao.updatePdMaterial({ lumaPhi: 10, depthPhi: 2, normalPhi: 3, radius: 6, radiusExponent: 1, rings: 2, samples: 12 });
composer.addPass(gtao);
const bloom = new UnrealBloomPass(new THREE.Vector2(2, 2), 0.4, 0.65, 0.93); composer.addPass(bloom);
const grade = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 } },
  vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime; varying vec2 vUv;
void main(){ vec4 c = texture2D(tDiffuse, vUv); float l = dot(c.rgb, vec3(0.299, 0.587, 0.114));
  c.rgb = mix(vec3(l), c.rgb, 1.12); c.rgb = (c.rgb - 0.18) * 1.07 + 0.18;
  c.rgb *= mix(vec3(0.95, 1.0, 1.06), vec3(1.07, 1.0, 0.92), smoothstep(0.0, 0.6, l));
  vec2 q = vUv - 0.5; c.rgb *= mix(0.5, 1.0, smoothstep(0.95, 0.25, length(q) * 1.2));
  float g = fract(sin(dot(vUv * vec2(1731.0, 1237.0) + uTime, vec2(12.9898, 78.233))) * 43758.5453); c.rgb += (g - 0.5) * 0.028;
  gl_FragColor = c; }` });
composer.addPass(grade); composer.addPass(new OutputPass());
const orbit = new OrbitControls(camera, renderer.domElement); orbit.enableDamping = true; orbit.target.set(0, 0, 0); orbit.maxPolarAngle = Math.PI / 2.02;
{ const pm = new THREE.PMREMGenerator(renderer); scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture; scene.environmentIntensity = 0.35; }
scene.add(new THREE.HemisphereLight('#dfe8ff', '#4a3f35', 0.75));
const sun = new THREE.DirectionalLight('#fff4e4', 1.5); sun.position.set(8, 16, 6); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.03; scene.add(sun, sun.target);
const grid = new THREE.GridHelper(60, 60, '#2a313f', '#1b212b'); grid.position.y = -0.11; scene.add(grid);
const levelGroup = new THREE.Group(); levelGroup.name = 'LevelDez_Level'; scene.add(levelGroup);
const lightGroup = new THREE.Group(); scene.add(lightGroup);
scene.fog = new THREE.FogExp2('#0b0d12', 0.0045);
// fixed pool of point lights re-assigned to the sources nearest the camera focus (constant light count = no shader recompiles)
const POOL = 18, SHADOWED = 3, lightPool = Array.from({ length: POOL }, (_, k) => { const l = new THREE.PointLight('#ffffff', 0, 8, 1.7); if (k < SHADOWED) { l.castShadow = true; l.shadow.mapSize.set(512, 512); l.shadow.bias = -0.0018; l.shadow.normalBias = 0.035; l.shadow.camera.near = 0.25; } lightGroup.add(l); return l; });
let lightSig = '';
let lightSources = [], assignedLights = [], lightTick = 0;
function updateLights(t) {
  if (lightTick++ % 20 === 0) {
    const tx = orbit.target.x, tz = orbit.target.z;
    assignedLights = lightSources.map(s => ({ s, d: Math.hypot(s.x - tx, s.z - tz) + (s.bias || 0) })).sort((a, b) => a.d - b.d).slice(0, POOL).map(o => o.s);
    const sig = assignedLights.slice(0, SHADOWED).map(s => s.x.toFixed(1) + s.z.toFixed(1)).join('|'); if (sig !== lightSig) { lightSig = sig; renderer.shadowMap.needsUpdate = true; }
  }
  lightPool.forEach((l, k) => {
    const s = assignedLights[k]; if (!s) { l.intensity = 0; return; }
    l.position.set(s.x, s.y, s.z); l.color.set(s.color); l.distance = s.dist; l.decay = s.decay || 1.7;
    l.intensity = s.i * (s.flicker ? 1 + 0.13 * Math.sin(t * 8 + s.phase) + 0.08 * Math.sin(t * 19.3 + s.phase * 1.7) : 1);
  });
}
// drifting dust motes around the camera focus (lit-looking, additive)
const dust = (() => {
  const N = 450, pos = new Float32Array(N * 3), seed = new Float32Array(N); for (let i = 0; i < N; i++) { pos[i * 3] = (Math.random() - 0.5) * 16; pos[i * 3 + 1] = Math.random() * 3.2; pos[i * 3 + 2] = (Math.random() - 0.5) * 16; seed[i] = Math.random() * 6.28; }
  const c = document.createElement('canvas'); c.width = c.height = 32; const g = c.getContext('2d'), gr = g.createRadialGradient(16, 16, 0, 16, 16, 16); gr.addColorStop(0, 'rgba(255,230,190,1)'); gr.addColorStop(1, 'rgba(255,230,190,0)'); g.fillStyle = gr; g.fillRect(0, 0, 32, 32);
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const pts = new THREE.Points(geo, new THREE.PointsMaterial({ map: new THREE.CanvasTexture(c), size: 0.07, transparent: true, opacity: 0.32, depthWrite: false, blending: THREE.AdditiveBlending, fog: false })); pts.userData.base = pos.slice(); pts.userData.seed = seed; pts.frustumCulled = false; scene.add(pts); return pts;
})();
function updateDust(t) {
  dust.visible = S.fx && !S.exporting; if (!dust.visible) return; dust.position.set(orbit.target.x, 0, orbit.target.z);
  const p = dust.geometry.attributes.position, b = dust.userData.base, s = dust.userData.seed;
  for (let i = 0; i < s.length; i++) { p.array[i * 3] = b[i * 3] + Math.sin(t * 0.13 + s[i]) * 0.5; p.array[i * 3 + 1] = (b[i * 3 + 1] + t * 0.03 * (0.4 + (s[i] % 1))) % 3.2; p.array[i * 3 + 2] = b[i * 3 + 2] + Math.cos(t * 0.11 + s[i] * 1.3) * 0.5; }
  p.needsUpdate = true;
}
function scaleUV(geo, su, sv) { const uv = geo.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * su, uv.getY(i) * sv); return geo; }
let wallProps = []; // wall-mounted props: hidden together with a cut-away wall
const selBox = new THREE.Box3Helper(new THREE.Box3(), '#ffb454'); selBox.visible = false; scene.add(selBox);
const gizmo = new TransformControls(camera, renderer.domElement); gizmo.setTranslationSnap(0.05); gizmo.setRotationSnap(Math.PI / 12); gizmo.showY = false; scene.add(gizmo);
gizmo.addEventListener('dragging-changed', e => { orbit.enabled = !e.value; if (!e.value) commitGizmo(); });
function resize() { const w = view.clientWidth, h = view.clientHeight; renderer.setSize(w, h); composer.setPixelRatio(renderer.getPixelRatio()); composer.setSize(w, h); camera.aspect = w / h; camera.updateProjectionMatrix(); }
new ResizeObserver(resize).observe(view);

const texCache = new Map();
function plankTexture(color, pattern = 'plank') {
  const key = color + pattern; if (texCache.has(key)) return texCache.get(key);
  const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d'); g.fillStyle = color; g.fillRect(0, 0, 256, 256);
  if (pattern === 'stone') { // flagstones with per-tile shading and mortar lines
    for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { const x = j * 64 + (i % 2) * 32 - 32; g.fillStyle = `rgba(${(i * 53 + j * 29) % 2 ? '255,255,255' : '0,0,0'},${0.02 + ((i * 7 + j * 13) % 6) / 100})`; g.fillRect(x, i * 64, 64, 64); g.fillStyle = 'rgba(0,0,0,.55)'; g.fillRect(x, i * 64, 64, 2.5); g.fillRect(x, i * 64, 2.5, 64); g.fillRect(x + 64, i * 64, 2.5, 64); }
  } else for (let i = 0; i < 8; i++) { g.fillStyle = `rgba(0,0,0,${0.03 + (i * 37 % 7) / 100})`; g.fillRect(0, i * 32, 256, 32); g.fillStyle = 'rgba(0,0,0,.28)'; g.fillRect(0, i * 32, 256, 1.5); g.fillRect((i * 97) % 256, i * 32, 1.5, 32); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; texCache.set(key, t); return t;
}
const glassMat = new THREE.MeshStandardMaterial({ color: '#bfe0f5', roughness: 0.05, metalness: 0.1, transparent: true, opacity: 0.28, name: 'glass' });

function buildWall(r, wall, M) {
  const len = LV.wallLen(r, wall) + ((wall === 'N' || wall === 'S') ? 2 * WT : 0), h = r.h, ops = LV.roomOpenings(L(), r).filter(o => o.wall === wall);
  const shape = new THREE.Shape(); shape.moveTo(-len / 2, 0); shape.lineTo(len / 2, 0); shape.lineTo(len / 2, h); shape.lineTo(-len / 2, h); shape.closePath();
  for (const o of ops) { const x0 = o.t - o.w / 2, x1 = o.t + o.w / 2, y0 = o.sill + (o.type === 'door' ? 0.001 : 0), y1 = Math.min(h - 0.05, o.sill + o.h); const hole = new THREE.Path(); hole.moveTo(x0, y0); hole.lineTo(x0, y1); hole.lineTo(x1, y1); hole.lineTo(x1, y0); hole.closePath(); shape.holes.push(hole); }
  const g = new THREE.ExtrudeGeometry(shape, { depth: WT, bevelEnabled: false }); g.translate(0, 0, -WT);
  const grp = new THREE.Group(); grp.name = `wall_${r.name.replace(/\W+/g, '_')}_${wall}`;
  const m = new THREE.Mesh(g, M.wall); m.castShadow = m.receiveShadow = true; m.name = 'wall'; grp.add(m);
  // skirting board, split around doors
  const sk = mat(M.trim, { r: 0.6 }); let cur = -LV.wallLen(r, wall) / 2; const doors = ops.filter(o => o.type === 'door').sort((a, b) => a.t - b.t);
  const seg = (a, b) => { if (b - a > 0.05) { const s = new THREE.Mesh(new THREE.BoxGeometry(b - a, 0.1, 0.018), sk); s.position.set((a + b) / 2, 0.05, 0.009); s.name = 'skirting'; s.receiveShadow = true; grp.add(s); } };
  if (!M.wainMat) { for (const d of doors) { seg(cur, d.t - d.w / 2); cur = d.t + d.w / 2; } seg(cur, LV.wallLen(r, wall) / 2); }
  else { // wainscot panelling below the sill line + chair rail, cut around doors
    const H = 0.88, wseg = (a, b) => { if (b - a < 0.06) return; const w = b - a, pm = new THREE.Mesh(scaleUV(new THREE.BoxGeometry(w, H, 0.026), w / M.wainTile, H / M.wainTile), M.wainMat); pm.position.set((a + b) / 2, H / 2, 0.013); pm.receiveShadow = true; pm.name = 'wainscot'; grp.add(pm);
      const rl = new THREE.Mesh(new THREE.BoxGeometry(w, 0.05, 0.045), mat(M.trim, { r: 0.5 })); rl.position.set((a + b) / 2, H + 0.025, 0.0225); rl.name = 'chair_rail'; grp.add(rl); };
    for (const d of doors) { wseg(cur, d.t - d.w / 2); cur = d.t + d.w / 2; } wseg(cur, LV.wallLen(r, wall) / 2);
  }
  { const L0 = LV.wallLen(r, wall), cm = new THREE.Mesh(new THREE.BoxGeometry(L0, 0.1, 0.06), mat(M.trim, { r: 0.5 })); cm.position.set(0, r.h - 0.05, 0.03); cm.name = 'crown_molding'; grp.add(cm); }
  // door + window dressing
  const frame = mat(M.trim, { r: 0.5 }), wood = mat(pal().wood);
  for (const o of ops) {
    const fb = (w, hh, d, x, y, z, mm, n) => { const b = new THREE.Mesh(new THREE.BoxGeometry(w, hh, d), mm); b.position.set(x, y + hh / 2, z); b.castShadow = true; b.name = n; grp.add(b); return b; };
    const top = Math.min(r.h - 0.05, o.sill + o.h), ft = 0.06;
    fb(ft, top - o.sill, 0.1, o.t - o.w / 2 - ft / 2, o.sill, -WT / 2, frame, o.type + '_frame'); fb(ft, top - o.sill, 0.1, o.t + o.w / 2 + ft / 2, o.sill, -WT / 2, frame, o.type + '_frame'); fb(o.w + 2 * ft, ft, 0.1, o.t, top, -WT / 2, frame, o.type + '_frame');
    if (o.type === 'door') { if (LV.wallIsExterior(L(), r, wall)) { const leaf = fb(o.w - 0.02, o.h - 0.02, 0.04, 0, 0, 0, wood, 'door_leaf'); leaf.geometry.translate(o.w / 2, 0, 0); leaf.position.set(o.t - o.w / 2 + 0.01, (o.h - 0.02) / 2, -WT / 2 + 0.2); leaf.position.y = (o.h - 0.02) / 2; leaf.rotation.y = -1.45; leaf.position.z = 0.02; fb(0.04, 0.04, 0.06, o.t + o.w / 2 - 0.1, 1.0, 0.06, mat(pal().metal, { m: 0.8 }), 'knob').visible = false; } }
    else { fb(o.w, 0.03, 0.1, o.t, o.sill - 0.03, -WT / 2, frame, 'sill'); fb(o.w, 0.03, 0.03, o.t, o.sill + o.h / 2, -WT / 2, frame, 'mullion'); fb(0.03, o.h, 0.03, o.t, o.sill, -WT / 2, frame, 'mullion'); const gl = new THREE.Mesh(new THREE.PlaneGeometry(o.w, o.h), glassMat); gl.position.set(o.t, o.sill + o.h / 2, -WT / 2); gl.name = 'glass'; grp.add(gl); }
  }
  const [bx, bz] = LV.wallBase(r, wall); grp.position.set(bx, 0, bz); grp.rotation.y = THREE.MathUtils.degToRad(WALLS[wall].rot);
  grp.userData = { wall: true, roomId: r.id, base: [bx, bz], inward: WALLS[wall].inward };
  return grp;
}

function rebuild() {
  for (const c of [...levelGroup.children]) { levelGroup.remove(c); c.traverse(o => { if (o.isMesh && o.geometry && !o.geometry.userData.shared) { /* geometry cache is shared in catalog; walls dispose via GC */ } }); }
  lightSources = [];
  const style = L().style; let box = new THREE.Box3();
  for (const r of L().rooms) {
    const rg = new THREE.Group(); rg.name = 'room_' + r.name.replace(/\W+/g, '_'); rg.userData.roomId = r.id;
    const th = r.theme, tile = x => Math.max(0.5, x?.tile || 2);
    let fm, M;
    if (th) {
      fm = surfaceMaterial(th.floor, [1, 1], { name: 'floor_' + r.id });
      M = { wall: surfaceMaterial(th.wall, [1 / tile(th.wall), 1 / tile(th.wall)], { name: 'wall_' + r.id }), trim: th.trim || '#cfc9bd',
        wainMat: th.wains ? (th.wains.tex ? surfaceMaterial({ tex: th.wains.tex, color: th.wains.color }, [1, 1], { name: 'wain_' + r.id }) : mat(th.wains.color, { r: 0.6 })) : null, wainTile: 1 };
      if (M.wainMat && M.wainMat.map === null && th.wains.tex) M.wainMat.userData.repeat1 = true;
      lightSources.push({ x: r.x, y: r.h * 0.8, z: r.z, color: th.mood.color, i: th.mood.i * 16, dist: Math.max(r.w, r.d) * 0.9 + 2, decay: 1.4, flicker: false, phase: 0, bias: -3 });
    } else {
      const ft = plankTexture(r.floorColor || pal().floor, pal().floorPattern).clone(); ft.needsUpdate = true; ft.repeat.set(r.w / 2, r.d / 2);
      fm = new THREE.MeshStandardMaterial({ map: ft, roughness: 0.6, name: 'floor_' + r.id }); M = { wall: mat(r.wallColor || pal().wall, { r: 0.92 }), trim: '#f1eee8', wainMat: null };
    }
    const floorGeo = new THREE.BoxGeometry(r.w + 2 * WT, 0.1, r.d + 2 * WT); if (th) scaleUV(floorGeo, (r.w + 2 * WT) / tile(th.floor), (r.d + 2 * WT) / tile(th.floor));
    const floor = new THREE.Mesh(floorGeo, fm); floor.position.set(r.x, -0.05, r.z); floor.receiveShadow = true; floor.name = 'floor'; floor.userData.roomId = r.id; rg.add(floor);
    const ceil = new THREE.Mesh(new THREE.BoxGeometry(r.w + 2 * WT, 0.06, r.d + 2 * WT), mat('#f7f5f0', { r: 1 })); ceil.position.set(r.x, r.h + 0.03, r.z); ceil.name = 'ceiling'; ceil.userData.ceiling = true; ceil.visible = S.ceiling; ceil.castShadow = false; rg.add(ceil);
    for (const w of Object.keys(WALLS)) rg.add(buildWall(r, w, M));
    levelGroup.add(rg); box.expandByPoint(new THREE.Vector3(r.x - r.w / 2, 0, r.z - r.d / 2)).expandByPoint(new THREE.Vector3(r.x + r.w / 2, r.h, r.z + r.d / 2));
  }
  const pg = new THREE.Group(); pg.name = 'props'; levelGroup.add(pg); let nl = 0; wallProps = [];
  for (const p of L().props) {
    const g = buildProp(p, style); pg.add(g);
    if (CATALOG[p.type]?.tags?.includes('ceiling-decor')) { g.userData.ceiling = true; g.visible = S.ceiling; } // vaults/ribs are part of the ceiling
    if (CATALOG[p.type]?.place === 'wall') { const a = THREE.MathUtils.degToRad(p.rot || 0); wallProps.push({ g, n: [Math.sin(a), Math.cos(a)] }); }
    const lt = lightOf(p); if (lt) lightSources.push({ x: p.x, y: (p.y || 0) + lt.y * (p.scale || 1), z: p.z, color: lt.color || pal().light, i: lt.i * 7, dist: 7, decay: 1.8, flicker: true, phase: (p.x * 7.3 + p.z * 3.1) % 6.28, bias: 0 });
  }
  if (!box.isEmpty()) { const c = box.getCenter(new THREE.Vector3()), s = box.getSize(new THREE.Vector3()); sun.target.position.copy(c); const m = Math.max(s.x, s.z) * 0.8 + 3; Object.assign(sun.shadow.camera, { left: -m, right: m, top: m, bottom: -m, near: 1, far: 60 }); sun.shadow.camera.updateProjectionMatrix(); sun.position.copy(c).add(new THREE.Vector3(m * 0.6, 18, m * 0.4)); }
  scene.background.set(L().style === 'luxe' ? '#0d0f14' : '#12151c');
  attachSelection(); renderer.shadowMap.needsUpdate = true;
  const need = neededKeys(L().props);
  if (need.length) ensureAssets(need).then(() => rebuild()); // lazy GLB download, then redraw with real models
}
function propGroup(id) { let f = null; levelGroup.traverse(o => { if (!f && o.userData.type && o.userData.propId === id && o.parent?.name === 'props') f = o; }); return f; }
function attachSelection() {
  const g = S.selProp && propGroup(S.selProp);
  if (g) { gizmo.attach(g); selBox.visible = true; selBox.box.setFromObject(g); } else { gizmo.detach(); selBox.visible = false; }
}
function commitGizmo() {
  const g = gizmo.object; if (!g) return; const p = prop(); if (!p) return;
  const nx = g.position.x, nz = g.position.z, nr = Math.round(THREE.MathUtils.radToDeg(g.rotation.y) * 10) / 10;
  if (Math.abs(nx - p.x) + Math.abs(nz - p.z) + Math.abs(nr - p.rot) < 1e-4) return;
  mutate(() => LV.moveProp(L(), p.id, nx, nz, nr));
}
gizmo.addEventListener('objectChange', () => { if (gizmo.object) selBox.box.setFromObject(gizmo.object); });

// ---------------------------------------------------------------- picking & placing
const ray = new THREE.Raycaster(), ndc = new THREE.Vector2(), floorPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
function pointer(e) { const b = renderer.domElement.getBoundingClientRect(); ndc.set(((e.clientX - b.left) / b.width) * 2 - 1, -((e.clientY - b.top) / b.height) * 2 + 1); ray.setFromCamera(ndc, camera); }
function floorPoint() { const v = new THREE.Vector3(); return ray.ray.intersectPlane(floorPlane, v) ? v : null; }
function roomAt(x, z) { return L().rooms.find(r => Math.abs(x - r.x) <= r.w / 2 && Math.abs(z - r.z) <= r.d / 2); }
let down = null;
renderer.domElement.addEventListener('pointerdown', e => { down = [e.clientX, e.clientY]; });
renderer.domElement.addEventListener('pointerup', e => {
  if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 4 || gizmo.dragging) return; down = null; pointer(e);
  if (S.placing) return place(S.placing);
  const hits = ray.intersectObjects(levelGroup.children, true).filter(h => h.object.visible && !h.object.userData.ceiling);
  for (const h of hits) { let o = h.object; while (o) { if (o.userData?.propId && o.parent?.name === 'props') { select({ prop: o.userData.propId }); return; } o = o.parent; } if (h.object.userData.roomId && h.object.name === 'floor') { select({ room: h.object.userData.roomId }); return; } }
  select({});
});
function select({ prop: pid = null, room: rid = null }) {
  S.selProp = pid; if (pid) S.selRoom = prop().room; else if (rid) S.selRoom = rid; refreshUI(); attachSelection();
}
function place(type) {
  const fp = floorPoint(); if (!fp) return; const r = roomAt(fp.x, fp.z); const def = CATALOG[type];
  if (!r) return toast('Click inside a room');
  let x = Math.round(fp.x * 10) / 10, z = Math.round(fp.z * 10) / 10, rot = 0, extra = {};
  if (def.place === 'wall') { const w = LV.nearestWall(r, { x, z }); const len = LV.wallLen(r, w); const t = THREE.MathUtils.clamp((x - r.x) * WALLS[w].tan[0] + (z - r.z) * WALLS[w].tan[1], -len / 2 + def.size[0] / 2, len / 2 - def.size[0] / 2); [x, z] = LV.wallPoint(r, w, t, def.size[1] / 2 + 0.005); rot = WALLS[w].rot; }
  else if (def.place === 'surface') { const host = L().props.filter(p => p.room === r.id && LV.hasTag(p, 'holds-decor')).find(p => LV.rectsOverlap(LV.rectOf(p), { cx: x, cz: z, hw: .05, hd: .05, rot: 0 })); if (!host) return toast('Drop onto a table, shelf or cabinet'); extra = { host: host.id, y: LV.topY(host) }; x = host.x; z = host.z; rot = host.rot; }
  else if (def.place === 'floor' && def.tags.includes('wall-hug')) { const w = LV.nearestWall(r, { x, z }); const near = [x, z]; const dist = { N: z - (r.z - r.d / 2), S: r.z + r.d / 2 - z, W: x - (r.x - r.w / 2), E: r.x + r.w / 2 - x }[w]; if (dist < 1.2) { const s = LV.wallSpots(L(), r, w, type, (x - r.x) * WALLS[w].tan[0] + (z - r.z) * WALLS[w].tan[1])[0]; if (s) { x = s.x; z = s.z; rot = s.rot; } } }
  const p = mutate(() => LV.addProp(L(), r, type, x, z, rot, extra)); S.selProp = p.id; S.selRoom = r.id; refreshUI(); attachSelection();
  const prob = def.place === 'floor' && LV.placementProblem(L(), r, p); if (prob) toast(`Placed - note: ${prob}`);
}

// ---------------------------------------------------------------- UI
function field(label, value, onChange, { type = 'number', step = 0.1, opts = null } = {}) {
  let inp; if (opts) { inp = el('select'); opts.forEach(o => inp.append(el('option', { value: o }, o))); inp.value = value; }
  else { inp = el('input', { type, step, value: value ?? '' }); if (type === 'color') inp.value = value || '#888888'; }
  inp.addEventListener('change', () => onChange(type === 'number' ? parseFloat(inp.value) : inp.value)); return el('div', { class: 'row' }, el('label', {}, label), inp);
}
function renderInspector() {
  const pane = $('#p-insp'); pane.innerHTML = ''; const p = prop(), r = room();
  if (p) {
    const def = CATALOG[p.type];
    pane.append(el('h3', {}, `${def?.label || p.type} `, el('small', {}, p.id)), el('div', { class: 'sec' },
      field('X', p.x, v => mutate(() => LV.moveProp(L(), p.id, v, p.z, p.rot))), field('Z', p.z, v => mutate(() => LV.moveProp(L(), p.id, p.x, v, p.rot))),
      field('Height', p.y || 0, v => mutate(() => p.y = v), {}), field('Rotation', p.rot, v => mutate(() => LV.moveProp(L(), p.id, p.x, p.z, v)), { step: 15 }),
      field('Scale', p.scale || 1, v => mutate(() => p.scale = Math.max(0.2, v)), { step: 0.05 }), field('Colour', p.color, v => mutate(() => p.color = v), { type: 'color' }),
      el('div', { class: 'row' }, el('button', { onclick: () => mutate(() => p.color = null) }, 'Reset colour'), el('button', { onclick: () => dupProp(p) }, 'Duplicate'), el('button', { onclick: () => delProp() }, 'Delete')),
      el('small', {}, `Source: ${hasExternal(p.type) ? 'Blender GLB asset' : 'procedural'} · hosted: ${p.host || '-'}`)));
    const prob = def?.place === 'floor' && r && LV.placementProblem(L(), r, p); if (prob) pane.append(el('div', { class: 'sec' }, el('span', { class: 'pill bad' }, prob)));
  } else if (r) {
    const f = LV.analyze(L(), r);
    pane.append(el('h3', {}, 'Room'), el('div', { class: 'sec' }, field('Name', r.name, v => mutate(() => r.name = v), { type: 'text' }), field('Type', r.type, v => mutate(() => r.type = v), { opts: LV.ROOM_TYPES }),
      field('Width', r.w, v => mutate(() => r.w = Math.max(2, v))), field('Depth', r.d, v => mutate(() => r.d = Math.max(2, v))), field('Height', r.h, v => mutate(() => r.h = Math.max(2, v))),
      field('X', r.x, v => mutate(() => LV.moveRoom(L(), r, v, r.z))), field('Z', r.z, v => mutate(() => LV.moveRoom(L(), r, r.x, v))),
      field('Theme', r.theme?.key || '', v => mutate(() => { r.theme = resolveTheme(v, pal(), Math.random); }), { opts: Object.keys(THEMES).filter(k => THEMES[k].styles.includes(L().style)) }),
      el('div', { class: 'row' }, el('button', { onclick: () => mutate(() => LV.assignThemes(L(), { reroll: true, only: r })) }, 'Re-roll theme'), el('button', { onclick: () => delRoom(r) }, 'Delete room'))),
      el('h3', {}, 'Openings'), el('div', { class: 'sec' }, ...LV.roomOpenings(L(), r).map(o => el('div', { class: 'row' }, el('span', { style: 'width:62px' }, `${o.type} ${o.wall}`), el('input', { type: 'number', step: 0.1, value: o.t, title: 'offset along wall', onchange: e => mutate(() => o.t = parseFloat(e.target.value)) }), el('input', { type: 'number', step: 0.1, value: o.w, title: 'width', onchange: e => mutate(() => o.w = Math.max(.5, parseFloat(e.target.value))) }), el('button', { onclick: () => mutate(() => L().openings = L().openings.filter(x => x !== o)) }, '×'))),
        el('div', { class: 'row' }, ...['N', 'S', 'E', 'W'].map(w => el('button', { onclick: () => mutate(() => LV.addOpening(L(), r, w, 'window', 0)) }, `+win ${w}`))),
        el('div', { class: 'row' }, ...['N', 'S', 'E', 'W'].map(w => el('button', { onclick: () => mutate(() => LV.addOpening(L(), r, w, 'door', 0.0)) }, `+door ${w}`)))),
      el('h3', {}, 'Analysis'), el('div', { class: 'sec' }, el('small', {}, `Richness ${f.score}/100 · fill ${(f.fill * 100) | 0}% · free square ${f.freeSquare} m · ${f.furnishedItems} pieces · lights ${f.lights} · plants ${f.plants} · wall art ${f.wallArt} · decor ${f.decor} · problems ${f.problems.length}`)));
  } else pane.append(el('div', { class: 'sec dim' }, 'Add a room to start.'));
}
function dupProp(p) { const q = mutate(() => LV.addProp(L(), LV.getRoom(L(), p.room), p.type, p.x + 0.4, p.z + 0.4, p.rot, { scale: p.scale, color: p.color, y: p.y })); S.selProp = q.id; refreshUI(); attachSelection(); }
function delProp() { const p = prop(); if (!p) return; mutate(() => LV.removeProp(L(), p.id)); S.selProp = null; refreshUI(); attachSelection(); }
function delRoom(r) { mutate(() => { L().rooms = L().rooms.filter(x => x !== r); L().props = L().props.filter(p => p.room !== r.id); L().openings = L().openings.filter(o => o.room !== r.id); }); S.selRoom = L().rooms[0]?.id || null; S.selProp = null; refreshUI(); }
function renderRooms() {
  const list = $('#roomList'); list.innerHTML = '';
  for (const r of L().rooms) { const f = LV.analyze(L(), r); list.append(el('div', { class: 'room' + (r.id === S.selRoom ? ' sel' : ''), onclick: () => { S.selRoom = r.id; S.selProp = null; refreshUI(); attachSelection(); focusRoom(r); } }, el('span', {}, r.name), el('span', { class: 'chip', title: 'richness score' }, f.score))); }
}
let catQuery = '';
function renderCatalog() {
  const box = $('#catalog'); box.innerHTML = ''; const groups = {}; const q = catQuery.trim().toLowerCase();
  for (const t of Object.keys(CATALOG)) {
    const d = CATALOG[t]; if (q && !(`${d.label} ${t} ${d.cat} ${d.pack || ''} ${d.tags.join(' ')}`.toLowerCase().includes(q))) continue;
    (groups[d.pack ? `${d.pack} · ${d.cat}` : d.cat] ||= []).push(t);
  }
  const keys = Object.keys(groups).sort((a, b) => (a.includes('·') - b.includes('·')) || a.localeCompare(b));
  if (!keys.length) box.append(el('div', { class: 'dim' }, 'No matches'));
  for (const c of keys) {
    const det = el('details', { class: 'cat' }, el('summary', {}, c + ' ', el('small', {}, `(${groups[c].length})`)),
      el('div', { class: 'grid' }, ...groups[c].map(t => el('button', { class: S.placing === t ? 'on' : '', title: CATALOG[t].external ? 'Blender asset' : hasExternal(t) ? 'has Blender variants' : '', onclick: () => { S.placing = S.placing === t ? null : t; renderCatalog(); renderer.domElement.style.cursor = S.placing ? 'crosshair' : ''; } }, CATALOG[t].label + (hasExternal(t) ? ' ★' : '')))));
    if (!c.includes('·') || q || groups[c].includes(S.placing)) det.open = true;
    box.append(det);
  }
}
$('#catSearch').addEventListener('input', e => { catQuery = e.target.value; renderCatalog(); });
function renderActions() {
  const box = $('#actions'); box.innerHTML = ''; const groups = {};
  ACTIONS.forEach(a => (groups[a.group] ||= []).push(a));
  for (const [g, as] of Object.entries(groups)) box.append(el('div', { class: 'dim', style: 'margin:6px 0 3px;font-size:11px;text-transform:uppercase' }, g), el('div', { class: 'grid' }, ...as.map(a => el('button', { class: 'btn-act', id: 'act-' + a.id, title: a.desc, onclick: () => manual(a.id) }, a.label))));
}
function renderHud() { const r = room(); const f = r && LV.analyze(L(), r); $('#hud').innerHTML = r ? `<b>${r.name}</b> · richness <b>${f.score}</b>/100 · ${f.furnishedItems} pieces · fill ${(f.fill * 100) | 0}%${f.problems.length ? ` · <span style="color:var(--no)">${f.problems.length} problems</span>` : ''}` : ''; }
function refreshPackSel() {
  const sel = $('#packSel'); sel.innerHTML = ''; sel.append(el('option', { value: '' }, 'no pack')); listPacks().forEach(k => sel.append(el('option', { value: k }, 'pack: ' + k))); sel.value = L().pack || '';
}
function refreshUI() { if ($('#packSel').value !== (L().pack || '')) $('#packSel').value = L().pack || ''; renderRooms(); renderInspector(); renderHud(); if (document.activeElement !== $('#jsonBox')) $('#jsonBox').value = JSON.stringify(L(), null, 1); $('#lvlName').value = L().meta.name; $('#styleSel').value = L().style; }
function refresh() { LV.assignThemes(L()); rebuild(); refreshUI(); try { localStorage.setItem('leveldez.level', JSON.stringify(L())); } catch {} }
function frameLevel() {
  const rs = L().rooms; if (!rs.length) return;
  const x0 = Math.min(...rs.map(r => r.x - r.w / 2)), x1 = Math.max(...rs.map(r => r.x + r.w / 2)), z0 = Math.min(...rs.map(r => r.z - r.d / 2)), z1 = Math.max(...rs.map(r => r.z + r.d / 2));
  const cx = (x0 + x1) / 2, cz = (z0 + z1) / 2, span = Math.max(x1 - x0, z1 - z0);
  orbit.target.set(cx, 0.5, cz); camera.position.set(cx + span * 0.15, span * 0.95 + 4, cz + span * 0.75 + 3);
}
function focusRoom(r) { orbit.target.set(r.x, 0.8, r.z); const d = Math.max(r.w, r.d) * 1.5 + 2; camera.position.set(r.x + d * 0.6, d * 0.95, r.z + d * 0.9); }

// ---------------------------------------------------------------- Decision panel
function log(e) {
  const box = $('#log'); const bar = e.p != null ? el('span', { class: 'bar', style: `width:${Math.round(e.p * 46)}px;background:${e.p >= .5 ? 'var(--yes)' : 'var(--no)'}` }) : '';
  const row = el('div', {}, el('span', { class: 'tag ' + e.kind }, e.kind === 'panel' ? 'ask' : e.kind), el('span', {}, e.kind === 'panel' ? `${e.title}: ` + e.items.map(i => `${i.label} ${(i.p * 100) | 0}%`).join(' · ') : e.text, e.p != null ? [' ', el('small', {}, `${(e.p * 100) | 0}%`), bar] : ''));
  box.prepend(row); updateStat();
}
function updateStat() { const s = $('#decStat'); s.textContent = DC.isOffline() ? 'offline (keyword mode)' : `${DC.stats.calls} calls · $${DC.stats.cost.toFixed(5)}`; s.className = 'pill' + (DC.isOffline() ? ' bad' : ''); }
function flash(id) { const b = $('#act-' + id); if (b) { b.classList.remove('hit'); void b.offsetWidth; b.classList.add('hit'); } }
function targets() { return $('#scopeAll').checked || !room() ? L().rooms : [room()]; }
const apply = (id, r, params = {}) => { const res = LV.runAction(L(), id, r, params, Math.floor(Math.random() * 1e9)); if (id === 'generate_layout') { S.selRoom = L().rooms[0]?.id || null; S.selProp = null; frameLevel(); } flash(id); rebuild(); refreshUI(); return res; };
function manual(id) { if (id === 'vary_surfaces') return busy(async () => { snapshot(); const rs = $('#scopeAll').checked || !room() ? L().rooms : [room()]; log({ kind: 'press', text: 'Vary surfaces: ' + await varySurfaces(rs) }); flash(id); });
  mutate(() => { const res = LV.runAction(L(), id, $('#scopeAll').checked ? null : room(), ACTION[id].params ? Object.fromEntries(ACTION[id].params.map(p => [p.key, p.def])) : {}, Date.now()); log({ kind: 'press', text: `${ACTION[id].label}: ${res.msg}` }); flash(id); if (id === 'generate_layout') { S.selRoom = L().rooms[0]?.id || null; S.selProp = null; frameLevel(); } }); }
async function varySurfaces(rooms) { // Decision picks a finish per room; local variety if it is unavailable
  let map = null;
  if (!DC.isOffline()) { try { map = await DC.chooseThemes(L(), rooms); } catch (e) { log({ kind: 'no', text: `Decision theme choice failed (${e.message}) - local variety instead` }); } }
  if (!map) { rooms.forEach(r => LV.assignThemes(L(), { reroll: true, only: r })); return `${rooms.length} room(s) re-themed locally`; }
  for (const r of rooms) { r.theme = resolveTheme(map[r.id], pal(), Math.random); }
  refresh(); return rooms.map(r => `${r.name} -> ${map[r.id]}`).join(' | ');
}
async function busy(fn) { if (S.busy) return; S.busy = true; document.querySelectorAll('#p-dec button').forEach(b => b.disabled = true); try { await fn(); } catch (e) { log({ kind: 'no', text: 'Decision error: ' + e.message }); } finally { S.busy = false; document.querySelectorAll('#p-dec button').forEach(b => b.disabled = false); updateStat(); } }

$('#bRoute').onclick = () => busy(async () => {
  const text = $('#cmd').value.trim(); if (!text) return; log({ kind: 'info', text: '> ' + text });
  let plan; try { plan = DC.isOffline() ? DC.routeOffline(text, S.selRoom) : await DC.route(L(), text, S.selRoom, log); } catch (e) { log({ kind: 'no', text: `Decision unavailable (${e.message}) - using keyword routing` }); plan = DC.routeOffline(text, S.selRoom); }
  if (!plan.steps.length) return log({ kind: 'no', text: 'No button matched that request.' });
  snapshot();
  for (const s of plan.steps) { if (s.id === 'generate_layout') plan.scope = 'all'; const rooms = plan.scope === 'all' ? L().rooms : [LV.getRoom(L(), plan.scope) || room()]; const a = ACTION[s.id], r = a.scope === 'level' ? null : rooms;
    if (s.id === 'vary_surfaces') { log({ kind: 'press', text: 'Vary surfaces - ' + await varySurfaces(rooms), p: s.p }); flash(s.id); rebuild(); continue; } const res = (r ? rooms : [null]).map(rm => apply(s.id, rm, s.params)); const msg = res.map(x => x.msg).filter(m => m !== 'nothing to do').join(' | ') || 'nothing to do'; log({ kind: 'press', text: `${a.label} - ${msg}`, p: s.p }); await new Promise(r => setTimeout(r, 120)); }
});
$('#cmd').addEventListener('keydown', e => { if (e.key === 'Enter') $('#bRoute').click(); });
$('#bAuto').onclick = () => busy(async () => {
  snapshot(); log({ kind: 'info', text: `Autopilot on ${targets().map(r => r.name).join(', ')}` });
  await DC.autopilot(L(), { rooms: targets, log, apply: (id, r, p) => apply(id, r, p), maxRounds: 4 });
});
$('#bCrit').onclick = () => busy(async () => { for (const r of targets()) { const c = await DC.critic(L(), r); log({ kind: 'critic', text: `${r.name}: "${c.label}" (${c.score.toFixed(1)}/4) · cohesive ${(c.cohesive * 100) | 0}% · cosy ${(c.cozy * 100) | 0}%` }); } });
$('#bAsk').onclick = () => busy(async () => { const q = $('#ask').value.trim(); if (!q) return; const p = await DC.freeAsk(L(), room(), q); log({ kind: p >= .5 ? 'yes' : 'no', text: `Q: ${q}`, p }); });
$('#ask').addEventListener('keydown', e => { if (e.key === 'Enter') $('#bAsk').click(); });
$('#bClearLog').onclick = () => $('#log').innerHTML = '';

// ---------------------------------------------------------------- export / import
const download = (blob, name) => { const a = el('a', { href: URL.createObjectURL(blob), download: name }); a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000); };
const slug = () => (L().meta.name || 'level').replace(/[^\w\-]+/g, '_');
async function serverSave(blob, ext) { try { const r = await fetch(`/api/save?name=${slug()}&ext=${ext}`, { method: 'POST', body: blob }); const j = await r.json(); return j.saved; } catch { return null; } }
$('#bJson').onclick = async () => { const blob = new Blob([JSON.stringify(L(), null, 2)], { type: 'application/json' }); download(blob, slug() + '.json'); const s = await serverSave(blob, 'json'); toast(s ? `Saved ${s}` : 'JSON downloaded'); };
$('#bGlb').onclick = async () => {
  await whenTexturesReady();
  S.exporting = true; selBox.visible = false; gizmo.detach(); levelGroup.traverse(o => { o.visible = o.userData.ceiling ? S.ceiling : true; });
  levelGroup.userData.leveldez = { name: L().meta.name, style: L().style, rooms: L().rooms.length, props: L().props.length };
  new GLTFExporter().parse(levelGroup, async buf => {
    S.exporting = false; attachSelection(); const blob = new Blob([buf], { type: 'model/gltf-binary' }); download(blob, slug() + '.glb'); const s = await serverSave(blob, 'glb'); toast(`GLB ${(buf.byteLength / 1024) | 0} KB${s ? ' · saved ' + s : ''}`);
  }, e => { S.exporting = false; toast('GLB export failed: ' + e.message); }, { binary: true, onlyVisible: true, maxTextureSize: 1024 });
};
function loadLevel(obj) { if (!Array.isArray(obj.rooms) || !Array.isArray(obj.props)) throw new Error('not a LevelDez level'); snapshot(); obj.openings ||= []; obj.meta ||= { name: 'Imported' }; obj.style ||= 'modern'; S.level = obj; S.selRoom = obj.rooms[0]?.id || null; S.selProp = null; refresh(); }
$('#bImport').onclick = () => $('#fileIn').click();
$('#fileIn').onchange = async e => { try { loadLevel(JSON.parse(await e.target.files[0].text())); toast('Imported'); } catch (x) { toast(x.message); } e.target.value = ''; };
$('#bApplyJson').onclick = () => { try { loadLevel(JSON.parse($('#jsonBox').value)); toast('Applied'); } catch (x) { toast('JSON error: ' + x.message); } };
$('#bCopyJson').onclick = () => navigator.clipboard.writeText($('#jsonBox').value).then(() => toast('Copied'));

// ---------------------------------------------------------------- header / misc
Object.keys(STYLES).forEach(s => $('#styleSel').append(el('option', { value: s }, s)));
$('#styleSel').onchange = e => mutate(() => ACTION.restyle.run({ level: L(), room: null, rnd: Math.random }, { style: e.target.value }));
$('#packSel').onchange = e => mutate(() => { L().pack = e.target.value || null; const n = LV.reskinLevel(L()); toast(L().pack ? `Pack ${L().pack}: ${n} props re-skinned` : `Pack off: ${n} props reverted`); });
$('#lvlName').onchange = e => mutate(() => L().meta.name = e.target.value);
LV.ROOM_TYPES.forEach(t => $('#newRoomType').append(el('option', { value: t }, t)));
$('#bAddRoom').onclick = () => { snapshot(); const r = ACTION.add_room.run({ level: L(), rnd: Math.random }, { type: $('#newRoomType').value }); if (!L().rooms.length) { } const nr = L().rooms.at(-1); S.selRoom = nr.id; refresh(); focusRoom(nr); };
$('#bLayout').onclick = () => {
  if ((L().rooms.length || L().props.length) && !confirm('Replace the current level with a generated floor plan? (Ctrl+Z restores it)')) return;
  snapshot(); const res = LV.runAction(L(), 'generate_layout', null, { size: $('#layoutSize').value }, Date.now());
  S.selRoom = L().rooms[0]?.id || null; S.selProp = null; frameLevel(); refresh(); toast(res.msg + ' - run Autopilot (all rooms) or Furnish core to fill them');
};
$('#bNew').onclick = () => {
  if ((L().rooms.length || L().props.length) && !confirm('Start a blank level? The current one is kept in undo history (Ctrl+Z).')) return;
  snapshot(); S.level = LV.newLevel(); S.selRoom = null; S.selProp = null; S.placing = null;
  camera.position.set(9, 9, 11); orbit.target.set(0, 0, 0); renderCatalog(); refresh(); toast('New blank level - add a room to begin');
};
$('#bUndo').onclick = undo; $('#bRedo').onclick = redo;
$('#bCeil').onclick = e => { S.ceiling = !S.ceiling; e.target.classList.toggle('on', S.ceiling); rebuild(); };
$('#bFx').onclick = e => { S.fx = !S.fx; e.target.classList.toggle('on', S.fx); };
$('#bFx').classList.toggle('on', S.fx);
$('#bCut').onclick = e => { S.cutaway = !S.cutaway; e.target.classList.toggle('on', S.cutaway); };
$('#bTop').onclick = e => { S.top = !S.top; e.target.classList.toggle('on', S.top); const r = room() || L().rooms[0]; if (S.top) { const t = orbit.target; camera.position.set(t.x, 22, t.z + 0.01); } else if (r) focusRoom(r); };
document.querySelectorAll('.tabs button').forEach(b => b.onclick = () => { document.querySelectorAll('.tabs button,.pane').forEach(x => x.classList.remove('on')); b.classList.add('on'); $('#p-' + b.dataset.tab).classList.add('on'); if (b.dataset.tab === 'blender') renderBlender(); });
addEventListener('keydown', e => {
  if (/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) return;
  if (e.key === 'Delete' || e.key === 'Backspace') delProp();
  else if (e.key === 'Escape') { S.placing = null; renderCatalog(); select({}); }
  else if (e.key.toLowerCase() === 'r' && prop()) { const p = prop(); mutate(() => LV.moveProp(L(), p.id, p.x, p.z, (p.rot + 45) % 360)); }
  else if (e.key.toLowerCase() === 't') $('#bTop').click();
  else if (e.ctrlKey && e.key.toLowerCase() === 'z') { e.preventDefault(); undo(); } else if (e.ctrlKey && e.key.toLowerCase() === 'y') { e.preventDefault(); redo(); }
});

// ---------------------------------------------------------------- Blender tab
async function renderBlender() {
  const pane = $('#p-blender'); pane.innerHTML = '<div class="sec dim">Checking…</div>';
  let st = {}, as = { files: [], manifest: {} }; try { st = await (await fetch('/api/status')).json(); as = await (await fetch('/api/assets')).json(); } catch {}
  pane.innerHTML = '';
  pane.append(el('h3', {}, 'Blender bridge'), el('div', { class: 'sec' }, el('span', { class: 'pill' + (st.blender ? '' : ' bad') }, st.blender ? 'Blender connected (:9876)' : 'Blender not reachable'),
    el('p', { class: 'dim' }, 'Assets are GLB files in /assets listed in assets/manifest.json. Any catalog type with a GLB uses the Blender model instead of the procedural one (★).'),
    el('div', { class: 'row' }, el('button', { class: 'pri', disabled: !st.blender, onclick: sendToBlender }, 'Import current GLB into Blender'), el('button', { onclick: async () => { const loaded = await loadExternalAssets(); renderCatalog(); refresh(); refreshPackSel(); toast(`Loaded ${loaded.length} Blender assets`); } }, 'Reload assets'))),
    el('h3', {}, 'Assets'), el('div', { class: 'sec' }, ...(Object.keys(as.manifest).length || as.files.length ? Object.entries(as.manifest).sort().map(([k, e]) => el('div', { class: 'row' }, el('span', { style: 'flex:1' }, k), el('span', { class: 'pill' }, e.as ? 'as ' + e.as : e.place || 'override'))) : [el('div', { class: 'dim' }, 'No assets yet. Put GLBs in assets/<pack>/ (a manifest.json is optional).')]),
      el('small', {}, `${as.files.length} GLB file(s) · ${Object.keys(as.manifest).length} manifest entries · packs: ${listPacks().join(', ') || 'none'}`)));
}
async function sendToBlender() {
  $('#bGlb').click(); await new Promise(r => setTimeout(r, 1500));
  const r = await fetch('/api/blender-import?name=' + slug()).then(r => r.json()).catch(e => ({ error: e.message })); toast(r.error ? 'Blender: ' + r.error : 'Imported into Blender');
}

// ---------------------------------------------------------------- boot
let t0 = performance.now();
function animate() {
  requestAnimationFrame(animate); orbit.update();
  if (!S.exporting) levelGroup.traverse(o => { if (o.userData.wall) { if (S.cutaway && !S.top) { const [bx, bz] = o.userData.base, [nx, nz] = o.userData.inward; o.visible = ((camera.position.x - bx) * nx + (camera.position.z - bz) * nz) > 0; } else o.visible = true; } });
  for (const w of wallProps) w.g.visible = S.exporting || !S.cutaway || S.top || ((camera.position.x - w.g.position.x) * w.n[0] + (camera.position.z - w.g.position.z) * w.n[1]) > 0;
  const tt = performance.now() / 1000; updateLights(tt); updateDust(tt);
  if (S.fx && !S.exporting) { grade.uniforms.uTime.value = tt % 10; composer.render(); } else renderer.render(scene, camera);
}
await loadTextureManifest(); LV.assignThemes(L());
resize(); renderCatalog(); renderActions(); rebuild(); refreshUI(); animate(); focusRoom(room());
loadExternalAssets().then(l => { refreshPackSel(); if (l.length) { renderCatalog(); refresh(); } });
fetch('/api/status').then(r => r.json()).then(s => { if (!s.hasKey) DC.setOffline(true); $('#decStat').title = s.model; updateStat(); }).catch(() => { DC.setOffline(true); updateStat(); });
window.LD = { S, LV, DC, apply, refresh, camera, orbit, THREE, renderer }; // handy for debugging in the console
