# ============ DECOR & CLUTTER (~70) ============

@family("urn", "decor", ["funerary_tall", "canopic_jar", "pot_urn", "ashes_urn", "gold_ornate", "cracked_urn"], cat="decor", place="surface", tags=["decor"], replaces="vase")
def _urn(A, v):
    k = v["n"]
    prof = {"funerary_tall": [(0.0, 0), (0.07, 0.0), (0.06, 0.04), (0.11, 0.2), (0.07, 0.3), (0.08, 0.36), (0.0, 0.36)], "canopic_jar": [(0.0, 0), (0.07, 0.0), (0.09, 0.15), (0.08, 0.22), (0.0, 0.22)],
            "pot_urn": [(0.0, 0), (0.08, 0.0), (0.14, 0.12), (0.12, 0.22), (0.07, 0.26), (0.08, 0.3), (0.0, 0.3)], "ashes_urn": [(0.0, 0), (0.07, 0.0), (0.11, 0.1), (0.1, 0.2), (0.06, 0.25), (0.0, 0.25)],
            "gold_ornate": [(0.0, 0), (0.06, 0.0), (0.05, 0.03), (0.12, 0.17), (0.06, 0.28), (0.09, 0.32), (0.0, 0.32)], "cracked_urn": [(0.0, 0), (0.08, 0.0), (0.12, 0.12), (0.1, 0.2), (0.0, 0.2)]}[k]
    mat = {"gold_ornate": "gold", "ashes_urn": "stone_dark", "canopic_jar": "stone_light", "cracked_urn": "stone"}.get(k, "wood_pale" if k == "pot_urn" else "stone_light")
    lathe(A, prof, (0, 0, 0), mat, verts=18)
    if k == "canopic_jar": sph(A, 0.07, (0, 0, 0.27), "stone_light", scale=(1, 1.1, 1.0), seg=10); box(A, (0.05, 0.02, 0.01), (0, -0.065, 0.28), "black", bevel=0)
    if k in ("funerary_tall", "gold_ornate"): tor(A, 0.1, 0.006, (0, 0, 0.18), "gold", seg=20)
    if k == "cracked_urn": limb(A, (0.0, -0.1, 0.2), (0.03, -0.11, 0.06), 0.004, 0.002, "black", 4)
    for s in (-1, 1) if k in ("funerary_tall", "pot_urn", "gold_ornate") else (): tor(A, 0.04, 0.007, (s * 0.1, 0, 0.2), "gold" if k != "pot_urn" else "iron", rot=(PI / 2, 0, 0), seg=14)


@family("chalice", "decor", ["gold", "skull_goblet", "bone_cup", "silver", "wine_pair", "blood_horn"], cat="decor", place="surface", tags=["decor"])
def _chalice(A, v):
    k = v["n"]; m = {"gold": "gold", "skull_goblet": "bone", "bone_cup": "bone", "silver": "silver", "wine_pair": "pewter", "blood_horn": "bone"}[k]
    def cup(x, mat, liq="blood"):
        lathe(A, [(0.0, 0), (0.04, 0.0), (0.012, 0.03), (0.012, 0.1), (0.05, 0.14), (0.055, 0.2), (0.045, 0.2), (0.0, 0.15)], (x, 0, 0), mat, verts=14); cyl(A, 0.043, 0.006, (x, 0, 0.18), liq, verts=12)
    if k in ("gold", "silver", "bone_cup"): cup(0, m)
    elif k == "wine_pair": cup(-0.07, m, "potion_red"); cup(0.07, m, "potion_red")
    elif k == "skull_goblet": skull(A, (0, 0, 0.1), 0.9, jaw=False); lathe(A, [(0.0, 0), (0.05, 0.0), (0.02, 0.04), (0.02, 0.1)], (0, 0, 0), "gold", verts=10)
    elif k == "blood_horn": limb(A, (-0.1, 0, 0.1), (0.05, 0, 0.13), 0.045, 0.02, "bone", 10); limb(A, (0.05, 0, 0.13), (0.12, 0, 0.2), 0.02, 0.008, "bone", 8); cyl(A, 0.04, 0.01, (-0.1, 0, 0.1), "blood", rot=(0, PI / 2, 0), verts=10); box(A, (0.1, 0.04, 0.05), (-0.04, 0, 0.03), "iron", bevel=0.005)


