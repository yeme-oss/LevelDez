# ============ ALCHEMY & NECROMANCY LAB (~95) ============

def _glow(c, i=0.8, y=0.9):
    return {"light": i, "lightColor": c, "lightY": y, "tags": ["light", "glow"]}


@family("cauldron", "alchemy", [{"n": "copper_big", "mat": "copper", "liq": "potion", "s": 1.1, "meta": _glow("#59ff7a", 0.9, 0.9)},
                                {"n": "witch_small", "mat": "iron", "liq": "potion_purple", "s": 0.75, "meta": _glow("#b070ff", 0.7, 0.65)},
                                {"n": "bone_rim", "mat": "iron", "liq": "ecto", "s": 0.95, "bones": True, "meta": _glow("#40ffe0", 0.8, 0.8)},
                                {"n": "soul_cauldron", "mat": "black", "liq": "soulfire", "s": 1.0, "meta": _glow("#4dffd0", 1.1, 0.9)},
                                {"n": "blood_cauldron", "mat": "iron", "liq": "potion_red", "s": 1.0, "meta": _glow("#ff2a2a", 0.8, 0.8)},
                                {"n": "tripod_fire", "mat": "iron", "liq": "potion_amber", "s": 0.9, "tripod": True, "meta": _glow("#ff8a30", 1.2, 0.9)}],
        cat="alchemy", place="floor", tags=["decor", "wall-hug"])
def _cauldron(A, v):
    s = v["s"]; m = v["mat"]
    lathe(A, [(0.2, 0.08), (0.36, 0.22), (0.43, 0.5), (0.36, 0.76), (0.3, 0.82)], (0, 0, 0), m, verts=24, scale=s)
    tor(A, 0.34 * s, 0.03 * s, (0, 0, 0.82 * s), m, seg=28); cyl(A, 0.31 * s, 0.02, (0, 0, 0.79 * s), v["liq"], verts=24)
    for sx in (-1, 1): tor(A, 0.07 * s, 0.014, (sx * 0.41 * s, 0, 0.6 * s), "iron", rot=(0, PI / 2, 0))
    if v.get("tripod"):
        for i in range(3): a = i * 2 * PI / 3 + 0.5; limb(A, (0.5 * math.cos(a), 0.5 * math.sin(a), 0.0), (0.12 * math.cos(a), 0.12 * math.sin(a), 0.9), 0.03, 0.02, "iron")
        for i in range(5): a = i * 1.26; sph(A, 0.07, (0.15 * math.cos(a), 0.15 * math.sin(a), 0.08), "ember", scale=(1, 1, 1.5), seg=8)
        for i in range(3): box(A, (0.4, 0.06, 0.06), (0, 0, 0.04), "wood", rot=(0, 0, i * 1.05), bevel=0.01)
    else:
        for i in range(3): a = i * 2 * PI / 3 + 0.3; cyl(A, 0.03 * s, 0.16, (0.26 * s * math.cos(a), 0.26 * s * math.sin(a), 0.08), m, r2=0.045 * s, verts=8)
    if v.get("bones"):
        for i in range(6): a = i * PI / 3; skull(A, (0.43 * s * math.cos(a), 0.43 * s * math.sin(a), 0.72 * s), 0.5, yaw=a + PI / 2)
    for (x, y) in [(0.05, 0.02), (-0.1, 0.08), (0.12, -0.1)]: sph(A, 0.04 * s, (x * s, y * s, 0.8 * s), v["liq"], seg=8)


@family("lab_bench", "alchemy", [{"n": "apparatus_bench", "meta": {"size": [1.8, 0.7, 0.9]}}, {"n": "herb_bench", "meta": {"size": [1.8, 0.7, 0.9]}}, {"n": "dissection_bench", "meta": {"size": [1.8, 0.7, 0.9]}}, {"n": "grinding_bench", "meta": {"size": [1.8, 0.7, 0.9]}}],
        cat="alchemy", place="floor", tags=["wall-hug", "holds-decor"])
