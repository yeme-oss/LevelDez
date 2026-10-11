# Loads the kit, the generic generator core and every scifi recipe module into one namespace. exec() this file inside Blender.
#   LEVELDEZ_ROOT = r"/path/to/LevelDez"; exec(open(LEVELDEZ_ROOT + "/tools/scifi/load.py").read())
#   generate(limit=40)   status()   redo("bed_pod")   write_plan(path)
import os as _os0
_R = str(globals().get("LEVELDEZ_ROOT") or _os0.environ.get("LEVELDEZ_ROOT") or "").replace("\\", "/").rstrip("/")
if not _R:
    raise RuntimeError("Set LEVELDEZ_ROOT before exec-ing this file")
_T = _R + "/tools"
exec(open(_T + "/blender_kit.py").read())
PACK = "scifi"
exec(open(_T + "/scifi/kit.py").read())
exec(open(_T + "/gothic/core.py").read())      # family registry, resumable generate(), status(), sheet()
exec(open(_T + "/scifi/review.py").read())
exec(open(_T + "/scifi/common.py").read())
for _f in ["recipes_sleep", "recipes_seating", "recipes_tables", "recipes_storage", "recipes_home", "recipes_signature", "recipes_lighting", "recipes_wall", "recipes_decor", "recipes_arch"]:
    _p = _T + f"/scifi/{_f}.py"
    if _os0.path.exists(_p):
        exec(open(_p).read())


def write_plan(path):
    prog = load_progress()
    lines = ["# Scifi pack plan", "", f"{len(plan())} assets. [x] built, [ ] todo. Regenerate with write_plan() from tools/scifi/load.py.", ""]
    cur_g = cur_f = None
    for it in plan():
        if it["group"] != cur_g:
            cur_g = it["group"]; cur_f = None
            lines += ["", f"## {nice(cur_g)} ({sum(1 for p in plan() if p['group'] == cur_g)})"]
        if it["family"] != cur_f:
            cur_f = it["family"]; f = it["fam"]; m = f["meta"]
            lines += ["", f"**{nice(cur_f)}** - {m.get('place', 'floor')}" + (f", as `{m['as']}`" if m.get('as') else "") + (f", replaces `{m['replaces']}`" if m.get('replaces') else "") + (f" - tags: {', '.join(m.get('tags', []))}" if m.get('tags') else "")]
        lines.append(f"- [{'x' if it['id'] in prog['done'] else ' '}] `{it['id']}`")
    open(path, "w", encoding="utf8").write("\n".join(lines) + "\n")
    return len(plan())
