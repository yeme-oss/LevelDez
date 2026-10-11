# ============ SACRED & DEATH (~65) ============

_ALTAR_META = lambda w, d, h: {"size": [w, d, h]}


@family("altar", "sacred", [{"n": "stone_slab", "meta": _ALTAR_META(1.6, 0.8, 1.0)}, {"n": "bone_altar", "meta": _ALTAR_META(1.6, 0.8, 1.0)}, {"n": "sacrificial", "meta": _ALTAR_META(1.7, 0.9, 0.95)},
                            {"n": "obsidian", "meta": _ALTAR_META(1.6, 0.8, 1.0)}, {"n": "reliquary_altar", "meta": _ALTAR_META(1.6, 0.8, 1.0)}, {"n": "black_altar", "meta": _ALTAR_META(1.5, 0.8, 1.0)},
                            {"n": "tiered_altar", "meta": _ALTAR_META(1.6, 0.9, 1.0)}],
        cat="sacred", place="floor", tags=["wall-hug", "holds-decor", "altar", "focal"])
def _altar(A, v):
    k = v["n"]; base = {"stone_slab": "stone_light", "bone_altar": "stone", "sacrificial": "stone", "obsidian": "obsidian", "reliquary_altar": "marble", "black_altar": "black", "tiered_altar": "stone_light"}[k]
    box(A, (1.6, 0.8, 0.12), (0, 0, 0.06), "stone_dark", bevel=0.02); box(A, (1.45, 0.65, 0.78), (0, 0, 0.51), base, bevel=0.02); box(A, (1.6, 0.8, 0.1), (0, 0, 0.95), base, bevel=0.02)
    for x in (-0.45, 0, 0.45): prism(A, arch_pts(0.34, 0.2, 0.7), 0.03, (x, -0.34, 0.28), "stone_dark" if k != "bone_altar" else "bone", bevel=0.004)
    if k == "bone_altar":
        for s in (-1, 1): bone(A, (s * 0.76, -0.38, 0.1), (s * 0.76, -0.38, 0.95), 0.04); skull(A, (s * 0.76, -0.38, 0.95), 0.0 + 0.01) if False else None
        for x in np_range(-0.6, 0.6, 0.15): skull(A, (x, -0.4, 0.72), 0.55)
    elif k == "sacrificial":
        box(A, (1.6, 0.7, 0.03), (0, 0, 1.015), "stone_dark", bevel=0); box(A, (0.06, 0.6, 0.02), (0.55, 0, 1.03), "blood", bevel=0)
        for s in (-1, 1):
            tor(A, 0.05, 0.01, (s * 0.7, -0.35, 0.75), "iron", rot=(PI / 2, 0, 0)); chain(A, (s * 0.7, -0.36, 0.72), (s * 0.7, -0.4, 0.5))
    elif k == "obsidian":
        tor(A, 0.3, 0.012, (0, 0, 1.005), "rune", seg=30); box(A, (1.5, 0.02, 0.02), (0, -0.395, 0.9), "rune", bevel=0)
    elif k == "reliquary_altar":
        box(A, (1.2, 0.5, 0.04), (0, 0, 1.0), "cloth", bevel=0); box(A, (1.65, 0.85, 0.03), (0, 0, 0.99), "gold", bevel=0)
    elif k == "black_altar":
        for s in (-1, 1): cyl(A, 0.05, 0.4, (s * 0.7, -0.38, 0.8), "iron", r2=0.0, verts=6)
    elif k == "tiered_altar":
        box(A, (1.0, 0.6, 0.12), (0, 0.0, 1.0), "stone", bevel=0.02); box(A, (1.0, 0.6, 0.0001 + 0.001), (0, 0, 1.06), "cloth", bevel=0)


