# ============ FURNITURE (alias variants of base types + new natives) ============

def _legs(A, w, d, h, t=0.06, mat="wood", inset=0.05, z0=0.0):
    for sx in (-1, 1):
        for sy in (-1, 1): box(A, (t, t, h), (sx * (w / 2 - inset), sy * (d / 2 - inset), z0 + h / 2), mat, bevel=0.005)


def _bedding(A, z0, w=1.5, d=1.95, blanket="cloth"):
    box(A, (w, d, 0.22), (0, 0, z0 + 0.11), "black", bevel=0.05)
    box(A, (w + 0.02, 1.25, 0.07), (0, -0.33, z0 + 0.25), blanket, bevel=0.03); box(A, (w + 0.02, 0.16, 0.12), (0, 0.28, z0 + 0.27), blanket, bevel=0.04)
    for s in (-1, 1): box(A, (0.55, 0.36, 0.13), (s * 0.37, d / 2 - 0.25, z0 + 0.29), "ivory", bevel=0.05)


@family("bed", "furniture", ["coffin_bed", "bone_frame", "black_canopy", "stone_slab", "sleigh_gothic", "double_arch"], cat="furniture", place="floor", tags=["bed", "headwall"], **{"as": "bed"})
def _bed(A, v):
    k = v["n"]
    if k == "coffin_bed":
        out = [(-0.4, -1.05), (0.4, -1.05), (0.82, 0.55), (0.62, 1.05), (-0.62, 1.05), (-0.82, 0.55)]
        prism(A, topview(out), 0.4, (0, 0, 0.3), "wood_red", rot=(PI / 2, 0, 0), bevel=0.02)
        prism(A, topview([(x * 0.86, y * 0.94) for x, y in out]), 0.05, (0, 0, 0.5), "black", rot=(PI / 2, 0, 0), bevel=0.01)
        box(A, (1.0, 1.2, 0.08), (0, -0.25, 0.56), "cloth", bevel=0.03)
        for s in (-1, 1): box(A, (0.5, 0.34, 0.12), (s * 0.28, 0.65, 0.58), "ivory", bevel=0.05)
        box(A, (1.7, 0.1, 0.9), (0, 1.1, 0.6), "wood", bevel=0.02); prism(A, arch_pts(1.7, 0.0, 0.3), 0.1, (0, 1.1, 1.05), "wood")
    elif k == "bone_frame":
        box(A, (1.6, 2.1, 0.12), (0, 0, 0.3), "bone", bevel=0.02)
        for sx in (-1, 1):
            bone(A, (sx * 0.8, -1.04, 0.1), (sx * 0.8, -1.04, 0.5), 0.045); bone(A, (sx * 0.8, 1.04, 0.1), (sx * 0.8, 1.04, 1.4), 0.05); skull(A, (sx * 0.8, 1.04, 1.4), 1.2, yaw=PI)
            bone(A, (sx * 0.8, -1.04, 0.36), (sx * 0.8, 1.04, 0.36), 0.04)
        bone(A, (-0.8, 1.04, 1.2), (0.8, 1.04, 1.2), 0.04); bone(A, (-0.8, 1.04, 0.7), (0.8, 1.04, 0.7), 0.035)
        for x in (-0.5, -0.17, 0.17, 0.5): bone(A, (x, 1.04, 0.74), (x, 1.04, 1.18), 0.025)
        _bedding(A, 0.36)
    elif k == "black_canopy":
        box(A, (1.6, 2.1, 0.26), (0, 0, 0.13), "wood", bevel=0.02); _bedding(A, 0.26, blanket="cloth2")
        for sx in (-1, 1):
            for sy in (-1, 1): box(A, (0.07, 0.07, 2.0), (sx * 0.82, sy * 1.04, 1.0), "black", bevel=0.008)
        box(A, (1.78, 2.2, 0.06), (0, 0, 2.03), "black", bevel=0.01)
        for sx in (-1, 1):
            for sy in (-1, 1): box(A, (0.04, 0.5, 1.7), (sx * 0.84, sy * 0.8, 1.1), "black", bevel=0.01)
        box(A, (1.7, 0.08, 0.9), (0, 1.04, 0.7), "wood", bevel=0.02)
    elif k == "stone_slab":
        box(A, (1.7, 2.15, 0.4), (0, 0, 0.2), "stone", bevel=0.03); box(A, (1.74, 2.2, 0.06), (0, 0, 0.43), "stone_light", bevel=0.02)
        box(A, (1.5, 1.6, 0.06), (0, -0.2, 0.49), "leather", bevel=0.03); box(A, (1.55, 0.9, 0.05), (0, -0.45, 0.54), "cloth", bevel=0.03)
        for s in (-1, 1): box(A, (0.5, 0.34, 0.12), (s * 0.37, 0.8, 0.55), "bone", bevel=0.05)
        for s in (-1, 1): skull(A, (s * 0.8, -1.05, 0.4), 1.0)
    elif k == "sleigh_gothic":
        box(A, (1.6, 2.1, 0.26), (0, 0, 0.13), "wood_red", bevel=0.02); _bedding(A, 0.26)
        prism(A, arch_pts(1.7, 0.3, 0.5), 0.1, (0, 1.05, 0.2), "wood_red"); prism(A, arch_pts(1.7, 0.1, 0.25), 0.1, (0, -1.05, 0.2), "wood_red")
        for s in (-1, 1): cyl(A, 0.05, 0.12, (s * 0.85, 1.05, 1.5), "gold", r2=0.0, verts=8)
    elif k == "double_arch":
        box(A, (1.6, 2.1, 0.28), (0, 0, 0.14), "wood", bevel=0.02); _bedding(A, 0.28, blanket="cloth2")
        for y in (-1.04, 1.04): prism(A, arch_pts(1.7, 1.0, 0.6), 0.09, (0, y, 0.2), "wood_red")
        for s in (-1, 1): box(A, (0.06, 2.1, 0.08), (s * 0.84, 0, 2.0), "wood_red")
        box(A, (1.7, 0.06, 0.06), (0, 0, 2.0), "iron")


