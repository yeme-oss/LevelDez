# Loads the kit, the generator core and every recipe module into one namespace. exec() this file inside Blender.
import os as _os0
_R = str(globals().get("LEVELDEZ_ROOT") or _os0.environ.get("LEVELDEZ_ROOT") or "").replace("\\", "/").rstrip("/")
if not _R:
    raise RuntimeError("Set LEVELDEZ_ROOT = r'/path/to/LevelDez' (or the LEVELDEZ_ROOT env var) before exec-ing this file")
_T = _R + "/tools"
exec(open(_T + "/blender_kit.py").read())
exec(open(_T + "/gothic/core.py").read())
exec(open(_T + "/gothic/common.py").read())
import os as _os
for _f in ["recipes_arch", "recipes_furniture", "recipes_sacred", "recipes_alchemy", "recipes_light", "recipes_study", "recipes_decor", "recipes_academy", "recipes_art", "recipes_extra"]:
    _p = _T + f"/gothic/{_f}.py"
    if _os.path.exists(_p):
        exec(open(_p).read())
