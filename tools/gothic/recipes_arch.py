# ============ ARCHITECTURE (82) ============

# ---- freestanding columns, 2.7 m (room height 2.8) ----
@family("column", "architecture", ["plain", "fluted", "clustered", "twisted", "bone", "skull", "banded", "chained", "broken", "rune"],
        cat="architecture", place="floor", tags=["arch", "pillar"])
def _column(A, v):
    k = v["n"]; H = 1.35 if k == "broken" else 2.7
    box(A, (0.58, 0.58, 0.16), (0, 0, 0.08), "stone_dark", bevel=0.02); box(A, (0.48, 0.48, 0.1), (0, 0, 0.21), "stone", bevel=0.015)
    sh = H - (0.26 if k == "broken" else 0.52)
    column_shaft(A, k if k in ("fluted", "clustered", "twisted") else "plain", sh, 0.2, (0, 0, 0.26), "stone" if k in ("bone", "skull") else "stone_light")
    top = 0.26 + sh
    if k != "broken":
        box(A, (0.48, 0.48, 0.1), (0, 0, top + 0.05), "stone", bevel=0.015); box(A, (0.6, 0.6, 0.16), (0, 0, top + 0.18), "stone_dark", bevel=0.02)
    if k == "bone":
        for px, py, _, a in ring_of(8, 0.19):
            cyl(A, 0.032, sh, (px, py, 0.26 + sh / 2), "bone", verts=8)
        for z in (0.9, 1.8):
            for px, py, _, a in ring_of(4, 0.23, start=0.4):
                skull(A, (px, py, z), 0.8, yaw=a + PI / 2)
    elif k == "skull":
        for z in (0.7, 1.3, 1.9):
            for px, py, _, a in ring_of(4, 0.2, start=z):
                skull(A, (px, py, z), 0.85, yaw=a + PI / 2)
    elif k == "banded":
        for z in (0.6, 1.3, 2.0): tor(A, 0.215, 0.022, (0, 0, z), "iron", seg=24)
    elif k == "chained":
        chain(A, (0.22, 0.0, 2.35), (0.23, 0.0, 1.2)); chain(A, (-0.22, 0.0, 2.35), (0.0, -0.23, 1.5)); chain(A, (0.0, 0.22, 2.3), (-0.2, 0.1, 1.0))
        for z in (2.35,): tor(A, 0.215, 0.02, (0, 0, z), "iron", seg=24)
    elif k == "broken":
        box(A, (0.3, 0.3, 0.16), (0.04, 0, top + 0.06), "stone_light", rot=(0.25, 0.2, 0.5), bevel=0.01)
        for (x, y, s) in [(0.4, 0.3, 0.14), (-0.35, 0.4, 0.1), (0.3, -0.4, 0.18), (-0.4, -0.3, 0.12)]:
            box(A, (s, s * 1.2, s * 0.8), (x, y, s * 0.4), "stone_light", rot=(0.2, 0.3, x), bevel=0.01)
    elif k == "rune":
        for px, py, _, a in ring_of(4, 0.205):
            for z in (0.9, 1.3, 1.7): box(A, (0.012, 0.07, 0.12), (px, py, z), "rune", rot=(0, 0, a), bevel=0)


# ---- wall pilasters (engaged half-columns), 2.7 m ----
@family("pilaster", "architecture", ["plain", "fluted", "rune", "skull", "ribbed", "banded", "bone",
                                     {"n": "shrine", "meta": {"light": 0.45, "lightColor": "#ff9a3c", "lightY": 1.5, "tags": ["light"]}}],
        cat="architecture", place="wall", y=0.0, tags=["arch", "pilaster"])
