"""Run inside Blender (e.g. via BlenderMCP execute_blender_code) to publish the selected objects as a LevelDez asset.
Model conventions: metres, front of the object faces -Y in Blender (-> +Z in glTF), origin anywhere (the tool re-centres
and drops it on the floor). Name materials 'tint_*' to have the level's style palette recolour them.
Usage: set TYPE (a catalog key such as 'armchair', or a brand-new key) and call publish(TYPE)."""
import bpy, json, os
ASSETS = (os.environ.get("LEVELDEZ_ROOT") or "/path/to/LevelDez").replace("\\", "/").rstrip("/") + "/assets"  # set LEVELDEZ_ROOT

def publish(type_, tint="fabric", **entry):
    os.makedirs(ASSETS, exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=f"{ASSETS}/{type_}.glb", export_format='GLB', use_selection=True, export_apply=True, export_yup=True)
    mf_path = f"{ASSETS}/manifest.json"
    mf = json.load(open(mf_path)) if os.path.exists(mf_path) else {}
    mf[type_] = {"file": f"{type_}.glb", "tint": tint, "source": "blender", **entry}   # new types also take label/cat/size/place/tags
    json.dump(mf, open(mf_path, "w"), indent=1)
    print("published", type_)