def _lab_bench(A, v):
    k = v["n"]
    box(A, (1.8, 0.7, 0.07), (0, 0, 0.865), "wood", bevel=0.012)
    for sx in (-1, 1):
        for sy in (-1, 1): box(A, (0.09, 0.09, 0.83), (sx * 0.8, sy * 0.28, 0.415), "wood")
    box(A, (1.6, 0.06, 0.06), (0, 0.28, 0.25), "wood"); box(A, (1.6, 0.06, 0.06), (0, -0.28, 0.25), "wood")
    if k == "apparatus_bench":
        for i, c in enumerate(["potion", "potion_purple", "potion_red"]): sph(A, 0.07, (-0.6 + i * 0.25, 0.1, 0.97), c, seg=10); cyl(A, 0.022, 0.1, (-0.6 + i * 0.25, 0.1, 1.07), "glass_clear", verts=8)
    elif k == "herb_bench":
        for i in range(4): cyl(A, 0.06, 0.1, (-0.6 + i * 0.35, 0.0, 0.94), "leather", r2=0.07, verts=10)
        for x in (-0.5, 0.2): limb(A, (x, 0.2, 0.9), (x + 0.15, 0.2, 1.0), 0.01, 0.01, "moss", 5)
    elif k == "dissection_bench":
        box(A, (1.2, 0.5, 0.02), (0, 0, 0.91), "stone_light", bevel=0.005); box(A, (0.3, 0.02, 0.01), (0.3, -0.1, 0.93), "silver", rot=(0, 0, 0.3), bevel=0)
        sph(A, 0.05, (-0.3, 0, 0.95), "potion_red", scale=(1.3, 1, 0.7), seg=8)
    elif k == "grinding_bench":
        lathe(A, [(0.0, 0.9), (0.12, 0.9), (0.14, 1.0), (0.1, 1.0), (0.0, 0.92)], (-0.4, 0, 0), "stone_dark", verts=14); limb(A, (-0.4, 0, 0.96), (-0.3, 0.05, 1.12), 0.018, 0.012, "wood")
    box(A, (1.7, 0.05, 0.4), (0, 0.33, 1.15), "wood_red", bevel=0.01); box(A, (1.7, 0.03, 0.03), (0, 0.31, 1.0), "wood")


@family("apparatus", "alchemy", ["retort", "alembic", "distill_rig", "bubbling_flask", "burner_stand", "crucible", "scales", "mortar_pestle"], cat="alchemy", place="surface", tags=["decor"])
def _apparatus(A, v):
    k = v["n"]
    if k == "retort":
        sph(A, 0.1, (0, 0, 0.2), "glass_clear", seg=14); sph(A, 0.075, (0, 0, 0.17), "potion_purple", scale=(1, 1, 0.8), seg=10); limb(A, (0.06, 0, 0.26), (0.28, 0, 0.18), 0.03, 0.015, "glass_clear", 8); cyl(A, 0.1, 0.02, (0, 0, 0.05), "iron", verts=12)
        for s in (-1, 1): limb(A, (s * 0.06, 0, 0.0), (s * 0.04, 0, 0.12), 0.01, 0.01, "iron", 5)
    elif k == "alembic":
        lathe(A, [(0.12, 0), (0.14, 0.1), (0.1, 0.22), (0.05, 0.3)], (0, 0, 0), "copper", verts=14); sph(A, 0.07, (0, 0, 0.34), "copper", seg=10); limb(A, (0.04, 0, 0.36), (0.3, 0, 0.3), 0.02, 0.012, "copper", 8); cyl(A, 0.05, 0.1, (0.32, 0, 0.1), "glass_clear", verts=10); cyl(A, 0.04, 0.04, (0.32, 0, 0.07), "potion_amber", verts=10)
    elif k == "distill_rig":
        box(A, (0.5, 0.2, 0.03), (0, 0, 0.015), "wood"); cyl(A, 0.012, 0.5, (-0.2, 0, 0.27), "iron", verts=6); cyl(A, 0.012, 0.5, (0.2, 0, 0.27), "iron", verts=6)
        sph(A, 0.07, (-0.2, 0, 0.5), "glass_clear", seg=10); sph(A, 0.05, (-0.2, 0, 0.48), "potion", seg=8); limb(A, (-0.15, 0, 0.5), (0.18, 0, 0.35), 0.014, 0.014, "glass_clear", 6); sph(A, 0.06, (0.2, 0, 0.1), "glass_clear", seg=10); sph(A, 0.04, (0.2, 0, 0.08), "potion", seg=8)
    elif k == "bubbling_flask":
        lathe(A, [(0.0, 0), (0.11, 0.0), (0.12, 0.06), (0.04, 0.2), (0.04, 0.3), (0.05, 0.31), (0.0, 0.3)], (0, 0, 0), "glass_clear", verts=14); lathe(A, [(0.0, 0.01), (0.1, 0.01), (0.1, 0.07), (0.0, 0.07)], (0, 0, 0), "potion_blue", verts=12)
        for (x, z) in [(0.0, 0.14), (0.02, 0.2), (-0.01, 0.26)]: sph(A, 0.012, (x, 0, z), "potion_blue", seg=6)
    elif k == "burner_stand":
        for i in range(3): a = i * 2 * PI / 3; limb(A, (0.1 * math.cos(a), 0.1 * math.sin(a), 0), (0.04 * math.cos(a), 0.04 * math.sin(a), 0.2), 0.008, 0.008, "iron", 5)
        tor(A, 0.09, 0.007, (0, 0, 0.2), "iron", seg=14); cyl(A, 0.03, 0.05, (0, 0, 0.03), "copper", verts=10); sph(A, 0.03, (0, 0, 0.1), "flame", scale=(1, 1, 1.8), seg=8); sph(A, 0.07, (0, 0, 0.27), "glass_clear", seg=10)
    elif k == "crucible":
        for i in range(3): a = i * 2 * PI / 3; limb(A, (0.12 * math.cos(a), 0.12 * math.sin(a), 0.0), (0.06 * math.cos(a), 0.06 * math.sin(a), 0.14), 0.01, 0.01, "iron", 5)
        lathe(A, [(0.0, 0.12), (0.06, 0.13), (0.09, 0.22), (0.07, 0.22), (0.05, 0.14)], (0, 0, 0), "stone_dark", verts=12); cyl(A, 0.065, 0.01, (0, 0, 0.2), "ember", verts=12)
    elif k == "scales":
        cyl(A, 0.08, 0.02, (0, 0, 0.01), "gold", verts=12); cyl(A, 0.012, 0.3, (0, 0, 0.17), "gold", verts=8); box(A, (0.4, 0.015, 0.015), (0, 0, 0.31), "gold", bevel=0)
        for s in (-1, 1): chain(A, (s * 0.2, 0, 0.31), (s * 0.2, 0, 0.18), 0.008, "gold"); cyl(A, 0.07, 0.012, (s * 0.2, 0, 0.17), "gold", r2=0.05, verts=14)
        sph(A, 0.03, (-0.2, 0, 0.19), "bone", seg=8)
    elif k == "mortar_pestle":
        lathe(A, [(0.0, 0.0), (0.07, 0.0), (0.1, 0.08), (0.11, 0.1), (0.09, 0.1), (0.0, 0.03)], (0, 0, 0), "stone_dark", verts=14); limb(A, (0.0, 0, 0.05), (0.08, 0.04, 0.2), 0.02, 0.015, "stone", 8)