def _pilaster(A, v):
    k = v["n"]; H = 2.7
    box(A, (0.46, 0.16, 0.14), (0, 0, 0.07), "stone_dark"); box(A, (0.36, 0.14, H - 0.3), (0, 0.01, 0.14 + (H - 0.3) / 2), "stone_light", bevel=0.01)
    box(A, (0.46, 0.16, 0.14), (0, 0, H - 0.07), "stone_dark"); box(A, (0.4, 0.15, 0.08), (0, 0, H - 0.16), "stone")
    if k == "fluted":
        for x in (-0.12, -0.04, 0.04, 0.12): cyl(A, 0.018, H - 0.4, (x, -0.065, H / 2), "stone", verts=6)
    elif k == "rune":
        for z in (0.8, 1.3, 1.8): box(A, (0.1, 0.01, 0.13), (0, -0.075, z), "rune", bevel=0)
    elif k == "skull":
        for z in (0.8, 1.4, 2.0): skull(A, (0, -0.07, z), 0.95)
    elif k == "ribbed":
        for x in (-0.11, 0, 0.11): box(A, (0.05, 0.06, H - 0.4), (x, -0.08, H / 2), "stone", bevel=0.01)
    elif k == "banded":
        for z in (0.5, 1.2, 1.9): box(A, (0.42, 0.17, 0.045), (0, 0, z), "iron", bevel=0.005)
    elif k == "bone":
        for x in (-0.1, 0.1): bone(A, (x, -0.08, 0.3), (x, -0.08, H - 0.3), 0.022)
        skull(A, (0, -0.075, 1.3), 1.0)
    elif k == "shrine":
        box(A, (0.22, 0.03, 0.5), (0, -0.08, 1.4), "black"); box(A, (0.24, 0.12, 0.03), (0, -0.11, 1.15), "stone"); candle(A, (0, -0.11, 1.17), h=0.14)
        prism(A, arch_pts(0.22, 0.2, 0.7), 0.02, (0, -0.085, 1.15), "stone_dark", bevel=0)


# ---- wall arch panels / blind arcades / relief ----
@family("wall_arch", "architecture", ["pointed", "trefoil", "triple", "rose", "arcade", {"n": "niche_candle", "meta": {"light": 0.5, "lightColor": "#ff9a3c", "lightY": 1.2, "tags": ["light"]}}],
        cat="architecture", place="wall", y=0.2, tags=["arch", "decor"])
def _wall_arch(A, v):
    k = v["n"]
    prism(A, arch_pts(1.2, 1.2, 0.8), 0.06, (0, 0.03, 0.0), "stone_dark", bevel=0.005)
    if k == "pointed":
        arch_ring(A, 0.9, 1.1, 0.8, 0.09, 0.1, (0, -0.02, 0.0)); jambs(A, 0.9, 1.1, 0.09, 0.1, (0, -0.02, 0.0))
    elif k == "trefoil":
        for (x, z) in [(0, 1.45), (-0.2, 1.1), (0.2, 1.1)]: tor(A, 0.15, 0.03, (x, -0.04, z), "stone_light", rot=(PI / 2, 0, 0))
        box(A, (0.9, 0.08, 0.1), (0, -0.04, 0.6), "stone_light"); box(A, (0.1, 0.08, 0.5), (0, -0.04, 0.3), "stone_light")
    elif k == "triple":
        for x in (-0.38, 0, 0.38):
            prism(A, arch_pts(0.3, 0.9, 0.8), 0.05, (x, -0.02, 0.1), "black", bevel=0.003); arch_ring(A, 0.3, 0.9, 0.8, 0.045, 0.07, (x, -0.04, 0.1), n=4)
    elif k == "rose":
        tor(A, 0.4, 0.04, (0, -0.04, 1.2), "stone_light", rot=(PI / 2, 0, 0)); sph(A, 0.07, (0, -0.05, 1.2), "stone_light")
        for i in range(8): a = i * PI / 4; box(A, (0.34, 0.04, 0.035), (0.2 * math.cos(a), -0.04, 1.2 + 0.2 * math.sin(a)), "stone_light", rot=(0, -a, 0))
        box(A, (1.0, 0.06, 0.08), (0, -0.04, 0.5), "stone_light")
    elif k == "arcade":
        for x in (-0.38, 0, 0.38): arch_ring(A, 0.3, 0.5, 0.8, 0.05, 0.07, (x, -0.04, 0.2), n=4); jambs(A, 0.3, 0.5, 0.05, 0.07, (x, -0.04, 0.2))
    elif k == "niche_candle":
        prism(A, arch_pts(0.5, 0.7, 0.8), 0.04, (0, -0.02, 0.3), "black", bevel=0); arch_ring(A, 0.5, 0.7, 0.8, 0.06, 0.09, (0, -0.04, 0.3), n=5)
        box(A, (0.4, 0.14, 0.04), (0, -0.1, 0.55), "stone_light"); candle(A, (0, -0.1, 0.57), h=0.16)


