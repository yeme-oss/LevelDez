// Decision-1 integration. The model returns calibrated probabilities for fixed answer options, so we use it as:
//  * ROUTER  : natural language -> which buttons to press (one batched yes/no panel, one `choice` per parameter)
//  * ADVISOR : autopilot asks gated yes/no "taste" questions about each room and presses the buttons it says yes to
//  * CRITIC  : a 5-level `score` rating of how furnished a room feels closes the loop (sparse -> fill, cluttered -> declutter)
import { ACTIONS, ACTION, describe, analyze } from './level.js';
import { THEMES } from './themes.js';

export const stats = { calls: 0, cost: 0, inTok: 0 };
export const THRESHOLD = 0.5;
let offline = false;
export const isOffline = () => offline;
export function setOffline(v) { offline = v; }

export async function decide(state, questions) {
  stats.calls++;
  const r = await fetch('/api/decide', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ state, questions }) });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) { offline = true; throw new Error(j.error || `HTTP ${r.status}`); }
  stats.cost = j.stats?.cost ?? stats.cost; stats.inTok = j.stats?.promptTokens ?? stats.inTok;
  return j.answers;
}
const noul = instructions => ({ type: 'noul', instructions });
const pYes = a => a?.noul ?? 0;

// execution order: structure first, then furniture, then dressing, then repair, finally style
const PHASE = ['restyle', 'reskin', 'generate_layout', 'add_room', 'vary_surfaces', 'resize_room', 'add_window', 'add_door', 'clear_room', 'furnish_core', 'compose_room', 'fill_empty', 'add_nightstands', 'add_rug', 'add_lighting', 'add_curtains', 'add_architecture', 'add_plants', 'add_wall_art', 'add_decor', 'add_clutter', 'declutter', 'face_focus', 'snap_walls', 'fix_problems', 'mirror_layout'];
export const byPhase = (a, b) => PHASE.indexOf(a.id) - PHASE.indexOf(b.id);

// ---- ROUTER -----------------------------------------------------------------
const ROUTABLE = ACTIONS.filter(a => a.id !== 'clear_room'); // destructive: only on explicit keyword
export async function route(L, text, selectedId, log) {
  const state = { user_request: text, level: L.rooms.map(r => describe(L, r)) };
  const qs = {};
  for (const a of ACTIONS) qs[a.id] = noul(`Does the user's request require pressing the button "${a.label}" (${a.desc})? Answer yes only if this button directly helps fulfil the request.`);
  qs.__whole_level = noul('Does the user request explicitly refer to the whole level, the entire house, or every room (rather than one specific room)?');
  const hasMany = L.rooms.length > 1;
  const roomCrit = { __selected: 'the request does not name a room, so it applies to the currently selected room' };
  L.rooms.forEach(r => roomCrit[r.id] = `the room called "${r.name}" (${r.type})`);
  if (hasMany) qs.__room = { type: 'choice', instructions: 'Which room does the user request target?', criteria: roomCrit };
  const ans = await decide(state, qs);
  let steps = ACTIONS.filter(a => pYes(ans[a.id]) >= THRESHOLD && (a.id !== 'clear_room' || /clear|empty|wipe|reset|start over|remove everything/i.test(text)))
    .map(a => ({ id: a.id, p: pYes(ans[a.id]), params: {} })).sort((x, y) => byPhase(x, y));
  if (steps.some(s => s.id === 'generate_layout')) steps = steps.filter(s => s.id !== 'add_room'); // a generated plan already includes its corridors and rooms
  log?.({ kind: 'panel', title: 'Router panel', items: ACTIONS.map(a => ({ label: a.label, p: pYes(ans[a.id]) })).sort((a, b) => b.p - a.p).slice(0, 8) });
  // parameters (one batched choice call)
  const pq = {};
  for (const s of steps) for (const prm of ACTION[s.id].params || []) if (!prm.multi) pq[`${s.id}.${prm.key}`] = { type: 'choice', instructions: `Which option does the user want for ${ACTION[s.id].label}?`, criteria: prm.criteria };
  if (Object.keys(pq).length) {
    const pa = await decide(state, pq);
    for (const s of steps) for (const prm of ACTION[s.id].params || []) if (!prm.multi) { const c = pa[`${s.id}.${prm.key}`]; s.params[prm.key] = c?.choice ?? prm.def; log?.({ kind: 'param', text: `${ACTION[s.id].label}.${prm.key} -> ${s.params[prm.key]}`, p: c?.confidence }); }
  }
  // multi-valued parameters (e.g. several rooms in one sentence): one yes/no per option, one step per approved option
  for (const s of [...steps]) for (const prm of ACTION[s.id].params || []) if (prm.multi) {
    const q2 = Object.fromEntries(Object.entries(prm.criteria).map(([k, d]) => [k, noul(`Does the user request ask for ${d} to be added?`)]));
    const a2 = await decide(state, q2), picked = Object.keys(prm.criteria).filter(k => pYes(a2[k]) >= THRESHOLD);
    log?.({ kind: 'param', text: `${ACTION[s.id].label}.${prm.key} -> ${picked.join(', ') || prm.def + ' (default)'}`, p: Math.max(...Object.keys(prm.criteria).map(k => pYes(a2[k]))) });
    const at = steps.indexOf(s); steps.splice(at, 1, ...(picked.length ? picked : [prm.def]).map(k => ({ ...s, params: { ...s.params, [prm.key]: k } })));
  }
  let scope = 'selected';
  if (!hasMany) scope = 'all'; else if (pYes(ans.__whole_level) >= THRESHOLD) scope = 'all'; else if (ans.__room?.choice && ans.__room.choice !== '__selected') scope = ans.__room.choice;
  return { steps, scope: scope === 'selected' ? (selectedId || 'all') : scope };
}
// offline fallback: keyword matching
export function routeOffline(text, selectedId) {
  const t = text.toLowerCase();
  const steps = ACTIONS.filter(a => a.id !== 'clear_room' || /clear|empty the|wipe|reset/.test(t)).filter(a => a.keywords.some(k => t.includes(k))).map(a => ({ id: a.id, p: 1, params: {} })).sort(byPhase);
  for (const s of steps) for (const prm of ACTION[s.id].params || []) { const hit = Object.keys(prm.criteria).find(k => t.includes(k) || (k === 'smaller' && /small|shrink/.test(t))); s.params[prm.key] = hit || prm.def; }
  return { steps, scope: /whole|entire|all rooms|every room/.test(t) ? 'all' : (selectedId || 'all') };
}