@family("wardrobe", "furniture", ["carved_skull", "iron_bound", "bone_inlay", "plain_tall", "mirror_door"], cat="furniture", place="floor", tags=["storage", "wall-hug", "tall"], **{"as": "wardrobe"})
def _wardrobe(A, v):
    k = v["n"]; body = {"carved_skull": "wood", "iron_bound": "wood", "bone_inlay": "wood_red", "plain_tall": "wood_pale", "mirror_door": "wood"}[k]
    box(A, (1.3, 0.6, 1.75), (0, 0, 0.1 + 0.875), body, bevel=0.012); box(A, (1.36, 0.64, 0.08), (0, 0, 1.89), body, bevel=0.01)
    prism(A, arch_pts(1.3, 0.0, 0.42), 0.58, (0, 0, 1.93), body, bevel=0.01)
    for sx in (-1, 1):
        for sy in (-1, 1): box(A, (0.1, 0.1, 0.1), (sx * 0.55, sy * 0.24, 0.05), "wood")
    for s in (-1, 1): box(A, (0.62, 0.03, 1.5), (s * 0.32, -0.31, 0.95), "black" if k == "carved_skull" else "wood_red", bevel=0.005); tor(A, 0.03, 0.007, (s * 0.06, -0.33, 1.0), "gold" if k != "iron_bound" else "iron", rot=(PI / 2, 0, 0))
    if k == "carved_skull":
        for s in (-1, 1): skull(A, (s * 0.32, -0.33, 0.9), 2.0, mat="bone")
        skull(A, (0, -0.32, 2.2), 1.2, mat="bone")
    elif k == "iron_bound":
        for z in (0.35, 0.95, 1.55):
            box(A, (1.3, 0.04, 0.07), (0, -0.325, z), "iron", bevel=0.004)
    elif k == "bone_inlay":
        for s in (-1, 1): box(A, (0.04, 0.02, 0.9), (s * 0.32, -0.33, 0.95), "bone", bevel=0); box(A, (0.4, 0.02, 0.04), (s * 0.32, -0.33, 1.05), "bone", bevel=0)
    elif k == "mirror_door":
        box(A, (0.5, 0.02, 1.2), (-0.32, -0.335, 0.95), "glass", bevel=0); box(A, (0.56, 0.015, 1.26), (-0.32, -0.33, 0.95), "gold", bevel=0)


def _shelf_frame(A, rows, mat="wood", w=0.95, h=1.78, d=0.32):
    for sx in (-1, 1): box(A, (0.05, d, h), (sx * (w / 2 - 0.025), 0, h / 2), mat)
    box(A, (w, 0.02, h), (0, d / 2 - 0.01, h / 2), mat)
    for i in range(rows + 1): box(A, (w - 0.1, d, 0.03), (0, 0, 0.015 + i * (h - 0.03) / rows), mat)


def _books_row(A, y0, z, width=0.85, h=0.26, rng=None):
    x = -width / 2; r = rng or random
    while x < width / 2 - 0.05:
        bw = 0.03 + r.random() * 0.035
        if r.random() < 0.12: x += 0.09; continue
        bh = h * (0.8 + r.random() * 0.25); box(A, (bw, 0.2, bh), (x + bw / 2, y0, z + bh / 2), random.choice(BOOKS), bevel=0.003); x += bw + 0.002


@family("bookshelf", "furniture", ["skull_crown", "bone_trim", "chained", "scroll_rack", "locked_cage", "candle_ledge", "cobwebbed", "rune_carved"], cat="furniture", place="floor", tags=["storage", "wall-hug", "holds-decor"], **{"as": "bookshelf"})
def _bookshelf(A, v):
    k = v["n"]; rows = 5; rng = random.Random(hash(k) & 0xffff)
    mat = "wood_pale" if k == "cobwebbed" else "wood_red" if k == "rune_carved" else "wood"
    _shelf_frame(A, rows, mat)
    for i in range(rows):
        z = 0.03 + i * 0.35
        if k == "scroll_rack":
            for x in np_range(-0.38, 0.38, 0.1): cyl(A, 0.03, 0.26, (x, 0, z + 0.04), "parchment", rot=(0, PI / 2 if False else 0, 0), verts=8)
        else: _books_row(A, 0.0, z, rng=rng)
    box(A, (1.0, 0.34, 0.07), (0, 0, 1.8), mat); prism(A, arch_pts(0.95, 0.0, 0.34), 0.3, (0, 0, 1.84), mat)
    if k == "skull_crown": skull(A, (0, -0.08, 2.1), 1.5)
    elif k == "bone_trim":
        for s in (-1, 1): bone(A, (s * 0.5, -0.17, 0.1), (s * 0.5, -0.17, 1.75), 0.022)
    elif k == "chained":
        for z in (0.5, 1.2): chain(A, (-0.47, -0.18, z), (0.47, -0.18, z - 0.15))
    elif k == "locked_cage":
        for x in np_range(-0.4, 0.4, 0.1): box(A, (0.02, 0.02, 1.7), (x, -0.17, 0.9), "iron", bevel=0)
        for z in (0.4, 0.9, 1.4): box(A, (0.9, 0.02, 0.02), (0, -0.17, z), "iron", bevel=0)
        box(A, (0.08, 0.04, 0.12), (0.42, -0.19, 0.9), "gold", bevel=0)
    elif k == "candle_ledge":
        box(A, (1.0, 0.16, 0.04), (0, -0.2, 1.1), mat)
        for x in (-0.3, 0, 0.3): candle(A, (x, -0.2, 1.12), h=0.12 + abs(x) * 0.2)
    elif k == "cobwebbed":
        for i in range(5): limb(A, (-0.47, -0.17, 1.76), (-0.47 + 0.15 * i, -0.17, 1.76 - 0.07 * (5 - i)), 0.003, 0.002, "ivory", 4)
        limb(A, (-0.45, -0.17, 1.7), (-0.2, -0.17, 1.3), 0.003, 0.002, "ivory", 4)
    elif k == "rune_carved":
        for s in (-1, 1):
            for z in (0.4, 0.8, 1.2, 1.6): box(A, (0.012, 0.02, 0.08), (s * 0.475, -0.17, z), "rune", bevel=0)


def np_range(a, b, step):
    out = []; x = a
    while x <= b + 1e-6: out.append(x); x += step
    return out