# ---- window surrounds (placed over openings; bottom = sill) ----
def _window_frame(A, ring_mat="stone_light"):
    jambs(A, 1.5, 1.15, 0.1, 0.14, (0, 0, 0.0), ring_mat); arch_ring(A, 1.5, 1.15, 0.7, 0.1, 0.14, (0, 0, 0.0), ring_mat, n=7)
    box(A, (1.78, 0.2, 0.07), (0, -0.04, -0.02), ring_mat, bevel=0.01)


@family("window_deco", "architecture", ["lancet", "double_lancet", "triple_lancet", "rose", "trefoil", "quatrefoil", "iron_grid", {"n": "stained_angel", "img": "glass_skeleton_angel"}, {"n": "stained_rose", "img": "glass_skull_rose"}, {"n": "stained_raven", "img": "glass_raven_sunset"}, {"n": "stained_lantern", "img": "glass_hooded_lantern"}],
        cat="architecture", place="wall", y=0.82, tags=["arch", "window-deco"])
def _window_deco(A, v):
    k = v["n"]; _window_frame(A)
    if k == "lancet": box(A, (0.06, 0.1, 1.15), (0, 0, 0.58), "stone_light")
    elif k == "double_lancet":
        box(A, (0.07, 0.1, 1.5), (0, 0, 0.75), "stone_light"); tor(A, 0.2, 0.025, (0, -0.02, 1.38), "stone_light", rot=(PI / 2, 0, 0))
    elif k == "triple_lancet":
        for x in (-0.25, 0.25): box(A, (0.06, 0.1, 1.25), (x, 0, 0.63), "stone_light")
    elif k == "rose":
        box(A, (1.4, 0.1, 0.06), (0, 0, 1.15), "stone_light"); tor(A, 0.33, 0.035, (0, -0.02, 1.62), "stone_light", rot=(PI / 2, 0, 0)); box(A, (0.07, 0.1, 1.15), (0, 0, 0.58), "stone_light")
        for i in range(6): a = i * PI / 3; box(A, (0.3, 0.05, 0.03), (0.17 * math.cos(a), -0.03, 1.62 + 0.17 * math.sin(a)), "stone_light", rot=(0, -a, 0))
    elif k == "trefoil":
        box(A, (0.07, 0.1, 1.15), (0, 0, 0.58), "stone_light")
        for (x, z) in [(0, 1.68), (-0.17, 1.42), (0.17, 1.42)]: tor(A, 0.12, 0.025, (x, -0.02, z), "stone_light", rot=(PI / 2, 0, 0))
    elif k == "quatrefoil":
        box(A, (1.4, 0.1, 0.06), (0, 0, 1.15), "stone_light")
        for (x, z) in [(-0.1, 1.55), (0.1, 1.55), (0, 1.43), (0, 1.67)]: tor(A, 0.09, 0.022, (x, -0.02, z), "stone_light", rot=(PI / 2, 0, 0))
    elif k == "iron_grid":
        for x in (-0.5, -0.25, 0, 0.25, 0.5): box(A, (0.025, 0.05, 1.15), (x, -0.02, 0.58), "iron", bevel=0.002)
        for z in (0.3, 0.6, 0.9): box(A, (1.3, 0.05, 0.025), (0, -0.02, z), "iron", bevel=0.002)
    elif k.startswith("stained"):
        pic = f"{ASSETS}/{PACK}/art/{v['img']}.jpg"; m = image_mat(f"win_{v['img']}", pic, emit=0.7) if os.path.exists(pic) else "sg_purple"
        prism(A, arch_pts(1.38, 1.15, 0.62), 0.02, (0, 0.03, 0.0), m, bevel=0, uv=True)
        for x in (-0.35, 0.35): box(A, (0.03, 0.04, 2.0), (x, 0.0, 1.0), "iron", bevel=0)
        box(A, (1.4, 0.04, 0.03), (0, 0.0, 1.15), "iron", bevel=0)


# ---- door surrounds ----
def _door_frame(A, mat="stone_light", sq=0.5):
    jambs(A, 1.1, 2.1, 0.14, 0.2, (0, 0, 0.0), mat); arch_ring(A, 1.1, 2.1, sq, 0.13, 0.2, (0, 0, 0.0), mat, n=7)


@family("door_deco", "architecture", ["pointed", "skull_keystone", "iron_banded", "gargoyle_top", "double_arch", "bone_arch"],
        cat="architecture", place="wall", y=0.0, tags=["arch", "door-deco"])