@family("serving", "decor", ["bone_plate", "tray_goblets", "candle_plate"], cat="decor", place="surface", tags=["decor"])
def _serving(A, v):
    k = v["n"]
    if k == "bone_plate": cyl(A, 0.12, 0.012, (0, 0, 0.006), "bone", r2=0.1, verts=24); [bone(A, (-0.06, -0.03 + i * 0.03, 0.02), (0.06, -0.03 + i * 0.03, 0.02), 0.008) for i in range(3)]
    elif k == "tray_goblets": cyl(A, 0.17, 0.015, (0, 0, 0.008), "silver", verts=24); [lathe(A, [(0.0, 0), (0.03, 0.0), (0.01, 0.025), (0.01, 0.06), (0.035, 0.09), (0.0, 0.09)], (0.08 * math.cos(a), 0.08 * math.sin(a), 0.015), "silver", verts=10) for a in (0, 2.1, 4.2)]
    elif k == "candle_plate": cyl(A, 0.1, 0.015, (0, 0, 0.008), "gold", verts=18); candle(A, (0, 0, 0.015), h=0.14, r=0.025); [sph(A, 0.012, (0.05 * math.cos(a), 0.05 * math.sin(a), 0.02), "wax", scale=(1, 1, 0.5), seg=6) for a in (0.5, 2, 3.5, 5)]


@family("raven", "decor", ["perched", "pair", "skull_raven", "hooded"], cat="decor", place="surface", tags=["decor"])
def _raven(A, v):
    k = v["n"]
    def bird(x, yaw=0.0, s=1.0):
        sph(A, 0.06 * s, (x, 0, 0.1 * s), "black", scale=(0.8, 1.4, 1), seg=10); sph(A, 0.035 * s, (x, -0.07 * s, 0.15 * s), "black", seg=8); cyl(A, 0.012 * s, 0.05 * s, (x, -0.11 * s, 0.15 * s), "gold", r2=0.0, rot=(PI / 2, 0, 0), verts=6)
        sph(A, 0.008 * s, (x + 0.018 * s, -0.095 * s, 0.165 * s), "ember", seg=5); prism(A, [(0, 0), (0.0, 0.14), (0.03, 0.2), (-0.03, 0.2)], 0.01, (x, 0.12 * s, 0.1 * s), "black", rot=(PI / 2.6, 0, 0), bevel=0)
        for sg in (-1, 1): prism(A, [(0, 0), (sg * 0.09, 0.02), (sg * 0.1, 0.1), (0, 0.12)] if sg > 0 else [(0, 0), (0, 0.12), (-0.1, 0.1), (-0.09, 0.02)], 0.008, (x, 0.0, 0.11 * s), "black", rot=(0, 0, 0), bevel=0)
    if k == "perched": bird(0)
    elif k == "pair": bird(-0.07, s=0.9); bird(0.07, s=1.0)
    elif k == "skull_raven": bird(0); skull(A, (0.0, -0.1, 0.1), 0.35, mat="ivory")
    elif k == "hooded": bird(0); cyl(A, 0.04, 0.05, (0, -0.03, 0.2), "cloth", r2=0.0, verts=8)
    box(A, (0.04, 0.04, 0.006), (0, 0, 0.003), "iron", bevel=0) if False else None