@family("table", "furniture", ["banquet", "stone_slab", "bone_legs", "round_pedestal", "coffin_lid", "ritual_inlay", "iron_trestle"], cat="furniture", place="floor", tags=["table", "holds-decor", "center"], **{"as": "dining_table"})
def _table(A, v):
    k = v["n"]
    if k == "banquet":
        box(A, (1.8, 0.95, 0.07), (0, 0, 0.745), "wood_red", bevel=0.02)
        for s in (-1, 1): box(A, (0.12, 0.8, 0.7), (s * 0.7, 0, 0.35), "wood", bevel=0.01); box(A, (0.3, 0.8, 0.07), (s * 0.7, 0, 0.035), "wood")
        box(A, (1.4, 0.07, 0.08), (0, 0, 0.3), "wood")
    elif k == "stone_slab":
        box(A, (1.8, 0.95, 0.12), (0, 0, 0.68), "stone_light", bevel=0.02)
        for s in (-1, 1): box(A, (0.25, 0.7, 0.62), (s * 0.65, 0, 0.31), "stone", bevel=0.02)
    elif k == "bone_legs":
        box(A, (1.8, 0.95, 0.06), (0, 0, 0.77), "wood", bevel=0.015)
        for sx in (-1, 1):
            for sy in (-1, 1): bone(A, (sx * 0.8, sy * 0.38, 0.0), (sx * 0.78, sy * 0.36, 0.74), 0.035)
    elif k == "round_pedestal":
        cyl(A, 0.55, 0.06, (0, 0, 0.75), "wood_red", verts=32); lathe(A, [(0.3, 0), (0.2, 0.06), (0.08, 0.3), (0.12, 0.6), (0.2, 0.72)], (0, 0, 0), "wood", verts=16)
        tor(A, 0.55, 0.02, (0, 0, 0.75), "gold", seg=32)
    elif k == "coffin_lid":
        out = [(-0.3, -0.9), (0.3, -0.9), (0.45, 0.4), (0.32, 0.9), (-0.32, 0.9), (-0.45, 0.4)]
        prism(A, topview([(x * 2.0 / 0.9 * 0.9, y) for x, y in out]), 0.07, (0, 0, 0.72), "wood_red", rot=(PI / 2, 0, 0), bevel=0.01)
        for sx in (-1, 1): box(A, (0.14, 0.7, 0.68), (sx * 0.65, 0, 0.34), "stone", bevel=0.02)
    elif k == "ritual_inlay":
        box(A, (1.8, 0.95, 0.07), (0, 0, 0.745), "black", bevel=0.02); tor(A, 0.36, 0.012, (0, 0, 0.785), "rune", seg=32)
        for x in (-0.6, 0.6): cyl(A, 0.06, 0.02, (x, 0, 0.785), "gold", verts=12)
        for s in (-1, 1): box(A, (0.12, 0.8, 0.7), (s * 0.7, 0, 0.35), "wood", bevel=0.01)
    elif k == "iron_trestle":
        box(A, (1.8, 0.95, 0.06), (0, 0, 0.75), "wood", bevel=0.01)
        for s in (-1, 1): limb(A, (s * 0.75, -0.35, 0.0), (s * 0.55, 0, 0.72), 0.03, 0.03, "iron"); limb(A, (s * 0.75, 0.35, 0.0), (s * 0.55, 0, 0.72), 0.03, 0.03, "iron")
        box(A, (1.5, 0.05, 0.05), (0, 0, 0.2), "iron")


@family("chair", "furniture", ["bone", "small_throne", "skull_back", "iron", "spiked", "tall_cushion"], cat="furniture", place="floor", tags=["seating", "chair"], **{"as": "dining_chair"})
def _chair(A, v):
    k = v["n"]; seat = {"bone": "bone", "iron": "iron", "spiked": "black"}.get(k, "wood")
    box(A, (0.45, 0.45, 0.05), (0, 0, 0.44), seat, bevel=0.008)
    if k in ("small_throne", "tall_cushion"): box(A, (0.4, 0.4, 0.06), (0, 0, 0.49), "cloth", bevel=0.02)
    for sx in (-1, 1):
        for sy in (-1, 1):
            if k == "bone": bone(A, (sx * 0.2, sy * 0.2, 0), (sx * 0.2, sy * 0.2, 0.44), 0.02)
            else: box(A, (0.045, 0.045, 0.44), (sx * 0.2, sy * 0.2, 0.22), "iron" if k == "iron" else "wood")
    if k == "bone":
        for s in (-1, 1): bone(A, (s * 0.2, 0.2, 0.46), (s * 0.2, 0.2, 1.0), 0.02)
        for x in (-0.1, 0.1): bone(A, (x, 0.2, 0.6), (x, 0.2, 0.95), 0.014)
        skull(A, (0, 0.2, 0.98), 0.9, yaw=PI)
    elif k == "small_throne": prism(A, arch_pts(0.44, 0.55, 0.9), 0.05, (0, 0.21, 0.46), "wood_red"); cyl(A, 0.03, 0.2, (0, 0.21, 1.5), "gold", r2=0.0, verts=8)
    elif k == "skull_back": box(A, (0.44, 0.04, 0.7), (0, 0.21, 0.8), "wood"); skull(A, (0, 0.18, 0.95), 1.6, yaw=PI)
    elif k == "iron":
        for x in np_range(-0.18, 0.18, 0.09): box(A, (0.02, 0.03, 0.55), (x, 0.21, 0.74), "iron")
        box(A, (0.44, 0.03, 0.04), (0, 0.21, 1.03), "iron")
    elif k == "spiked":
        box(A, (0.44, 0.04, 0.7), (0, 0.21, 0.8), "black")
        for x in (-0.15, 0, 0.15): cyl(A, 0.03, 0.2, (x, 0.21, 1.25), "iron", r2=0.0, verts=6)
    elif k == "tall_cushion": prism(A, arch_pts(0.42, 0.55, 0.95), 0.045, (0, 0.215, 0.5), "wood"); prism(A, arch_pts(0.3, 0.5, 0.9), 0.02, (0, 0.19, 0.55), "cloth", bevel=0)