def _door_deco(A, v):
    k = v["n"]
    _door_frame(A, "bone" if k == "bone_arch" else "stone_light")
    if k == "skull_keystone": skull(A, (0, -0.12, 2.52), 1.6, mat="bone")
    elif k == "iron_banded":
        for z in (0.5, 1.2, 1.9):
            for s in (-1, 1): box(A, (0.16, 0.22, 0.05), (s * 0.62, 0, z), "iron", bevel=0.004)
    elif k == "gargoyle_top":
        sph(A, 0.1, (0, -0.1, 2.72), "stone_light", scale=(1, 1.2, 1)); box(A, (0.1, 0.12, 0.07), (0, -0.2, 2.7), "stone_light"); limb(A, (-0.07, -0.1, 2.8), (-0.13, -0.1, 2.93), 0.02, 0.004, "stone", 6); limb(A, (0.07, -0.1, 2.8), (0.13, -0.1, 2.93), 0.02, 0.004, "stone", 6)
        sph(A, 0.03, (0, -0.2, 2.74), "ember", seg=6)
    elif k == "double_arch": arch_ring(A, 1.3, 2.1, 0.5, 0.1, 0.15, (0, -0.04, 0.0), "stone"); jambs(A, 1.3, 2.1, 0.1, 0.15, (0, -0.04, 0.0), "stone")
    elif k == "bone_arch":
        for s in (-1, 1): skull(A, (s * 0.7, -0.12, 2.0), 1.2)
        skull(A, (0, -0.12, 2.52), 1.3)


# ---- ceiling bosses and rib vaults ----
@family("ceiling_vault", "architecture", ["round_boss", "skull_boss", "star_boss", "rune_boss", "rosette", "rib_cross", "rib_double", "rib_star"],
        cat="architecture", place="ceiling", tags=["arch", "ceiling-decor"])
def _ceiling(A, v):
    k = v["n"]
    if k == "round_boss":
        lathe(A, [(0.45, 0.3), (0.45, 0.22), (0.3, 0.1), (0.12, 0.0), (0.0, -0.05)], (0, 0, 0), "stone_light", verts=24)
        for i in range(8): a = i * PI / 4; box(A, (0.4, 0.05, 0.06), (0.22 * math.cos(a), 0.22 * math.sin(a), 0.2), "stone", rot=(0, 0, a), bevel=0.005)
    elif k == "skull_boss":
        lathe(A, [(0.4, 0.3), (0.4, 0.2), (0.25, 0.08), (0.0, 0.06)], (0, 0, 0), "stone", verts=20); skull(A, (0, 0, -0.02), 1.4, yaw=0)
    elif k == "star_boss":
        for i in range(8): a = i * PI / 4; box(A, (0.55, 0.07, 0.08), (0.27 * math.cos(a), 0.27 * math.sin(a), 0.15), "stone_light", rot=(0, 0, a), bevel=0.006)
        cyl(A, 0.12, 0.2, (0, 0, 0.1), "gold", verts=12)
    elif k == "rune_boss":
        lathe(A, [(0.5, 0.3), (0.5, 0.2), (0.0, 0.14)], (0, 0, 0), "stone_dark", verts=24); tor(A, 0.33, 0.025, (0, 0, 0.12), "rune", seg=32); tor(A, 0.18, 0.02, (0, 0, 0.12), "rune", seg=24)
    elif k == "rosette":
        for r, z in [(0.5, 0.26), (0.38, 0.2), (0.26, 0.14), (0.14, 0.08)]: cyl(A, r, 0.06, (0, 0, z), "stone_light" if z > 0.1 else "gold", verts=24)
        for i in range(12): a = i * PI / 6; sph(A, 0.035, (0.44 * math.cos(a), 0.44 * math.sin(a), 0.22), "gold", seg=8)
    elif k in ("rib_cross", "rib_double", "rib_star"):
        n = {"rib_cross": 2, "rib_double": 4, "rib_star": 6}[k]
        for i in range(n): a = i * PI / n; box(A, (2.5, 0.12, 0.16), (0, 0, 0.18), "stone_light", rot=(0, 0, a), bevel=0.01)
        lathe(A, [(0.3, 0.3), (0.3, 0.22), (0.1, 0.1), (0.0, 0.05)], (0, 0, 0), "stone_dark", verts=16)