@family("sarcophagus", "sacred", ["effigy", "knight", "winged", "skull_lid", "rune_carved", "open_lid", "double_effigy"], cat="sacred", place="floor", tags=["wall-hug"])
def _sarcophagus(A, v):
    k = v["n"]; W = 1.0 if k != "double_effigy" else 1.5
    box(A, (W, 2.2, 0.55), (0, 0, 0.275), "stone", bevel=0.03); box(A, (W + 0.08, 2.28, 0.1), (0, 0, 0.6), "stone_light", bevel=0.025)
    for sx in (-1, 1):
        for sy in (-1, 1): box(A, (0.12, 0.12, 0.7), (sx * (W / 2 + 0.02), sy * 1.1, 0.42), "stone", bevel=0.02)
    if k == "open_lid":
        box(A, (W - 0.1, 2.1, 0.05), (0, 0, 0.62), "black", bevel=0); box(A, (W - 0.1, 2.0, 0.16), (0.55, 0.35, 0.78), "stone_light", rot=(0, 0.3, 0.2), bevel=0.04)
        sph(A, 0.07, (0, 0.65, 0.68), "bone", scale=(1, 1.1, 0.9), seg=10); box(A, (0.25, 0.4, 0.06), (0, 0.2, 0.66), "bone", bevel=0.02); bone(A, (-0.1, 0.3, 0.66), (-0.12, -0.3, 0.66), 0.02); bone(A, (0.1, 0.3, 0.66), (0.12, -0.3, 0.66), 0.02)
        return
    box(A, (W - 0.1, 2.1, 0.16), (0, 0, 0.73), "stone_light", bevel=0.04)
    def effigy(x, big=True):
        box(A, (0.34, 0.9, 0.09), (x, 0.15, 0.85), "stone_light", bevel=0.03); sph(A, 0.15, (x, 0.82, 0.88), "stone_light", scale=(1, 1.1, 0.9)); box(A, (0.28, 0.7, 0.07), (x, -0.55, 0.84), "stone_light", bevel=0.03)
        for sx in (-1, 1): box(A, (0.06, 0.5, 0.06), (x + sx * 0.1, 0.35, 0.91), "stone_light", rot=(0, 0, sx * 0.35), bevel=0.01)
    if k in ("effigy", "winged", "skull_lid", "rune_carved", "knight"): effigy(0)
    if k == "double_effigy": effigy(-0.3); effigy(0.3)
    if k == "knight": box(A, (0.06, 0.9, 0.04), (0.0, 0.0, 0.93), "iron", bevel=0.005); box(A, (0.3, 0.05, 0.04), (0, 0.45, 0.93), "iron", bevel=0.005)
    if k == "winged":
        for s in (-1, 1): prism(A, [(0, 0), (0.5 * s, 0.1), (0.7 * s, 0.7), (0.3 * s, 0.9), (0, 0.5)] if s > 0 else [(0, 0), (0, 0.5), (-0.3, 0.9), (-0.7, 0.7), (-0.5, 0.1)], 0.04, (s * 0.15, 0.25, 0.96), "stone_light", rot=(PI / 2, 0, 0), bevel=0.005)
    if k == "skull_lid": skull(A, (0, 0.0, 0.82), 2.5, mat="stone_light"); [skull(A, (s * 0.38, y, 0.82), 0.9, mat="stone_light") for s in (-1, 1) for y in (-0.6, 0.6)]
    if k == "rune_carved":
        for y in np_range(-0.9, 0.9, 0.3):
            for s in (-1, 1): box(A, (0.03, 0.1, 0.012), (s * 0.4, y, 0.815), "rune", bevel=0)


@family("coffin", "sacred", ["plain", "iron_bound", "glass_lid", "ajar", "upright", "double", "chained"], cat="sacred", place="floor", tags=["wall-hug"])
def _coffin(A, v):
    k = v["n"]; out = [(-0.16, -1.0), (0.16, -1.0), (0.3, 0.45), (0.22, 1.0), (-0.22, 1.0), (-0.3, 0.45)]
    if k == "upright":
        prism(A, topview(out), 0.5, (0, 0, 1.05), "wood_red", rot=(0, 0, 0), bevel=0.02) if False else None
        # standing coffin: build with the outline in the XZ plane (head at top)
        pts = [(-0.16, 0.0), (0.16, 0.0), (0.3, 1.45), (0.22, 2.0), (-0.22, 2.0), (-0.3, 1.45)]
        prism(A, pts, 0.5, (0, 0, 0.1), "wood_red", bevel=0.02); prism(A, [(x * 0.8, 0.15 + y * 0.9) for x, y in pts], 0.05, (0, -0.27, 0.1), "wood", bevel=0.008)
        box(A, (0.05, 0.02, 0.9), (0, -0.31, 1.35), "gold", bevel=0); box(A, (0.3, 0.02, 0.05), (0, -0.31, 1.55), "gold", bevel=0); box(A, (0.5, 0.5, 0.1), (0, 0, 0.05), "stone")
        return
    if k == "double": out = [(x * 1.9, y) for x, y in out]
    prism(A, topview(out), 0.42, (0, 0, 0.36), "wood_red" if k != "iron_bound" else "wood", rot=(PI / 2, 0, 0), bevel=0.02)
    lid = [(x * 0.88, y * 0.96) for x, y in out]
    if k == "glass_lid":
        prism(A, topview(lid), 0.05, (0, 0, 0.6), "glass", rot=(PI / 2, 0, 0), bevel=0.005); box(A, (0.3, 1.2, 0.06), (0, 0.1, 0.5), "bone", bevel=0.03); sph(A, 0.09, (0, 0.8, 0.55), "bone", scale=(1, 1.1, 0.9))
    elif k == "ajar":
        prism(A, topview(out), 0.04, (0, 0, 0.58), "black", rot=(PI / 2, 0, 0), bevel=0)
        prism(A, topview(lid), 0.06, (0.18, -0.15, 0.66), "wood", rot=(PI / 2, 0.0, 0.3), bevel=0.01)
    else:
        prism(A, topview(lid), 0.06, (0, 0, 0.6), "wood" if k != "chained" else "black", rot=(PI / 2, 0, 0), bevel=0.015)
        box(A, (0.06, 0.62, 0.012), (0, 0.18, 0.636), "gold", bevel=0); box(A, (0.3, 0.06, 0.012), (0, 0.4, 0.636), "gold", bevel=0)
    if k == "iron_bound":
        for y in (-0.6, 0.0, 0.5): box(A, (0.72, 0.06, 0.5), (0, y, 0.38), "iron", bevel=0.004)
    if k == "chained":
        for y in (-0.5, 0.2): chain(A, (-0.32, y, 0.4), (0.0, y, 0.68)); chain(A, (0.32, y, 0.4), (0.0, y, 0.68))
        tor(A, 0.06, 0.012, (0, 0.2, 0.68), "iron", seg=14)
    for sx in (-1, 1):
        for sy in (-0.8, 0.8): box(A, (0.08, 0.1, 0.12), (sx * 0.2 * (2.0 if k == "double" else 1), sy, 0.06), "wood")