@family("throne", "furniture", ["bone_throne", "lich_throne", "wing_chair", "stone_seat", "spider_chair"], cat="furniture", place="floor", tags=["seating", "faces-center"], **{"as": "armchair"})
def _throne(A, v):
    k = v["n"]
    if k == "bone_throne":
        box(A, (0.85, 0.85, 0.12), (0, 0, 0.06), "stone", bevel=0.02); box(A, (0.62, 0.62, 0.32), (0, 0, 0.28), "bone", bevel=0.03); box(A, (0.55, 0.55, 0.1), (0, -0.02, 0.5), "cloth", bevel=0.04)
        for sx in (-1, 1): bone(A, (sx * 0.38, 0.3, 0.2), (sx * 0.38, 0.3, 1.6), 0.04); bone(A, (sx * 0.38, -0.3, 0.2), (sx * 0.38, -0.3, 0.8), 0.035)
        for x in np_range(-0.25, 0.25, 0.125): bone(A, (x, 0.34, 0.6), (x, 0.34, 1.5 - abs(x) * 0.5), 0.022)
        skull(A, (0, 0.34, 1.55), 1.5, yaw=PI)
    elif k == "lich_throne":
        box(A, (0.85, 0.85, 0.15), (0, 0, 0.075), "obsidian", bevel=0.02); box(A, (0.7, 0.7, 0.3), (0, 0, 0.3), "black", bevel=0.03); box(A, (0.56, 0.56, 0.1), (0, -0.02, 0.52), "cloth2", bevel=0.04)
        prism(A, arch_pts(0.8, 0.9, 0.95), 0.1, (0, 0.35, 0.4), "obsidian")
        for s in (-1, 1): cyl(A, 0.05, 0.4, (s * 0.38, 0.35, 1.75), "obsidian", r2=0.0, verts=6); tor(A, 0.2, 0.012, (s * 0.2, 0.28, 1.15), "rune", rot=(PI / 2, 0, 0), seg=20)
        sph(A, 0.08, (0, 0.3, 1.45), "orb", seg=14)
    elif k == "wing_chair":
        box(A, (0.8, 0.8, 0.3), (0, 0, 0.3), "cloth2", bevel=0.05); box(A, (0.8, 0.2, 1.0), (0, 0.3, 0.9), "cloth2", bevel=0.06)
        for s in (-1, 1): box(A, (0.18, 0.5, 0.65), (s * 0.34, 0.1, 0.8), "cloth2", bevel=0.06)
        for sx in (-1, 1):
            for sy in (-1, 1): box(A, (0.06, 0.06, 0.15), (sx * 0.34, sy * 0.34, 0.075), "wood")
    elif k == "stone_seat":
        box(A, (0.85, 0.85, 0.5), (0, 0, 0.25), "stone", bevel=0.03); box(A, (0.85, 0.2, 1.1), (0, 0.32, 0.55), "stone_light", bevel=0.03)
        box(A, (0.6, 0.6, 0.06), (0, -0.05, 0.53), "leather", bevel=0.02)
        for s in (-1, 1): box(A, (0.14, 0.7, 0.2), (s * 0.36, -0.02, 0.6), "stone_light", bevel=0.02)
    elif k == "spider_chair":
        box(A, (0.6, 0.6, 0.08), (0, 0, 0.5), "black", bevel=0.02); sph(A, 0.28, (0, 0, 0.7), "black", scale=(1, 1, 0.5))
        for i in range(8):
            a = i * PI / 4; limb(A, (0.2 * math.cos(a), 0.2 * math.sin(a), 0.5), (0.45 * math.cos(a), 0.45 * math.sin(a), 0.4), 0.025, 0.02, "black"); limb(A, (0.45 * math.cos(a), 0.45 * math.sin(a), 0.4), (0.5 * math.cos(a), 0.5 * math.sin(a), 0.0), 0.02, 0.008, "black")
        prism(A, arch_pts(0.7, 0.4, 0.7), 0.05, (0, 0.3, 0.55), "black")
        for s in (-1, 1): sph(A, 0.03, (s * 0.1, -0.25, 0.8), "ember", seg=8)


@family("pew", "furniture", ["stone", "bone", "coffin_wood", "iron"], cat="furniture", place="floor", tags=["seating", "wall-hug"], **{"as": "bench"})
def _pew(A, v):
    k = v["n"]; m = {"stone": "stone_light", "bone": "bone", "coffin_wood": "wood_red", "iron": "iron"}[k]
    box(A, (1.2, 0.38, 0.07), (0, -0.0, 0.42), m, bevel=0.01)
    if k == "bone":
        for s in (-1, 1): bone(A, (s * 0.55, 0, 0.0), (s * 0.55, 0, 0.4), 0.035); bone(A, (s * 0.55, 0.17, 0.4), (s * 0.55, 0.17, 0.9), 0.03)
        for x in (-0.3, -0.1, 0.1, 0.3): bone(A, (x, 0.17, 0.5), (x, 0.17, 0.85), 0.018)
    elif k == "iron":
        for s in (-1, 1): box(A, (0.05, 0.36, 0.42), (s * 0.57, 0, 0.21), "iron"); box(A, (0.05, 0.05, 0.5), (s * 0.57, 0.17, 0.65), "iron")
        for x in np_range(-0.5, 0.5, 0.1): box(A, (0.025, 0.03, 0.4), (x, 0.17, 0.65), "iron")
    else:
        for s in (-1, 1): box(A, (0.1, 0.38, 0.4), (s * 0.55, 0, 0.2), m, bevel=0.01); box(A, (0.1, 0.06, 0.9), (s * 0.55, 0.17, 0.45), m, bevel=0.01)
        box(A, (1.2, 0.05, 0.5), (0, 0.17, 0.7), m, bevel=0.01)
        if k == "stone": skull(A, (0, 0.14, 0.78), 1.0, yaw=PI)


@family("desk", "furniture", ["scholar", "alchemist", "bone", "coffin_top", "scriptorium"], cat="furniture", place="floor", tags=["table", "holds-decor", "wall-hug", "desk"], **{"as": "desk"})
def _desk(A, v):
    k = v["n"]
    top = {"scholar": "wood_red", "alchemist": "wood", "bone": "wood", "coffin_top": "wood_red", "scriptorium": "wood_pale"}[k]
    box(A, (1.4, 0.7, 0.06), (0, 0, 0.72), top, bevel=0.012)
    if k == "scriptorium":
        box(A, (1.4, 0.4, 0.04), (0, -0.12, 0.88), top, rot=(-0.3, 0, 0), bevel=0.008); _legs(A, 1.4, 0.7, 0.72, 0.07, "wood", 0.05)
        book(A, (0.0, -0.1, 0.93), (0.4, 0.3, 0.04), "book_a", 0.0); cyl(A, 0.03, 0.14, (0.5, 0.15, 0.78), "iron", verts=8)
    elif k == "bone":
        for sx in (-1, 1):
            for sy in (-1, 1): bone(A, (sx * 0.62, sy * 0.28, 0.0), (sx * 0.62, sy * 0.28, 0.72), 0.03)
        skull(A, (-0.5, 0.1, 0.75), 1.0); book(A, (0.25, 0, 0.75), (0.3, 0.22, 0.04), "book_c", 0.2)
    elif k == "coffin_top":
        for sx in (-1, 1): box(A, (0.55, 0.62, 0.62), (sx * 0.42, 0, 0.35), "wood", bevel=0.01)
        for sx in (-1, 1): box(A, (0.4, 0.02, 0.12), (sx * 0.42, -0.32, 0.5), "gold", bevel=0)
        box(A, (0.04, 0.5, 0.01), (0.0, 0, 0.755), "gold", bevel=0)
    else:
        for sx in (-1, 1): box(A, (0.55, 0.62, 0.62), (sx * 0.42, 0, 0.35), "wood", bevel=0.01); tor(A, 0.018, 0.005, (sx * 0.42, -0.315, 0.5), "iron", rot=(PI / 2, 0, 0))
        if k == "alchemist":
            for x, c in [(-0.45, "potion"), (-0.3, "potion_purple")]: sph(A, 0.05, (x, 0.1, 0.8), c, seg=10); cyl(A, 0.018, 0.08, (x, 0.1, 0.87), "glass", verts=8)
        else: box(A, (0.3, 0.2, 0.015), (0.3, 0, 0.76), "parchment", rot=(0, 0, 0.2), bevel=0); cyl(A, 0.04, 0.1, (-0.45, 0.2, 0.75), "iron", r2=0.05, verts=10)