# ---- cobwebs for upper corners ----
@family("cobweb", "architecture", ["fan_small", "fan_large", "draped", "spider_web"], cat="architecture", place="wall", y=2.0, tags=["arch", "cobweb"])
def _cobweb(A, v):
    k = v["n"]; s = {"fan_small": 0.6, "fan_large": 1.0, "draped": 0.85, "spider_web": 0.8}[k]
    for i in range(7):
        a = PI * 0.12 + i * PI * 0.76 / 6
        limb(A, (0, 0, 0), (s * math.cos(a) * 0.9, 0, -s * math.sin(a)), 0.0035, 0.002, "ivory", 4)
    for r in (0.3, 0.55, 0.8):
        for i in range(6):
            a0 = PI * 0.12 + i * PI * 0.76 / 6; a1 = a0 + PI * 0.76 / 6
            limb(A, (s * r * math.cos(a0), 0, -s * r * math.sin(a0)), (s * r * math.cos(a1), 0, -s * r * math.sin(a1)), 0.002, 0.002, "ivory", 4)
    if k == "draped":
        for x in (-0.25, 0.1, 0.3): limb(A, (x * s, 0, -0.3 * s), (x * s * 1.2, 0, -1.1 * s), 0.003, 0.0015, "ivory", 4)
    if k == "spider_web":
        sph(A, 0.03, (0.05 * s, -0.01, -0.45 * s), "black", scale=(1, 1, 0.8), seg=8)
        for i in range(4):
            for sg in (-1, 1): limb(A, (0.05 * s, -0.01, -0.45 * s), (0.05 * s + sg * 0.06, -0.01, -0.45 * s - 0.03 + i * 0.02 - 0.03), 0.003, 0.002, "black", 4)


# ---- wall armour and weapons ----
def _round_shield(A, r, z, mat, boss="gold", rim="iron"):
    cyl(A, r, 0.05, (0, 0, z), mat, rot=(PI / 2, 0, 0), verts=28); tor(A, r, 0.02, (0, -0.025, z), rim, rot=(PI / 2, 0, 0), seg=28)
    sph(A, r * 0.22, (0, -0.045, z), boss, scale=(1, 0.5, 1), seg=12)


@family("wall_gear", "architecture", ["shield_round", "shield_heater", "shield_skull", "shield_spiked", "shield_rune", "swords_crossed", "axes_crossed", "halberd_rack", "staff_rack", "whip_rack"],
        cat="wall decor", place="wall", y=1.35, tags=["decor"])
def _wall_gear(A, v):
    k = v["n"]
    if k == "shield_round": _round_shield(A, 0.32, 0.4, "wood_red")
    elif k == "shield_heater":
        prism(A, [(0, -0.3), (0.25, 0.05), (0.25, 0.35), (-0.25, 0.35), (-0.25, 0.05)], 0.05, (0, 0, 0.4), "black", bevel=0.01)
        box(A, (0.06, 0.03, 0.55), (0, -0.04, 0.42), "cloth", bevel=0); box(A, (0.34, 0.03, 0.06), (0, -0.04, 0.5), "cloth", bevel=0)
    elif k == "shield_skull": _round_shield(A, 0.32, 0.4, "black", boss="stone_dark"); skull(A, (0, -0.05, 0.33), 1.5)
    elif k == "shield_spiked":
        _round_shield(A, 0.32, 0.4, "iron", rim="rust")
        for px, _, pz, a in [(0.22 * math.cos(t), 0, 0.22 * math.sin(t), t) for t in [i * PI / 3 for i in range(6)]]: cyl(A, 0.03, 0.1, (px, -0.07, 0.4 + pz), "iron", r2=0.0, rot=(PI / 2, 0, 0), verts=8)
    elif k == "shield_rune":
        _round_shield(A, 0.32, 0.4, "stone_dark", boss="rune", rim="gold"); tor(A, 0.2, 0.012, (0, -0.052, 0.4), "rune", rot=(PI / 2, 0, 0), seg=24)
    elif k == "swords_crossed":
        _round_shield(A, 0.3, 0.45, "wood")
        for s in (-1, 1):
            box(A, (0.06, 0.02, 0.95), (0, -0.07, 0.45), "silver", rot=(0, s * 0.62, 0), bevel=0.004); box(A, (0.28, 0.03, 0.04), (s * -0.28, -0.075, 0.1), "gold", rot=(0, s * 0.62, 0), bevel=0.004)
    elif k == "axes_crossed":
        for s in (-1, 1):
            limb(A, (s * -0.3, -0.05, 0.0), (s * 0.3, -0.05, 0.9), 0.02, 0.02, "wood", 8)
            prism(A, [(0, -0.12), (0.2, 0), (0.0, 0.12), (-0.04, 0)], 0.02, (s * 0.3, -0.05, 0.85), "silver", bevel=0.002)
    elif k == "halberd_rack":
        box(A, (1.0, 0.05, 0.1), (0, 0, 0.25), "wood"); box(A, (1.0, 0.05, 0.1), (0, 0, 1.1), "wood")
        for x in (-0.3, 0, 0.3): limb(A, (x, -0.05, 0.0), (x, -0.05, 1.5), 0.016, 0.016, "wood", 8); prism(A, [(0, 0.0), (0.09, 0.15), (0.0, 0.32), (-0.03, 0.15)], 0.015, (x, -0.05, 1.5), "silver", bevel=0.002)
    elif k == "staff_rack":
        box(A, (0.9, 0.05, 0.08), (0, 0, 0.3), "wood"); box(A, (0.9, 0.05, 0.08), (0, 0, 1.2), "wood")
        for i, x in enumerate((-0.33, -0.11, 0.11, 0.33)): limb(A, (x, -0.06, 0.0), (x, -0.06, 1.6), 0.014, 0.014, "wood", 8); sph(A, 0.045, (x, -0.06, 1.64), ["orb", "rune", "ecto", "flame"][i], seg=10)
    elif k == "whip_rack":
        box(A, (0.9, 0.05, 0.3), (0, 0, 0.5), "wood")
        for x in (-0.3, 0, 0.3): tor(A, 0.1, 0.012, (x, -0.06, 0.45), "leather", rot=(PI / 2, 0, 0), seg=14); cyl(A, 0.012, 0.1, (x, -0.06, 0.55), "iron", rot=(PI / 2, 0, 0), verts=6)
        chain(A, (-0.4, -0.05, 0.62), (0.4, -0.05, 0.62), 0.016)


