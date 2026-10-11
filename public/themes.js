// Room themes: wall finish + floor finish + wainscot + mood light. Pure data (no THREE) so level.js and decision.js can use it.
// wall.pattern: plaster | stone_blocks | moss_stone | brick | damask | stripes | panels | tiles | bone_plaster
// floor.pattern: flagstone | checker | plank | herringbone | cobble | diamond | marble | carpet
// wains: lower wall band { pattern: panels|planks|stone, color } or null;  mood: { color, i } fill light for the room
const T = (label, desc, wall, floor, wains, trim, mood, styles = ['gothic']) => ({ label, desc, wall, floor, wains, trim, mood, styles });
const W = (pattern, color, color2, tile = 2) => ({ pattern, color, color2, tile });
const F = (pattern, color, color2, tile = 2) => ({ pattern, color, color2, tile });

export const THEMES = {
  crypt_stone: T('Crypt stone', 'cold damp crypt: mossy stone blocks, cobblestone floor, green-cyan glow', W('moss_stone', '#4a4d52', '#3f6b45', 2), F('cobble', '#3a3c40', '#202226', 2), null, '#2a2c30', { color: '#3ad6b0', i: 0.55 }),
  catacomb_brick: T('Catacomb brick', 'dark blackened brick catacomb, flagstone floor, dim amber light', W('brick', '#3a2420', '#1d1210', 2), F('flagstone', '#2e2c2e', '#1a1a1c', 2), { pattern: 'stone', color: '#26262a' }, '#1d1d20', { color: '#ff9a3c', i: 0.45 }),
  chapel_marble: T('Chapel marble', 'sacred chapel: pale stone blocks, black and white marble checker floor, violet and golden glow', W('stone_blocks', '#8d8a86', '#6e6c68', 2), F('checker', '#d9d6cf', '#1b1b1f', 2), null, '#c9c5bd', { color: '#b88cff', i: 0.6 }),
  scholar_green: T('Scholar green', 'scholar library: deep green damask wallpaper, dark oak wainscot, plank floor, warm amber light', W('damask', '#17352b', '#c9a24b', 2), F('plank', '#3a2416', '#241409', 2), { pattern: 'panels', color: '#2b1a10' }, '#c9a24b', { color: '#ffb35a', i: 0.55 }),
  velvet_crimson: T('Velvet crimson', 'bedchamber: crimson damask wallpaper, dark panelled wainscot, plank floor, warm red glow', W('damask', '#5a0f1c', '#d4af37', 2), F('plank', '#2f1b12', '#1c0f08', 2), { pattern: 'panels', color: '#241109' }, '#d4af37', { color: '#ff4a4a', i: 0.5 }),
  alchemist_teal: T('Alchemist teal', 'alchemy laboratory: dark teal glazed tiles, diamond tile floor, green and violet glow', W('tiles', '#1d4a4a', '#0e2424', 2), F('diamond', '#2b2f33', '#14383a', 2), null, '#0e2424', { color: '#59ff9a', i: 0.6 }),
  oak_study: T('Oak study', 'study with oak panelled walls, herringbone floor, amber light', W('panels', '#4a2d18', '#2d1a0d', 2), F('herringbone', '#3b2515', '#22140a', 2), null, '#2d1a0d', { color: '#ffb35a', i: 0.5 }),
  manor_stripes: T('Manor stripes', 'manor dining room: burgundy and gold striped wallpaper, panelled wainscot, checker floor, warm candlelight', W('stripes', '#4a1018', '#2a0a10', 2), F('checker', '#2a2024', '#120c0e', 2), { pattern: 'panels', color: '#2a170d' }, '#d4af37', { color: '#ff9a3c', i: 0.55 }),
  violet_salon: T('Violet salon', 'salon: purple damask wallpaper, herringbone floor, cool violet light', W('damask', '#2f1747', '#b9a0d8', 2), F('herringbone', '#2c2230', '#17111b', 2), { pattern: 'panels', color: '#1d1224' }, '#b9a0d8', { color: '#a070ff', i: 0.55 }),
  bone_plaster: T('Bone plaster', 'ossuary: stained bone-white plaster, flagstone floor, cold pale light', W('bone_plaster', '#9b9484', '#5a5448', 2), F('flagstone', '#58554f', '#2b2a27', 2), null, '#7a7466', { color: '#cfe0ff', i: 0.4 }),
  obsidian_ritual: T('Obsidian ritual', 'ritual chamber: black polished stone blocks, veined marble floor, purple rune glow', W('stone_blocks', '#16161c', '#0a0a0e', 2), F('marble', '#1a1a22', '#6a4aa8', 2), null, '#2a1a44', { color: '#9a5cff', i: 0.7 }),
  mossy_dungeon: T('Mossy dungeon', 'dungeon: moss-covered rough stone, cobble floor, damp green light', W('moss_stone', '#3b3f3c', '#2f5a30', 2), F('cobble', '#2c302d', '#161916', 2), null, '#1d211e', { color: '#6fd070', i: 0.45 }),
  grand_hall: T('Grand hall', 'grand hall: tall pale stone blocks, big checker marble floor, golden light', W('stone_blocks', '#6f6a63', '#524e48', 2), F('checker', '#cfc9bd', '#2a2623', 2), { pattern: 'stone', color: '#4e4a44' }, '#b9a98a', { color: '#ffc870', i: 0.6 }),
  tiled_bath: T('Tiled bath', 'bathroom: white and black tiles, diamond tile floor, cool light', W('tiles', '#cfd2d4', '#5a5d60', 2), F('diamond', '#d8dadc', '#2a2c2e', 2), null, '#8a8d90', { color: '#bfe4ff', i: 0.4 }),
  rust_kitchen: T('Rust kitchen', 'kitchen: rough warm brick, flagstone floor, hot orange light', W('brick', '#6a3524', '#2a140c', 2), F('flagstone', '#4a423a', '#26211c', 2), { pattern: 'planks', color: '#3a2415' }, '#2a140c', { color: '#ff8a30', i: 0.55 }),
  gallery_noir: T('Noir gallery', 'portrait gallery: black damask wallpaper with silver pattern, marble floor, cool white light', W('damask', '#16161a', '#9aa0aa', 2), F('marble', '#24242a', '#8a8f9a', 2), { pattern: 'panels', color: '#0e0e12' }, '#9aa0aa', { color: '#cfd6ff', i: 0.45 }),
  // sci-fi (pack: scifi)
  hull_white: T('Hull white', 'clean white ship hull: pale tile panels, dark diamond deck plating, cool cyan light', W('tiles', '#d7dde3', '#aab4be', 2), F('diamond', '#59626e', '#2a3038', 2), null, '#7e8a96', { color: '#7fe6ff', i: 0.45 }, ['scifi']),
  bridge_navy: T('Bridge navy', 'command deck: dark navy panels, checker deck plating, blue instrument glow', W('panels', '#1b2a40', '#101a2a', 2), F('checker', '#2a3140', '#11151d', 2), null, '#2d6a8a', { color: '#4fb8ff', i: 0.6 }, ['scifi']),
  neon_noir: T('Neon noir', 'cyberpunk lounge: deep purple walls, black diamond floor, hot magenta neon', W('plaster', '#241633', '#140c1e', 2), F('diamond', '#1c1626', '#0d0a12', 2), null, '#5b2a7a', { color: '#ff3fb0', i: 0.65 }, ['scifi']),
  lab_clean: T('Clean lab', 'sterile laboratory: white tiles, light diamond floor, mint light', W('tiles', '#e6eef2', '#b9cad2', 2), F('diamond', '#cbd5db', '#8d9aa3', 2), null, '#8fa3ad', { color: '#9fffe0', i: 0.45 }, ['scifi']),
  cargo_grey: T('Cargo grey', 'cargo deck: scuffed grey panels, flagstone-like deck, amber work light', W('panels', '#5b636b', '#3a4046', 2), F('flagstone', '#3a3d42', '#202226', 2), null, '#d9a521', { color: '#ffb04a', i: 0.5 }, ['scifi']),
  hydro_green: T('Hydroponic green', 'grow deck: deep green tiles, dark plank floor, magenta grow-light wash', W('tiles', '#16352e', '#0b1f1a', 2), F('plank', '#2a3a30', '#16211a', 2), null, '#2f7a5c', { color: '#ff4fd0', i: 0.55 }, ['scifi']),
  crew_amber: T('Crew quarters', 'cosy crew cabin: charcoal stripes, checker floor, warm amber light', W('stripes', '#33363d', '#23252b', 2), F('checker', '#2b2d33', '#17181c', 2), null, '#8a6a3a', { color: '#ffb35a', i: 0.45 }, ['scifi']),
  med_white: T('Medbay white', 'medbay: soft white plaster, pale diamond floor, clean green-white light', W('plaster', '#e3ecef', '#b4c3c9', 2), F('diamond', '#aeb9bf', '#79858c', 2), null, '#8fa3ad', { color: '#bfffe8', i: 0.4 }, ['scifi']),
  // non-gothic styles (colours are replaced by the style palette when applied)
  plain_plaster: T('Plain plaster', 'simple plastered walls with a plank floor', W('plaster', '@wall', '@wall2', 2), F('plank', '@floor', '@floor2', 2), null, '@wall2', { color: '#fff1d6', i: 0.35 }, ['modern', 'scandi', 'rustic', 'industrial', 'luxe']),
  soft_stripes: T('Soft stripes', 'light striped wallpaper with wainscot and checker floor', W('stripes', '@wall', '@wall2', 2), F('checker', '@floor', '@floor2', 2), { pattern: 'panels', color: '@wood' }, '@wall2', { color: '#fff1d6', i: 0.35 }, ['modern', 'scandi', 'rustic', 'luxe']),
  warm_panels: T('Warm panels', 'wood panelled walls and herringbone floor', W('panels', '@wood', '@wood2', 2), F('herringbone', '@floor', '@floor2', 2), null, '@wood2', { color: '#ffd9a0', i: 0.4 }, ['modern', 'scandi', 'rustic', 'industrial', 'luxe']),
  loft_brick: T('Loft brick', 'exposed brick walls with flagstone floor', W('brick', '@accent', '@wall2', 2), F('flagstone', '@floor', '@floor2', 2), null, '@wall2', { color: '#ffe2b8', i: 0.35 }, ['modern', 'rustic', 'industrial']),
  soft_damask: T('Soft damask', 'damask wallpaper with plank floor', W('damask', '@wall', '@accent', 2), F('plank', '@floor', '@floor2', 2), { pattern: 'panels', color: '@wood' }, '@accent', { color: '#fff1d6', i: 0.35 }, ['modern', 'scandi', 'luxe']),
  clean_tiles: T('Clean tiles', 'tiled walls and diamond tile floor', W('tiles', '@wall', '@wall2', 2), F('diamond', '@floor', '@floor2', 2), null, '@wall2', { color: '#e8f4ff', i: 0.3 }, ['modern', 'scandi', 'rustic', 'industrial', 'luxe']),
};