@family("chest", "furniture", ["skull_chest", "bone_dresser", "stone_coffer", "drawers_black"], cat="furniture", place="floor", tags=["storage", "wall-hug", "holds-decor"], **{"as": "dresser"})
def _chest(A, v):
    k = v["n"]
    if k == "skull_chest":
        box(A, (1.2, 0.46, 0.55), (0, 0, 0.35), "wood", bevel=0.02); cyl(A, 0.23, 1.2, (0, 0, 0.63), "wood_red", rot=(0, PI / 2, 0), verts=20)
        for x in (-0.5, 0, 0.5): box(A, (0.06, 0.47, 0.5), (x, 0, 0.35), "iron", bevel=0.004)
        skull(A, (0, -0.24, 0.35), 1.2)
    elif k == "bone_dresser":
        box(A, (1.2, 0.46, 0.75), (0, 0, 0.45), "wood", bevel=0.015); box(A, (1.26, 0.5, 0.05), (0, 0, 0.84), "bone", bevel=0.01)
        for z in (0.25, 0.47, 0.69): box(A, (1.1, 0.01, 0.01), (0, -0.235, z - 0.1), "black", bevel=0); bone(A, (-0.08, -0.25, z), (0.08, -0.25, z), 0.01)
        for sx in (-1, 1):
            for sy in (-1, 1): bone(A, (sx * 0.55, sy * 0.18, 0), (sx * 0.55, sy * 0.18, 0.1), 0.03)
    elif k == "stone_coffer":
        box(A, (1.2, 0.46, 0.5), (0, 0, 0.25), "stone", bevel=0.025); box(A, (1.26, 0.5, 0.1), (0, 0, 0.55), "stone_light", bevel=0.02)
        for x in (-0.4, 0.4): tor(A, 0.04, 0.01, (x, -0.24, 0.35), "iron", rot=(PI / 2, 0, 0))
    elif k == "drawers_black":
        box(A, (1.2, 0.46, 0.8), (0, 0, 0.45), "black", bevel=0.015); box(A, (1.26, 0.5, 0.05), (0, 0, 0.87), "obsidian", bevel=0.01)
        for z in (0.25, 0.5, 0.75):
            box(A, (1.1, 0.01, 0.2), (0, -0.235, z - 0.08), "stone_dark", bevel=0); box(A, (0.14, 0.02, 0.025), (0, -0.25, z - 0.08), "silver", bevel=0.002)


@family("nightstand", "furniture", ["skull_stand", "coffin_stand", "iron_stand", "drawers_small"], cat="furniture", place="floor", tags=["holds-decor", "beside"], **{"as": "nightstand"})
def _nightstand(A, v):
    k = v["n"]
    if k == "skull_stand":
        box(A, (0.45, 0.4, 0.4), (0, 0, 0.25), "wood", bevel=0.01); box(A, (0.5, 0.45, 0.04), (0, 0, 0.47), "wood_red"); skull(A, (0, -0.21, 0.3), 0.9)
        for sx in (-1, 1):
            for sy in (-1, 1): box(A, (0.05, 0.05, 0.06), (sx * 0.19, sy * 0.16, 0.03), "wood")
    elif k == "coffin_stand":
        out = [(-0.12, -0.2), (0.12, -0.2), (0.22, 0.05), (0.16, 0.2), (-0.16, 0.2), (-0.22, 0.05)]
        prism(A, topview(out), 0.55, (0, 0, 0.27), "wood_red", rot=(PI / 2, 0, 0), bevel=0.01); box(A, (0.02, 0.3, 0.01), (0, -0.0, 0.56), "gold", bevel=0)
    elif k == "iron_stand":
        box(A, (0.45, 0.4, 0.04), (0, 0, 0.5), "iron", bevel=0.005); _legs(A, 0.45, 0.4, 0.5, 0.03, "iron", 0.03); box(A, (0.4, 0.35, 0.03), (0, 0, 0.18), "iron", bevel=0.004)
    elif k == "drawers_small":
        box(A, (0.45, 0.4, 0.5), (0, 0, 0.27), "black", bevel=0.01); box(A, (0.5, 0.45, 0.04), (0, 0, 0.54), "stone_dark")
        for z in (0.15, 0.37): box(A, (0.38, 0.01, 0.17), (0, -0.205, z + 0.04), "stone_dark", bevel=0); tor(A, 0.014, 0.004, (0, -0.215, z + 0.05), "silver", rot=(PI / 2, 0, 0))


@family("side_table", "furniture", ["tripod_iron", "skull_pedestal", "stone_pillar", "bone_stool", "cauldron_table"], cat="furniture", place="floor", tags=["table", "holds-decor", "beside"], **{"as": "side_table"})
def _side(A, v):
    k = v["n"]
    if k == "tripod_iron":
        cyl(A, 0.22, 0.03, (0, 0, 0.53), "iron", verts=24)
        for i in range(3): a = i * 2 * PI / 3; limb(A, (0.18 * math.cos(a), 0.18 * math.sin(a), 0.52), (0.28 * math.cos(a), 0.28 * math.sin(a), 0.0), 0.016, 0.01, "iron", 6)
        tor(A, 0.2, 0.01, (0, 0, 0.2), "iron", seg=20)
    elif k == "skull_pedestal":
        cyl(A, 0.23, 0.04, (0, 0, 0.53), "wood_red", verts=24); cyl(A, 0.12, 0.06, (0, 0, 0.0), "stone", verts=16); cyl(A, 0.03, 0.4, (0, 0, 0.1), "bone", verts=10)
        skull(A, (0, 0, 0.3), 0.7)
    elif k == "stone_pillar": lathe(A, [(0.2, 0), (0.15, 0.06), (0.13, 0.4), (0.2, 0.5), (0.24, 0.52), (0.24, 0.56), (0.0, 0.56)], (0, 0, 0), "stone_light", verts=20)
    elif k == "bone_stool":
        cyl(A, 0.22, 0.05, (0, 0, 0.5), "bone", verts=20)
        for i in range(4): a = i * PI / 2 + PI / 4; bone(A, (0.15 * math.cos(a), 0.15 * math.sin(a), 0.0), (0.12 * math.cos(a), 0.12 * math.sin(a), 0.5), 0.022)
    elif k == "cauldron_table":
        sph(A, 0.2, (0, 0, 0.28), "iron", scale=(1, 1, 0.8), seg=14); cyl(A, 0.23, 0.04, (0, 0, 0.5), "black", verts=20)
        for i in range(3): a = i * 2 * PI / 3; cyl(A, 0.02, 0.1, (0.15 * math.cos(a), 0.15 * math.sin(a), 0.05), "iron", verts=6)


