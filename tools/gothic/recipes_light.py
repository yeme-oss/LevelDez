# ============ LIGHTING (~41) ============
WARM = "#ff9a3c"; COLD = "#4dffd0"; VIOLET = "#b070ff"; FIRE = "#ff7a2a"


def _L(color, i, y):
    return {"light": i, "lightColor": color, "lightY": y, "tags": ["light", "glow"]}


def _arms(A, n, r, z, r0=0.04, mat="iron", fl="flame", h=0.18, soul=False):
    for px, py, _, a in ring_of(n, r):
        limb(A, (r0 * math.cos(a), r0 * math.sin(a), z - 0.12), (px, py, z), 0.014, 0.011, mat, 6)
        cyl(A, 0.03, 0.025, (px, py, z + 0.0), mat, r2=0.04, verts=10)
        cyl(A, 0.022, h, (px, py, z + 0.0125 + h / 2), "wax" if not soul else "bone", verts=10)
        sph(A, 0.014, (px, py, z + h + 0.035), fl, scale=(1, 1, 1.9), seg=6)


@family("candelabra", "lighting", [{"n": "five_arm", "meta": _L(WARM, 1.1, 1.62)}, {"n": "bone_tall", "meta": _L(WARM, 1.1, 1.7)}, {"n": "seven_branch", "meta": _L(WARM, 1.3, 1.5)},
                                   {"n": "twisted_iron", "meta": _L(WARM, 1.0, 1.55)}, {"n": "skull_base", "meta": _L(WARM, 1.0, 1.5)}, {"n": "soul_flame", "meta": _L(COLD, 1.2, 1.6)}],
        cat="light", place="floor", tags=["corner", "light", "glow"])
def _candelabra(A, v):
    k = v["n"]; fl = "soulfire" if k == "soul_flame" else "flame"
    base = "bone" if k == "bone_tall" else "iron"
    cyl(A, 0.2, 0.05, (0, 0, 0.025), base, r2=0.14, verts=20)
    if k == "bone_tall":
        bone(A, (0, 0, 0.05), (0, 0, 1.3), 0.03); [skull(A, (0.0, 0, 0.5 + 0.35 * i), 0.5, yaw=PI * i) for i in range(2)]
    elif k == "twisted_iron":
        for i in range(2): a = i * PI; [limb(A, (0.04 * math.cos(a + t * 0.9), 0.04 * math.sin(a + t * 0.9), 0.05 + t * 0.12), (0.04 * math.cos(a + (t + 1) * 0.9), 0.04 * math.sin(a + (t + 1) * 0.9), 0.05 + (t + 1) * 0.12), 0.012, 0.012, "iron", 6) for t in range(10)]
    elif k == "skull_base":
        skull(A, (0, 0, 0.05), 1.6, mat="ivory"); cyl(A, 0.02, 1.0, (0, 0, 0.8), "iron", verts=8)
    else: cyl(A, 0.022, 1.25, (0, 0, 0.65), "iron", verts=10); [sph(A, 0.04, (0, 0, z), "iron", seg=8) for z in (0.35, 0.85)]
    n = 7 if k == "seven_branch" else 5
    _arms(A, n, 0.22 if n == 5 else 0.28, 1.38 if k != "bone_tall" else 1.45, fl=fl, soul=(k == "soul_flame")); candle(A, (0, 0, 1.3), h=0.25) if k != "soul_flame" else sph(A, 0.03, (0, 0, 1.42), "soulfire", scale=(1, 1, 1.8), seg=6)


@family("chandelier", "lighting", [{"n": "wagon_wheel", "meta": _L(WARM, 2.0, 0.4)}, {"n": "bone_ring", "meta": _L(WARM, 1.8, 0.4)}, {"n": "iron_cage", "meta": _L(WARM, 1.6, 0.4)},
                                   {"n": "crystal_drops", "meta": _L("#ffd9a0", 1.8, 0.4)}, {"n": "skull_crown", "meta": _L(WARM, 1.7, 0.4)}, {"n": "soul_wheel", "meta": _L(COLD, 1.8, 0.4)}],
        cat="light", place="ceiling", tags=["light", "glow"])
