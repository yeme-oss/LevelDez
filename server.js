// LevelDez local server: static files + Decision-1 proxy (OpenRouter) + asset/export IO + Blender bridge.
// Zero dependencies. Run: node server.js   (needs OPENROUTER_API_KEY in env for Decision)
const http = require('http');
const fs = require('fs');
const path = require('path');
const net = require('net');

// optional .env next to this file (KEY=value lines); real environment variables win
try { for (const l of fs.readFileSync(path.join(__dirname, '.env'), 'utf8').split(/\r?\n/)) { const m = l.match(/^\s*([A-Za-z0-9_]+)\s*=\s*(.*?)\s*$/); if (m && !(m[1] in process.env)) process.env[m[1]] = m[2].replace(/^['"]|['"]$/g, ''); } } catch {}
const PORT = +process.env.PORT || 5173;
const HOST = process.env.HOST || '127.0.0.1'; // localhost only by default: this server proxies your API key and can drive Blender
const MODEL = process.env.DECISION_MODEL || 'microsoft/microsoft-decision-1';
const KEY = process.env.OPENROUTER_API_KEY || '';
const ROOT = __dirname;
const PUB = path.join(ROOT, 'public');
const ASSETS = path.join(ROOT, 'assets');
const OUT = path.join(ROOT, 'exports');
const BLENDER_PORT = +process.env.BLENDER_PORT || 9876;
for (const d of [ASSETS, OUT]) fs.mkdirSync(d, { recursive: true });

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
  '.glb': 'model/gltf-binary', '.png': 'image/png', '.svg': 'image/svg+xml' };

const stats = { calls: 0, errors: 0, promptTokens: 0, completionTokens: 0, cost: 0 };

function body(req, limit = 64e6) {
  return new Promise((res, rej) => {
    const chunks = []; let n = 0;
    req.on('data', c => { n += c.length; if (n > limit) { rej(new Error('too large')); req.destroy(); } else chunks.push(c); });
    req.on('end', () => res(Buffer.concat(chunks)));
    req.on('error', rej);
  });
}
const json = (res, code, obj) => { res.writeHead(code, { 'Content-Type': 'application/json' }); res.end(JSON.stringify(obj)); };
const safeName = s => String(s || 'level').replace(/[^\w\-]+/g, '_').slice(0, 60);

// One batched Decision-1 call. `questions` is { id: {type:'noul'|'choice'|'score', instructions, criteria?} }.
// Returns the model's per-question answers (noul -> probability of YES, choice -> probabilities, score -> level probs).
async function decide(state, questions) {
  if (!KEY) throw Object.assign(new Error('OPENROUTER_API_KEY not set'), { code: 503 });
  stats.calls++;
  const r = await fetch('https://openrouter.ai/api/alpha/decisions', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + KEY, 'Content-Type': 'application/json',
      'HTTP-Referer': 'http://localhost:' + PORT, 'X-Title': 'LevelDez' },
    body: JSON.stringify({ model: MODEL, state, questions }),
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) { stats.errors++; throw Object.assign(new Error(j.error?.message || ('HTTP ' + r.status)), { code: 502 }); }
  const u = j.usage || {};
  stats.promptTokens += u.input_tokens || 0; stats.completionTokens += u.output_tokens || 0; stats.cost += u.cost || 0;
  return j.answers || {};
}

// Recursive scan: assets/**.glb plus a manifest.json per folder. Folder entries are namespaced "<folder>_<key>",
// their `file` is relative to assets/, and `pack` defaults to the top-level folder name.
// Bounding box [w, d, h] (glTF x, z, y) of a GLB, from accessor min/max + node transforms. Cached by mtime.
const bboxCache = new Map();
function glbBBox(file) {
  const st = fs.statSync(file), c = bboxCache.get(file);
  if (c && c.m === st.mtimeMs) return c.v;
  let out = null;
  try {
    const buf = fs.readFileSync(file), jl = buf.readUInt32LE(12), g = JSON.parse(buf.slice(20, 20 + jl).toString());
    const nodes = g.nodes || [], acc = g.accessors || [], meshes = g.meshes || [];
    const mul = (a, b) => { const o = new Array(16).fill(0); for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) for (let k = 0; k < 4; k++) o[j * 4 + i] += a[k * 4 + i] * b[j * 4 + k]; return o; };
    const local = n => {
      if (n.matrix) return n.matrix;
      const t = n.translation || [0, 0, 0], q = n.rotation || [0, 0, 0, 1], s = n.scale || [1, 1, 1], [x, y, z, w] = q;
      return [(1 - 2 * (y * y + z * z)) * s[0], (2 * (x * y + z * w)) * s[0], (2 * (x * z - y * w)) * s[0], 0, (2 * (x * y - z * w)) * s[1], (1 - 2 * (x * x + z * z)) * s[1], (2 * (y * z + x * w)) * s[1], 0,
        (2 * (x * z + y * w)) * s[2], (2 * (y * z - x * w)) * s[2], (1 - 2 * (x * x + y * y)) * s[2], 0, t[0], t[1], t[2], 1];
    };
    const mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9];
    const walk = (i, parent) => {
      const n = nodes[i], m = mul(parent, local(n));
      if (n.mesh != null) for (const pr of meshes[n.mesh].primitives) {
        const a = acc[pr.attributes.POSITION]; if (!a || !a.min) continue;
        for (let c = 0; c < 8; c++) {
          const v = [c & 1 ? a.max[0] : a.min[0], c & 2 ? a.max[1] : a.min[1], c & 4 ? a.max[2] : a.min[2]];
          for (let k = 0; k < 3; k++) { const w = m[k] * v[0] + m[4 + k] * v[1] + m[8 + k] * v[2] + m[12 + k]; mn[k] = Math.min(mn[k], w); mx[k] = Math.max(mx[k], w); }
        }
      }
      (n.children || []).forEach(ch => walk(ch, m));
    };
    const I = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
    const roots = (g.scenes && g.scenes[g.scene || 0] || { nodes: nodes.map((_, i) => i) }).nodes;
    roots.forEach(r => walk(r, I));
    out = [mx[0] - mn[0], mx[2] - mn[2], mx[1] - mn[1]].map(v => Math.round(v * 1000) / 1000);
  } catch { out = null; }
  bboxCache.set(file, { m: st.mtimeMs, v: out });
  return out;
}