// themes that suit each room type, best first
export const TYPE_THEMES = {
  gothic: { crypt: ['crypt_stone', 'mossy_dungeon', 'bone_plaster', 'catacomb_brick'], chapel: ['chapel_marble', 'obsidian_ritual', 'grand_hall'], library: ['scholar_green', 'oak_study', 'violet_salon'],
    laboratory: ['alchemist_teal', 'mossy_dungeon', 'bone_plaster', 'obsidian_ritual'], bedroom: ['velvet_crimson', 'violet_salon', 'manor_stripes', 'oak_study'], office: ['oak_study', 'scholar_green', 'gallery_noir'],
    dining: ['manor_stripes', 'velvet_crimson', 'grand_hall'], living: ['violet_salon', 'velvet_crimson', 'gallery_noir', 'manor_stripes'], hall: ['grand_hall', 'gallery_noir', 'chapel_marble'],
    corridor: ['catacomb_brick', 'crypt_stone', 'gallery_noir', 'bone_plaster'], classroom: ['oak_study', 'scholar_green', 'gallery_noir'], dormitory: ['velvet_crimson', 'oak_study', 'violet_salon', 'manor_stripes'], ritual: ['obsidian_ritual', 'crypt_stone', 'chapel_marble'], bathroom: ['tiled_bath', 'alchemist_teal'], kitchen: ['rust_kitchen', 'catacomb_brick'] },
  scifi: { bedroom: ['crew_amber', 'neon_noir', 'hull_white'], dormitory: ['crew_amber', 'hull_white', 'neon_noir'], office: ['bridge_navy', 'hull_white'], laboratory: ['lab_clean', 'hydro_green', 'med_white', 'hull_white'],
    hall: ['hull_white', 'cargo_grey', 'bridge_navy'], corridor: ['hull_white', 'cargo_grey', 'bridge_navy'], kitchen: ['cargo_grey', 'hull_white', 'lab_clean'], dining: ['crew_amber', 'hull_white', 'cargo_grey'],
    living: ['neon_noir', 'crew_amber', 'bridge_navy'], bathroom: ['lab_clean', 'med_white'], classroom: ['bridge_navy', 'hull_white'], library: ['bridge_navy', 'neon_noir', 'hydro_green'], default: ['hull_white', 'bridge_navy', 'neon_noir', 'lab_clean', 'cargo_grey', 'hydro_green', 'crew_amber', 'med_white'] },
  plain: { default: ['plain_plaster', 'soft_stripes', 'warm_panels', 'soft_damask', 'loft_brick'], bathroom: ['clean_tiles'], kitchen: ['loft_brick', 'clean_tiles', 'plain_plaster'], corridor: ['plain_plaster', 'warm_panels'] },
};