def _chandelier(A, v):
    k = v["n"]; fl = "soulfire" if k == "soul_wheel" else "flame"; R = 0.6 if k == "wagon_wheel" else 0.4
    cyl(A, 0.012, 0.5, (0, 0, 0.82), "iron", verts=8); tor(A, R, 0.025, (0, 0, 0.3), "bone" if k == "bone_ring" else "iron", seg=40)
    if k == "wagon_wheel":
        for i in range(8): a = i * PI / 4; box(A, (R * 1.0, 0.025, 0.025), (R * 0.5 * math.cos(a), R * 0.5 * math.sin(a), 0.3), "iron", rot=(0, 0, a), bevel=0);
        tor(A, 0.25, 0.015, (0, 0, 0.3), "iron", seg=24)
    n = 12 if k == "wagon_wheel" else 6
    for px, py, _, a in ring_of(n, R):
        candle(A, (px, py, 0.325), h=0.16) if k != "soul_wheel" else sph(A, 0.03, (px, py, 0.38), "soulfire", scale=(1, 1, 1.8), seg=6)
        if k == "bone_ring": skull(A, (px, py, 0.18), 0.4, yaw=a + PI / 2)
        if k == "crystal_drops": limb(A, (px, py, 0.3), (px, py, 0.12), 0.006, 0.014, "glass_clear", 6); sph(A, 0.02, (px, py, 0.1), "glass_clear", seg=6)
    if k == "iron_cage": [limb(A, (R * 0.5 * math.cos(a), R * 0.5 * math.sin(a), 0.8), (R * math.cos(a), R * math.sin(a), 0.3), 0.01, 0.01, "iron", 5) for a in np_range(0, 6.2, 0.78)]
    if k == "skull_crown": [skull(A, (0.12 * math.cos(a), 0.12 * math.sin(a), 0.1), 0.7, yaw=a + PI / 2) for a in np_range(0, 6.2, 1.57)]
    sph(A, 0.07, (0, 0, 0.14), "bone", scale=(1, 1.1, 1.0)) if k not in ("skull_crown",) else None; cyl(A, 0.02, 0.15, (0, 0, 0.04), "iron", r2=0.0, verts=8)


@family("sconce", "lighting", [{"n": "iron_single", "meta": _L(WARM, 0.8, 0.3)}, {"n": "iron_double", "meta": _L(WARM, 1.0, 0.3)}, {"n": "skull_holder", "meta": _L(WARM, 0.8, 0.32)},
                               {"n": "bone_hand", "meta": _L(WARM, 0.8, 0.32)}, {"n": "torch_wall", "meta": _L(FIRE, 1.3, 0.5)}, {"n": "crystal_sconce", "meta": _L(VIOLET, 0.9, 0.3)},
                               {"n": "brass_arm", "meta": _L(WARM, 0.9, 0.3)}, {"n": "bat_sconce", "meta": _L(WARM, 0.8, 0.3)}],
        cat="light", place="wall", y=1.7, tags=["light", "glow"])
def _sconce(A, v):
    k = v["n"]
    box(A, (0.14, 0.03, 0.3), (0, 0.015, 0.15), "iron" if k != "brass_arm" else "gold", bevel=0.004)
    if k == "iron_single": box(A, (0.05, 0.14, 0.05), (0, -0.05, 0.12), "iron"); cyl(A, 0.07, 0.03, (0, -0.12, 0.1), "iron", r2=0.05, verts=14); candle(A, (0, -0.12, 0.11), h=0.2, r=0.028); tor(A, 0.05, 0.007, (0, -0.12, 0.2), "iron")
    elif k == "iron_double":
        for s in (-1, 1): limb(A, (0, -0.02, 0.12), (s * 0.14, -0.1, 0.18), 0.015, 0.012, "iron", 6); cyl(A, 0.045, 0.025, (s * 0.14, -0.1, 0.16), "iron", r2=0.035, verts=10); candle(A, (s * 0.14, -0.1, 0.17), h=0.18)
    elif k == "skull_holder": skull(A, (0, -0.05, 0.08), 1.1); cyl(A, 0.03, 0.14, (0, -0.06, 0.23), "wax", verts=10); sph(A, 0.016, (0, -0.06, 0.33), "flame", scale=(1, 1, 1.9), seg=6)
    elif k == "bone_hand":
        box(A, (0.07, 0.08, 0.05), (0, -0.06, 0.1), "bone", bevel=0.01); [bone(A, (-0.03 + i * 0.02, -0.08, 0.12), (-0.035 + i * 0.023, -0.1, 0.22), 0.009) for i in range(4)]; candle(A, (0, -0.1, 0.19), h=0.15)
    elif k == "torch_wall":
        cyl(A, 0.02, 0.5, (0, -0.1, 0.2), "wood", rot=(0.35, 0, 0), verts=8); tor(A, 0.045, 0.01, (0, -0.07, 0.2), "iron", rot=(0.35, 0, 0)); sph(A, 0.06, (0, -0.2, 0.52), "flame", scale=(1, 1, 1.7), seg=8)
    elif k == "crystal_sconce": box(A, (0.05, 0.1, 0.05), (0, -0.05, 0.1), "iron"); [limb(A, (0.0, -0.1, 0.12), (0.03 * math.cos(a), -0.1 + 0.03 * math.sin(a), 0.26), 0.03, 0.004, "rune", 6) for a in (0, 2.1, 4.2)]
    elif k == "brass_arm": limb(A, (0, -0.0, 0.1), (0, -0.2, 0.16), 0.015, 0.015, "gold", 6); cyl(A, 0.05, 0.03, (0, -0.2, 0.14), "gold", r2=0.035, verts=12); candle(A, (0, -0.2, 0.155), h=0.2)
    elif k == "bat_sconce":
        sph(A, 0.04, (0, -0.04, 0.15), "black", scale=(1, 1, 1.2), seg=8)
        for s in (-1, 1): prism(A, [(0, 0), (s * 0.14, 0.02), (s * 0.12, 0.1), (0, 0.06)] if s > 0 else [(0, 0), (0, 0.06), (-0.12, 0.1), (-0.14, 0.02)], 0.01, (0, -0.04, 0.14), "black", rot=(0, 0, 0), bevel=0)
        cyl(A, 0.04, 0.025, (0, -0.1, 0.05), "iron", r2=0.03, verts=10); candle(A, (0, -0.1, 0.06), h=0.14)