@family("barrel", "decor", ["wine_barrel", "big_cask", "small_keg", "rune_barrel"], cat="decor", place="floor", tags=["wall-hug", "decor"])
def _barrel(A, v):
    k = v["n"]; R, H = {"wine_barrel": (0.32, 0.8), "big_cask": (0.45, 1.1), "small_keg": (0.22, 0.45), "rune_barrel": (0.32, 0.8)}[k]
    lathe(A, [(R * 0.8, 0), (R * 0.95, H * 0.2), (R, H * 0.5), (R * 0.95, H * 0.8), (R * 0.8, H)], (0, 0, 0), "wood", verts=20)
    for z in (0.12, 0.3, 0.7, 0.88): tor(A, R * (0.84 + 0.16 * math.sin(PI * z)) , 0.014, (0, 0, H * z), "iron", seg=22, minor=5)
    cyl(A, R * 0.78, 0.01, (0, 0, H), "wood_red", verts=20); box(A, (0.05, 0.03, 0.05), (0, -R, H * 0.4), "iron", bevel=0.004)
    if k == "rune_barrel": [box(A, (0.015, 0.01, 0.08), (R * math.sin(a) * 0.98, -R * math.cos(a) * 0.98, H * 0.5), "rune", rot=(0, 0, a), bevel=0) for a in (-0.4, 0, 0.4)]
    if k == "big_cask": cyl(A, 0.03, 0.12, (0, -R - 0.03, H * 0.3), "gold", rot=(PI / 2, 0, 0), verts=8)


@family("crate", "decor", ["plain", "stacked", "coffin_crate", "trunk"], cat="decor", place="floor", tags=["wall-hug", "decor"])
def _crate(A, v):
    k = v["n"]
    def crate(x, y, z, s=0.6):
        box(A, (s, s, s), (x, y, z + s / 2), "wood_pale", bevel=0.01)
        for a in (-1, 1): box(A, (0.04, s + 0.02, s + 0.02), (x + a * (s / 2 - 0.02), y, z + s / 2), "wood", bevel=0.004); box(A, (s + 0.02, 0.04, s + 0.02), (x, y + a * (s / 2 - 0.02), z + s / 2), "wood", bevel=0.004)
    if k == "plain": crate(0, 0, 0)
    elif k == "stacked": crate(-0.2, 0, 0, 0.6); crate(0.35, 0.05, 0, 0.5); crate(0.0, 0.0, 0.6, 0.45)
    elif k == "coffin_crate":
        box(A, (0.55, 1.6, 0.4), (0, 0, 0.2), "wood_pale", bevel=0.01); [box(A, (0.57, 0.05, 0.42), (0, y, 0.2), "wood", bevel=0.004) for y in (-0.7, 0, 0.7)]; box(A, (0.3, 0.02, 0.1), (0, -0.81, 0.25), "black", bevel=0)
    elif k == "trunk":
        box(A, (0.9, 0.5, 0.45), (0, 0, 0.225), "leather", bevel=0.02); cyl(A, 0.25, 0.9, (0, 0, 0.45), "leather", rot=(0, PI / 2, 0), verts=18); [box(A, (0.05, 0.52, 0.6), (x, 0, 0.3), "iron", bevel=0.004) for x in (-0.3, 0.3)]; box(A, (0.08, 0.02, 0.1), (0, -0.26, 0.38), "gold", bevel=0)


@family("sack", "decor", ["pile", "single", "grain"], cat="decor", place="floor", tags=["wall-hug", "decor"])
def _sack(A, v):
    k = v["n"]
    def sack(x, y, s=1.0, rot=0.0):
        lathe(A, [(0.0, 0), (0.2, 0.0), (0.25, 0.15), (0.2, 0.35), (0.1, 0.5), (0.12, 0.55), (0.04, 0.6), (0.0, 0.6)], (x, y, 0), "burlap", verts=14, scale=s); tor(A, 0.1 * s, 0.015, (x, y, 0.5 * s), "rope", seg=14, minor=4)
    if k == "single": sack(0, 0)
    elif k == "pile": sack(-0.25, 0, 0.9); sack(0.25, 0.05, 1.0); sack(0.0, -0.05, 0.85); sph(A, 0.0001, (0, 0, 0.01), "burlap", seg=3)
    elif k == "grain": sack(0, 0, 1.1); [sph(A, 0.012, (0.15 + 0.02 * i, 0.05 * (i % 3), 0.01), "wood_pale", seg=5) for i in range(8)]


def _rug_base(A, w=2.6, d=1.8, border="cloth", field="black"):
    box(A, (w, d, 0.012), (0, 0, 0.006), "black", bevel=0.003); box(A, (w - 0.1, d - 0.1, 0.016), (0, 0, 0.008), border, bevel=0.003); box(A, (w - 0.3, d - 0.3, 0.02), (0, 0, 0.01), field, bevel=0.003)