@family("tombstone", "sacred", ["celtic_cross", "angel_marker", "obelisk_small", "broken_stone", "skull_stone", "urn_stone", "iron_cross", "twin_slabs"], cat="sacred", place="floor", tags=["wall-hug", "decor"])
def _tombstone(A, v):
    k = v["n"]; box(A, (0.8, 0.4, 0.1), (0, 0, 0.05), "stone", bevel=0.02)
    if k == "celtic_cross":
        box(A, (0.14, 0.12, 1.2), (0, 0, 0.7), "stone_light", bevel=0.01); box(A, (0.6, 0.12, 0.14), (0, 0, 0.95), "stone_light", bevel=0.01); tor(A, 0.2, 0.03, (0, -0.0, 0.95), "stone_light", rot=(PI / 2, 0, 0), seg=20)
    elif k == "angel_marker":
        box(A, (0.5, 0.3, 0.5), (0, 0, 0.35), "stone_light", bevel=0.02); lathe(A, [(0.17, 0), (0.12, 0.3), (0.1, 0.5), (0.06, 0.55)], (0, 0, 0.6), "marble", verts=12); sph(A, 0.07, (0, 0, 1.2), "marble")
        for s in (-1, 1): prism(A, [(0, 0), (s * 0.35, 0.15), (s * 0.4, 0.55), (s * 0.1, 0.45)] if s > 0 else [(0, 0), (-0.1, 0.45), (-0.4, 0.55), (-0.35, 0.15)], 0.03, (s * 0.04, 0.1, 0.75), "marble", rot=(0, 0, 0), bevel=0.003)
    elif k == "obelisk_small":
        box(A, (0.4, 0.4, 0.3), (0, 0, 0.25), "stone_light", bevel=0.02); box(A, (0.28, 0.28, 1.0), (0, 0, 0.9), "stone_light", bevel=0.01); cyl(A, 0.2, 0.3, (0, 0, 1.55), "stone_light", r2=0.0, verts=4, rot=(0, 0, PI / 4))
    elif k == "broken_stone":
        prism(A, [(-0.3, 0), (0.3, 0), (0.3, 0.55), (0.1, 0.7), (-0.05, 0.5), (-0.3, 0.6)], 0.14, (0, 0, 0.1), "stone_light", bevel=0.01); box(A, (0.2, 0.12, 0.15), (0.45, 0.2, 0.07), "stone_light", rot=(0.3, 0.2, 0.5), bevel=0.01)
    elif k == "skull_stone":
        prism(A, arch_pts(0.62, 0.5, 0.55), 0.14, (0, 0, 0.1), "stone_light", bevel=0.012); skull(A, (0, -0.07, 0.65), 1.0, mat="bone")
    elif k == "urn_stone":
        box(A, (0.45, 0.3, 0.6), (0, 0, 0.4), "stone_light", bevel=0.02); lathe(A, [(0.1, 0), (0.16, 0.12), (0.12, 0.28), (0.06, 0.34)], (0, 0, 0.7), "stone_dark", verts=14)
    elif k == "iron_cross":
        box(A, (0.06, 0.06, 1.1), (0, 0, 0.65), "iron", bevel=0.004); box(A, (0.5, 0.06, 0.06), (0, 0, 0.95), "iron", bevel=0.004); cyl(A, 0.04, 0.12, (0, 0, 1.25), "iron", r2=0.0, verts=6)
    elif k == "twin_slabs":
        for x in (-0.22, 0.22): prism(A, arch_pts(0.34, 0.4, 0.5), 0.12, (x, 0, 0.1), "stone_light", bevel=0.01)