@family("candle_group", "lighting", [{"n": "drip_pile", "meta": _L(WARM, 0.6, 0.2)}, {"n": "tall_trio", "meta": _L(WARM, 0.6, 0.45)}, {"n": "black_candles", "meta": _L("#c070ff", 0.5, 0.3)},
                                     {"n": "votive_row", "meta": _L(WARM, 0.6, 0.12)}, {"n": "pillar_big", "meta": _L(WARM, 0.7, 0.4)}, {"n": "bone_cluster", "meta": _L(WARM, 0.55, 0.2)}],
        cat="light", place="surface", tags=["decor", "light", "glow"])
def _candles(A, v):
    k = v["n"]
    if k == "drip_pile":
        sph(A, 0.1, (0, 0, 0.012), "wax", scale=(1.4, 1.3, 0.2), seg=10)
        for (x, y, h) in [(0, 0, 0.2), (0.07, 0.04, 0.12), (-0.06, 0.05, 0.08), (0.02, -0.07, 0.15)]: candle(A, (x, y, 0.02), h=h, r=0.022)
    elif k == "tall_trio":
        for i, x in enumerate((-0.06, 0.0, 0.06)): cyl(A, 0.035, 0.015, (x, 0, 0.008), "iron", verts=10); candle(A, (x, 0, 0.015), h=0.28 + 0.06 * (i % 2), r=0.02)
    elif k == "black_candles":
        for i, x in enumerate((-0.05, 0.05)): cyl(A, 0.03, 0.2 + 0.1 * i, (x, 0, 0.1 + 0.05 * i), "black", verts=10); sph(A, 0.014, (x, 0, 0.23 + 0.1 * i), "rune", scale=(1, 1, 1.9), seg=6)
        cyl(A, 0.12, 0.012, (0, 0, 0.006), "iron", verts=16)
    elif k == "votive_row":
        for x in np_range(-0.14, 0.14, 0.07): cyl(A, 0.025, 0.04, (x, 0, 0.02), "glass_clear", verts=10); sph(A, 0.012, (x, 0, 0.05), "flame", scale=(1, 1, 1.6), seg=6)
    elif k == "pillar_big": cyl(A, 0.07, 0.3, (0, 0, 0.15), "wax", verts=14); cyl(A, 0.1, 0.02, (0, 0, 0.01), "iron", verts=16); sph(A, 0.025, (0, 0, 0.34), "flame", scale=(1, 1, 1.9), seg=8); sph(A, 0.03, (0.06, 0, 0.1), "wax", scale=(0.5, 0.5, 2), seg=6)
    elif k == "bone_cluster":
        skull(A, (0, 0, 0.0), 0.9); [candle(A, (x, y, 0.0), h=0.12 + 0.04 * i, r=0.018) for i, (x, y) in enumerate([(0.12, 0.03), (-0.11, 0.05), (0.04, 0.12)])]; bone(A, (-0.15, -0.06, 0.012), (0.15, -0.06, 0.012), 0.012)


