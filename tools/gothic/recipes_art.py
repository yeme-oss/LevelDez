# ============ WALL ART (50): paintings, tapestries, stained glass - images from Nano Banana (gen_art.py) ============
exec(open(_T + "/gothic/art_prompts.py").read())

_FRAMES = ["gold", "black", "bone", "iron", "wood_red"]
_PLACEHOLDER_COL = {"portrait": "wood", "landscape": "stone_dark", "wide": "stone_dark", "square": "parchment", "tapestry": "cloth", "window": "sg_purple"}
_ART_Y = {"portrait": 1.3, "landscape": 1.4, "wide": 1.4, "square": 1.4, "tapestry": 0.75, "window": 0.9}


def _art_variants():
    out = []
    for i, (name, kind, style, subject) in enumerate(ART):
        out.append({"n": name, "kind": kind, "frame": _FRAMES[i % len(_FRAMES)], "label": " ".join(w.capitalize() for w in name.replace("glass_", "stained glass ").replace("tapestry_", "tapestry ").split("_")),
                    "meta": {"y": _ART_Y[kind], "tags": ["decor", "art"] + (["curtain"] if False else [])}})
    return out


@family("art", "art", _art_variants(), cat="wall art", place="wall", y=1.4, tags=["decor", "art"])
def _art(A, v):
    kind = v["kind"]; w, h = SIZES[kind]; name = v["n"]
    img = f"{ASSETS}/{PACK}/art/{name}.jpg"
    if os.path.exists(img):
        m = image_mat(f"art_{name}", img, emit=1.1 if kind == "window" else 0.35)
    else:
        PLACEHOLDER_IDS.add(A)
        m = _PLACEHOLDER_COL[kind]
    ft = 0.07 if kind not in ("tapestry",) else 0.0
    # image plane facing -Y
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -0.012, h / 2 + ft), rotation=(PI / 2, 0, 0))
    _reg(A, bpy.context.active_object, m, scale=(w, h, 1))
    if m == _PLACEHOLDER_COL[kind] and kind not in ("tapestry", "window"):  # simple stand-in composition so it is not a blank slab
        if kind == "portrait":
            sph(A, 0.11, (0, -0.02, h * 0.62 + ft), "bone", scale=(0.9, 0.3, 1.15), seg=12); box(A, (0.4, 0.02, 0.4), (0, -0.015, h * 0.25 + ft), "cloth", bevel=0)
        else:
            sph(A, 0.1, (w * 0.2, -0.02, h * 0.7 + ft), "ivory", scale=(1, 0.1, 1), seg=10); prism(A, [(-w / 2 + 0.05, 0), (-0.1, h * 0.35), (0.2, 0.1), (w / 2 - 0.05, 0.3), (w / 2 - 0.05, 0)], 0.02, (0, -0.016, ft + 0.02), "black", bevel=0)
    elif m == _PLACEHOLDER_COL[kind] and kind == "window":
        for j, c in enumerate(["sg_red", "sg_blue", "sg_amber", "sg_green"]):
            box(A, (w * 0.4, 0.01, h * 0.22), (-w * 0.2 + (j % 2) * w * 0.4, -0.02, h * (0.15 + 0.22 * (j // 2) * 1.6) + 0.05), c, bevel=0)
    elif m == _PLACEHOLDER_COL[kind] and kind == "tapestry":
        tor(A, w * 0.22, 0.012, (0, -0.02, h * 0.55), "gold", rot=(PI / 2, 0, 0), seg=26); skull(A, (0, -0.02, h * 0.5), 1.4, mat="bone")
    # frame / hanging hardware
    if kind == "tapestry":
        cyl(A, 0.016, w + 0.15, (0, 0.0, h + 0.03), "iron", rot=(0, PI / 2, 0), verts=8); [sph(A, 0.03, (s * (w / 2 + 0.08), 0, h + 0.03), "gold", seg=8) for s in (-1, 1)]
        for x in np_range(-w / 2 + 0.05, w / 2, 0.1): limb(A, (x, -0.012, 0.0), (x, -0.012, -0.06), 0.006, 0.003, "gold", 4)
    elif kind == "window":
        t = 0.06
        [box(A, (t, 0.08, h + 2 * t), (s * (w / 2 + t / 2), 0, h / 2 + t), "stone_light", bevel=0.008) for s in (-1, 1)]
        box(A, (w + 2 * t, 0.08, t), (0, 0, h + t * 1.5), "stone_light", bevel=0.008); box(A, (w + 2 * t, 0.1, t), (0, -0.01, 0.0 + t / 2), "stone_light", bevel=0.008)
        box(A, (0.025, 0.02, h), (0, -0.02, h / 2 + t), "iron", bevel=0)
    else:
        fm = v["frame"]; t = 0.07
        [box(A, (t, 0.06, h + 2 * t), (s * (w / 2 + t / 2), 0, h / 2 + t), fm, bevel=0.01) for s in (-1, 1)]
        [box(A, (w + 2 * t, 0.06, t), (0, 0, z), fm, bevel=0.01) for z in (t / 2, h + t * 1.5)]
        if fm == "gold": [sph(A, 0.035, (sx * (w / 2 + t / 2), -0.03, sz), "gold", seg=8) for sx in (-1, 1) for sz in (t / 2, h + t * 1.5)]
        if fm == "bone": skull(A, (0, -0.02, h + 2 * t - 0.01), 0.4, mat="ivory")
        if kind in ("portrait", "wide"): box(A, (0.14, 0.015, 0.035), (0, -0.04, 0.0 + t / 2 - 0.01), "gold", bevel=0)  # nameplate