function scanAssets() {
  const files = [], manifest = {};
  (function walk(dir, rel) {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, e.name), r = rel ? rel + '/' + e.name : e.name;
      if (e.isDirectory()) walk(full, r);
      else if (e.name.toLowerCase().endsWith('.glb')) files.push(r);
      else if (e.name === 'manifest.json') {
        let m = {}; try { m = JSON.parse(fs.readFileSync(full, 'utf8')); } catch { continue; }
        for (const [k, v] of Object.entries(m)) {
          if (!v || !v.file || !String(v.file).toLowerCase().endsWith('.glb')) continue; // texture/image manifests live in assets too
          manifest[rel ? rel.replace(/\//g, '_') + '_' + k : k] = { ...v, file: rel ? rel + '/' + v.file : v.file, pack: v.pack ?? (rel ? rel.split('/')[0] : undefined) };
        }
      }
    }
  })(ASSETS, '');
  // measure anything without a bbox (older assets, loose GLBs) so the client never has to download a GLB just to size it
  const looseBBox = {};
  for (const e of Object.values(manifest)) if (!e.bbox) e.bbox = glbBBox(path.join(ASSETS, e.file));
  const listed = new Set(Object.values(manifest).map(e => e.file));
  for (const f of files) if (!listed.has(f)) looseBBox[f] = glbBBox(path.join(ASSETS, f));
  return { files, manifest, looseBBox };
}

function blenderCall(payload, timeout = 120000) {
  return new Promise((resolve, reject) => {
    const s = net.createConnection({ host: '127.0.0.1', port: BLENDER_PORT });
    let buf = ''; const t = setTimeout(() => { s.destroy(); reject(new Error('Blender timeout')); }, timeout);
    s.on('connect', () => s.write(JSON.stringify(payload)));
    s.on('data', d => { buf += d; try { const o = JSON.parse(buf); clearTimeout(t); s.end(); resolve(o); } catch {} });
    s.on('error', e => { clearTimeout(t); reject(new Error('Blender not reachable on :' + BLENDER_PORT + ' (' + e.code + ')')); });
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://x');
  const p = url.pathname;
  try {
    if (p === '/api/status') {
      let blender = false;
      await blenderCall({ type: 'get_scene_info', params: {} }, 1500).then(() => blender = true).catch(() => {});
      return json(res, 200, { model: MODEL, hasKey: !!KEY, blender, stats });
    }
    if (p === '/api/decide' && req.method === 'POST') {
      const { state, questions } = JSON.parse((await body(req)).toString());
      return json(res, 200, { answers: await decide(state, questions), stats });
    }
    if (p === '/api/assets') return json(res, 200, scanAssets());
    if (p === '/api/save' && req.method === 'POST') {
      const name = safeName(url.searchParams.get('name'));
      const ext = url.searchParams.get('ext') === 'glb' ? 'glb' : 'json';
      const buf = await body(req);
      fs.writeFileSync(path.join(OUT, `${name}.${ext}`), buf);
      return json(res, 200, { saved: `exports/${name}.${ext}`, bytes: buf.length });
    }
    if (p === '/api/blender' && req.method === 'POST') {
      if (process.env.LEVELDEZ_ALLOW_RAW_BLENDER !== '1') return json(res, 403, { error: 'raw Blender bridge disabled (set LEVELDEZ_ALLOW_RAW_BLENDER=1 to enable)' });
      return json(res, 200, await blenderCall(JSON.parse((await body(req)).toString())));
    }
    if (p === '/api/blender-import') {
      const f = path.join(OUT, safeName(url.searchParams.get('name')) + '.glb').split(path.sep).join('/');
      const code = `import bpy\nbpy.ops.import_scene.gltf(filepath=r"${f}")\nprint("imported", r"${f}")`;
      const r = await blenderCall({ type: 'execute_code', params: { code } });
      const lines = String(r.result?.result ?? r.result ?? '').split(/\r?\n/).filter(l => l && !/INFO: Blender create/.test(l));
      return json(res, r.status === 'error' ? 500 : 200, r.status === 'error' ? { error: r.message } : { ok: true, result: lines.slice(-3).join(' | ') });
    }
    // static: /assets/* from ./assets, everything else from ./public
    let file = p === '/' ? '/index.html' : decodeURIComponent(p);
    const base = file.startsWith('/assets/') ? ROOT : PUB;
    const full = path.normalize(path.join(base, file));
    if (!full.startsWith(base)) { res.writeHead(403); return res.end(); }
    if (!fs.existsSync(full) || fs.statSync(full).isDirectory()) { res.writeHead(404); return res.end('not found'); }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(full)] || 'application/octet-stream', 'Cache-Control': 'no-cache' });
    fs.createReadStream(full).pipe(res);
  } catch (e) {
    json(res, e.code === 503 ? 503 : 500, { error: e.message });
  }
});
server.listen(PORT, HOST, () => console.log(`LevelDez on http://${HOST === '127.0.0.1' ? 'localhost' : HOST}:${PORT}  | Decision model: ${MODEL} | key: ${KEY ? 'set' : 'MISSING'}`));