@family("chaise", "furniture", ["velvet", "bone", "stone_couch", "coffin_settee"], cat="furniture", place="floor", tags=["seating", "faces-center"], **{"as": "sofa"})
def _chaise(A, v):
    k = v["n"]
    if k == "velvet":
        box(A, (2.1, 0.95, 0.4), (0, 0, 0.3), "cloth2", bevel=0.06); box(A, (2.1, 0.25, 0.6), (0, 0.35, 0.8), "cloth2", bevel=0.07)
        for s in (-1, 1): box(A, (0.2, 0.95, 0.5), (s * 0.95, 0, 0.45), "cloth2", bevel=0.07)
        for i in range(8): sph(A, 0.022, (-0.9 + i * 0.26, 0.2, 0.9 + (0.1 if i % 2 else 0)), "gold", seg=6)
        _legs(A, 2.0, 0.85, 0.1, 0.06, "wood", 0.1)
    elif k == "bone":
        box(A, (2.1, 0.9, 0.3), (0, 0, 0.35), "black", bevel=0.05); box(A, (2.1, 0.12, 0.7), (0, 0.4, 0.8), "bone", bevel=0.03)
        for x in np_range(-0.9, 0.9, 0.3): bone(A, (x, 0.42, 0.45), (x, 0.42, 1.1), 0.025)
        for s in (-1, 1): bone(A, (s * 1.0, -0.4, 0.0), (s * 1.0, -0.4, 0.4), 0.04); bone(A, (s * 1.0, 0.4, 0.0), (s * 1.0, 0.4, 0.4), 0.04)
        bone(A, (-1.0, 0.42, 1.15), (1.0, 0.42, 1.15), 0.035); skull(A, (0, 0.4, 1.2), 1.2, yaw=PI)
    elif k == "stone_couch":
        box(A, (2.1, 0.95, 0.45), (0, 0, 0.225), "stone", bevel=0.03); box(A, (2.0, 0.7, 0.1), (0, -0.05, 0.5), "leather", bevel=0.03); box(A, (2.1, 0.2, 0.9), (0, 0.38, 0.65), "stone_light", bevel=0.03)
        for s in (-1, 1): box(A, (0.2, 0.95, 0.6), (s * 0.95, 0, 0.3), "stone_light", bevel=0.03)
    elif k == "coffin_settee":
        out = [(-0.4, -0.35), (0.4, -0.35), (1.0, -0.1), (1.05, 0.35), (-1.05, 0.35), (-1.0, -0.1)]
        prism(A, topview(out), 0.4, (0, 0, 0.3), "wood_red", rot=(PI / 2, 0, 0), bevel=0.02); box(A, (1.8, 0.7, 0.12), (0, -0.02, 0.56), "cloth", bevel=0.05)
        prism(A, arch_pts(2.1, 0.0, 0.2), 0.15, (0, 0.38, 0.5), "wood_red")
        box(A, (2.0, 0.15, 0.4), (0, 0.4, 0.55), "cloth", bevel=0.06)


@family("low_table", "furniture", ["sarcophagus_lid", "bone_low", "brazier_table", "coffin_coffee"], cat="furniture", place="floor", tags=["table", "holds-decor", "center"], **{"as": "coffee_table"})
def _low(A, v):
    k = v["n"]
    if k == "sarcophagus_lid":
        box(A, (1.0, 0.6, 0.1), (0, 0, 0.36), "stone_light", bevel=0.025); box(A, (0.9, 0.5, 0.06), (0, 0, 0.44), "stone", bevel=0.02); skull(A, (0, 0, 0.45), 0.8)
        for sx in (-1, 1): box(A, (0.12, 0.5, 0.32), (sx * 0.38, 0, 0.16), "stone", bevel=0.02)
    elif k == "bone_low":
        box(A, (1.0, 0.6, 0.05), (0, 0, 0.4), "wood", bevel=0.01)
        for sx in (-1, 1):
            for sy in (-1, 1): bone(A, (sx * 0.43, sy * 0.24, 0.0), (sx * 0.43, sy * 0.24, 0.4), 0.025)
    elif k == "brazier_table":
        box(A, (1.0, 0.6, 0.04), (0, 0, 0.4), "iron", bevel=0.004); _legs(A, 1.0, 0.6, 0.4, 0.04, "iron", 0.05); tor(A, 0.2, 0.012, (0, 0, 0.425), "ember", seg=20)
        cyl(A, 0.2, 0.02, (0, 0, 0.42), "ember", verts=20)
    elif k == "coffin_coffee":
        out = [(-0.2, -0.28), (0.2, -0.28), (0.5, -0.1), (0.5, 0.1), (0.2, 0.28), (-0.2, 0.28), (-0.5, 0.1), (-0.5, -0.1)]
        prism(A, topview(out), 0.4, (0, 0, 0.25), "wood_red", rot=(PI / 2, 0, 0), bevel=0.015); box(A, (0.02, 0.5, 0.01), (0, 0, 0.46), "gold", bevel=0); box(A, (0.4, 0.02, 0.01), (0, 0.08, 0.46), "gold", bevel=0)


@family("focus_stand", "furniture", ["scrying_mirror", "crystal_dais"], cat="furniture", place="floor", tags=["media", "wall-hug", "faces-center", "focal"], **{"as": "tv_unit"})
def _focus(A, v):
    if v["n"] == "scrying_mirror":
        box(A, (1.6, 0.4, 0.4), (0, 0, 0.2), "stone", bevel=0.02); prism(A, arch_pts(1.0, 0.5, 0.8), 0.06, (0, 0.05, 0.4), "iron"); prism(A, arch_pts(0.82, 0.45, 0.8), 0.03, (0, -0.0, 0.46), "obsidian", bevel=0)
        for s in (-1, 1): candle(A, (s * 0.7, 0, 0.4), h=0.2)
        tor(A, 0.3, 0.015, (0, -0.015, 1.0), "rune", rot=(PI / 2, 0, 0), seg=24)
    else:
        box(A, (1.6, 0.42, 0.3), (0, 0, 0.15), "stone_dark", bevel=0.02); cyl(A, 0.3, 0.1, (0, 0, 0.35), "stone", verts=24); cyl(A, 0.1, 0.4, (0, 0, 0.55), "gold", r2=0.14, verts=14); sph(A, 0.2, (0, 0, 1.0), "orb", seg=18)
        for s in (-1, 1): candle(A, (s * 0.6, 0, 0.3), h=0.2)


