"""LevelDez Blender kit (v2). Load inside Blender (BlenderMCP execute_blender_code):

    LEVELDEZ_ROOT = r"/path/to/LevelDez"      # or set the LEVELDEZ_ROOT environment variable
    exec(open(LEVELDEZ_ROOT + "/tools/blender_kit.py").read())
    A = "coffin"; box(A, (0.7, 2.0, 0.5), (0, 0, 0.25), "wood"); finish(A, label="Coffin", cat="undead", tags=["wall-hug"])

Conventions: metres, Z up, the FRONT of every asset faces -Y (becomes +Z in glTF), origin anywhere (the tool re-centres
and drops it on the floor). Materials named tint_<palette key> are recoloured by the level style.
finish() bakes modifiers, merges meshes per material, exports <ASSETS>/<PACK>/<asset>.glb and merges the entry
(+ measured bbox [w,d,h]) into <PACK>/manifest.json.
Entry keys: as, replaces, label, cat, size, place (floor|wall|ceiling|surface), y, tags, light, lightColor, lightY.
"""
import bpy, json, math, os, random, io, contextlib, logging
from mathutils import Matrix, Vector

for _n in list(logging.root.manager.loggerDict):
    if 'gltf' in _n.lower() or 'io_scene' in _n.lower():
        logging.getLogger(_n).setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)

ROOT = str(globals().get("LEVELDEZ_ROOT") or os.environ.get("LEVELDEZ_ROOT") or "").replace("\\", "/").rstrip("/")
if not ROOT:
    raise RuntimeError("Set LEVELDEZ_ROOT = r'/path/to/LevelDez' (or the LEVELDEZ_ROOT env var) before loading the kit")
ASSETS = ROOT + "/assets"
PACK = "gothic"
PI = math.pi