@family("lantern", "lighting", [{"n": "hand_lantern", "place": "surface", "meta": {**_L(WARM, 0.7, 0.25), "place": "surface"}}, {"n": "standing_lantern", "meta": _L(WARM, 1.1, 1.5)}, {"n": "hanging_lantern", "meta": {**_L(WARM, 1.0, 0.2), "place": "ceiling"}},
                                {"n": "oil_lamp", "meta": {**_L(WARM, 0.6, 0.12), "place": "surface"}}, {"n": "spirit_lantern", "meta": {**_L(COLD, 0.8, 0.25), "place": "surface"}}, {"n": "skull_lantern", "meta": {**_L(WARM, 0.7, 0.25), "place": "surface"}}],
        cat="light", place="floor", tags=["light", "glow", "decor"])
def _lantern(A, v):
    k = v["n"]; fl = "soulfire" if k == "spirit_lantern" else "flame"
    def lamp(z0, s=1.0):
        box(A, (0.16 * s, 0.16 * s, 0.02), (0, 0, z0 + 0.01), "iron"); box(A, (0.16 * s, 0.16 * s, 0.02), (0, 0, z0 + 0.3 * s), "iron")
        for sx in (-1, 1):
            for sy in (-1, 1): box(A, (0.015, 0.015, 0.3 * s), (sx * 0.075 * s, sy * 0.075 * s, z0 + 0.15 * s), "iron")
        cyl(A, 0.065 * s, 0.26 * s, (0, 0, z0 + 0.15 * s), "glass_clear", verts=12); sph(A, 0.03 * s, (0, 0, z0 + 0.12 * s), fl, scale=(1, 1, 1.6), seg=8)
        cyl(A, 0.09 * s, 0.07 * s, (0, 0, z0 + 0.35 * s), "iron", r2=0.0, verts=4, rot=(0, 0, PI / 4)); tor(A, 0.04 * s, 0.008, (0, 0, z0 + 0.4 * s), "iron", rot=(PI / 2, 0, 0))
    if k in ("hand_lantern", "hanging_lantern", "spirit_lantern"): lamp(0.0)
    elif k == "standing_lantern": cyl(A, 0.2, 0.04, (0, 0, 0.02), "iron", r2=0.14, verts=14); cyl(A, 0.02, 1.1, (0, 0, 0.6), "iron", verts=8); limb(A, (0, 0, 1.1), (0.0, -0.18, 1.18), 0.015, 0.015, "iron", 6); lamp(1.0 - 0.08, 1.0)
    elif k == "oil_lamp": lathe(A, [(0.0, 0), (0.07, 0.0), (0.09, 0.05), (0.04, 0.12), (0.04, 0.16)], (0, 0, 0), "glass_clear", verts=14); cyl(A, 0.05, 0.04, (0, 0, 0.18), "gold", r2=0.03, verts=10); sph(A, 0.016, (0, 0, 0.23), "flame", scale=(1, 1, 1.9), seg=6); lathe(A, [(0.0, 0.01), (0.062, 0.02), (0.07, 0.05), (0.0, 0.05)], (0, 0, 0), "potion_amber", verts=12)
    elif k == "skull_lantern": skull(A, (0, 0, 0.0), 1.5, glow="flame"); sph(A, 0.05, (0, 0, 0.19), "flame", scale=(1, 1, 1.4), seg=8); tor(A, 0.05, 0.007, (0, 0, 0.26), "iron", rot=(PI / 2, 0, 0))


@family("brazier", "lighting", [{"n": "tripod_bowl", "meta": _L(FIRE, 1.4, 1.1)}, {"n": "pedestal", "meta": _L(FIRE, 1.4, 1.2)}, {"n": "skull_brazier", "meta": _L(FIRE, 1.4, 1.0)},
                                {"n": "iron_basket", "meta": _L(FIRE, 1.5, 1.3)}, {"n": "soul_brazier", "meta": _L(COLD, 1.5, 1.1)}],
        cat="light", place="floor", tags=["corner", "light", "glow"])