@family("crypt_niche", "sacred", ["skull_niche", "ossuary_wall", "sealed_slab", "coffin_slot"], cat="sacred", place="wall", y=0.3, tags=["decor"])
def _niche(A, v):
    k = v["n"]
    box(A, (1.1, 0.3, 1.9), (0, 0.15, 0.95), "stone_dark", bevel=0.01)
    if k == "skull_niche":
        prism(A, arch_pts(0.6, 0.5, 0.7), 0.1, (0, -0.0, 0.4), "black", bevel=0); arch_ring(A, 0.62, 0.5, 0.7, 0.07, 0.14, (0, -0.05, 0.4), "stone_light", n=5)
        for x in (-0.15, 0.15): skull(A, (x, 0.0, 0.42), 1.0)
        skull(A, (0, 0.0, 0.58), 1.0)
    elif k == "ossuary_wall":
        for i in range(5):
            for j in range(4): skull(A, (-0.4 + j * 0.27 + (0.13 if i % 2 else 0), -0.13, 0.15 + i * 0.35), 1.1, mat="bone" if (i + j) % 2 else "ivory")
        for i in range(3): bone(A, (-0.5, -0.14, 0.4 + i * 0.5), (0.5, -0.14, 0.4 + i * 0.5), 0.02)
    elif k == "sealed_slab":
        box(A, (0.95, 0.06, 1.6), (0, -0.04, 0.9), "stone_light", bevel=0.02); box(A, (0.5, 0.02, 0.3), (0, -0.08, 1.3), "stone", bevel=0)
        for y in (1.1, 1.2): box(A, (0.4, 0.015, 0.02), (0, -0.09, y), "stone_dark", bevel=0)
        for s in (-1, 1): tor(A, 0.04, 0.01, (s * 0.35, -0.08, 0.2), "iron", rot=(PI / 2, 0, 0))
    elif k == "coffin_slot":
        prism(A, topview([(-0.28, -0.2), (0.28, -0.2), (0.4, 0.1), (0.3, 0.2), (-0.3, 0.2), (-0.4, 0.1)]), 1.9, (0, -0.0, 0.95), "black", rot=(0, PI / 2, 0), bevel=0) if False else box(A, (0.8, 0.02, 0.6), (0, -0.03, 0.6), "black", bevel=0)
        box(A, (0.85, 0.12, 0.65), (0, -0.07, 0.6), "wood_red", bevel=0.02); box(A, (0.8, 0.02, 0.5), (0, -0.14, 0.6), "wood", bevel=0.005); box(A, (0.06, 0.02, 0.4), (0, -0.15, 0.6), "gold", bevel=0)


# ---- statues on plinths ----
def _plinth(A, w=0.6, h=0.3, mat="stone"):
    box(A, (w, w, h), (0, 0, h / 2), mat, bevel=0.02); box(A, (w + 0.08, w + 0.08, 0.06), (0, 0, 0.03), "stone_dark", bevel=0.01); box(A, (w + 0.05, w + 0.05, 0.05), (0, 0, h - 0.02), "stone_light", bevel=0.01)


def _robed(A, mat, z0=0.3, H=1.1):
    lathe(A, [(0.27, 0), (0.22, 0.35 * H), (0.15, 0.8 * H), (0.14, 0.95 * H), (0.1, H)], (0, 0, z0), mat, verts=18)
    for s in (-1, 1): limb(A, (s * 0.13, 0, z0 + H * 0.92), (s * 0.19, -0.2, z0 + H * 0.68), 0.04, 0.03, mat, 8)


@family("statue", "sacred", ["reaper", "mourning_angel", "knight", "skeleton_warrior", "hooded_monk", "gargoyle_perched", "gargoyle_winged", "raven", "lich", "demon", "saint_praying", "dragon_skull"],
        cat="sacred", place="floor", tags=["wall-hug", "decor"])