# ---- wall trophies ----
@family("skull_mount", "architecture", ["demon", "ram", "stag", "bull", "dragon", "raven"], cat="wall decor", place="wall", y=1.7, tags=["decor"])
def _skull_mount(A, v):
    k = v["n"]
    prism(A, [(0, -0.28), (0.24, -0.08), (0.2, 0.22), (-0.2, 0.22), (-0.24, -0.08)], 0.04, (0, 0.05, 0.28), "wood", bevel=0.008)
    if k == "demon": skull(A, (0, -0.0, 0.12), 2.0, horns=2); limb(A, (-0.07, -0.05, 0.42), (-0.2, -0.05, 0.62), 0.03, 0.006, "black", 6); limb(A, (0.07, -0.05, 0.42), (0.2, -0.05, 0.62), 0.03, 0.006, "black", 6)
    elif k == "ram":
        skull(A, (0, 0, 0.12), 1.7)
        for s in (-1, 1): tor(A, 0.1, 0.028, (s * 0.12, -0.03, 0.38), "bone", rot=(0, PI / 2, 0), seg=16)
    elif k == "stag":
        skull(A, (0, 0, 0.1), 1.6)
        for s in (-1, 1):
            limb(A, (s * 0.05, -0.02, 0.38), (s * 0.18, -0.02, 0.62), 0.016, 0.01, "bone", 6)
            limb(A, (s * 0.12, -0.02, 0.5), (s * 0.28, -0.02, 0.55), 0.01, 0.006, "bone", 6); limb(A, (s * 0.16, -0.02, 0.58), (s * 0.12, -0.02, 0.76), 0.01, 0.006, "bone", 6)
    elif k == "bull":
        skull(A, (0, 0, 0.12), 1.8)
        for s in (-1, 1): limb(A, (s * 0.09, -0.03, 0.38), (s * 0.3, -0.03, 0.4), 0.025, 0.014, "ivory", 8); limb(A, (s * 0.3, -0.03, 0.4), (s * 0.4, -0.03, 0.55), 0.014, 0.004, "ivory", 8)
    elif k == "dragon":
        box(A, (0.16, 0.34, 0.12), (0, -0.14, 0.3), "bone", bevel=0.015); sph(A, 0.13, (0, 0.02, 0.38), "bone", scale=(1, 1.1, 0.9))
        for sx in (-1, 1):
            sph(A, 0.03, (sx * 0.07, -0.08, 0.4), "ember", seg=6)
            limb(A, (sx * 0.08, 0.1, 0.45), (sx * 0.2, 0.2, 0.7), 0.035, 0.006, "black", 6)
            for i in range(4): cyl(A, 0.008, 0.04, (sx * 0.075, -0.2 + i * 0.07, 0.235), "ivory", r2=0.0, rot=(PI, 0, 0), verts=5)
    elif k == "raven": skull(A, (0, -0.0, 0.18), 0.8, mat="ivory"); cyl(A, 0.012, 0.1, (0, -0.07, 0.3), "black", r2=0.0, rot=(PI / 2, 0, 0), verts=6)


