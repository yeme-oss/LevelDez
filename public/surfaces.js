// Wall / floor / wainscot materials from the AI texture library (assets/textures/manifest.json), with plain-colour fallbacks.
import * as THREE from 'three';
import { mix } from './themes.js';

let manifest = {};
const bases = new Map();   // texture id -> Promise<THREE.Texture> (loaded once, cloned per use)
const loader = new THREE.TextureLoader();
const pending = new Set();

export async function loadTextureManifest() {
  try { manifest = await (await fetch('/assets/textures/manifest.json', { cache: 'no-cache' })).json(); } catch { manifest = {}; }
  return Object.keys(manifest).length;
}
export const textureIds = () => Object.keys(manifest);
export const hasTexture = id => !!manifest[id];
export const whenTexturesReady = () => Promise.all([...pending]);

function baseTexture(id) {
  if (!bases.has(id)) {
    const p = new Promise(res => loader.load('/assets/textures/' + manifest[id].file, t => { t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 8; res(t); }, undefined, () => res(null)));
    bases.set(id, p);
  }
  return bases.get(id);
}
const details = new Map();
// neutral grayscale detail map (linear, repeating); returns a Texture immediately, pixels arrive when loaded
export function detailTexture(id) {
  if (!manifest[id]) return null;
  if (!details.has(id)) { const t = loader.load('/assets/textures/' + manifest[id].file); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.NoColorSpace; t.anisotropy = 8; details.set(id, t); }
  return details.get(id);
}

function roughnessFor(id) { return /marble|checker|diamond|tiles/.test(id) ? 0.35 : /plank|herring|wain|panel/.test(id) ? 0.55 : 0.92; }

// A material for `spec` ({tex, color, ...}). `repeat` = [u, v] tiles across the surface. Textures apply when they arrive (no rebuild needed).
export function surfaceMaterial(spec, repeat, { name = 'surface', bump = 1.0, bright = 1.0 } = {}) {
  const info = spec.tex && manifest[spec.tex];
  const m = new THREE.MeshStandardMaterial({ color: info ? (info.neutral ? mix('#ffffff', spec.color || '#888888', 0.85) : '#ffffff') : (spec.color || '#777777'), roughness: info ? roughnessFor(spec.tex) : 0.9, metalness: 0.0 });
  m.name = name; if (info && bright !== 1) m.color.multiplyScalar(bright);
  if (info) {
    const p = pending.add(baseTexture(spec.tex).then(t => {
      if (!t) return;
      const tex = t.clone(); tex.needsUpdate = true; tex.userData.mimeType = 'image/jpeg'; tex.repeat.set(repeat[0], repeat[1]);
      m.map = tex; m.bumpMap = tex; m.bumpScale = bump * (/stone|brick|cobble|flag|moss|obsidian/.test(spec.tex) ? 1.6 : 0.5); m.needsUpdate = true;
    }));
  }
  return m;
}