@family("lectern", "furniture", ["bone", "iron", "eagle", "stone_pulpit"], cat="furniture", place="floor", tags=["wall-hug", "focal"])
def _lectern(A, v):
    k = v["n"]
    if k == "bone":
        for i in range(3): a = i * 2 * PI / 3; bone(A, (0.2 * math.cos(a), 0.2 * math.sin(a), 0.0), (0.04 * math.cos(a), 0.04 * math.sin(a), 1.0), 0.025)
        box(A, (0.56, 0.4, 0.04), (0, 0, 1.12), "wood_red", rot=(-0.4, 0, 0), bevel=0.008); skull(A, (0, 0.0, 1.02), 0.7)
    elif k == "iron":
        for i in range(3): a = i * 2 * PI / 3 + 0.5; limb(A, (0.22 * math.cos(a), 0.22 * math.sin(a), 0.0), (0.03 * math.cos(a), 0.03 * math.sin(a), 1.1), 0.02, 0.015, "iron")
        box(A, (0.56, 0.4, 0.03), (0, 0, 1.18), "iron", rot=(-0.4, 0, 0), bevel=0.004); book(A, (0, 0.0, 1.22), (0.4, 0.3, 0.05), "book_c", 0.0)
    elif k == "eagle":
        lathe(A, [(0.2, 0), (0.1, 0.1), (0.06, 0.9), (0.1, 1.0)], (0, 0, 0), "gold", verts=14)
        sph(A, 0.14, (0, 0.0, 1.15), "gold", scale=(1.2, 0.8, 1.2)); limb(A, (-0.1, 0, 1.2), (-0.45, 0.05, 1.35), 0.05, 0.01, "gold", 6); limb(A, (0.1, 0, 1.2), (0.45, 0.05, 1.35), 0.05, 0.01, "gold", 6)
        sph(A, 0.07, (0, -0.1, 1.3), "gold"); box(A, (0.6, 0.35, 0.03), (0, -0.1, 1.22), "wood_red", rot=(-0.4, 0, 0))
    elif k == "stone_pulpit":
        box(A, (0.8, 0.7, 1.0), (0, 0, 0.5), "stone", bevel=0.03); box(A, (0.9, 0.8, 0.12), (0, 0, 1.06), "stone_light", bevel=0.03); prism(A, arch_pts(0.5, 0.3, 0.7), 0.04, (0, -0.36, 0.2), "stone_dark")
        book(A, (0, 0, 1.15), (0.35, 0.25, 0.05), "book_a", 0.3)


@family("stool", "furniture", ["bone", "iron", "skull", "cushion", "stump"], cat="furniture", place="floor", tags=["seating"])
def _stool(A, v):
    k = v["n"]
    if k == "bone":
        cyl(A, 0.2, 0.05, (0, 0, 0.43), "bone", verts=16)
        for i in range(3): a = i * 2 * PI / 3; bone(A, (0.12 * math.cos(a), 0.12 * math.sin(a), 0.0), (0.1 * math.cos(a), 0.1 * math.sin(a), 0.43), 0.02)
    elif k == "iron":
        cyl(A, 0.2, 0.03, (0, 0, 0.45), "iron", verts=16)
        for i in range(3): a = i * 2 * PI / 3; limb(A, (0.2 * math.cos(a), 0.2 * math.sin(a), 0.0), (0.1 * math.cos(a), 0.1 * math.sin(a), 0.45), 0.015, 0.015, "iron")
        tor(A, 0.15, 0.01, (0, 0, 0.2), "iron", seg=16)
    elif k == "skull":
        sph(A, 0.2, (0, 0, 0.22), "bone", scale=(1, 1.1, 1)); cyl(A, 0.17, 0.05, (0, 0, 0.43), "cloth", verts=16)
    elif k == "cushion":
        cyl(A, 0.2, 0.2, (0, 0, 0.22), "cloth2", r2=0.22, verts=18); cyl(A, 0.2, 0.04, (0, 0, 0.0), "gold", verts=18); sph(A, 0.03, (0, 0, 0.42), "gold", seg=8)
    elif k == "stump":
        lathe(A, [(0.26, 0), (0.2, 0.15), (0.19, 0.35), (0.2, 0.42), (0.0, 0.42)], (0, 0, 0), "wood", verts=14)


@family("cabinet", "furniture", ["apothecary", "glass_display", "skull_cabinet", "specimen", "potion_rack", "curio"], cat="furniture", place="floor", tags=["storage", "wall-hug", "holds-decor", "tall"])
def _cabinet(A, v):
    k = v["n"]
    box(A, (1.0, 0.45, 1.8), (0, 0, 0.9), "wood" if k != "glass_display" else "black", bevel=0.012); box(A, (1.06, 0.5, 0.06), (0, 0, 1.83), "wood_red", bevel=0.01)
    if k == "apothecary":
        for i in range(3):
            for j in range(5): box(A, (0.17, 0.01, 0.14), (-0.4 + j * 0.2, -0.23, 0.35 + i * 0.4), "wood_red", bevel=0); tor(A, 0.012, 0.004, (-0.4 + j * 0.2, -0.24, 0.35 + i * 0.4), "gold", rot=(PI / 2, 0, 0))
    elif k == "glass_display":
        box(A, (0.9, 0.01, 1.6), (0, -0.23, 0.95), "glass_clear", bevel=0)
        for z in (0.5, 0.95, 1.4): box(A, (0.9, 0.35, 0.02), (0, 0, z), "wood", bevel=0); skull(A, (0.0, 0, z + 0.02), 0.8)
    elif k == "skull_cabinet":
        for i in range(4):
            for j in range(4): skull(A, (-0.36 + j * 0.24, -0.23, 0.3 + i * 0.4), 0.7, mat="ivory")
    elif k == "specimen":
        for i in range(3):
            for j in range(3): cyl(A, 0.07, 0.2, (-0.3 + j * 0.3, -0.12, 0.45 + i * 0.5), "glass_clear", verts=12); sph(A, 0.04, (-0.3 + j * 0.3, -0.12, 0.5 + i * 0.5), ["potion", "potion_purple", "potion_red"][(i + j) % 3], seg=8)
    elif k == "potion_rack":
        for z in (0.5, 0.95, 1.4): box(A, (0.9, 0.12, 0.02), (0, -0.2, z), "wood", bevel=0)
        for i in range(3):
            for j in range(6): sph(A, 0.045, (-0.4 + j * 0.16, -0.2, 0.56 + i * 0.45), ["potion", "potion_red", "potion_blue", "potion_purple", "potion_amber", "potion"][(i + j) % 6], seg=8); cyl(A, 0.015, 0.07, (-0.4 + j * 0.16, -0.2, 0.63 + i * 0.45), "glass_clear", verts=6)
    elif k == "curio":
        for z in (0.5, 0.95, 1.4): box(A, (0.9, 0.35, 0.02), (0, -0.02, z), "wood", bevel=0)
        sph(A, 0.08, (-0.25, -0.1, 0.62), "orb", seg=10); skull(A, (0.2, -0.1, 0.97), 0.9); book(A, (-0.2, -0.1, 1.42), (0.22, 0.16, 0.05), "book_f", 0.2); candle(A, (0.25, -0.1, 1.42), h=0.15)