def _statue(A, v):
    k = v["n"]; _plinth(A)
    if k == "reaper":
        _robed(A, "black"); sph(A, 0.13, (0, 0, 1.55), "black", scale=(1, 1.1, 1.1)); skull(A, (0, -0.05, 1.4), 0.9); limb(A, (-0.28, -0.22, 0.3), (-0.3, -0.22, 2.0), 0.02, 0.02, "wood")
        prism(A, [(0, 0), (-0.45, 0.05), (-0.55, -0.12), (-0.12, -0.04)], 0.015, (-0.28, -0.22, 1.98), "silver", rot=(0, 0, 0), bevel=0.002)
    elif k == "mourning_angel":
        _robed(A, "marble"); sph(A, 0.1, (0, -0.04, 1.45), "marble");
        for s in (-1, 1): prism(A, [(0, 0), (s * 0.5, 0.2), (s * 0.7, 0.9), (s * 0.3, 1.1), (s * 0.1, 0.5)] if s > 0 else [(0, 0), (-0.1, 0.5), (-0.3, 1.1), (-0.7, 0.9), (-0.5, 0.2)], 0.04, (s * 0.1, 0.18, 0.95), "marble", bevel=0.004)
        limb(A, (-0.12, -0.2, 1.1), (-0.04, -0.14, 1.4), 0.03, 0.03, "marble"); limb(A, (0.12, -0.2, 1.1), (0.04, -0.14, 1.4), 0.03, 0.03, "marble")
    elif k == "knight":
        box(A, (0.34, 0.22, 0.55), (0, 0, 0.78), "iron", bevel=0.03); box(A, (0.14, 0.14, 0.5), (-0.09, 0, 0.5), "iron"); box(A, (0.14, 0.14, 0.5), (0.09, 0, 0.5), "iron"); box(A, (0.2, 0.22, 0.24), (0, 0, 1.18), "iron", bevel=0.03)
        box(A, (0.12, 0.02, 0.03), (0, -0.115, 1.2), "black", bevel=0); box(A, (0.05, 0.03, 0.8), (0.0, -0.3, 1.0), "silver", bevel=0.004); box(A, (0.3, 0.04, 0.04), (0.0, -0.3, 0.7), "gold", bevel=0.004)
        for s in (-1, 1): limb(A, (s * 0.2, 0, 1.0), (s * 0.12, -0.3, 0.75), 0.04, 0.035, "iron")
    elif k == "skeleton_warrior":
        for z in np_range(0.75, 1.15, 0.1): tor(A, 0.1, 0.015, (0, 0, z), "bone", seg=14).data.transform(Matrix.Diagonal((1, 0.7, 1, 1)))
        limb(A, (0, 0.05, 0.4), (0, 0.05, 1.2), 0.025, 0.025, "bone"); box(A, (0.24, 0.12, 0.1), (0, 0, 0.6), "bone", bevel=0.03)
        for s in (-1, 1): bone(A, (s * 0.07, 0, 0.6), (s * 0.08, 0, 0.3), 0.02); bone(A, (s * 0.12, 0, 1.1), (s * 0.2, -0.2, 0.9), 0.016)
        skull(A, (0, 0, 1.25), 1.1); box(A, (0.04, 0.02, 0.7), (0.2, -0.22, 0.95), "rust", bevel=0)
    elif k == "hooded_monk":
        _robed(A, "stone_light", H=1.2); sph(A, 0.15, (0, 0.0, 1.62), "stone_light", scale=(1, 1.1, 1.1)); box(A, (0.12, 0.05, 0.1), (0, -0.12, 1.5), "black", bevel=0.01)
        box(A, (0.1, 0.08, 0.12), (0, -0.2, 1.05), "stone_light", bevel=0.02)
    elif k in ("gargoyle_perched", "gargoyle_winged"):
        box(A, (0.5, 0.5, 0.0001), (0, 0, 0.3), "stone", bevel=0); sph(A, 0.2, (0, 0.02, 0.58), "stone_light", scale=(1.1, 1.3, 1.0)); sph(A, 0.13, (0, -0.2, 0.78), "stone_light"); box(A, (0.1, 0.1, 0.07), (0, -0.31, 0.74), "stone_light")
        for s in (-1, 1):
            limb(A, (s * 0.08, -0.2, 0.9), (s * 0.15, -0.2, 1.05), 0.025, 0.004, "stone", 6); sph(A, 0.012, (s * 0.05, -0.31, 0.82), "ember", seg=6)
            w = 0.9 if k == "gargoyle_winged" else 0.5
            prism(A, [(0, 0), (s * w * 0.9, 0.1), (s * w, 0.5), (s * w * 0.5, 0.7), (0, 0.4)] if s > 0 else [(0, 0), (0, 0.4), (-w * 0.5, 0.7), (-w, 0.5), (-w * 0.9, 0.1)], 0.03, (s * 0.12, 0.1, 0.55), "stone", bevel=0.004)
            box(A, (0.08, 0.28, 0.08), (s * 0.14, -0.2, 0.45), "stone_light", rot=(0.3, 0, 0), bevel=0.01)
    elif k == "raven":
        cyl(A, 0.03, 0.9, (0, 0, 0.75), "iron", verts=8); sph(A, 0.14, (0, 0, 1.3), "black", scale=(0.8, 1.4, 0.9)); sph(A, 0.08, (0, -0.18, 1.42), "black")
        cyl(A, 0.025, 0.14, (0, -0.28, 1.42), "gold", r2=0.0, rot=(PI / 2, 0, 0), verts=6); sph(A, 0.012, (0.04, -0.23, 1.45), "ember", seg=6)
        for s in (-1, 1): prism(A, [(0, 0), (s * 0.4, 0.1), (s * 0.3, 0.35), (0, 0.3)] if s > 0 else [(0, 0), (0, 0.3), (-0.3, 0.35), (-0.4, 0.1)], 0.02, (s * 0.1, 0.0, 1.22), "black", rot=(0, 0, 0), bevel=0)
    elif k == "lich":
        _robed(A, "cloth2", H=1.2); skull(A, (0, 0, 1.35), 1.4, glow="ecto");
        for i in range(5): a = -0.8 + i * 0.4; cyl(A, 0.012, 0.12, (0.0 + 0.12 * math.sin(a), 0.02, 1.62 + 0.04 * math.cos(a)), "gold", r2=0.0, verts=5)
        limb(A, (0.3, -0.25, 0.3), (0.3, -0.25, 1.8), 0.02, 0.02, "wood"); sph(A, 0.08, (0.3, -0.25, 1.88), "ecto", seg=10)
    elif k == "demon":
        sph(A, 0.22, (0, 0, 0.7), "stone_dark", scale=(1, 0.9, 1.4)); sph(A, 0.13, (0, -0.05, 1.18), "stone_dark")
        for s in (-1, 1):
            limb(A, (s * 0.08, -0.05, 1.28), (s * 0.2, -0.05, 1.55), 0.03, 0.005, "black", 6); sph(A, 0.012, (s * 0.05, -0.17, 1.2), "ember", seg=6)
            prism(A, [(0, 0), (s * 0.7, 0.2), (s * 0.9, 0.8), (s * 0.4, 0.7), (s * 0.1, 0.4)] if s > 0 else [(0, 0), (-0.1, 0.4), (-0.4, 0.7), (-0.9, 0.8), (-0.7, 0.2)], 0.03, (s * 0.15, 0.15, 0.6), "black", bevel=0.004)
            limb(A, (s * 0.2, -0.05, 0.9), (s * 0.28, -0.25, 0.7), 0.045, 0.03, "stone_dark")
    elif k == "saint_praying":
        _robed(A, "stone_light", H=1.1); sph(A, 0.09, (0, -0.02, 1.48), "stone_light"); tor(A, 0.12, 0.012, (0, 0.08, 1.58), "gold", rot=(PI / 2.5, 0, 0), seg=20); box(A, (0.1, 0.08, 0.14), (0, -0.2, 1.05), "stone_light", bevel=0.02)
    elif k == "dragon_skull":
        box(A, (0.4, 0.9, 0.12), (0, 0, 0.36), "stone", bevel=0.02); box(A, (0.3, 0.8, 0.2), (0, -0.1, 0.52), "bone", bevel=0.03); sph(A, 0.22, (0, 0.28, 0.65), "bone", scale=(1, 1.1, 0.9))
        for s in (-1, 1):
            sph(A, 0.06, (s * 0.1, 0.08, 0.7), "black"); sph(A, 0.025, (s * 0.1, 0.03, 0.7), "ember", seg=6); limb(A, (s * 0.15, 0.4, 0.78), (s * 0.35, 0.65, 1.1), 0.05, 0.008, "black", 6)
            for i in range(5): cyl(A, 0.014, 0.08, (s * 0.12, -0.35 + i * 0.12, 0.43), "ivory", r2=0.0, rot=(PI, 0, 0), verts=5)