@family("rug", "decor", ["pentagram_red", "runic_circle", "skull_border", "blood_ring", "gold_border", "tattered", "moon_phases", "spiral_sigil"], cat="decor", place="floor", tags=["rug", "flat", "center"], **{"as": "rug"})
def _rug(A, v):
    k = v["n"]
    _rug_base(A, border="cloth2" if k in ("runic_circle", "moon_phases") else "cloth", field="stone_dark" if k == "tattered" else "black")
    if k == "pentagram_red":
        tor(A, 0.6, 0.014, (0, 0, 0.024), "blood", seg=48); [box(A, (math.hypot(0.57 * (math.cos(math.radians(90 + (i + 1) * 144)) - math.cos(math.radians(90 + i * 144))), 0.57 * (math.sin(math.radians(90 + (i + 1) * 144)) - math.sin(math.radians(90 + i * 144)))), 0.016, 0.004), (0.57 * (math.cos(math.radians(90 + i * 144)) + math.cos(math.radians(90 + (i + 1) * 144))) / 2, 0.57 * (math.sin(math.radians(90 + i * 144)) + math.sin(math.radians(90 + (i + 1) * 144))) / 2, 0.026), "blood", rot=(0, 0, math.atan2(math.sin(math.radians(90 + (i + 1) * 144)) - math.sin(math.radians(90 + i * 144)), math.cos(math.radians(90 + (i + 1) * 144)) - math.cos(math.radians(90 + i * 144)))), bevel=0) for i in range(5)]
    elif k == "runic_circle":
        for r in (0.65, 0.5, 0.35): tor(A, r, 0.01, (0, 0, 0.024), "rune", seg=48, minor=4)
        for a in np_range(0, 6.2, PI / 6): box(A, (0.05, 0.012, 0.004), (0.57 * math.cos(a), 0.57 * math.sin(a), 0.026), "rune", rot=(0, 0, a), bevel=0)
    elif k == "skull_border":
        for x in np_range(-1.1, 1.1, 0.22): [skull(A, (x, s * 0.72, 0.02), 0.45, yaw=(PI if s > 0 else 0)) for s in (-1, 1)]
        tor(A, 0.45, 0.012, (0, 0, 0.024), "gold", seg=40)
    elif k == "blood_ring": tor(A, 0.55, 0.05, (0, 0, 0.026), "blood", seg=40); tor(A, 0.3, 0.025, (0, 0, 0.026), "blood", seg=32); cyl(A, 0.1, 0.004, (0, 0, 0.024), "blood", verts=18)
    elif k == "gold_border": box(A, (2.3, 0.04, 0.004), (0, 0.65, 0.024), "gold", bevel=0); box(A, (2.3, 0.04, 0.004), (0, -0.65, 0.024), "gold", bevel=0); [box(A, (0.04, 1.3, 0.004), (s * 1.15, 0, 0.024), "gold", bevel=0) for s in (-1, 1)]; tor(A, 0.4, 0.015, (0, 0, 0.025), "gold", seg=36)
    elif k == "tattered": [box(A, (0.3, 0.2, 0.002), (x, y, 0.022), "ash", rot=(0, 0, x), bevel=0) for x, y in [(-0.8, 0.3), (0.7, -0.4), (0.1, 0.5), (-0.3, -0.5)]]; [sph(A, 0.08, (x, y, 0.02), "moss", scale=(1, 1, 0.1), seg=6) for x, y in [(1.0, 0.5), (-1.0, -0.4)]]
    elif k == "moon_phases":
        for i, x in enumerate(np_range(-0.9, 0.9, 0.3)): sph(A, 0.1, (x, 0, 0.026), "ivory", scale=(1, 1, 0.05), seg=12); sph(A, 0.09, (x + 0.05 * (i - 3), 0.0, 0.03), "black", scale=(1, 1, 0.05), seg=12)
    elif k == "spiral_sigil":
        for i in range(40): a = i * 0.4; r = 0.03 + i * 0.016; box(A, (0.06, 0.012, 0.004), (r * math.cos(a), r * math.sin(a), 0.025), "rune", rot=(0, 0, a + PI / 2), bevel=0)