// ---- ADVISOR / autopilot ----------------------------------------------------
const area = f => f.area;
export const PROBES = [
  { id: 'furnish_core', gate: f => f.furnishedItems === 0, q: 'Is this room empty, so that its core furniture should be placed now?' },
  { id: 'compose_room', gate: f => f.furnishedItems > 0 && f.composed === 0 && f.fill < 0.26 && f.area >= 9, q: 'Does the furniture look scattered and the room underdesigned, lacking cohesive themed setups such as a reading nook, altar arrangement, workbench group or lounge?' },
  { id: 'fill_empty', gate: f => f.furnishedItems > 0 && f.fill < 0.2, q: 'Does this room look sparse, with a large empty floor area that more furniture should fill?' },
  { id: 'add_window', gate: f => f.windows === 0 && f.furnishedItems > 0, q: 'Does this room lack natural light and need a window?' },
  { id: 'add_nightstands', gate: f => f.beds > 0 && f.nightstands < 2 * f.beds, q: 'Does the bed lack bedside tables that a bedroom would normally have?' },
  { id: 'add_rug', gate: f => !f.hasRug && (f.seating > 0 || f.hasBed || f.cats.table > 0) && f.furnishedItems > 1, q: 'Would a rug under the main furniture group make this room feel warmer and more finished?' },
  { id: 'add_lighting', gate: f => f.lights < Math.max(1, Math.round(area(f) / 10)) && f.furnishedItems > 0, q: 'Is the lighting insufficient for the room to feel comfortable and inviting?' },
  { id: 'add_curtains', gate: f => f.windowsBare > 0 && f.furnishedItems > 0, q: 'Do the bare windows need curtains to look finished?' },
  { id: 'add_plants', gate: f => f.freeCorners.length > 0 && f.plants < Math.round(area(f) / 9) && f.furnishedItems > 0, q: 'Would greenery in empty corners improve the atmosphere of this room?' },
  { id: 'add_wall_art', gate: f => f.wallArt < f.wallArtTarget && f.furnishedItems > 0, q: 'Do the walls look bare and need paintings, mirrors or shelves?' },
  { id: 'add_architecture', gate: f => f.packActive && f.furnishedItems > 0 && f.arch < 3, q: 'Do the bare walls, windows, doors and ceiling need gothic architectural detail such as pillars, window tracery and ceiling vaults?' },
  { id: 'add_clutter', gate: f => f.packActive && f.furnishedItems > 0 && f.clutter < Math.round(f.area / 7), q: 'Does the room look too tidy and need lived-in clutter such as barrels, crates, bone heaps and statues?' },
  { id: 'add_decor', gate: f => f.hostsBare > 0, q: 'Do the table, shelf and cabinet surfaces look bare and need small decorative items?' },
  { id: 'declutter', gate: f => f.fill > 0.32, q: 'Is the room too cramped to move through comfortably?' },
];
export const FIX = { id: 'fix_problems', gate: f => f.problems.length > 0 };