@family("slab", "sacred", ["sacrificial_blood", "dissection_chained"], cat="sacred", place="floor", tags=["wall-hug", "holds-decor"], size=[1.0, 2.0, 0.9])
def _slab(A, v):
    box(A, (1.0, 2.0, 0.78), (0, 0, 0.39), "stone", bevel=0.03); box(A, (1.1, 2.1, 0.1), (0, 0, 0.83), "stone_light", bevel=0.03)
    if v["n"] == "sacrificial_blood":
        for x in (-0.3, 0.3): box(A, (0.04, 1.6, 0.015), (x, 0, 0.885), "blood", bevel=0)
        box(A, (0.5, 0.25, 0.02), (0, -0.7, 0.885), "blood", rot=(0, 0, 0.2), bevel=0)
    else:
        for s in (-1, 1):
            for y in (-0.75, 0.55): tor(A, 0.05, 0.01, (s * 0.52, y, 0.8), "iron", rot=(0, PI / 2, 0)); chain(A, (s * 0.52, y, 0.78), (s * 0.55, y, 0.5))


@family("font", "sacred", ["blood_font", "bone_font", "soul_font"], cat="sacred", place="floor", tags=["wall-hug", "decor", "light"],
        light=0.5, lightColor="#ff3030", lightY=0.9)
