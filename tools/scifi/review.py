# Contact-sheet renderer for reviewing assets: shot(ids, path) lays the built assets out in a grid and renders a 3/4 view to a PNG.
import bpy, json, math
from mathutils import Vector


def _studio():
    sc = bpy.context.scene
    for e in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        try:
            sc.render.engine = e; break
        except TypeError:
            pass
    w = sc.world or bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND"); bg.inputs[0].default_value = (0.045, 0.05, 0.07, 1); bg.inputs[1].default_value = 1.0
    for name, loc, e, col in (("RV_key", (4, -6, 7), 900, (1, 0.97, 0.92)), ("RV_fill", (-6, -4, 4), 400, (0.7, 0.85, 1.0)), ("RV_back", (0, 6, 5), 500, (1, 1, 1))):
        o = bpy.data.objects.get(name)
        if not o:
            l = bpy.data.lights.new(name, "AREA"); l.size = 5; o = bpy.data.objects.new(name, l); bpy.context.collection.objects.link(o)
        o.data.energy = e; o.data.color = col; o.location = loc
        d = (Vector((0, 0, 0.8)) - Vector(loc)); o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    sc.render.film_transparent = False


def shot(ids, path, per_row=6, width=1500, height=900, yaw=28, pitch=30, pad=0.45):
    """Lay out `ids` in a grid at the origin and render. Front of assets faces -Y; the camera looks from the front-right."""
    _studio()
    mf = json.load(open(ASSETS + "/" + PACK + "/manifest.json"))
    for o in bpy.data.objects:
        if o.name.startswith("GD_"):
            r = o.parent or o
            o.hide_render = o.hide_viewport = r.name[3:] not in ids
    x = y = 0.0; rowh = 0.0; col = 0; pos = []
    cell = max([max(mf[i]["bbox"][0], mf[i]["bbox"][1]) for i in ids if i in mf] + [0.6]) + pad
    cell = min(cell, 2.4)
    for n, i in enumerate(ids):
        r = bpy.data.objects.get(f"GD_{i}")
        if not r:
            continue
        cx, cy = (n % per_row) * cell, -(n // per_row) * cell
        r.location = (cx, cy, 0); pos.append((cx, cy))
    rows = (len(ids) + per_row - 1) // per_row
    cols = min(per_row, len(ids))
    ctr = Vector(((cols - 1) * cell / 2, -(rows - 1) * cell / 2, 0.6))
    cam = bpy.data.objects.get("RV_cam") or bpy.data.objects.new("RV_cam", bpy.data.cameras.new("RV_cam"))
    if cam.name not in bpy.context.collection.objects:
        bpy.context.collection.objects.link(cam)
    cam.data.type = "ORTHO"
    span = max(cols * cell, rows * cell * 1.1)
    cam.data.ortho_scale = span * 1.0 + 0.5
    ya, pa = math.radians(yaw), math.radians(pitch)
    d = Vector((math.sin(ya) * math.cos(pa), -math.cos(ya) * math.cos(pa), math.sin(pa))) * 30
    cam.location = ctr + d; cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    sc = bpy.context.scene; sc.camera = cam; sc.render.resolution_x = width; sc.render.resolution_y = height
    sc.render.filepath = path; sc.render.image_settings.file_format = "PNG"
    try:
        sc.eevee.taa_render_samples = 24
    except Exception:
        pass
    bpy.ops.render.render(write_still=True)
    for o in bpy.data.objects:
        if o.name.startswith("GD_"):
            o.hide_render = False; o.hide_viewport = False
    return path