def _mat(name, rgb, rough=0.7, metal=0.0, emit=None, strength=4.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = strength
    return m


_M = {  # key: (blender name, rgb, rough, metal, emit, strength)
    "stone": ("stone", (0.17, 0.17, 0.19), 0.93, 0, None, 0),
    "stone_light": ("stone_light", (0.34, 0.33, 0.31), 0.9, 0, None, 0),
    "stone_dark": ("stone_dark", (0.08, 0.08, 0.095), 0.95, 0, None, 0),
    "marble": ("marble", (0.72, 0.72, 0.74), 0.3, 0, None, 0),
    "brick": ("brick", (0.22, 0.1, 0.08), 0.9, 0, None, 0),
    "moss": ("moss", (0.09, 0.2, 0.08), 0.95, 0, None, 0),
    "wood": ("wood_dark", (0.075, 0.045, 0.032), 0.55, 0, None, 0),
    "wood_red": ("wood_mahogany", (0.16, 0.05, 0.035), 0.5, 0, None, 0),
    "wood_pale": ("wood_pale", (0.32, 0.22, 0.13), 0.6, 0, None, 0),
    "iron": ("iron", (0.045, 0.045, 0.055), 0.45, 0.9, None, 0),
    "rust": ("rust", (0.25, 0.1, 0.05), 0.75, 0.5, None, 0),
    "copper": ("copper", (0.6, 0.28, 0.12), 0.4, 1.0, None, 0),
    "silver": ("silver", (0.72, 0.74, 0.78), 0.3, 1.0, None, 0),
    "pewter": ("pewter", (0.35, 0.36, 0.4), 0.5, 0.8, None, 0),
    "gold": ("gold", (0.75, 0.55, 0.15), 0.35, 1.0, None, 0),
    "bone": ("bone", (0.82, 0.76, 0.62), 0.65, 0, None, 0),
    "ivory": ("ivory", (0.9, 0.88, 0.8), 0.5, 0, None, 0),
    "cloth": ("tint_fabric", (0.33, 0.03, 0.07), 0.95, 0, None, 0),
    "cloth2": ("tint_accent", (0.22, 0.06, 0.36), 0.95, 0, None, 0),
    "black": ("cloth_black", (0.025, 0.025, 0.03), 0.95, 0, None, 0),
    "leather": ("leather", (0.12, 0.07, 0.04), 0.8, 0, None, 0),
    "burlap": ("burlap", (0.3, 0.25, 0.15), 0.98, 0, None, 0),
    "rope": ("rope", (0.35, 0.28, 0.15), 0.95, 0, None, 0),
    "wax": ("wax", (0.86, 0.8, 0.66), 0.5, 0, None, 0),
    "parchment": ("parchment", (0.72, 0.62, 0.42), 0.9, 0, None, 0),
    "canvas": ("canvas", (0.8, 0.75, 0.6), 0.9, 0, None, 0),
    "ash": ("ash", (0.1, 0.1, 0.1), 0.98, 0, None, 0),
    "blood": ("blood", (0.3, 0.0, 0.02), 0.25, 0, None, 0),
    "obsidian": ("obsidian", (0.02, 0.02, 0.03), 0.1, 0.3, None, 0),
    "glass": ("glass_dark", (0.42, 0.52, 0.56), 0.12, 0.15, None, 0),
    "glass_clear": ("glass_clear", (0.75, 0.9, 0.95), 0.05, 0, None, 0),
    "flame": ("flame", (1.0, 0.5, 0.12), 0.5, 0, (1.0, 0.45, 0.1), 8.0),
    "ember": ("ember", (1.0, 0.35, 0.05), 0.6, 0, (1.0, 0.3, 0.05), 6.0),
    "orb": ("orb", (0.5, 0.2, 0.95), 0.08, 0, (0.5, 0.2, 1.0), 3.5),
    "rune": ("rune", (0.6, 0.3, 1.0), 0.3, 0, (0.6, 0.3, 1.0), 5.0),
    "ecto": ("ecto", (0.2, 1.0, 0.9), 0.2, 0, (0.2, 1.0, 0.9), 4.0),
    "soulfire": ("soulfire", (0.3, 1.0, 0.8), 0.5, 0, (0.3, 1.0, 0.8), 7.0),
    "potion": ("potion_green", (0.15, 0.9, 0.3), 0.2, 0, (0.2, 1.0, 0.35), 3.0),
    "potion_red": ("potion_red", (0.9, 0.05, 0.08), 0.2, 0, (1.0, 0.05, 0.1), 3.0),
    "potion_blue": ("potion_blue", (0.1, 0.4, 1.0), 0.2, 0, (0.15, 0.45, 1.0), 3.0),
    "potion_amber": ("potion_amber", (1.0, 0.6, 0.05), 0.2, 0, (1.0, 0.6, 0.05), 3.0),
    "potion_purple": ("potion_purple", (0.6, 0.1, 0.9), 0.2, 0, (0.6, 0.1, 0.95), 3.0),
    "sg_red": ("sg_red", (0.8, 0.05, 0.08), 0.2, 0, (0.9, 0.08, 0.1), 0.55),
    "sg_blue": ("sg_blue", (0.1, 0.25, 0.8), 0.2, 0, (0.15, 0.3, 0.9), 0.55),
    "sg_green": ("sg_green", (0.1, 0.55, 0.25), 0.2, 0, (0.15, 0.7, 0.3), 0.55),
    "sg_amber": ("sg_amber", (0.9, 0.55, 0.05), 0.2, 0, (1.0, 0.6, 0.05), 0.55),
    "sg_purple": ("sg_purple", (0.45, 0.1, 0.7), 0.2, 0, (0.5, 0.15, 0.8), 0.55),
    "book_a": ("book_red", (0.30, 0.04, 0.05), 0.8, 0, None, 0),
    "book_b": ("book_green", (0.05, 0.16, 0.09), 0.8, 0, None, 0),
    "book_c": ("book_black", (0.05, 0.045, 0.05), 0.8, 0, None, 0),
    "book_d": ("book_brown", (0.18, 0.10, 0.05), 0.8, 0, None, 0),
    "book_e": ("book_blue", (0.05, 0.08, 0.22), 0.8, 0, None, 0),
    "book_f": ("book_purple", (0.18, 0.05, 0.22), 0.8, 0, None, 0),
}
MATS = {k: _mat(n, rgb, r, m, e, s) for k, (n, rgb, r, m, e, s) in _M.items()}
# transparent glass for bottles, jars and orbs
_b = next(n for n in MATS["glass_clear"].node_tree.nodes if n.type == "BSDF_PRINCIPLED")
_b.inputs["Alpha"].default_value = 0.28
for _attr, _val in (("surface_render_method", "BLENDED"), ("blend_method", "BLEND")):
    try:
        setattr(MATS["glass_clear"], _attr, _val)
    except Exception:
        pass
BOOKS = ["book_a", "book_b", "book_c", "book_d", "book_e", "book_f"]


def matref(m):
    return MATS[m] if isinstance(m, str) else m


def _count(asset):
    return len([o for o in bpy.data.objects if o.name.startswith(f"GD_{asset}__")])


def _reg(asset, o, mat, bevel=0.0, smooth=False, scale=None, sub=0):
    if scale:
        o.data.transform(Matrix.Diagonal((scale[0], scale[1], scale[2], 1.0)))
    o.name = f"GD_{asset}__{_count(asset)}"
    o.data.materials.clear()
    o.data.materials.append(matref(mat))
    if smooth:
        o.data.polygons.foreach_set("use_smooth", [True] * len(o.data.polygons))
    if bevel:
        m = o.modifiers.new("bv", "BEVEL")
        m.width = bevel
        m.segments = 3
        m.limit_method = "ANGLE"
    if sub:
        s = o.modifiers.new("ss", "SUBSURF")
        s.levels = sub
        s.render_levels = sub
    return o


def box(a, size, loc, mat="stone", rot=(0, 0, 0), bevel=0.012):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    return _reg(a, bpy.context.active_object, mat, bevel, scale=size)


def cyl(a, r, h, loc, mat="iron", r2=None, rot=(0, 0, 0), verts=20, bevel=0.0):
    if r2 is None or abs(r2 - r) < 1e-6:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=h, location=loc, rotation=rot)
    return _reg(a, bpy.context.active_object, mat, bevel, smooth=True)