@family("banner", "decor", ["house_red", "house_purple", "black_skull", "gold_rune", "academy_crest", "long_pennant_red", "long_pennant_black", "scroll_banner", "hex_banner", "bone_banner", "torn_banner", "twin_pennants"],
        cat="wall decor", place="wall", y=0.9, tags=["decor"])
def _banner(A, v):
    k = v["n"]; w, h = (0.8, 1.7)
    if "long" in k: w, h = 0.5, 2.2
    cyl(A, 0.014, w + 0.15, (0, 0.03, h + 0.05), "iron", rot=(0, PI / 2, 0), verts=8); [sph(A, 0.028, (s * (w / 2 + 0.07), 0.03, h + 0.05), "gold", seg=8) for s in (-1, 1)]
    col = {"house_red": "cloth", "house_purple": "cloth2", "black_skull": "black", "gold_rune": "black", "academy_crest": "cloth2", "long_pennant_red": "cloth", "long_pennant_black": "black", "scroll_banner": "parchment", "hex_banner": "cloth", "bone_banner": "cloth2", "torn_banner": "cloth", "twin_pennants": "cloth"}[k]
    if k == "twin_pennants":
        for s in (-1, 1): prism(A, [(-0.2, 1.2), (0.2, 1.2), (0.2, 0.2), (0.0, 0.0), (-0.2, 0.2)], 0.02, (s * 0.25, 0.02, 0.0), col, bevel=0.003)
    elif k == "hex_banner": prism(A, [(0, 0), (0.4, 0.3), (0.4, 1.4), (0, 1.7), (-0.4, 1.4), (-0.4, 0.3)], 0.02, (0, 0.02, 0.0), col, bevel=0.004)
    elif k == "torn_banner": prism(A, [(-0.4, 0.2), (-0.15, 0.0), (0.0, 0.35), (0.2, 0.1), (0.4, 0.4), (0.4, 1.7), (-0.4, 1.7)], 0.02, (0, 0.02, 0.0), col, bevel=0.003)
    elif "long" in k: prism(A, [(0, 0), (0.25, 0.4), (0.25, 2.2), (-0.25, 2.2), (-0.25, 0.4)], 0.02, (0, 0.02, 0.0), col, bevel=0.003)
    else: prism(A, [(-0.4, 0.3), (0.0, 0.1), (0.4, 0.3), (0.4, 1.7), (-0.4, 1.7)], 0.02, (0, 0.02, 0.0), col, bevel=0.003)
    if k in ("black_skull", "bone_banner"): skull(A, (0, 0.0, 1.1), 1.7)
    elif k in ("gold_rune", "house_red", "house_purple", "hex_banner"): tor(A, 0.14, 0.01, (0, -0.005, 1.1), "gold", rot=(PI / 2, 0, 0), seg=22); box(A, (0.015, 0.012, 0.36), (0, -0.006, 1.1), "gold", bevel=0); box(A, (0.24, 0.012, 0.015), (0, -0.006, 1.14), "gold", bevel=0)
    elif k == "academy_crest": tor(A, 0.18, 0.012, (0, -0.005, 1.1), "silver", rot=(PI / 2, 0, 0), seg=26); skull(A, (0, -0.005, 1.02), 1.3, mat="silver"); [bone(A, (-0.12 + 0.24 * i, -0.005, 0.95), (0.12 - 0.24 * i, -0.005, 1.25), 0.01, "silver") for i in range(2)]
    elif k == "scroll_banner": [box(A, (0.5, 0.008, 0.012), (0, -0.006, 1.3 - i * 0.12), "black", bevel=0) for i in range(5)]
    elif "long" in k: [box(A, (0.1, 0.01, 0.015), (0, -0.006, 1.6 - 0.2 * i), "gold", bevel=0) for i in range(4)]


