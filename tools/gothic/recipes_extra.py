# ============ COMPOSITION PIECES (fireplaces, wall bookcases, kneelers, grand candelabras) ============

@family("fireplace", "composition", [{"n": "stone_hearth", "meta": {"light": 1.5, "lightColor": "#ff7a2a", "lightY": 0.6}}, {"n": "arch_hearth", "meta": {"light": 1.5, "lightColor": "#ff7a2a", "lightY": 0.6}},
                                     {"n": "bone_hearth", "meta": {"light": 1.5, "lightColor": "#ff8a3a", "lightY": 0.6}}, {"n": "grand_hearth", "meta": {"light": 1.9, "lightColor": "#ff7a2a", "lightY": 0.7}}],
        cat="hearth", place="floor", tags=["wall-hug", "hearth", "light", "glow", "focal"])
def _fireplace(A, v):
    k = v["n"]; W = 2.6 if k == "grand_hearth" else 1.8; H = 2.45; mat = "stone_light" if k != "obsidian" else "obsidian"
    box(A, (W, 0.7, 0.18), (0, 0.0, 0.09), "stone_dark", bevel=0.015)                               # hearth slab
    box(A, (W * 0.2, 0.7, 1.2), (-W * 0.4, 0.0, 0.78), mat, bevel=0.02); box(A, (W * 0.2, 0.7, 1.2), (W * 0.4, 0.0, 0.78), mat, bevel=0.02)  # jambs
    box(A, (W, 0.7, 0.22), (0, 0.0, 1.49), mat, bevel=0.02)                                         # lintel
    box(A, (W + 0.2, 0.85, 0.1), (0, -0.04, 1.65), "stone_dark", bevel=0.015)                       # mantel shelf
    box(A, (W * 0.78, 0.5, H - 1.7), (0, 0.1, 1.7 + (H - 1.7) / 2), "stone", bevel=0.02)             # chimney breast
    box(A, (W * 0.6, 0.35, 1.18), (0, 0.17, 0.77), "black", bevel=0)                                # firebox
    for i in range(3): cyl(A, 0.07, W * 0.5, (0, 0.05, 0.25 + 0.0), "wood", rot=(0, PI / 2, 0), verts=8).location.y += (i - 1) * 0.12
    for x in (-0.28, -0.1, 0.1, 0.3): sph(A, 0.11, (x, 0.05, 0.5 + 0.1 * (x == 0.1)), "flame", scale=(0.8, 0.8, 2.0), seg=8)
    sph(A, 0.3, (0, 0.05, 0.3), "ember", scale=(1.5, 1, 0.4), seg=10)
    if k == "arch_hearth": prism(A, arch_pts(W * 0.6, 0.6, 0.6), 0.04, (0, -0.2, 0.2), "stone_dark", bevel=0); skull(A, (0, -0.37, 1.56), 1.3, mat="bone")
    elif k == "bone_hearth":
        for x in np_range(-W * 0.4, W * 0.4, 0.25): skull(A, (x, -0.37, 1.45), 0.7, yaw=0)
        for s in (-1, 1): bone(A, (s * W * 0.38, -0.37, 0.2), (s * W * 0.38, -0.37, 1.4), 0.03)
    elif k == "grand_hearth":
        for s in (-1, 1): cyl(A, 0.12, 1.7, (s * (W / 2 - 0.12), -0.4, 0.95), "stone_light", verts=12); cyl(A, 0.16, 0.1, (s * (W / 2 - 0.12), -0.4, 1.85), "stone_dark", verts=12)
        tor(A, 0.25, 0.03, (0, -0.37, 2.0), "gold", rot=(PI / 2, 0, 0), seg=24); skull(A, (0, -0.37, 1.95), 1.0, mat="gold")
    elif k == "stone_hearth":
        for s in (-1, 1): cyl(A, 0.05, 0.1, (s * 0.5, -0.4, 1.75), "iron", r2=0.0, verts=6)
        box(A, (0.5, 0.05, 0.3), (0, -0.37, 2.0), "iron", bevel=0.005)


