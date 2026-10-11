"""Gothic pack generator core: family registry, plan, resumable driver.

Run inside Blender (BlenderMCP):
    exec(open(r".../tools/gothic/load.py").read())     # loads kit + recipes into this namespace
    generate(limit=30)                                  # builds the next 30 not-yet-done assets; safe to re-run / resume
    generate(limit=30, groups=["architecture"])         # restrict to groups
    status()                                            # progress summary
Progress lives in assets/gothic/_progress.json (done / failed). Delete an id from "done" (or call redo(id)) to rebuild it.
"""
import json, os, re, time

FAMILIES = []
PLACEHOLDER_IDS = set()  # recipes add ids here when they had to use stand-in art (e.g. image not generated yet)
PROGRESS_FILE = ASSETS + "/" + PACK + "/_progress.json"


def family(name, group, variants, **meta):
    """Register a recipe. variants: list of names or dicts {'n': name, ...params, 'meta': {entry overrides}}."""
    def deco(fn):
        vs = [v if isinstance(v, dict) else {"n": v} for v in variants]
        FAMILIES.append({"name": name, "group": group, "fn": fn, "variants": vs, "meta": meta})
        return fn
    return deco


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def nice(s):
    return " ".join(w.capitalize() for w in s.replace("_", " ").split())


def plan():
    items = []
    for f in FAMILIES:
        for v in f["variants"]:
            items.append({"id": slug(f"{f['name']}_{v['n']}"), "family": f["name"], "group": f["group"], "v": v, "fam": f})
    ids = [i["id"] for i in items]
    assert len(ids) == len(set(ids)), "duplicate ids: " + str([i for i in ids if ids.count(i) > 1][:5])
    return items


def load_progress():
    try:
        return json.load(open(PROGRESS_FILE))
    except Exception:
        return {"done": {}, "failed": {}, "placeholder": []}


def save_progress(p):
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    json.dump(p, open(PROGRESS_FILE, "w"), indent=1)


def entry_for(it):
    f, v = it["fam"], it["v"]
    m = {"cat": f["group"], "place": "floor", **f["meta"], **v.get("meta", {})}
    m.setdefault("label", v.get("label") or nice(f"{v['n']} {f['name']}" if f["meta"].get("label_family") else v["n"]))
    m["tags"] = list(dict.fromkeys(list(f["meta"].get("tags", [])) + list(v.get("meta", {}).get("tags", [])) + list(v.get("tags", []))))
    m.pop("label_family", None)
    return m


def generate(limit=30, groups=None, families=None, ids=None, redo=False, verbose=False):
    """Build the next `limit` outstanding assets (resumable). Returns a short report."""
    purge()
    prog = load_progress()
    todo = [it for it in plan()
            if (redo or it["id"] not in prog["done"])
            and (not groups or it["group"] in groups) and (not families or it["family"] in families) and (not ids or it["id"] in ids)]
    built, failed = [], []
    t0 = time.time()
    for it in todo[:limit]:
        A = it["id"]
        try:
            it["fam"]["fn"](A, it["v"])
            info = finish(A, **entry_for(it))
            prog["done"][A] = {"faces": info["faces"], "bbox": info["bbox"]}
            prog["failed"].pop(A, None)
            if A in PLACEHOLDER_IDS:
                PLACEHOLDER_IDS.discard(A)
                if A not in prog["placeholder"]: prog["placeholder"].append(A)
            elif A in prog["placeholder"]: prog["placeholder"].remove(A)
            built.append(A)
        except Exception as e:
            clear(A)
            prog["failed"][A] = repr(e)[:200]
            failed.append((A, repr(e)[:160]))
        save_progress(prog)
    left = len(todo) - len(built) - len(failed)
    return {"built": built, "failed": failed, "remaining": max(0, left), "done_total": len(prog["done"]), "plan_total": len(plan()), "secs": round(time.time() - t0, 1)}


def redo(*ids):
    return generate(limit=len(ids), ids=set(ids), redo=True)


def status():
    prog = load_progress()
    by = {}
    for it in plan():
        g = by.setdefault(it["group"], [0, 0])
        g[1] += 1
        g[0] += it["id"] in prog["done"]
    return {"done": len(prog["done"]), "plan": len(plan()), "failed": prog["failed"], "by_group": by}


def sheet(ids, spacing=None, per_row=8, origin=(0, 0)):
    """Arrange built assets in a grid (by actual width) for a contact-sheet look()."""
    x = y = 0.0; row_h = 0.0; col = 0
    for i in ids:
        r = bpy.data.objects.get(f"GD_{i}")
        if not r:
            continue
        mf = json.load(open(ASSETS + "/" + PACK + "/manifest.json")).get(i, {})
        w, d, h = mf.get("bbox", [1, 1, 1])
        r.location = (origin[0] + x + w / 2, origin[1] - y, 0)
        x += max(w, 0.6) + 0.5
        row_h = max(row_h, d)
        col += 1
        if col >= per_row:
            col = 0; x = 0.0; y += max(row_h, 1.0) + 1.0; row_h = 0.0


def write_plan_md(path):
    prog = load_progress()
    lines = ["# Necromancer Academy - gothic pack plan", "", f"{len(plan())} assets. Status: [x] built, [ ] todo. Regenerate with tools/gothic/load.py -> write_plan_md().", ""]
    cur_g = cur_f = None
    for it in plan():
        if it["group"] != cur_g:
            cur_g = it["group"]; cur_f = None
            n = sum(1 for p in plan() if p["group"] == cur_g)
            lines += ["", f"## {nice(cur_g)} ({n})"]
        if it["family"] != cur_f:
            cur_f = it["family"]; f = it["fam"]
            lines += ["", f"**{nice(cur_f)}** - {f['meta'].get('place', 'floor')}" + (f", as `{f['meta']['as']}`" if f['meta'].get('as') else "") + (f", replaces `{f['meta']['replaces']}`" if f['meta'].get('replaces') else "") + (f" - tags: {', '.join(f['meta'].get('tags', []))}" if f['meta'].get('tags') else "")]
        lines.append(f"- [{'x' if it['id'] in prog['done'] else ' '}] `{it['id']}`")
    open(path, "w", encoding="utf8").write("\n".join(lines) + "\n")
    return len(plan())


def refresh_art():
    """Re-bake placeholder paintings whose generated image now exists in assets/gothic/art/."""
    prog = load_progress()
    ids = [i for i in prog["placeholder"] if os.path.exists(f"{ASSETS}/{PACK}/art/{i[4:]}.jpg")]
    return redo(*ids) if ids else {"built": [], "note": "no placeholder has an image yet", "placeholders": len(prog["placeholder"])}