def sph(a, r, loc, mat="bone", scale=(1, 1, 1), seg=16):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=seg, ring_count=max(6, seg // 2), location=loc)
    return _reg(a, bpy.context.active_object, mat, smooth=True, scale=scale)


def tor(a, R, r, loc, mat="iron", rot=(0, 0, 0), seg=24, minor=8):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=seg, minor_segments=minor, location=loc, rotation=rot)
    return _reg(a, bpy.context.active_object, mat, smooth=True)


def arch_pts(w, hs, squash=1.0, n=8):
    """Lancet (pointed) arch silhouette in the XZ plane: width w, straight sides up to hs, then two arcs meeting at an apex."""
    pts = [(-w / 2, 0.0), (w / 2, 0.0), (w / 2, hs)]
    for i in range(1, n + 1):
        t = math.radians(60 * i / n)
        pts.append((-w / 2 + w * math.cos(t), hs + w * math.sin(t) * squash))
    for i in range(1, n):
        t = math.radians(120 + 60 * i / n)
        pts.append((w / 2 + w * math.cos(t), hs + w * math.sin(t) * squash))
    pts.append((-w / 2, hs))
    return pts


def prism(a, pts, depth, loc, mat="wood", rot=(0, 0, 0), bevel=0.008, uv=False):
    """Extrude a convex XZ polygon along Y (depth), centred on loc."""
    n = len(pts)
    verts = [(x, -depth / 2, z) for x, z in pts] + [(x, depth / 2, z) for x, z in pts]
    faces = [tuple(reversed(range(n))), tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    me = bpy.data.meshes.new("prism")
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new("prism", me)
    bpy.context.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = rot
    if uv:  # project the XZ silhouette onto 0..1 so an image material fits the shape (front face at -Y)
        xs = [x for x, _ in pts]; zs = [z for _, z in pts]; x0, x1, z0, z1 = min(xs), max(xs), min(zs), max(zs)
        layer = me.uv_layers.new(name="UVMap")
        for loop in me.loops:
            vx, _, vz = me.vertices[loop.vertex_index].co
            layer.data[loop.index].uv = ((vx - x0) / (x1 - x0), (vz - z0) / (z1 - z0))
    bpy.context.view_layer.objects.active = o
    return _reg(a, o, mat, bevel)


def topview(pts_y):
    """(x, y_world) CCW seen from above -> prism profile for rot=(pi/2,0,0)."""
    return [(x, -y) for x, y in reversed(pts_y)]


def lathe(a, prof, loc, mat="stone", verts=24, scale=1.0, rot=(0, 0, 0)):
    """Surface of revolution about Z from a [(radius, z), ...] profile (bottom to top)."""
    import bmesh
    bm = bmesh.new()
    rings = []
    for r, z in prof:
        rings.append([bm.verts.new((r * scale * math.cos(2 * PI * i / verts), r * scale * math.sin(2 * PI * i / verts), z * scale)) for i in range(verts)])
    for j in range(len(rings) - 1):
        for i in range(verts):
            bm.faces.new((rings[j][i], rings[j][(i + 1) % verts], rings[j + 1][(i + 1) % verts], rings[j + 1][i]))
    if prof[0][0] > 0:
        bm.faces.new(rings[0])
    if prof[-1][0] > 0:
        bm.faces.new(rings[-1])
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new("lathe")
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("lathe", me)
    bpy.context.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = rot
    bpy.context.view_layer.objects.active = o
    return _reg(a, o, mat, smooth=True)


def limb(a, p0, p1, r0, r1, mat="wood", verts=8):
    """Tapered cylinder between two points."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    mid = (p0 + p1) / 2
    eul = Vector((0, 0, 1)).rotation_difference(d.normalized()).to_euler()
    return cyl(a, r0, d.length, tuple(mid), mat, r2=r1, rot=tuple(eul), verts=verts)


def bone(a, p0, p1, r=0.012, mat="bone"):
    limb(a, p0, p1, r, r, mat, verts=8)
    for p in (p0, p1):
        sph(a, r * 1.5, p, mat, seg=8)


def skull(a, loc, s=1.0, mat="bone", yaw=0.0, jaw=True, horns=0, glow=None):
    """Skull facing -Y (rotated by yaw about Z). s=1 is life size (~0.18 m)."""
    x, y, z = loc
    c, sn = math.cos(yaw), math.sin(yaw)
    def P(dx, dy, dz): return (x + dx * c - dy * sn, y + dx * sn + dy * c, z + dz)
    sph(a, 0.052 * s, P(0, 0.005 * s, 0.07 * s), mat, scale=(1, 1.12, 1.0), seg=12)
    box(a, (0.07 * s, 0.05 * s, 0.03 * s), P(0, -0.035 * s, 0.03 * s), mat, rot=(0, 0, yaw), bevel=0.003 * s)
    for sx in (-1, 1):
        sph(a, 0.016 * s, P(sx * 0.024 * s, -0.045 * s, 0.075 * s), "black", seg=8)
        if glow:
            sph(a, 0.007 * s, P(sx * 0.024 * s, -0.056 * s, 0.075 * s), glow, seg=6)
    box(a, (0.012 * s, 0.01 * s, 0.02 * s), P(0, -0.055 * s, 0.05 * s), "black", rot=(0, 0, yaw), bevel=0)
    if jaw:
        box(a, (0.055 * s, 0.05 * s, 0.025 * s), P(0, -0.03 * s, 0.01 * s), mat, rot=(0, 0, yaw), bevel=0.003 * s)
        box(a, (0.05 * s, 0.006 * s, 0.01 * s), P(0, -0.055 * s, 0.035 * s), "ivory", rot=(0, 0, yaw), bevel=0)
    for k in range(horns):
        sg = -1 if k % 2 == 0 else 1
        limb(a, P(sg * 0.04 * s, 0, 0.1 * s), P(sg * 0.1 * s, 0, 0.17 * s), 0.014 * s, 0.003 * s, "black", verts=6)


def book(a, loc, size=(0.2, 0.28, 0.04), mat="book_a", rot_z=0.0, spine=True):
    w, d, h = size
    box(a, (w, d, h), loc, mat, rot=(0, 0, rot_z), bevel=0.004)
    box(a, (w - 0.016, d - 0.012, h * 0.7), (loc[0], loc[1], loc[2] + 0.001), "parchment", rot=(0, 0, rot_z), bevel=0.002)
    if spine:
        c, s = math.cos(rot_z), math.sin(rot_z)
        box(a, (0.01, d + 0.002, h + 0.002), (loc[0] - (w / 2) * c, loc[1] - (w / 2) * s, loc[2]), "gold", rot=(0, 0, rot_z), bevel=0)


def chain(a, p0, p1, link=0.018, mat="iron"):
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    n = max(2, int(d.length / (link * 1.7)))
    eul = Vector((0, 0, 1)).rotation_difference(d.normalized()).to_euler()
    for i in range(n):
        p = p0 + d * ((i + 0.5) / n)
        t = tor(a, link, link * 0.28, tuple(p), mat, rot=(eul[0] + (PI / 2 if i % 2 else 0), eul[1], eul[2]), seg=10, minor=5)
        t.data.transform(Matrix.Diagonal((1, 0.65, 1, 1)))


def candle(a, loc, h=0.18, r=0.022, flame=True, mat="wax"):
    cyl(a, r, h, (loc[0], loc[1], loc[2] + h / 2), mat, verts=10)
    if flame:
        sph(a, 0.014, (loc[0], loc[1], loc[2] + h + 0.022), "flame", scale=(1, 1, 1.9), seg=8)


def image_mat(name, path, emit=0.3, max_px=512):
    """Material showing an image (shaded + a little emission so art stays readable in dark rooms). Image is downscaled to max_px."""
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in [n for n in nt.nodes if n.type == "TEX_IMAGE"]:
        nt.nodes.remove(n)
    b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    img = bpy.data.images.load(path, check_existing=False)
    w, h = img.size
    k = min(1.0, max_px / max(w, h))
    if k < 1.0:
        img.scale(max(1, int(w * k)), max(1, int(h * k)))
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
    nt.links.new(tex.outputs["Color"], b.inputs["Emission Color"])
    b.inputs["Emission Strength"].default_value = emit
    b.inputs["Roughness"].default_value = 0.8
    return m


def ring_of(n, radius, z=0.0, start=0.0):
    return [(radius * math.cos(start + 2 * PI * i / n), radius * math.sin(start + 2 * PI * i / n), z, start + 2 * PI * i / n) for i in range(n)]


def clear(asset):
    for o in [o for o in bpy.data.objects if o.name.startswith(f"GD_{asset}")]:
        bpy.data.objects.remove(o, do_unlink=True)


def purge():
    """Remove every GD_* object and orphaned mesh data (materials are kept)."""
    for o in [o for o in bpy.data.objects if o.name.startswith("GD_")]:
        bpy.data.objects.remove(o, do_unlink=True)
    for me in [m for m in bpy.data.meshes if m.users == 0]:
        bpy.data.meshes.remove(me)


def finish(asset, **entry):
    """Bake modifiers, merge meshes per material, export GLB into the pack folder, update the pack manifest."""
    parts = [o for o in bpy.data.objects if o.name.startswith(f"GD_{asset}__")]
    dg = bpy.context.evaluated_depsgraph_get()
    for o in parts:
        me = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
        o.modifiers.clear()
        o.data = me
    groups = {}
    for o in parts:
        groups.setdefault(o.data.materials[0].name if o.data.materials else "", []).append(o)
    merged = []
    for name, objs in groups.items():
        bpy.ops.object.select_all(action="DESELECT")
        for o in objs:
            o.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        if len(objs) > 1:
            bpy.ops.object.join()
        merged.append(bpy.context.view_layer.objects.active)
    for i, o in enumerate(merged):
        o.name = f"GD_{asset}__m{i}"
    root = bpy.data.objects.get(f"GD_{asset}") or bpy.data.objects.new(f"GD_{asset}", None)
    if root.name not in bpy.context.collection.objects:
        bpy.context.collection.objects.link(root)
    for o in merged:
        o.parent = root
    bpy.context.view_layer.update()
    mn = Vector((1e9, 1e9, 1e9)); mx = Vector((-1e9, -1e9, -1e9))
    for o in merged:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            mn = Vector((min(mn[i], w[i]) for i in range(3))); mx = Vector((max(mx[i], w[i]) for i in range(3)))
    bbox = [round(mx[i] - mn[i], 3) for i in range(3)]  # Blender axes: width x, depth y, height z
    bpy.ops.object.select_all(action="DESELECT")
    for o in merged + [root]:
        o.select_set(True)
    bpy.context.view_layer.objects.active = root
    folder = f"{ASSETS}/{PACK}"
    os.makedirs(folder, exist_ok=True)
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        bpy.ops.export_scene.gltf(filepath=f"{folder}/{asset}.glb", export_format="GLB", use_selection=True, export_apply=False, export_yup=True,
                                  export_image_format="JPEG", export_jpeg_quality=85)
    mp = f"{folder}/manifest.json"
    mf = json.load(open(mp)) if os.path.exists(mp) else {}
    mf[asset] = {"file": f"{asset}.glb", "source": "blender-mcp", "bbox": bbox, **entry}
    json.dump(mf, open(mp, "w"), indent=1)
    return {"asset": asset, "meshes": len(merged), "faces": sum(len(o.data.polygons) for o in merged), "bbox": bbox}


def gallery(names, spacing=3.2, per_row=7, origin=(0, 0)):
    """Lay finished assets out in a grid so they can be inspected together with look()."""
    for i, n in enumerate(names):
        r = bpy.data.objects.get(f"GD_{n}")
        if r:
            r.location = (origin[0] + (i % per_row) * spacing, origin[1] - (i // per_row) * spacing, 0)