# ---- hanging chains, manacles, hooks ----
@family("wall_chain", "architecture", ["chains_short", "chains_long", "manacles_pair", "manacles_high", "hooks_row", "iron_rings"], cat="wall decor", place="wall", y=1.0, tags=["decor"])
def _wall_chain(A, v):
    k = v["n"]
    if k in ("chains_short", "chains_long"):
        L = 0.6 if k == "chains_short" else 1.4
        box(A, (0.9, 0.04, 0.05), (0, 0, L + 0.1), "iron", bevel=0.003)
        for x in (-0.35, 0, 0.35): tor(A, 0.03, 0.007, (x, -0.04, L + 0.1), "iron", rot=(PI / 2, 0, 0), seg=10); chain(A, (x, -0.04, L + 0.06), (x, -0.05, 0.1 + (0.2 if x == 0 else 0))); sph(A, 0.03, (x, -0.05, 0.08), "iron", seg=8)
    elif k in ("manacles_pair", "manacles_high"):
        for s in (-1, 1):
            box(A, (0.12, 0.04, 0.12), (s * 0.3, 0, 0.9), "iron", bevel=0.004); tor(A, 0.04, 0.012, (s * 0.3, -0.04, 0.9), "iron", rot=(PI / 2, 0, 0), seg=10)
            chain(A, (s * 0.3, -0.04, 0.87), (s * 0.3, -0.06, 0.55)); tor(A, 0.07, 0.014, (s * 0.3, -0.07, 0.48), "iron", rot=(0, 0, 0), seg=14); box(A, (0.03, 0.03, 0.04), (s * 0.3 + 0.07, -0.07, 0.5), "iron", bevel=0)
        if k == "manacles_high": chain(A, (-0.3, -0.07, 0.5), (0.3, -0.07, 0.5))
    elif k == "hooks_row":
        box(A, (0.9, 0.05, 0.08), (0, 0, 0.5), "wood")
        for x in (-0.35, -0.12, 0.12, 0.35):
            cyl(A, 0.01, 0.12, (x, -0.07, 0.42), "iron", rot=(PI / 2, 0, 0), verts=6); tor(A, 0.05, 0.01, (x, -0.13, 0.37), "iron", rot=(0, PI / 2, 0), seg=12)
    elif k == "iron_rings":
        for (x, z) in [(-0.25, 0.55), (0.25, 0.55), (0, 0.15)]: box(A, (0.1, 0.04, 0.1), (x, 0, z), "iron", bevel=0.004); tor(A, 0.07, 0.014, (x, -0.06, z - 0.03), "iron", rot=(PI / 2, 0, 0), seg=14)