@family("mirror", "decor", ["cracked", "ornate_gold", "bone_frame", "oval_black", "skull_crowned"], cat="wall decor", place="wall", y=0.7, tags=["decor"], replaces="mirror")
def _mirror(A, v):
    k = v["n"]; frame = {"cracked": "iron", "ornate_gold": "gold", "bone_frame": "bone", "oval_black": "black", "skull_crowned": "iron"}[k]
    if k == "oval_black":
        cyl(A, 0.35, 0.05, (0, 0, 0.7), frame, rot=(PI / 2, 0, 0), verts=32).data.transform(Matrix.Diagonal((1, 1, 1.3, 1))) if False else None
        sph(A, 0.37, (0, 0, 0.75), frame, scale=(1, 0.14, 1.4), seg=24); sph(A, 0.32, (0, -0.02, 0.75), "glass", scale=(1, 0.1, 1.38), seg=24)
    else:
        prism(A, arch_pts(0.7, 0.55, 0.9), 0.05, (0, 0, 0.1), frame, bevel=0.008); prism(A, arch_pts(0.58, 0.5, 0.9), 0.03, (0, -0.02, 0.16), "glass", bevel=0.002)
        if k == "cracked": [limb(A, (0.0, -0.04, 0.5 + 0.1 * i), (0.15 * (-1) ** i, -0.04, 0.3 + 0.15 * i), 0.004, 0.002, "black", 4) for i in range(4)]
        if k == "bone_frame": [bone(A, (s * 0.35, -0.03, 0.15), (s * 0.35, -0.03, 0.9), 0.025, "bone") for s in (-1, 1)]; skull(A, (0, -0.03, 1.3), 0.7, mat="ivory")
        if k == "skull_crowned": skull(A, (0, -0.03, 1.4), 1.0, mat="ivory"); [cyl(A, 0.008, 0.04, (0.05 * i, -0.03, 1.57), "gold", r2=0.0, verts=4) for i in range(-2, 3)]
        if k == "ornate_gold": [sph(A, 0.03, (s * 0.35, -0.03, z), "gold", seg=8) for s in (-1, 1) for z in (0.3, 0.7)]


@family("clock", "decor", [{"n": "grandfather", "meta": {"place": "floor", "tags": ["wall-hug", "tall"]}}, {"n": "wall_skull", "meta": {"place": "wall", "y": 1.9}}, {"n": "wall_sun", "meta": {"place": "wall", "y": 1.9}}], cat="decor", place="floor", tags=["decor"])
def _clock(A, v):
    k = v["n"]
    if k == "grandfather":
        box(A, (0.5, 0.3, 0.2), (0, 0, 0.1), "wood", bevel=0.01); box(A, (0.4, 0.26, 1.3), (0, 0, 0.85), "wood_red", bevel=0.01); box(A, (0.5, 0.3, 0.5), (0, 0, 1.75), "wood", bevel=0.01); prism(A, arch_pts(0.5, 0.0, 0.3), 0.3, (0, 0, 2.0), "wood")
        cyl(A, 0.17, 0.02, (0, -0.15, 1.75), "ivory", rot=(PI / 2, 0, 0), verts=28); tor(A, 0.17, 0.012, (0, -0.16, 1.75), "gold", rot=(PI / 2, 0, 0), seg=28); box(A, (0.012, 0.01, 0.12), (0, -0.17, 1.8), "black", bevel=0); box(A, (0.1, 0.01, 0.012), (0.04, -0.17, 1.75), "black", rot=(0, 0.5, 0), bevel=0)
        box(A, (0.2, 0.01, 0.8), (0, -0.135, 0.9), "glass", bevel=0); cyl(A, 0.06, 0.012, (0, -0.14, 0.5), "gold", rot=(PI / 2, 0, 0), verts=16); limb(A, (0, -0.14, 1.2), (0, -0.14, 0.56), 0.005, 0.005, "gold", 6)
    elif k == "wall_skull":
        cyl(A, 0.2, 0.05, (0, 0, 0.3), "bone", rot=(PI / 2, 0, 0), verts=28); tor(A, 0.2, 0.02, (0, -0.025, 0.3), "gold", rot=(PI / 2, 0, 0), seg=28); skull(A, (0, -0.03, 0.34), 0.8, mat="ivory"); box(A, (0.012, 0.01, 0.12), (0, -0.04, 0.34), "black", bevel=0)
    elif k == "wall_sun":
        cyl(A, 0.15, 0.04, (0, 0, 0.3), "gold", rot=(PI / 2, 0, 0), verts=24)
        for i in range(12): a = i * PI / 6; cyl(A, 0.02, 0.18, (0.24 * math.cos(a), 0, 0.3 + 0.24 * math.sin(a)), "gold", r2=0.0, rot=(0, PI / 2 - a, 0), verts=4)
        cyl(A, 0.11, 0.01, (0, -0.025, 0.3), "ivory", rot=(PI / 2, 0, 0), verts=22); box(A, (0.01, 0.01, 0.08), (0, -0.032, 0.33), "black", bevel=0)