def _brazier(A, v):
    k = v["n"]; fire = "soulfire" if k == "soul_brazier" else "flame"; em = "soulfire" if k == "soul_brazier" else "ember"
    if k == "tripod_bowl":
        for i in range(3): a = i * 2 * PI / 3 + 0.5; limb(A, (0.28 * math.cos(a), 0.28 * math.sin(a), 0.0), (0.08 * math.cos(a), 0.08 * math.sin(a), 0.8), 0.025, 0.02, "iron")
        lathe(A, [(0.1, 0.78), (0.3, 0.88), (0.34, 1.0), (0.3, 1.0), (0.0, 0.84)], (0, 0, 0), "iron", verts=22)
    elif k == "pedestal":
        lathe(A, [(0.25, 0), (0.15, 0.05), (0.1, 0.8), (0.18, 0.9)], (0, 0, 0), "stone_light", verts=18); lathe(A, [(0.12, 0.88), (0.3, 0.98), (0.3, 1.1), (0.26, 1.1), (0.0, 0.95)], (0, 0, 0), "iron", verts=22)
    elif k == "skull_brazier":
        box(A, (0.4, 0.4, 0.5), (0, 0, 0.25), "stone", bevel=0.02); lathe(A, [(0.15, 0.5), (0.3, 0.6), (0.32, 0.8), (0.28, 0.8), (0.0, 0.58)], (0, 0, 0), "iron", verts=20)
        [skull(A, (0.35 * math.cos(a), 0.35 * math.sin(a), 0.4), 0.7, yaw=a + PI / 2) for a in np_range(0, 6.2, 1.57)]
    elif k == "iron_basket":
        for i in range(3): a = i * 2 * PI / 3; limb(A, (0.22 * math.cos(a), 0.22 * math.sin(a), 0.0), (0.05 * math.cos(a), 0.05 * math.sin(a), 1.0), 0.02, 0.02, "iron")
        for a in np_range(0, 6.2, 0.7): limb(A, (0.05 * math.cos(a), 0.05 * math.sin(a), 1.0), (0.2 * math.cos(a), 0.2 * math.sin(a), 1.25), 0.01, 0.01, "iron", 5)
        tor(A, 0.2, 0.012, (0, 0, 1.25), "iron", seg=18)
    elif k == "soul_brazier":
        lathe(A, [(0.2, 0), (0.12, 0.05), (0.1, 0.7), (0.2, 0.85), (0.3, 1.0), (0.26, 1.0), (0.0, 0.9)], (0, 0, 0.0), "black", verts=20); tor(A, 0.3, 0.02, (0, 0, 1.0), "silver", seg=24)
    top = {"tripod_bowl": 0.9, "pedestal": 0.98, "skull_brazier": 0.62, "iron_basket": 1.05, "soul_brazier": 0.92}[k]
    sph(A, 0.24, (0, 0, top), em, scale=(1, 1, 0.35), seg=12)
    for i in range(5): a = i * 1.26; sph(A, 0.07, (0.1 * math.cos(a), 0.1 * math.sin(a), top + 0.1 + 0.05 * (i % 2)), fire, scale=(0.8, 0.8, 1.9), seg=8)
    sph(A, 0.09, (0, 0, top + 0.18), fire, scale=(0.8, 0.8, 2.0), seg=8)


@family("floating_light", "lighting", [{"n": "wisp", "meta": _L(COLD, 0.9, 0.4)}, {"n": "rune_orb", "meta": _L(VIOLET, 0.9, 0.4)}, {"n": "ghost_flame", "meta": _L("#a0ffd0", 0.9, 0.4)}, {"n": "hanging_crystal", "meta": _L("#ff5acd", 0.9, 0.4)}],
        cat="light", place="ceiling", tags=["light", "glow"])
def _floating(A, v):
    k = v["n"]
    chain(A, (0, 0, 0.9), (0, 0, 0.5), 0.012)
    if k == "wisp": sph(A, 0.1, (0, 0, 0.4), "ecto", scale=(1, 1, 1.3), seg=14); [sph(A, 0.03 - 0.006 * i, (0.04 * math.cos(i * 2), 0.04 * math.sin(i * 2), 0.28 - 0.07 * i), "ecto", seg=6) for i in range(4)]
    elif k == "rune_orb":
        sph(A, 0.1, (0, 0, 0.4), "orb", seg=16); tor(A, 0.16, 0.008, (0, 0, 0.4), "rune", seg=28); tor(A, 0.16, 0.008, (0, 0, 0.4), "rune", rot=(PI / 2, 0, 0), seg=28); tor(A, 0.16, 0.008, (0, 0, 0.4), "rune", rot=(0, PI / 2, 0), seg=28)
    elif k == "ghost_flame": [sph(A, 0.09 - 0.02 * i, (0.02 * i, 0, 0.35 + 0.1 * i), "soulfire", scale=(1, 1, 1.6), seg=10) for i in range(3)]; cyl(A, 0.05, 0.05, (0, 0, 0.5), "iron", r2=0.03, verts=10)
    elif k == "hanging_crystal": cyl(A, 0.09, 0.4, (0, 0, 0.3), "potion_purple", r2=0.0, verts=6, rot=(PI, 0, 0)); cyl(A, 0.09, 0.15, (0, 0, 0.55), "potion_purple", r2=0.0, verts=6); tor(A, 0.05, 0.01, (0, 0, 0.64), "gold", seg=10)