const hex = c => { const n = parseInt(c.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
const toHex = a => '#' + a.map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, '0')).join('');
export const shade = (c, f) => toHex(hex(c).map(v => v * f));
export const mix = (a, b, t) => { const A = hex(a), B = hex(b); return toHex(A.map((v, i) => v + (B[i] - v) * t)); };

// resolve '@wall' style placeholders against a style palette, and apply a little per-room variation
const THEME_TEX = { // [wall, floor, wainscot]
  crypt_stone: ['wall_moss_stone', 'floor_cobble_dark', null], catacomb_brick: ['wall_brick_dark', 'floor_flagstone_dark', 'wain_stone'], chapel_marble: ['wall_stone_pale', 'floor_checker_marble', null],
  scholar_green: ['wall_damask_green', 'floor_plank_dark', 'wain_oak_dark'], velvet_crimson: ['wall_damask_crimson', 'floor_plank_dark', 'wain_oak_dark'], alchemist_teal: ['wall_tiles_teal', 'floor_diamond_teal', null],
  oak_study: ['wall_panels_oak', 'floor_herringbone_oak', null], manor_stripes: ['wall_stripes_burgundy', 'floor_checker_dark', 'wain_oak_dark'], violet_salon: ['wall_damask_purple', 'floor_herringbone_dark', 'wain_oak_dark'],
  bone_plaster: ['wall_plaster_bone', 'floor_flagstone_warm', null], obsidian_ritual: ['wall_obsidian_blocks', 'floor_marble_black', null], mossy_dungeon: ['wall_stone_rough', 'floor_cobble_dark', null],
  grand_hall: ['wall_stone_pale', 'floor_checker_marble', 'wain_stone'], tiled_bath: ['wall_tiles_white', 'floor_diamond_bw', null], rust_kitchen: ['wall_brick_warm', 'floor_flagstone_warm', 'wain_planks'],
  gallery_noir: ['wall_damask_noir', 'floor_marble_black', 'wain_oak_dark'],
  hull_white: ['n_wall_tiles', 'n_floor_diamond', null], bridge_navy: ['n_wall_panels', 'n_floor_checker', null], neon_noir: ['n_wall_plaster', 'n_floor_diamond', null], lab_clean: ['n_wall_tiles', 'n_floor_diamond', null],
  cargo_grey: ['n_wall_panels', 'n_floor_flagstone', null], hydro_green: ['n_wall_tiles', 'n_floor_plank', null], crew_amber: ['n_wall_stripes', 'n_floor_checker', null], med_white: ['n_wall_plaster', 'n_floor_diamond', null],
  plain_plaster: ['n_wall_plaster', 'n_floor_plank', null], soft_stripes: ['n_wall_stripes', 'n_floor_checker', 'wain_planks'], warm_panels: ['n_wall_panels', 'n_floor_herringbone', null],
  loft_brick: ['n_wall_brick', 'n_floor_flagstone', null], soft_damask: ['n_wall_damask', 'n_floor_plank', 'wain_planks'], clean_tiles: ['n_wall_tiles', 'n_floor_diamond', null],
};

export function resolveTheme(key, pal, rnd = Math.random) {
  const th = THEMES[key]; if (!th) return null;
  const sub = c => typeof c !== 'string' || c[0] !== '@' ? c : ({ '@wall': pal.wall, '@wall2': shade(pal.wall, 0.78), '@floor': pal.floor, '@floor2': shade(pal.floor, 0.6), '@wood': pal.wood, '@wood2': shade(pal.wood, 0.6), '@accent': pal.accent })[c];
  const jit = c => (typeof c === 'string' && c[0] === '#' && rnd) ? shade(c, 0.9 + rnd() * 0.2) : c;
  return {
    key, wall: { ...th.wall, tex: (THEME_TEX[key] || [])[0], color: jit(sub(th.wall.color)), color2: sub(th.wall.color2) }, floor: { ...th.floor, tex: (THEME_TEX[key] || [])[1], color: jit(sub(th.floor.color)), color2: sub(th.floor.color2) },
    wains: th.wains ? { ...th.wains, tex: (THEME_TEX[key] || [])[2] || null, color: sub(th.wains.color) } : null, trim: sub(th.trim), mood: { ...th.mood },
  };
}