@family("mask", "decor", ["plague_doctor", "demon", "bone_mask", "venetian_black"], cat="wall decor", place="wall", y=1.6, tags=["decor"])
def _mask(A, v):
    k = v["n"]
    prism(A, [(0, -0.12), (0.12, -0.04), (0.12, 0.1), (-0.12, 0.1), (-0.12, -0.04)], 0.04, (0, 0.03, 0.15), {"plague_doctor": "leather", "demon": "blood", "bone_mask": "bone", "venetian_black": "black"}[k], bevel=0.01)
    for s in (-1, 1): sph(A, 0.025, (s * 0.05, -0.02, 0.25), "black", scale=(1, 0.4, 1.1), seg=8); sph(A, 0.012, (s * 0.05, -0.03, 0.25), "ember" if k == "demon" else "ivory", seg=6)
    if k == "plague_doctor": limb(A, (0, -0.04, 0.2), (0, -0.2, 0.12), 0.03, 0.008, "leather", 8)
    elif k == "demon": [limb(A, (s * 0.08, -0.02, 0.3), (s * 0.16, -0.02, 0.42), 0.02, 0.004, "black", 6) for s in (-1, 1)]
    elif k == "venetian_black": [limb(A, (s * 0.1, -0.02, 0.2), (s * 0.2, -0.02, 0.1), 0.003, 0.003, "gold", 4) for s in (-1, 1)]
    elif k == "bone_mask": [box(A, (0.03, 0.01, 0.02), (x, -0.045, 0.1), "ivory", bevel=0) for x in (-0.05, -0.017, 0.017, 0.05)]


@family("drapes", "decor", ["ragged", "purple_heavy", "tattered_black", "cobweb_curtain"], cat="wall decor", place="wall", y=0.05, tags=["curtain"], replaces="curtains")
def _drapes(A, v):
    k = v["n"]; col = {"ragged": "cloth", "purple_heavy": "cloth2", "tattered_black": "black", "cobweb_curtain": "ash"}[k]
    cyl(A, 0.016, 1.95, (0, 0.05, 2.32), "iron" if k != "purple_heavy" else "gold", rot=(0, PI / 2, 0), verts=10); [sph(A, 0.035, (s * 1.0, 0.05, 2.32), "iron", seg=8) for s in (-1, 1)]
    for s in (-1, 1):
        for i in range(5):
            h = 2.2 - (0.06 if i % 2 else 0.0) - (0.35 * (i / 4) if k in ("ragged", "tattered_black") else 0)
            box(A, (0.12, 0.09 + (i % 2) * 0.05, h), (s * (0.55 + i * 0.11), 0.04 + (i % 2) * 0.02, 0.1 + 2.2 - h / 2 - 0.1 + (h / 2 - h / 2)), col, bevel=0.02) if False else box(A, (0.12, 0.09 + (i % 2) * 0.05, h), (s * (0.55 + i * 0.11), 0.04 + (i % 2) * 0.02, 2.3 - h / 2), col, bevel=0.02)
    if k == "cobweb_curtain": [limb(A, (-0.6, 0.0, 2.3), (-0.6 + 0.3 * i, 0.0, 1.7 - 0.2 * (i % 2)), 0.003, 0.002, "ivory", 4) for i in range(5)]