@family("instrument", "furniture", ["pipe_organ", "bone_harp", "harpsichord"], cat="furniture", place="floor", tags=["wall-hug", "focal"])
def _instrument(A, v):
    k = v["n"]
    if k == "pipe_organ":
        box(A, (2.4, 1.0, 1.0), (0, 0.0, 0.5), "wood", bevel=0.02); box(A, (2.0, 0.5, 0.06), (0, -0.55, 0.95), "wood_red")
        for x in np_range(-0.9, 0.9, 0.15): box(A, (0.06, 0.04, 0.12), (x, -0.55, 0.99), "ivory", bevel=0)
        for i, x in enumerate(np_range(-1.0, 1.0, 0.18)): h = 1.2 + 1.2 * (1 - abs(x) / 1.1); cyl(A, 0.065, h, (x, 0.35, 1.0 + h / 2), "silver", verts=10)
        prism(A, arch_pts(2.4, 0.0, 0.22), 0.1, (0, 0.5, 2.3), "wood")
    elif k == "bone_harp":
        box(A, (0.6, 0.4, 0.06), (0, 0, 0.05), "bone"); bone(A, (0.25, 0, 0.0), (0.25, 0, 1.4), 0.04); limb(A, (-0.25, 0, 0.08), (0.25, 0, 1.4), 0.03, 0.03, "bone")
        for i in range(10): t = i / 9; limb(A, (-0.25 + 0.5 * t, 0, 0.1 + 1.25 * t), (0.25, 0, 0.1 + 1.2 * t), 0.004, 0.004, "silver", 4)
    elif k == "harpsichord":
        box(A, (1.6, 0.8, 0.12), (0, 0, 0.78), "black", bevel=0.02); box(A, (1.0, 0.3, 0.06), (0.0, -0.45, 0.8), "black")
        for x in np_range(-0.45, 0.45, 0.08): box(A, (0.05, 0.2, 0.02), (x, -0.45, 0.85), "ivory", bevel=0)
        for sx in (-1, 1):
            for sy in (-1, 1): box(A, (0.06, 0.06, 0.74), (sx * 0.7, sy * 0.3, 0.37), "black")
        box(A, (1.55, 0.04, 0.6), (0, 0.38, 1.15), "black", rot=(0.4, 0, 0))


# ---- bath / kitchen aliases ----
@family("bath_fixture", "furniture", ["bone_basin", "stone_basin", "blood_bath", "stone_tub", "garderobe"], cat="furniture", place="floor", tags=["bath", "wall-hug"])
def _bath(A, v):
    k = v["n"]
    if k in ("bone_basin", "stone_basin"):
        m = "bone" if k == "bone_basin" else "stone_light"
        box(A, (0.8, 0.5, 0.8), (0, 0, 0.4), "stone" if k == "stone_basin" else "wood", bevel=0.015); box(A, (0.84, 0.54, 0.06), (0, 0, 0.83), m, bevel=0.01); lathe(A, [(0.0, 0.84), (0.2, 0.86), (0.22, 0.9), (0.18, 0.9)], (0, 0, 0), "ivory", verts=16)
        cyl(A, 0.012, 0.2, (0, 0.2, 1.0), "gold", verts=8); skull(A, (0, -0.1, 0.9), 0.5)
    elif k in ("blood_bath", "stone_tub"):
        liquid = "blood" if k == "blood_bath" else "ecto"
        box(A, (1.7, 0.78, 0.55), (0, 0, 0.275), "stone" if k == "stone_tub" else "wood_red", bevel=0.03); box(A, (1.5, 0.6, 0.02), (0, 0, 0.55), liquid, bevel=0)
        for sx in (-1, 1):
            for sy in (-1, 1): sph(A, 0.08, (sx * 0.78, sy * 0.33, 0.06), "gold", seg=8)
        cyl(A, 0.015, 0.25, (-0.8, 0.0, 0.62), "gold", verts=8)
    elif k == "garderobe":
        box(A, (0.4, 0.5, 0.4), (0, 0.05, 0.2), "stone", bevel=0.02); cyl(A, 0.18, 0.06, (0, -0.05, 0.43), "wood", verts=16); cyl(A, 0.1, 0.07, (0, -0.05, 0.43), "black", verts=14)
        box(A, (0.4, 0.15, 0.6), (0, 0.28, 0.65), "stone_light", bevel=0.02)


@family("kitchen_fixture", "furniture", ["stone_counter", "butcher_block", "ice_vault"], cat="furniture", place="floor", tags=["kitchen", "wall-hug", "holds-decor"])
def _kitchen(A, v):
    k = v["n"]
    if k == "stone_counter":
        box(A, (1.2, 0.6, 0.86), (0, 0, 0.43), "stone", bevel=0.015); box(A, (1.24, 0.64, 0.06), (0, 0, 0.89), "stone_light", bevel=0.01)
        for x in (-0.3, 0.3): box(A, (0.5, 0.01, 0.6), (x, -0.305, 0.4), "stone_dark", bevel=0); tor(A, 0.02, 0.005, (x, -0.32, 0.55), "iron", rot=(PI / 2, 0, 0))
    elif k == "butcher_block":
        box(A, (1.2, 0.62, 0.86), (0, 0, 0.43), "wood", bevel=0.015); box(A, (1.26, 0.68, 0.1), (0, 0, 0.9), "wood_pale", bevel=0.01)
        box(A, (0.3, 0.02, 0.03), (0.3, -0.1, 0.96), "silver", rot=(0, 0, 0.3), bevel=0); box(A, (0.12, 0.03, 0.03), (0.15, -0.14, 0.96), "wood", rot=(0, 0, 0.3), bevel=0)
    elif k == "ice_vault":
        box(A, (0.72, 0.7, 1.85), (0, 0, 0.925), "stone_dark", bevel=0.02); box(A, (0.68, 0.03, 1.7), (0, -0.36, 0.95), "iron", bevel=0.005)
        for z in (0.5, 1.4): box(A, (0.7, 0.04, 0.06), (0, -0.38, z), "silver", bevel=0.003)
        box(A, (0.06, 0.05, 0.4), (0.28, -0.41, 1.1), "silver", bevel=0.005)