# ---- floor features ----
@family("floor_feature", "architecture", ["grate_round", "grate_square", "trapdoor", "bone_pit", "sigil_plate"], cat="architecture", place="floor", tags=["arch", "flat", "decal"])
def _floor_feature(A, v):
    k = v["n"]
    if k == "grate_round":
        cyl(A, 0.45, 0.02, (0, 0, 0.01), "stone_dark", verts=28); tor(A, 0.42, 0.02, (0, 0, 0.025), "iron", seg=28)
        for x in (-0.3, -0.15, 0, 0.15, 0.3): box(A, (0.025, 0.7, 0.02), (x, 0, 0.03), "iron", bevel=0)
    elif k == "grate_square":
        box(A, (0.8, 0.8, 0.02), (0, 0, 0.01), "stone_dark", bevel=0.003); box(A, (0.86, 0.86, 0.025), (0, 0, 0.012), "iron", bevel=0.003)
        for x in (-0.3, -0.15, 0, 0.15, 0.3): box(A, (0.03, 0.74, 0.02), (x, 0, 0.03), "black", bevel=0)
    elif k == "trapdoor":
        for i in range(6): box(A, (0.14, 0.9, 0.04), (-0.36 + i * 0.145, 0, 0.02), "wood", bevel=0.003)
        for y in (-0.3, 0.3): box(A, (0.9, 0.08, 0.02), (0, y, 0.05), "iron", bevel=0.003)
        tor(A, 0.06, 0.012, (0, 0.0, 0.06), "iron", seg=14)
    elif k == "bone_pit":
        cyl(A, 0.55, 0.02, (0, 0, 0.01), "black", verts=28); tor(A, 0.55, 0.04, (0, 0, 0.03), "stone", seg=28)
        for i in range(7): a = i * 0.9; bone(A, (0.15 * math.cos(a), 0.15 * math.sin(a), 0.04), (0.38 * math.cos(a + 0.5), 0.38 * math.sin(a + 0.5), 0.05), 0.015)
        skull(A, (0.05, -0.05, 0.02), 0.9)
    elif k == "sigil_plate":
        cyl(A, 0.5, 0.03, (0, 0, 0.015), "stone_dark", verts=6); tor(A, 0.42, 0.012, (0, 0, 0.032), "rune", seg=6, minor=6)
        for i in range(3): a = i * 2 * PI / 3 + PI / 2; box(A, (0.7, 0.014, 0.006), (0, 0, 0.034), "rune", rot=(0, 0, a), bevel=0)


@family("raised_floor", "architecture", ["dais_square", "dais_round", "stair_steps", "well", "stone_font"], cat="architecture", place="floor", tags=["arch", "raised", "wall-hug"])
def _raised_floor(A, v):
    k = v["n"]
    if k == "dais_square":
        for i, (w, h) in enumerate([(2.0, 0.14), (1.7, 0.28), (1.4, 0.42)]): box(A, (w, w * 0.8, h), (0, 0, h / 2), "stone_light" if i % 2 == 0 else "stone", bevel=0.015)
    elif k == "dais_round":
        for i, (r, h) in enumerate([(1.1, 0.14), (0.9, 0.28), (0.7, 0.42)]): cyl(A, r, h, (0, 0, h / 2), "stone_light" if i % 2 == 0 else "stone", verts=28)
    elif k == "stair_steps":
        for i in range(4): box(A, (1.3, 0.35, 0.16 * (i + 1)), (0, 0.5 - i * 0.35 + 0.0, 0.08 * (i + 1)), "stone_light" if i % 2 == 0 else "stone", bevel=0.01)
    elif k == "well":
        lathe(A, [(0.55, 0.0), (0.55, 0.7), (0.62, 0.72), (0.62, 0.8), (0.4, 0.8), (0.4, 0.72)], (0, 0, 0), "stone_light", verts=24)
        cyl(A, 0.4, 0.02, (0, 0, 0.7), "black", verts=24)
        for s in (-1, 1): cyl(A, 0.04, 1.2, (s * 0.6, 0, 1.3), "wood", verts=8)
        cyl(A, 0.035, 1.3, (0, 0, 1.85), "wood", rot=(0, PI / 2, 0), verts=8); cyl(A, 0.03, 0.6, (0, 0, 1.55), "iron", rot=(0, PI / 2, 0), verts=8)
    elif k == "stone_font":
        lathe(A, [(0.3, 0), (0.2, 0.05), (0.14, 0.5), (0.22, 0.65), (0.4, 0.75), (0.42, 0.85), (0.34, 0.85), (0.34, 0.8)], (0, 0, 0), "stone_light", verts=24)
        cyl(A, 0.33, 0.02, (0, 0, 0.8), "ecto", verts=20)


@family("buttress", "architecture", ["stone", "skull"], cat="architecture", place="floor", tags=["arch", "buttress", "wall-hug"])
def _buttress(A, v):
    for i, (w, d, h) in enumerate([(0.8, 0.6, 0.6), (0.65, 0.5, 1.6), (0.5, 0.4, 2.5)]):
        box(A, (w, d, h), (0, 0.3 - d / 2 + 0.0, h / 2), "stone_light" if i != 1 else "stone", bevel=0.02)
    prism(A, [(-0.25, 0), (0.25, 0), (0.0, 0.4)], 0.4, (0, 0.0, 2.5), "stone", bevel=0.01)
    if v["n"] == "skull": skull(A, (0, -0.25, 1.5), 2.2)