_BOTTLES = [("round", "potion"), ("tall", "potion_red"), ("flask", "potion_blue"), ("skull", "potion_purple"), ("vial", "potion_amber"), ("jar", "potion"), ("decanter", "potion_red"),
            ("triple", "potion_blue"), ("hex", "potion_purple"), ("teardrop", "potion_amber"), ("corked_big", "potion"), ("tiny_set", "potion_red")]


@family("potion", "alchemy", [{"n": f"{s}_{c.replace('potion_', '') or 'green'}", "shape": s, "liq": c} for s, c in _BOTTLES], cat="alchemy", place="surface", tags=["decor"])
def _potion(A, v):
    s, liq = v["shape"], v["liq"]
    def bottle(x, prof, h_liq, cork=True):
        lathe(A, prof, (x, 0, 0), "glass_clear", verts=14); lathe(A, [(r * 0.85, z) for r, z in prof if z <= h_liq][:-1] + [(0.0, h_liq)], (x, 0, 0.0), liq, verts=12) if False else None
        lathe(A, [(0.0, prof[0][1] + 0.01), (prof[1][0] * 0.88, prof[1][1] + 0.01), (prof[1][0] * 0.88, h_liq), (0.0, h_liq)], (x, 0, 0), liq, verts=12)
        if cork: cyl(A, 0.017, 0.05, (x, 0, prof[-1][1] + 0.015), "wood_pale", verts=8)
    if s == "round": bottle(0, [(0.0, 0), (0.07, 0.0), (0.085, 0.07), (0.03, 0.15), (0.03, 0.2)], 0.1)
    elif s == "tall": bottle(0, [(0.0, 0), (0.04, 0.0), (0.045, 0.2), (0.02, 0.26), (0.02, 0.32)], 0.18)
    elif s == "flask": bottle(0, [(0.0, 0), (0.1, 0.0), (0.11, 0.03), (0.03, 0.17), (0.03, 0.24)], 0.08)
    elif s == "skull": bottle(0, [(0.0, 0), (0.06, 0.0), (0.075, 0.07), (0.05, 0.13), (0.025, 0.16), (0.025, 0.2)], 0.1); skull(A, (0, -0.07, 0.03), 0.4)
    elif s == "vial": bottle(0, [(0.0, 0), (0.025, 0.0), (0.028, 0.1), (0.015, 0.12), (0.015, 0.14)], 0.07)
    elif s == "jar": bottle(0, [(0.0, 0), (0.07, 0.0), (0.075, 0.12), (0.06, 0.13), (0.06, 0.14)], 0.1, cork=False); cyl(A, 0.065, 0.03, (0, 0, 0.155), "pewter", verts=12)
    elif s == "decanter": bottle(0, [(0.0, 0), (0.08, 0.0), (0.085, 0.12), (0.03, 0.2), (0.025, 0.3), (0.04, 0.32)], 0.12)
    elif s == "triple":
        for x in (-0.07, 0, 0.07): bottle(x, [(0.0, 0), (0.03, 0.0), (0.032, 0.1), (0.015, 0.13), (0.015, 0.16)], 0.08)
    elif s == "hex": bottle(0, [(0.0, 0), (0.06, 0.0), (0.065, 0.14), (0.03, 0.18), (0.03, 0.22)], 0.1)
    elif s == "teardrop": bottle(0, [(0.0, 0), (0.06, 0.0), (0.09, 0.07), (0.04, 0.17), (0.02, 0.22), (0.02, 0.26)], 0.1)
    elif s == "corked_big": bottle(0, [(0.0, 0), (0.12, 0.0), (0.14, 0.15), (0.09, 0.28), (0.04, 0.33), (0.04, 0.38)], 0.2); cyl(A, 0.035, 0.07, (0, 0, 0.4), "wood_pale", verts=10)
    elif s == "tiny_set":
        for i, x in enumerate((-0.06, 0.0, 0.06)): bottle(x, [(0.0, 0), (0.02, 0.0), (0.022, 0.07), (0.01, 0.09), (0.01, 0.1)], 0.05)
        box(A, (0.2, 0.06, 0.015), (0, 0, -0.0), "wood", bevel=0)