// THEMES: one batched `choice` per room (Decision-1 sees the room's type/size and the level), then a greedy assignment that
// penalises reuse so neighbouring rooms stay distinct. Returns { roomId: themeKey }.
export async function chooseThemes(L, rooms) {
  const keys = Object.keys(THEMES).filter(k => THEMES[k].styles.includes(L.style));
  const criteria = Object.fromEntries(keys.map(k => [k, THEMES[k].desc]));
  const state = { style: L.style, asset_pack: L.pack || 'none', rooms: L.rooms.map(r => `${r.name}: ${r.type}, ${r.w}x${r.d} m`) };
  const qs = Object.fromEntries(rooms.map(r => [r.id, { type: 'choice', instructions: `Which wall, floor and lighting finish best suits "${r.name}", a ${r.type} of ${r.w}x${r.d} m, in this ${L.style} level? Rooms should feel varied and each have their own identity.`, criteria }]));
  const ans = await decide(state, qs), used = {}, out = {};
  for (const r of rooms) {
    const probs = ans[r.id]?.probabilities || {};
    const key = keys.map(k => [k, (probs[k] ?? 0) - 0.2 * (used[k] || 0)]).sort((a, b) => b[1] - a[1])[0][0];
    used[key] = (used[key] || 0) + 1; out[r.id] = key;
  }
  return out;
}

export async function critic(L, room) {
  const a = await decide(describe(L, room), { fill: { type: 'score', instructions: 'How furnished and lived-in does this room feel?', criteria: ['empty', 'sparse', 'balanced', 'rich', 'cluttered'] },
    cohesive: noul('Does the furniture arrangement look sensible, comfortable and well composed?'), cozy: noul('Does this room feel cosy, inviting and richly detailed?') });
  const labels = ['empty', 'sparse', 'balanced', 'rich', 'cluttered'];
  return { score: a.fill?.score ?? 2, label: labels[Math.round(a.fill?.score ?? 2)] ?? 'balanced', probs: a.fill?.probabilities, cohesive: pYes(a.cohesive), cozy: pYes(a.cozy) };
}

// apply(id, room, params) executes a button and returns {n,msg}. snapshotting is the caller's job.
export async function autopilot(L, { apply, log, rooms, maxRounds = 4 }) {
  for (let round = 1; round <= maxRounds; round++) {
    let pressed = 0;
    for (const room of rooms()) {
      let f = analyze(L, room);
      if (FIX.gate(f)) { const r = apply(FIX.id, room, {}); log({ kind: 'press', text: `${room.name}: ${ACTION[FIX.id].label} (auto) ${r.msg}`, p: 1 }); f = analyze(L, room); }
      const probes = PROBES.filter(p => p.gate(f));
      if (!probes.length) { log({ kind: 'info', text: `${room.name}: round ${round} - nothing to ask` }); continue; }
      const qs = Object.fromEntries(probes.map(p => [p.id, noul(p.q)]));
      let ans; try { ans = offline ? null : await decide(describe(L, room), qs); } catch (e) { log({ kind: 'no', text: `Decision unavailable (${e.message}) - gates only` }); ans = null; }
      if (!ans) ans = Object.fromEntries(probes.map(p => [p.id, { noul: 1 }]));
      const yes = probes.map(p => ({ ...p, pr: pYes(ans[p.id]) }));
      yes.forEach(p => log({ kind: p.pr >= THRESHOLD ? 'yes' : 'no', text: `${room.name}: ${p.q}`, p: p.pr }));
      for (const p of yes.filter(p => p.pr >= THRESHOLD).sort(byPhase)) { const r = apply(p.id, room, {}); if (r.n) { pressed++; log({ kind: 'press', text: `${room.name}: ${ACTION[p.id].label} - ${r.msg}`, p: p.pr }); } }
    }
    if (!pressed) { // nothing to do via gates - let the critic judge whether we're finished
      let extra = 0;
      for (const room of rooms()) {
        if (offline) break;
        const c = await critic(L, room); log({ kind: 'critic', text: `${room.name}: Decision rates it "${c.label}" (${c.score.toFixed(1)}), cohesive ${(c.cohesive * 100) | 0}%, cosy ${(c.cozy * 100) | 0}%` });
        const act = c.score < 1.6 ? 'fill_empty' : c.score > 3.2 ? 'declutter' : (c.cozy < 0.4 && round < maxRounds ? 'add_decor' : null);
        if (act) { const r = apply(act, room, {}); if (r.n) { extra++; log({ kind: 'press', text: `${room.name}: ${ACTION[act].label} (critic) - ${r.msg}` }); } }
      }
      if (!extra) { log({ kind: 'done', text: `Autopilot converged after ${round} round(s).` }); return; }
    }
  }
  log({ kind: 'done', text: 'Autopilot stopped at max rounds.' });
}

export async function freeAsk(L, room, question) {
  const a = await decide(room ? describe(L, room) : { level: L.rooms.map(r => describe(L, r)) }, { q: noul(question) });
  return pYes(a.q);
}