@family("withered_plant", "decor", ["dead_tree_a", "dead_tree_b", "dead_tree_c", "thorn_pot"], cat="decor", place="floor", tags=["plant", "corner", "decor"], **{"as": "plant"})
def _wplant(A, v):
    k = v["n"]
    lathe(A, [(0.0, 0), (0.17, 0.0), (0.2, 0.15), (0.17, 0.32), (0.0, 0.32)], (0, 0, 0), "stone" if k != "thorn_pot" else "black", verts=16); tor(A, 0.19, 0.022, (0, 0, 0.32), "stone_dark", seg=22); cyl(A, 0.17, 0.02, (0, 0, 0.31), "ash", verts=16)
    rng = random.Random(len(k) * 3 + ord(k[-1]))
    def br(p0, p1, r0, r1, depth):
        limb(A, p0, p1, r0, r1, "wood", 6)
        if depth > 0:
            for t in (0, 1, 2):
                a = rng.random() * 6.28; d = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
                q = (p1[0] + 0.18 * math.cos(a) + d[0] * 0.5, p1[1] + 0.18 * math.sin(a) + d[1] * 0.5, p1[2] + 0.2 + rng.random() * 0.1)
                br(p1, q, r1, r1 * 0.55, depth - 1)
    base = (0, 0, 0.31)
    n = {"dead_tree_a": 1, "dead_tree_b": 2, "dead_tree_c": 3, "thorn_pot": 0}[k]
    if k == "thorn_pot":
        for i in range(7): a = i * 0.9; limb(A, (0.05 * math.cos(a), 0.05 * math.sin(a), 0.3), (0.2 * math.cos(a) * (1 + i * 0.1), 0.2 * math.sin(a), 0.7 + 0.1 * i), 0.012, 0.004, "black", 5); sph(A, 0.02, (0.2 * math.cos(a) * (1 + i * 0.1), 0.2 * math.sin(a), 0.7 + 0.1 * i), "blood", seg=5)
    else:
        for i in range(n + 1): br(base, (0.05 * (i - n / 2), 0.03 * i, 0.9 + 0.1 * i), 0.04, 0.025, 2)


@family("withered_sprig", "decor", ["bone_sprout", "thorn_pot_small", "mushroom_cluster", "black_roses", "fungus_log"], cat="decor", place="surface", tags=["decor"], **{"as": "plant_small"})
def _sprig(A, v):
    k = v["n"]
    cyl(A, 0.06, 0.1, (0, 0, 0.05), "black" if k != "bone_sprout" else "bone", r2=0.045, verts=12)
    if k == "bone_sprout": [bone(A, (0.0, 0, 0.1), (0.06 * math.cos(a), 0.06 * math.sin(a), 0.28 + 0.03 * i), 0.008) for i, a in enumerate((0, 2.1, 4.2))]
    elif k == "thorn_pot_small": [limb(A, (0, 0, 0.1), (0.07 * math.cos(a), 0.07 * math.sin(a), 0.3), 0.007, 0.002, "black", 4) for a in (0, 1.5, 3, 4.5)]
    elif k == "mushroom_cluster": [(limb(A, (x, y, 0.1), (x, y, 0.1 + h), 0.01, 0.012, "ivory", 6), sph(A, 0.035, (x, y, 0.1 + h), "cloth2", scale=(1, 1, 0.6), seg=8)) for x, y, h in [(0, 0, 0.14), (0.04, 0.03, 0.09), (-0.04, 0.02, 0.07)]]
    elif k == "black_roses": [(limb(A, (0, 0, 0.1), (0.04 * math.cos(a), 0.04 * math.sin(a), 0.26), 0.004, 0.004, "moss", 5), sph(A, 0.03, (0.04 * math.cos(a), 0.04 * math.sin(a), 0.27), "black", seg=8)) for a in (0, 2.4, 4.8)]
    elif k == "fungus_log": box(A, (0.14, 0.06, 0.05), (0, 0, 0.12), "wood", rot=(0, 0, 0.2), bevel=0.01); [sph(A, 0.025, (0.04 * i - 0.04, -0.03, 0.14 + 0.01 * i), "potion", scale=(1, 0.6, 0.5), seg=6) for i in range(3)]