_JARS = [("brain", "potion_purple"), ("heart", "potion_amber"), ("eyes", "ecto"), ("hand", "potion"), ("spider", "potion_amber"), ("tentacle", "potion_blue"), ("lungs", "potion_red"), ("bat", "potion")]


@family("specimen_jar", "alchemy", [{"n": k, "what": k, "liq": c} for k, c in _JARS], cat="alchemy", place="surface", tags=["decor"])
def _jar(A, v):
    k, liq = v["what"], v["liq"]
    lathe(A, [(0.0, 0), (0.1, 0.0), (0.105, 0.02), (0.105, 0.24), (0.09, 0.26), (0.0, 0.26)], (0, 0, 0), "glass_clear", verts=18); lathe(A, [(0.0, 0.015), (0.092, 0.02), (0.092, 0.22), (0.0, 0.22)], (0, 0, 0), liq, verts=14)
    cyl(A, 0.1, 0.03, (0, 0, 0.275), "pewter", verts=16); cyl(A, 0.11, 0.025, (0, 0, 0.01), "pewter", verts=16)
    if k == "brain": sph(A, 0.07, (0, 0, 0.13), "potion_red", scale=(1.2, 1, 0.8), seg=10); sph(A, 0.045, (0.03, 0, 0.16), "potion_red", scale=(1, 1, 0.8), seg=8)
    elif k == "heart": sph(A, 0.055, (0, 0, 0.13), "blood", scale=(1, 0.9, 1.1), seg=10); limb(A, (0, 0, 0.17), (0.02, 0, 0.22), 0.015, 0.01, "blood", 6)
    elif k == "eyes":
        for x in (-0.035, 0.035): sph(A, 0.03, (x, 0, 0.13), "ivory", seg=10); sph(A, 0.013, (x, -0.025, 0.13), "ember", seg=6)
    elif k == "hand":
        box(A, (0.06, 0.03, 0.05), (0, 0, 0.1), "bone", bevel=0.005)
        for i in range(4): bone(A, (-0.03 + i * 0.02, 0, 0.12), (-0.035 + i * 0.023, 0, 0.18), 0.007)
    elif k == "spider":
        sph(A, 0.04, (0, 0, 0.13), "black", scale=(1, 1.2, 0.8), seg=8)
        for i in range(4):
            for s in (-1, 1): limb(A, (s * 0.03, 0, 0.13), (s * 0.08, (i - 1.5) * 0.03, 0.1), 0.004, 0.003, "black", 4)
    elif k == "tentacle":
        for i, a in enumerate((0, 2.1, 4.2)): limb(A, (0.02 * math.cos(a), 0.02 * math.sin(a), 0.03), (0.05 * math.cos(a + 1), 0.05 * math.sin(a + 1), 0.18), 0.02, 0.006, "potion_purple", 6)
    elif k == "lungs":
        for s in (-1, 1): sph(A, 0.04, (s * 0.04, 0, 0.12), "potion_red", scale=(0.8, 0.8, 1.5), seg=8)
    elif k == "bat":
        sph(A, 0.03, (0, 0, 0.13), "black", seg=8)
        for s in (-1, 1): prism(A, [(0, 0), (s * 0.08, 0.02), (s * 0.06, 0.07), (0, 0.04)] if s > 0 else [(0, 0), (0, 0.04), (-0.06, 0.07), (-0.08, 0.02)], 0.004, (0, 0, 0.13), "black", rot=(PI / 2, 0, 0), bevel=0)