def _font(A, v):
    k = v["n"]; liq = {"blood_font": "blood", "bone_font": "ecto", "soul_font": "soulfire"}[k]
    lathe(A, [(0.3, 0), (0.2, 0.05), (0.14, 0.5), (0.22, 0.65), (0.4, 0.75), (0.42, 0.85), (0.34, 0.85), (0.34, 0.8)], (0, 0, 0), "bone" if k == "bone_font" else "stone_light", verts=24)
    cyl(A, 0.33, 0.02, (0, 0, 0.8), liq, verts=20)
    if k == "bone_font":
        for i in range(6): a = i * PI / 3; skull(A, (0.4 * math.cos(a), 0.4 * math.sin(a), 0.7), 0.6, yaw=a + PI / 2)
    if k == "soul_font":
        for i in range(3): a = i * 2 * PI / 3; limb(A, (0.1 * math.cos(a), 0.1 * math.sin(a), 0.82), (0.05 * math.cos(a), 0.05 * math.sin(a), 1.2 + 0.1 * i), 0.03, 0.002, "soulfire", 6)


@family("reliquary", "sacred", ["casket", "skull_shrine", "monstrance", "bone_box"], cat="sacred", place="surface", tags=["decor"])
def _reliquary(A, v):
    k = v["n"]
    if k == "casket":
        box(A, (0.3, 0.16, 0.12), (0, 0, 0.06), "gold", bevel=0.01); prism(A, [(-0.15, 0), (0.15, 0), (0.1, 0.08), (-0.1, 0.08)], 0.16, (0, 0, 0.12), "gold", rot=(0, 0, 0), bevel=0.005)
        for x in (-0.08, 0.08): sph(A, 0.018, (x, -0.085, 0.07), "potion_red", seg=6)
    elif k == "skull_shrine":
        box(A, (0.22, 0.2, 0.04), (0, 0, 0.02), "gold"); cyl(A, 0.11, 0.18, (0, 0, 0.13), "glass", verts=12); skull(A, (0, 0, 0.05), 0.9); cyl(A, 0.12, 0.02, (0, 0, 0.23), "gold", verts=12)
    elif k == "monstrance":
        cyl(A, 0.1, 0.02, (0, 0, 0.01), "gold", r2=0.08, verts=16); cyl(A, 0.015, 0.2, (0, 0, 0.12), "gold", verts=8); tor(A, 0.08, 0.012, (0, 0, 0.3), "gold", rot=(PI / 2, 0, 0), seg=18); sph(A, 0.04, (0, 0, 0.3), "ecto", seg=8)
        for i in range(12): a = i * PI / 6; cyl(A, 0.006, 0.07, (0.12 * math.cos(a), 0, 0.3 + 0.12 * math.sin(a)), "gold", r2=0.0, rot=(0, PI / 2 - a, 0), verts=4)
    elif k == "bone_box":
        box(A, (0.26, 0.16, 0.1), (0, 0, 0.05), "bone", bevel=0.01); box(A, (0.28, 0.18, 0.03), (0, 0, 0.115), "ivory", bevel=0.005); skull(A, (0, -0.0, 0.13), 0.35)