@family("wall_bookcase", "composition", ["oak", "arched", "locked"], cat="library", place="floor", tags=["storage", "wall-hug", "library-wall", "tall"])
def _wall_bookcase(A, v):
    k = v["n"]; W = 2.5; H = 2.3; mat = "wood_red" if k == "oak" else "wood"; rng = random.Random(len(k))
    for sx in (-1, 1): box(A, (0.06, 0.34, H), (sx * (W / 2 - 0.03), 0, H / 2), mat)
    box(A, (W, 0.02, H), (0, 0.16, H / 2), mat)
    for i in range(7): box(A, (W - 0.1, 0.34, 0.035), (0, 0, 0.02 + i * (H - 0.04) / 6), mat)
    for x in (-W / 6, W / 6): box(A, (0.04, 0.34, H), (x, 0, H / 2), mat)
    for i in range(6):
        for (x0, x1) in [(-W / 2 + 0.06, -W / 6), (-W / 6, W / 6), (W / 6, W / 2 - 0.06)]:
            xx = x0 + 0.03
            while xx < x1 - 0.06:
                bw = 0.03 + rng.random() * 0.04
                if rng.random() < 0.1: xx += 0.1; continue
                bh = 0.26 + rng.random() * 0.1; box(A, (bw, 0.22, bh), (xx + bw / 2, 0.0, 0.055 + i * (H - 0.04) / 6 + bh / 2), random.choice(BOOKS), bevel=0.003); xx += bw + 0.002
    box(A, (W + 0.08, 0.38, 0.1), (0, 0, H + 0.04), mat, bevel=0.01)
    if k == "arched":
        for x in (-W / 3, 0, W / 3): prism(A, arch_pts(W / 3 - 0.05, 0.0, 0.3), 0.3, (x, 0, H + 0.09), mat)
    elif k == "locked":
        for x in np_range(-W / 2 + 0.1, W / 2 - 0.1, 0.1): box(A, (0.015, 0.02, H - 0.2), (x, -0.18, H / 2), "iron", bevel=0)
        for z in (0.6, 1.2, 1.8): box(A, (W - 0.2, 0.02, 0.02), (0, -0.18, z), "iron", bevel=0)
        box(A, (0.1, 0.04, 0.14), (0.0, -0.2, 1.15), "gold", bevel=0.004)
    else: cyl(A, 0.015, W, (0, -0.2, H - 0.05), "iron", rot=(0, PI / 2, 0), verts=8)      # ladder rail


@family("kneeler", "composition", ["cushioned", "bone"], cat="sacred", place="floor", tags=["seating", "wall-hug", "decor"])
def _kneeler(A, v):
    k = v["n"]
    if k == "cushioned":
        box(A, (0.9, 0.4, 0.3), (0, 0, 0.15), "wood", bevel=0.01); box(A, (0.85, 0.34, 0.06), (0, -0.0, 0.33), "cloth", bevel=0.03); box(A, (0.9, 0.12, 0.7), (0, 0.18, 0.55), "wood", bevel=0.01); box(A, (0.88, 0.05, 0.08), (0, 0.18, 0.92), "wood_red")
    else:
        box(A, (0.9, 0.4, 0.08), (0, 0, 0.3), "bone", bevel=0.01); [bone(A, (s * 0.4, -0.15 + t * 0.3, 0.0), (s * 0.4, -0.15 + t * 0.3, 0.3), 0.03) for s in (-1, 1) for t in (0, 1)]
        box(A, (0.85, 0.34, 0.05), (0, 0, 0.35), "cloth2", bevel=0.02); bone(A, (-0.4, 0.2, 0.3), (-0.4, 0.2, 0.8), 0.03); bone(A, (0.4, 0.2, 0.3), (0.4, 0.2, 0.8), 0.03); bone(A, (-0.4, 0.2, 0.8), (0.4, 0.2, 0.8), 0.03)


@family("grand_candelabra", "composition", [{"n": "tall_iron", "meta": {"light": 1.5, "lightColor": "#ff9a3c", "lightY": 2.1}}, {"n": "twin_skull", "meta": {"light": 1.5, "lightColor": "#ff9a3c", "lightY": 2.0}}],
        cat="light", place="floor", tags=["corner", "light", "glow", "decor"])
def _grand_candelabra(A, v):
    k = v["n"]
    cyl(A, 0.24, 0.06, (0, 0, 0.03), "iron", r2=0.17, verts=20); cyl(A, 0.03, 1.9, (0, 0, 1.0), "iron", verts=10); [sph(A, 0.05, (0, 0, z), "iron", seg=8) for z in (0.4, 1.0, 1.55)]
    n = 9 if k == "tall_iron" else 6
    for px, py, _, a in ring_of(n, 0.3):
        limb(A, (0.05 * math.cos(a), 0.05 * math.sin(a), 1.75), (px, py, 1.98), 0.014, 0.011, "iron", 6); cyl(A, 0.034, 0.03, (px, py, 1.98), "iron", r2=0.045, verts=10); candle(A, (px, py, 2.0), h=0.2)
    candle(A, (0, 0, 1.92), h=0.28)
    if k == "twin_skull": [skull(A, (0, 0, z), 0.7, yaw=a) for z, a in ((0.45, 0.0), (1.0, PI))]