@family("hanging_herbs", "alchemy", ["lavender", "nightshade", "garlic_braid", "mushroom_string", "root_bundle", "bat_wings"], cat="alchemy", place="ceiling", tags=["decor"])
def _herbs(A, v):
    k = v["n"]
    box(A, (0.3, 0.04, 0.03), (0, 0, 0.7), "wood", bevel=0.003)
    cols = {"lavender": "cloth2", "nightshade": "black", "garlic_braid": "ivory", "mushroom_string": "leather", "root_bundle": "wood_pale", "bat_wings": "black"}
    for i in range(5):
        x = -0.12 + i * 0.06
        limb(A, (x, 0, 0.7), (x * 1.3, 0, 0.35 - (i % 2) * 0.1), 0.008, 0.012, "moss" if k in ("lavender", "nightshade") else "rope", 5)
        if k in ("lavender", "nightshade"): sph(A, 0.03, (x * 1.3, 0, 0.3 - (i % 2) * 0.1), cols[k], scale=(1, 1, 1.8), seg=6)
        elif k == "garlic_braid": sph(A, 0.035, (x * 0.3, 0, 0.62 - i * 0.12), "ivory", scale=(1, 1, 0.9), seg=8)
        elif k == "mushroom_string": sph(A, 0.03, (x * 0.2, 0, 0.6 - i * 0.12), cols[k], scale=(1.3, 1.3, 0.7), seg=8)
        elif k == "root_bundle": limb(A, (x * 1.3, 0, 0.35), (x * 1.8, 0, 0.1), 0.012, 0.003, "wood_pale", 5)
        elif k == "bat_wings": prism(A, [(0, 0), (0.1, 0.03), (0.09, 0.12), (0, 0.08)], 0.004, (x, 0, 0.25 - (i % 2) * 0.1), "black", rot=(PI / 2, 0, 0), bevel=0)


@family("grimoire", "alchemy", ["closed_red", "closed_black", "closed_green", "open_pages", "open_runes", "chained", "glowing", "bone_cover", "locked_clasp", "giant"], cat="alchemy", place="surface", tags=["decor"])
def _grimoire(A, v):
    k = v["n"]
    if k.startswith("closed"): book(A, (0, 0, 0.03), (0.22, 0.3, 0.06), {"closed_red": "book_a", "closed_black": "book_c", "closed_green": "book_b"}[k], 0.1); tor(A, 0.03, 0.004, (0.0, -0.15, 0.06), "gold", rot=(0, 0, 0), seg=10)
    elif k in ("open_pages", "open_runes"):
        box(A, (0.46, 0.3, 0.03), (0, 0, 0.015), "book_a", bevel=0.004)
        for s in (-1, 1): box(A, (0.21, 0.28, 0.025), (s * 0.11, 0, 0.04), "parchment", rot=(0, s * -0.1, 0), bevel=0.002)
        if k == "open_runes": tor(A, 0.07, 0.004, (-0.11, 0, 0.056), "rune", seg=18); tor(A, 0.07, 0.004, (0.11, 0, 0.056), "rune", seg=18); sph(A, 0.012, (0.11, 0, 0.058), "rune", seg=6)
    elif k == "chained": book(A, (0, 0, 0.04), (0.26, 0.34, 0.08), "book_c", 0.0); chain(A, (-0.14, 0, 0.1), (0.14, 0, 0.1), 0.012); box(A, (0.05, 0.06, 0.1), (0.0, -0.18, 0.04), "iron", bevel=0.004)
    elif k == "glowing": book(A, (0, 0, 0.03), (0.22, 0.3, 0.06), "book_f", 0.0); tor(A, 0.07, 0.006, (0, 0, 0.065), "rune", seg=18); sph(A, 0.03, (0, 0, 0.2), "rune", seg=8); sph(A, 0.015, (0.06, 0.03, 0.26), "rune", seg=6)
    elif k == "bone_cover": book(A, (0, 0, 0.03), (0.22, 0.3, 0.06), "bone", 0.1); skull(A, (0, -0.02, 0.06), 0.55, mat="ivory")
    elif k == "locked_clasp": book(A, (0, 0, 0.04), (0.24, 0.32, 0.08), "book_d", 0.0); box(A, (0.03, 0.05, 0.09), (0.12, 0.0, 0.04), "gold", bevel=0.003); box(A, (0.26, 0.02, 0.09), (0, -0.0, 0.04), "gold", bevel=0.003)
    elif k == "giant": book(A, (0, 0, 0.07), (0.4, 0.55, 0.14), "book_a", 0.0); tor(A, 0.08, 0.008, (0, 0, 0.145), "gold", seg=18); box(A, (0.02, 0.5, 0.15), (-0.2, 0, 0.07), "gold", bevel=0.002)