@family("bone_heap", "sacred", ["skull_pile_big", "bone_scatter", "ribcage_heap", "femur_stack", "ossuary_cart", "skull_pyramid"], cat="sacred", place="floor", tags=["wall-hug", "decor"])
def _heap(A, v):
    k = v["n"]; rng = random.Random(len(k))
    if k == "skull_pile_big":
        for i in range(12): a = rng.random() * 6.28; r = rng.random() * 0.28; skull(A, (r * math.cos(a), r * math.sin(a), 0.0 + (0.1 if r < 0.15 else 0.0)), 0.9 + rng.random() * 0.2, yaw=rng.random() * 6.28)
        for i in range(4): skull(A, (rng.random() * 0.15 - 0.075, rng.random() * 0.15 - 0.075, 0.2), 0.95, yaw=rng.random() * 6.28)
    elif k == "bone_scatter":
        for i in range(14): a = rng.random() * 6.28; r = 0.1 + rng.random() * 0.4; bone(A, (r * math.cos(a), r * math.sin(a), 0.015), (r * math.cos(a) + 0.2 * math.cos(a + 1), r * math.sin(a) + 0.2 * math.sin(a + 1), 0.015), 0.014)
        for i in range(3): skull(A, (rng.random() * 0.4 - 0.2, rng.random() * 0.4 - 0.2, 0.0), 0.9, yaw=rng.random() * 6.28)
    elif k == "ribcage_heap":
        for i in range(3):
            for j in range(5): tor(A, 0.1 - j * 0.008, 0.01, (i * 0.25 - 0.25, 0.0, 0.08 + j * 0.03), "bone", rot=(PI / 2, 0, 0.1 * i), seg=12, minor=4)
        for i in range(8): bone(A, (rng.random() * 0.5 - 0.25, rng.random() * 0.4 - 0.2, 0.02), (rng.random() * 0.5 - 0.25, rng.random() * 0.4 - 0.2, 0.05), 0.015)
    elif k == "femur_stack":
        for i in range(3):
            for j in range(4 - i): bone(A, (-0.35, -0.1 + j * 0.06 + i * 0.03, 0.03 + i * 0.04), (0.35, -0.1 + j * 0.06 + i * 0.03, 0.03 + i * 0.04), 0.02)
    elif k == "ossuary_cart":
        box(A, (0.9, 0.55, 0.06), (0, 0, 0.35), "wood", bevel=0.01)
        for s in (-1, 1): box(A, (0.04, 0.55, 0.3), (s * 0.44, 0, 0.52), "wood"); cyl(A, 0.2, 0.05, (s * 0.5, 0.0, 0.2), "wood", rot=(0, PI / 2, 0), verts=14)
        for i in range(8): skull(A, (-0.3 + (i % 4) * 0.2, -0.12 + (i // 4) * 0.22, 0.38), 1.0, yaw=i)
    elif k == "skull_pyramid":
        n = 4; idx = 0
        for row in range(n):
            for i in range(n - row): skull(A, (-(n - row - 1) * 0.1 + i * 0.2, 0.0, 0.0 + row * 0.1), 1.0)


@family("hanging_remains", "sacred", ["skeleton_wall", "skeleton_cage", "skeleton_seated"], cat="sacred", place="floor", tags=["decor", "wall-hug"])
def _remains(A, v):
    k = v["n"]
    def skeleton(x, y, z0, sit=False):
        skull(A, (x, y, z0 + 1.35), 1.0); limb(A, (x, y + 0.04, z0 + 0.7), (x, y + 0.04, z0 + 1.3), 0.015, 0.015, "bone")
        for j in range(5): tor(A, 0.09 - j * 0.005, 0.01, (x, y + 0.03, z0 + 0.95 + j * 0.06), "bone", seg=12, minor=4)
        box(A, (0.22, 0.1, 0.08), (x, y + 0.03, z0 + 0.65), "bone", bevel=0.02)
        for s in (-1, 1):
            bone(A, (x + s * 0.12, y, z0 + 1.2), (x + s * 0.2, y - 0.1, z0 + 0.8), 0.014); bone(A, (x + s * 0.07, y, z0 + 0.62), (x + s * 0.08, y - (0.35 if sit else 0.0), z0 + (0.5 if sit else 0.25)), 0.02)
    if k == "skeleton_wall":
        box(A, (1.0, 0.1, 0.1), (0, 0.2, 1.9), "iron", bevel=0.004)
        for s in (-1, 1): chain(A, (s * 0.35, 0.18, 1.88), (s * 0.3, 0.15, 1.3)); tor(A, 0.04, 0.01, (s * 0.3, 0.15, 1.28), "iron", rot=(0, 0, 0))
        skeleton(0, 0.1, 0.0)
    elif k == "skeleton_cage":
        for a in np_range(0, 6.2, 0.52): limb(A, (0.4 * math.cos(a), 0.4 * math.sin(a), 0.0), (0.3 * math.cos(a), 0.3 * math.sin(a), 1.6), 0.012, 0.01, "iron", 6)
        for z in (0.0, 0.7, 1.4): tor(A, 0.38 - z * 0.06, 0.012, (0, 0, z + 0.02), "iron", seg=24)
        cyl(A, 0.3, 0.04, (0, 0, 1.62), "iron", r2=0.05, verts=16); skeleton(0, 0, 0.0, True)
    elif k == "skeleton_seated":
        box(A, (0.6, 0.6, 0.45), (0, 0.15, 0.225), "stone", bevel=0.02); skeleton(0, 0.15, 0.25, True)


@family("grave_mound", "sacred", ["fresh_grave", "mossy_grave"], cat="sacred", place="floor", tags=["wall-hug", "decor"])
def _mound(A, v):
    lathe(A, [(0.0, 0.3), (0.35, 0.22), (0.7, 0.05), (0.85, 0.0)], (0, 0, 0), "moss" if v["n"] == "mossy_grave" else "ash", verts=20, scale=1.0)
    box(A, (0.05, 0.05, 0.7), (0, 0.5, 0.45), "wood", bevel=0.005); box(A, (0.35, 0.05, 0.05), (0, 0.5, 0.65), "wood", bevel=0.005)
    for i in range(5): sph(A, 0.05, (-0.2 + i * 0.1, -0.1, 0.08 + 0.03 * (i % 2)), "ash", scale=(1, 1, 0.6), seg=6)