@family("scroll", "alchemy", ["single_roll", "scroll_stack", "scroll_open", "wax_sealed", "map_roll", "scroll_tube"], cat="alchemy", place="surface", tags=["decor"])
def _scroll(A, v):
    k = v["n"]
    if k == "single_roll": cyl(A, 0.025, 0.3, (0, 0, 0.03), "parchment", rot=(0, PI / 2, 0.2), verts=10); cyl(A, 0.012, 0.34, (0, 0, 0.03), "wood", rot=(0, PI / 2, 0.2), verts=6)
    elif k == "scroll_stack":
        for i in range(5): cyl(A, 0.025, 0.28, (0.0, -0.03 + (i % 3) * 0.05, 0.03 + (i // 3) * 0.045), "parchment", rot=(0, PI / 2, 0.1 * i), verts=8)
    elif k == "scroll_open":
        box(A, (0.34, 0.24, 0.006), (0, 0, 0.004), "parchment", bevel=0); cyl(A, 0.02, 0.26, (-0.17, 0, 0.02), "parchment", rot=(PI / 2, 0, 0), verts=8); cyl(A, 0.02, 0.26, (0.17, 0, 0.02), "parchment", rot=(PI / 2, 0, 0), verts=8)
        for i in range(5): box(A, (0.2, 0.008, 0.002), (0, -0.08 + i * 0.04, 0.008), "black", bevel=0)
    elif k == "wax_sealed": cyl(A, 0.03, 0.26, (0, 0, 0.03), "parchment", rot=(0, PI / 2, 0), verts=10); cyl(A, 0.035, 0.012, (0, -0.0, 0.03), "book_a", rot=(0, PI / 2, 0), verts=10); sph(A, 0.018, (0.0, 0.0, 0.065), "book_a", scale=(1, 1, 0.5), seg=8)
    elif k == "map_roll": cyl(A, 0.035, 0.4, (0, 0, 0.04), "parchment", rot=(0, PI / 2, 0.4), verts=12); cyl(A, 0.015, 0.44, (0, 0, 0.04), "wood", rot=(0, PI / 2, 0.4), verts=6)
    elif k == "scroll_tube": cyl(A, 0.04, 0.34, (0, 0, 0.04), "leather", rot=(0, PI / 2, 0.15), verts=12); cyl(A, 0.043, 0.02, (0.17, 0, 0.04), "gold", rot=(0, PI / 2, 0.15), verts=12)


@family("orb", "alchemy", [{"n": "crystal_ball", "meta": _glow("#b070ff", 0.7, 0.2)}, {"n": "skull_orb", "meta": _glow("#40ffe0", 0.6, 0.2)}, {"n": "soul_jar", "meta": _glow("#4dffd0", 0.7, 0.2)},
                           {"n": "rune_crystal", "meta": _glow("#9a60ff", 0.7, 0.25)}, {"n": "shard_cluster", "meta": _glow("#ff5acd", 0.6, 0.2)}, {"n": "scrying_bowl", "meta": _glow("#60c0ff", 0.6, 0.12)}],
        cat="alchemy", place="surface", tags=["decor", "light", "glow"])
def _orb(A, v):
    k = v["n"]
    if k == "crystal_ball":
        cyl(A, 0.09, 0.05, (0, 0, 0.025), "gold", r2=0.07, verts=16)
        for i in range(3): a = i * 2 * PI / 3; sph(A, 0.022, (0.07 * math.cos(a), 0.07 * math.sin(a), 0.07), "gold", seg=8)
        sph(A, 0.1, (0, 0, 0.17), "orb", seg=20)
    elif k == "skull_orb": skull(A, (0, 0, 0.0), 1.0, mat="ivory", glow="ecto"); sph(A, 0.04, (0, 0, 0.13), "ecto", seg=10)
    elif k == "soul_jar":
        lathe(A, [(0.0, 0), (0.07, 0), (0.08, 0.02), (0.08, 0.16), (0.03, 0.2), (0.0, 0.2)], (0, 0, 0), "glass_clear", verts=14); sph(A, 0.045, (0, 0, 0.1), "soulfire", seg=10); limb(A, (0, 0, 0.1), (0.02, 0, 0.17), 0.03, 0.004, "soulfire", 6); cyl(A, 0.035, 0.03, (0, 0, 0.215), "iron", verts=10)
    elif k == "rune_crystal":
        for (x, y, h, r) in [(0, 0, 0.28, 0.05), (0.06, 0.03, 0.18, 0.035), (-0.05, 0.04, 0.2, 0.04), (0.02, -0.05, 0.14, 0.03)]: cyl(A, r, h, (x, y, h / 2), "rune", r2=0.0, verts=6)
        cyl(A, 0.1, 0.03, (0, 0, 0.015), "stone_dark", verts=8)
    elif k == "shard_cluster":
        for i in range(6): a = i * 1.05; h = 0.12 + 0.05 * (i % 3); limb(A, (0.04 * math.cos(a), 0.04 * math.sin(a), 0.0), (0.09 * math.cos(a), 0.09 * math.sin(a), h), 0.025, 0.003, "potion_purple", 5)
    elif k == "scrying_bowl":
        lathe(A, [(0.0, 0.0), (0.08, 0.0), (0.13, 0.05), (0.15, 0.1), (0.13, 0.1), (0.0, 0.03)], (0, 0, 0), "silver", verts=22); cyl(A, 0.125, 0.01, (0, 0, 0.085), "soulfire", verts=22)


@family("rune_item", "alchemy", ["stone_set", "glowing_runestone", "bone_dice", "rune_plate"], cat="alchemy", place="surface", tags=["decor"])
def _rune(A, v):
    k = v["n"]
    if k == "stone_set":
        for (x, y) in [(-0.08, 0), (0.0, 0.05), (0.08, -0.02)]: sph(A, 0.035, (x, y, 0.025), "stone_dark", scale=(1, 0.8, 0.6), seg=8); box(A, (0.02, 0.004, 0.02), (x, y - 0.03, 0.03), "rune", bevel=0)
    elif k == "glowing_runestone": sph(A, 0.07, (0, 0, 0.05), "stone_dark", scale=(1, 0.7, 1.2), seg=10); box(A, (0.05, 0.005, 0.07), (0, -0.05, 0.06), "rune", bevel=0)
    elif k == "bone_dice":
        for (x, y, r) in [(-0.04, 0, 0.3), (0.04, 0.02, 0.9)]: box(A, (0.04, 0.04, 0.04), (x, y, 0.02), "bone", rot=(0, 0, r), bevel=0.004)
    elif k == "rune_plate": cyl(A, 0.12, 0.015, (0, 0, 0.008), "stone_dark", verts=6); tor(A, 0.09, 0.005, (0, 0, 0.018), "rune", seg=6, minor=4)


@family("operating_table", "alchemy", [{"n": "wood_slab", "meta": {"size": [0.8, 1.9, 0.9]}}, {"n": "stone_slab", "meta": {"size": [0.8, 1.9, 0.9]}}, {"n": "strapped", "meta": {"size": [0.8, 1.9, 0.9]}}],
        cat="alchemy", place="floor", tags=["wall-hug", "holds-decor"])
def _optable(A, v):
    k = v["n"]; m = "stone_light" if k == "stone_slab" else "wood"
    box(A, (0.8, 1.9, 0.08), (0, 0, 0.86), m, bevel=0.015)
    for sx in (-1, 1):
        for sy in (-1, 1): box(A, (0.08, 0.08, 0.82), (sx * 0.34, sy * 0.85, 0.41), "iron" if k == "strapped" else m)
    box(A, (0.7, 1.7, 0.06), (0, 0, 0.2), m)
    if k == "strapped":
        for y in (-0.5, 0.0, 0.5): box(A, (0.86, 0.08, 0.02), (0, y, 0.91), "leather", bevel=0.003); box(A, (0.04, 0.05, 0.03), (0.3, y, 0.92), "iron", bevel=0)
    if k == "stone_slab":
        box(A, (0.04, 1.4, 0.015), (0, 0, 0.91), "blood", bevel=0)


@family("cage", "alchemy", ["small_cage", "bird_cage", "prison_cage", "crow_cage"], cat="alchemy", place="floor", tags=["wall-hug", "decor"])
def _cage(A, v):
    k = v["n"]; R, H = {"small_cage": (0.3, 0.6), "bird_cage": (0.25, 0.8), "prison_cage": (0.5, 1.9), "crow_cage": (0.3, 0.7)}[k]
    z0 = 0.05 if k != "bird_cage" else 0.5
    if k == "bird_cage": limb(A, (0, 0, 0.0), (0, 0, 0.5), 0.02, 0.02, "iron"); cyl(A, 0.15, 0.03, (0, 0, 0.0), "iron", verts=14)
    cyl(A, R, 0.04, (0, 0, z0), "iron", verts=16); cyl(A, R, 0.04, (0, 0, z0 + H), "iron", verts=16)
    for a in np_range(0, 6.2, 0.5): limb(A, (R * 0.95 * math.cos(a), R * 0.95 * math.sin(a), z0), (R * 0.95 * math.cos(a), R * 0.95 * math.sin(a), z0 + H), 0.01, 0.01, "iron", 5)
    for z in (z0 + H * 0.4, z0 + H * 0.8): tor(A, R * 0.95, 0.008, (0, 0, z), "iron", seg=18)
    if k == "bird_cage": tor(A, 0.04, 0.008, (0, 0, z0 + H + 0.06), "iron", rot=(PI / 2, 0, 0)); sph(A, 0.04, (0, 0, z0 + 0.1), "black", scale=(1, 1.3, 1), seg=8)
    if k == "crow_cage": sph(A, 0.07, (0, 0, z0 + 0.1), "black", scale=(0.8, 1.3, 1), seg=8); sph(A, 0.04, (0, -0.07, z0 + 0.16), "black", seg=8)
    if k == "prison_cage":
        box(A, (0.06, 0.04, 0.2), (R, 0, z0 + 0.9), "iron", bevel=0); cyl(A, 0.5, 0.01, (0, 0, z0 + 0.4), "black", verts=18)
        skull(A, (0.1, 0.1, z0 + 0.04), 0.9)


@family("occult_tool", "alchemy", ["ritual_dagger", "athame_set", "ritual_bowl", "ritual_bell"], cat="alchemy", place="surface", tags=["decor"])
def _occult(A, v):
    k = v["n"]
    if k == "ritual_dagger": box(A, (0.025, 0.2, 0.006), (0, 0, 0.005), "silver", rot=(0, 0, 0.3), bevel=0); box(A, (0.07, 0.02, 0.012), (0.03, -0.1, 0.008), "gold", rot=(0, 0, 0.3), bevel=0); cyl(A, 0.012, 0.1, (0.05, -0.15, 0.01), "black", rot=(PI / 2, 0, 0.3), verts=6)
    elif k == "athame_set":
        for i in range(3): box(A, (0.02, 0.16 + i * 0.03, 0.005), (-0.06 + i * 0.06, 0, 0.005), "silver", rot=(0, 0, 0.1 * i), bevel=0)
        box(A, (0.24, 0.05, 0.01), (0, -0.1, 0.005), "black", bevel=0)
    elif k == "ritual_bowl": lathe(A, [(0.0, 0.0), (0.06, 0.0), (0.11, 0.06), (0.12, 0.08), (0.1, 0.08), (0.0, 0.02)], (0, 0, 0), "gold", verts=20); cyl(A, 0.095, 0.008, (0, 0, 0.06), "blood", verts=18)
    elif k == "ritual_bell": lathe(A, [(0.07, 0.0), (0.06, 0.05), (0.04, 0.1), (0.02, 0.13), (0.0, 0.14)], (0, 0, 0), "gold", verts=16); cyl(A, 0.012, 0.08, (0, 0, 0.17), "wood", verts=6); sph(A, 0.012, (0, 0, 0.0), "iron", seg=6)


_SKULLS = [("plain", {}), ("cracked", {"crack": True}), ("crowned", {"crown": True}), ("horned", {"horns": 2}), ("jawless", {"jaw": False}), ("candle_skull", {"candle": True}),
           ("gem_eyes", {"glow": "potion_red"}), ("mossy", {"mat": "moss"}), ("gilded", {"mat": "gold"}), ("small_pair", {"pair": True})]


@family("skull", "alchemy", [{"n": n, **p, **({"meta": {"tags": ["light", "glow"], "light": 0.5, "lightColor": "#ff9a3c", "lightY": 0.25}} if n == "candle_skull" else {})} for n, p in _SKULLS], cat="alchemy", place="surface", tags=["decor"])
def _skull_item(A, v):
    mat = v.get("mat", "bone")
    if v.get("pair"):
        skull(A, (-0.08, 0, 0.0), 0.8, yaw=0.3); skull(A, (0.08, 0.02, 0.0), 0.7, yaw=-0.4); return
    skull(A, (0, 0, 0.0), 1.2, mat=mat, jaw=v.get("jaw", True), horns=v.get("horns", 0), glow=v.get("glow"))
    if v.get("crack"):
        limb(A, (0.0, -0.06, 0.15), (0.03, -0.06, 0.08), 0.004, 0.003, "black", 4); limb(A, (0.02, -0.06, 0.13), (-0.02, -0.06, 0.1), 0.003, 0.002, "black", 4)
    if v.get("crown"):
        tor(A, 0.07, 0.01, (0, 0.0, 0.18), "gold", seg=16); [cyl(A, 0.008, 0.035, (0.07 * math.cos(a), 0.07 * math.sin(a), 0.205), "gold", r2=0.0, verts=4) for a in np_range(0, 6.2, 0.9)]
    if v.get("candle"):
        cyl(A, 0.022, 0.1, (0, 0.0, 0.2), "wax", verts=10); sph(A, 0.012, (0, 0, 0.32), "flame", scale=(1, 1, 1.8), seg=6)
        for i in range(3): limb(A, (0.0, 0.0, 0.2), (0.025 * math.cos(i * 2), 0.025 * math.sin(i * 2), 0.14), 0.01, 0.006, "wax", 5)


@family("bone_item", "alchemy", ["ribcage_small", "hand_bones", "spine_curl", "femur_crossed"], cat="alchemy", place="surface", tags=["decor"])
def _bone_item(A, v):
    k = v["n"]
    if k == "ribcage_small":
        for j in range(6): tor(A, 0.09 - j * 0.008, 0.009, (0, 0, 0.04 + j * 0.03), "bone", rot=(0, 0, 0), seg=12, minor=4).data.transform(Matrix.Diagonal((1, 0.7, 1, 1)))
        limb(A, (0, 0.05, 0.02), (0, 0.05, 0.24), 0.012, 0.012, "bone")
    elif k == "hand_bones":
        box(A, (0.07, 0.04, 0.02), (0, 0, 0.012), "bone", bevel=0.004)
        for i in range(5): bone(A, (-0.03 + i * 0.015, 0.02, 0.012), (-0.05 + i * 0.025, 0.1 + (0.02 if i in (1, 2, 3) else 0), 0.012), 0.007)
    elif k == "spine_curl":
        for i in range(12): a = i * 0.45; sph(A, 0.017, (0.06 * math.cos(a) * (1 - i * 0.04), 0.06 * math.sin(a) * (1 - i * 0.04), 0.02 + i * 0.004), "bone", seg=6)
    elif k == "femur_crossed":
        bone(A, (-0.14, -0.06, 0.02), (0.14, 0.06, 0.02), 0.015); bone(A, (-0.14, 0.06, 0.036), (0.14, -0.06, 0.036), 0.015)
