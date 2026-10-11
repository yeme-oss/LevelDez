# ============ NECROMANCER ACADEMY (~35) ============

@family("student_desk", "academy", [{"n": "slanted", "meta": {"size": [1.0, 0.6, 0.78]}}, {"n": "bone_leg", "meta": {"size": [1.0, 0.6, 0.78]}}, {"n": "inkwell", "meta": {"size": [1.0, 0.6, 0.78]}}, {"n": "skull_desk", "meta": {"size": [1.0, 0.6, 0.78]}}],
        cat="academy", place="floor", tags=["table", "holds-decor", "desk"])
def _sdesk(A, v):
    k = v["n"]
    box(A, (1.0, 0.6, 0.05), (0, 0, 0.74), "wood_pale" if k != "skull_desk" else "wood", bevel=0.008)
    if k == "slanted": box(A, (1.0, 0.35, 0.03), (0, 0.1, 0.8), "wood_pale", rot=(-0.25, 0, 0), bevel=0.005); box(A, (1.0, 0.04, 0.05), (0, -0.2, 0.78), "wood_pale")
    for sx in (-1, 1):
        for sy in (-1, 1):
            if k == "bone_leg": bone(A, (sx * 0.44, sy * 0.24, 0.0), (sx * 0.44, sy * 0.24, 0.72), 0.022)
            else: box(A, (0.05, 0.05, 0.72), (sx * 0.44, sy * 0.24, 0.36), "wood")
    box(A, (0.9, 0.05, 0.04), (0, 0.24, 0.3), "wood")
    if k == "inkwell": [lathe(A, [(0.0, 0.0), (0.03, 0.0), (0.035, 0.04), (0.02, 0.06), (0.0, 0.06)], (x, 0.12, 0.765), "glass_clear", verts=10) for x in (-0.4, 0.4)]; box(A, (0.25, 0.18, 0.01), (0.0, -0.05, 0.77), "parchment", bevel=0)
    if k == "skull_desk": skull(A, (-0.35, 0.1, 0.765), 0.8); book(A, (0.15, 0, 0.8), (0.25, 0.18, 0.04), "book_a", 0.2)


@family("podium", "academy", ["lecture_bone", "lecture_stone", "teacher_lectern"], cat="academy", place="floor", tags=["wall-hug", "focal"])
def _podium(A, v):
    k = v["n"]
    if k == "lecture_stone": box(A, (0.8, 0.6, 1.1), (0, 0, 0.55), "stone", bevel=0.02); box(A, (0.9, 0.7, 0.08), (0, 0, 1.12), "stone_light", bevel=0.02); box(A, (0.7, 0.4, 0.04), (0, -0.02, 1.2), "wood_red", rot=(-0.35, 0, 0)); prism(A, arch_pts(0.5, 0.35, 0.7), 0.04, (0, -0.31, 0.2), "stone_dark")
    elif k == "lecture_bone":
        for s in (-1, 1): bone(A, (s * 0.35, 0.2, 0.0), (s * 0.3, 0.1, 1.15), 0.035); bone(A, (s * 0.35, -0.2, 0.0), (s * 0.3, -0.1, 1.15), 0.035)
        box(A, (0.8, 0.5, 0.06), (0, 0, 1.15), "wood", bevel=0.01); box(A, (0.74, 0.34, 0.04), (0, 0, 1.24), "wood_red", rot=(-0.35, 0, 0)); skull(A, (0, -0.28, 0.9), 1.4)
    else: lathe(A, [(0.25, 0), (0.15, 0.05), (0.1, 1.0), (0.2, 1.1)], (0, 0, 0), "wood_red", verts=12); box(A, (0.6, 0.45, 0.04), (0, -0.02, 1.2), "wood", rot=(-0.4, 0, 0)); book(A, (0, 0.0, 1.24), (0.3, 0.22, 0.04), "book_a", 0.0)


@family("blackboard", "academy", ["rune_slate", "anatomy_slate", "spell_diagram"], cat="wall decor", place="wall", y=0.9, tags=["decor"])
def _board(A, v):
    k = v["n"]
    box(A, (1.7, 0.05, 1.0), (0, 0, 0.5), "wood", bevel=0.01); box(A, (1.6, 0.03, 0.9), (0, -0.02, 0.5), "stone_dark", bevel=0); box(A, (1.7, 0.08, 0.03), (0, -0.03, 0.0), "wood"); [box(A, (0.1, 0.02, 0.02), (-0.5 + 0.2 * i, -0.05, 0.03), "ivory", bevel=0) for i in range(3)]
    if k == "rune_slate": [box(A, (0.12, 0.004, 0.14), (-0.6 + 0.24 * i, -0.04, 0.6 - 0.15 * (i % 2)), "ivory", bevel=0) for i in range(6)]
    elif k == "anatomy_slate": skull(A, (-0.3, -0.04, 0.4), 2.0, mat="ivory"); [limb(A, (0.3 + 0.12 * i, -0.04, 0.8), (0.3 + 0.12 * i, -0.04, 0.3), 0.004, 0.004, "ivory", 4) for i in range(4)]; tor(A, 0.14, 0.004, (0.55, -0.04, 0.55), "ivory", rot=(PI / 2, 0, 0), seg=16)
    elif k == "spell_diagram": tor(A, 0.3, 0.005, (0, -0.04, 0.5), "ivory", rot=(PI / 2, 0, 0), seg=30); [box(A, (0.58, 0.004, 0.006), (0, -0.04, 0.5), "ivory", rot=(0, a, 0), bevel=0) for a in (0, PI / 3, 2 * PI / 3)]; tor(A, 0.18, 0.005, (0, -0.04, 0.5), "ivory", rot=(PI / 2, 0, 0), seg=24)


@family("trophy_case", "academy", ["skull_trophies", "relic_case", "grimoire_case"], cat="academy", place="floor", tags=["wall-hug", "holds-decor", "tall"])
def _trophy(A, v):
    k = v["n"]
    box(A, (1.0, 0.45, 1.8), (0, 0, 0.9), "wood", bevel=0.012); box(A, (1.06, 0.5, 0.06), (0, 0, 1.83), "wood_red", bevel=0.01); box(A, (0.9, 0.01, 1.6), (0, -0.23, 0.95), "glass_clear", bevel=0)
    for z in (0.5, 0.95, 1.4):
        box(A, (0.9, 0.35, 0.02), (0, 0, z), "wood", bevel=0)
        if k == "skull_trophies": [skull(A, (x, 0, z + 0.01), 0.75, mat="gold" if x == 0 and z == 1.4 else "bone") for x in (-0.3, 0.0, 0.3)]
        elif k == "relic_case": sph(A, 0.07, (-0.25, 0, z + 0.08), "orb", seg=10); cyl(A, 0.03, 0.18, (0.0, 0, z + 0.1), "gold", r2=0.045, verts=10); box(A, (0.14, 0.1, 0.1), (0.28, 0, z + 0.06), "gold", bevel=0.01)
        elif k == "grimoire_case": [book(A, (-0.25 + 0.25 * i, 0.0, z + 0.04), (0.2, 0.26, 0.06), random.choice(BOOKS), 0.2 * i) for i in range(3)]


@family("mannequin", "academy", ["robe_red", "robe_black", "robe_purple", "armor_stand"], cat="academy", place="floor", tags=["wall-hug", "decor"])
def _mannequin(A, v):
    k = v["n"]
    cyl(A, 0.25, 0.04, (0, 0, 0.02), "wood", r2=0.2, verts=16); cyl(A, 0.025, 1.2, (0, 0, 0.64), "wood", verts=8)
    if k == "armor_stand":
        box(A, (0.4, 0.22, 0.5), (0, 0, 1.1), "iron", bevel=0.04); box(A, (0.22, 0.24, 0.24), (0, 0, 1.52), "iron", bevel=0.04); box(A, (0.14, 0.02, 0.03), (0, -0.12, 1.54), "black", bevel=0); [limb(A, (s * 0.22, 0, 1.3), (s * 0.3, -0.05, 0.9), 0.05, 0.04, "iron") for s in (-1, 1)]; cyl(A, 0.2, 0.3, (0, 0, 0.7), "iron", r2=0.15, verts=14)
    else:
        col = {"robe_red": "cloth", "robe_black": "black", "robe_purple": "cloth2"}[k]
        lathe(A, [(0.3, 0.1), (0.25, 0.5), (0.18, 1.0), (0.2, 1.3), (0.12, 1.4)], (0, 0, 0), col, verts=18); sph(A, 0.09, (0, 0, 1.55), "wood_pale", seg=10); [limb(A, (s * 0.2, 0, 1.3), (s * 0.35, -0.1, 0.85), 0.07, 0.05, col, 8) for s in (-1, 1)]
        cyl(A, 0.2, 0.18, (0, 0, 1.4), col, r2=0.3, verts=14); tor(A, 0.2, 0.012, (0, 0, 1.02), "gold", seg=16)


@family("rack", "academy", ["staff_stand", "scythe_rack", "broom_rack"], cat="academy", place="floor", tags=["wall-hug", "decor"])
def _rack(A, v):
    k = v["n"]
    if k == "staff_stand":
        box(A, (0.9, 0.3, 0.06), (0, 0, 0.03), "wood"); box(A, (0.9, 0.06, 0.06), (0, 0.1, 1.0), "wood")
        for i, x in enumerate(np_range(-0.34, 0.34, 0.17)): limb(A, (x, 0.0, 0.04), (x, 0.08, 1.6 + 0.1 * (i % 2)), 0.016, 0.016, "wood", 8); sph(A, 0.04, (x, 0.08, 1.64 + 0.1 * (i % 2)), ["orb", "rune", "ecto", "flame", "bone"][i % 5], seg=8)
    elif k == "wand_wall": pass
    elif k == "scythe_rack":
        box(A, (1.0, 0.3, 0.06), (0, 0, 0.03), "wood"); box(A, (1.0, 0.06, 0.06), (0, 0.1, 1.2), "wood")
        for x in (-0.3, 0.0, 0.3): limb(A, (x, 0.0, 0.04), (x, 0.08, 2.0), 0.018, 0.018, "wood", 8); prism(A, [(0, 0), (-0.4, 0.04), (-0.55, -0.1), (-0.12, -0.03)], 0.015, (x, 0.08, 1.98), "silver", bevel=0.002)
    elif k == "broom_rack":
        box(A, (0.8, 0.3, 0.06), (0, 0, 0.03), "wood"); box(A, (0.8, 0.06, 0.06), (0, 0.1, 1.0), "wood")
        for x in (-0.25, 0.0, 0.25): limb(A, (x, 0.0, 0.04), (x, 0.1, 1.5), 0.014, 0.014, "wood", 8); cyl(A, 0.06, 0.3, (x, 0.0, 0.2), "wood_pale", r2=0.0, verts=8, rot=(PI, 0, 0)) if False else cyl(A, 0.0, 0.3, (x, 0.0, 0.2), "wood_pale", r2=0.07, verts=8)


@family("wand_rack", "academy", ["wall_wands", "wall_daggers"], cat="wall decor", place="wall", y=1.4, tags=["decor"])
def _wandwall(A, v):
    box(A, (0.7, 0.04, 0.5), (0, 0, 0.25), "wood_red", bevel=0.008)
    for i in range(6):
        x = -0.28 + i * 0.112
        if v["n"] == "wall_wands": limb(A, (x, -0.04, 0.08), (x + 0.02, -0.04, 0.42), 0.012, 0.006, ["wood", "bone", "iron"][i % 3], 6); sph(A, 0.012, (x + 0.02, -0.04, 0.43), ["rune", "ecto", "orb"][i % 3], seg=6)
        else: box(A, (0.025, 0.012, 0.3), (x, -0.045, 0.25), "silver", bevel=0); box(A, (0.06, 0.016, 0.02), (x, -0.045, 0.1), "gold", bevel=0); box(A, (0.016, 0.016, 0.08), (x, -0.045, 0.05), "leather", bevel=0)


@family("hat_stand", "academy", ["pointed_hats", "cloak_tree"], cat="academy", place="floor", tags=["wall-hug", "decor"])
def _hatstand(A, v):
    cyl(A, 0.22, 0.04, (0, 0, 0.02), "wood", r2=0.16, verts=14); cyl(A, 0.025, 1.6, (0, 0, 0.84), "wood", verts=8)
    for i in range(4): a = i * PI / 2; limb(A, (0, 0, 1.45 - 0.1 * (i % 2)), (0.2 * math.cos(a), 0.2 * math.sin(a), 1.6 - 0.1 * (i % 2)), 0.012, 0.01, "wood", 6)
    if v["n"] == "pointed_hats":
        for i in range(3): a = i * 2 + 0.5; cyl(A, 0.13, 0.04, (0.2 * math.cos(a), 0.2 * math.sin(a), 1.62), "black", verts=14); cyl(A, 0.08, 0.28, (0.2 * math.cos(a), 0.2 * math.sin(a), 1.78), "black", r2=0.0, verts=12)
    else:
        for i in range(2): a = i * PI; prism(A, [(0, 0), (0.28, 0.0), (0.2, -0.7), (-0.2, -0.7), (-0.28, 0)], 0.04, (0.2 * math.cos(a) * 0.9, 0.2 * math.sin(a) * 0.9, 1.5), "black" if i else "cloth", rot=(PI / 2, 0, a), bevel=0.004)


@family("academy_misc", "academy", ["student_trunk", "bone_locker", "notice_board", "dormitory_bell", "summoning_stand", "ritual_circle_stand"], cat="academy", place="floor", tags=["wall-hug", "decor"])
def _acm(A, v):
    k = v["n"]
    if k == "student_trunk":
        box(A, (0.8, 0.45, 0.4), (0, 0, 0.2), "leather", bevel=0.02); cyl(A, 0.22, 0.8, (0, 0, 0.4), "leather", rot=(0, PI / 2, 0), verts=16); [box(A, (0.05, 0.47, 0.55), (x, 0, 0.27), "iron", bevel=0.004) for x in (-0.25, 0.25)]; box(A, (0.08, 0.02, 0.09), (0, -0.23, 0.33), "gold", bevel=0)
        cyl(A, 0.014, 0.2, (0.3, 0.0, 0.62), "iron", rot=(0, PI / 2, 0), verts=6) if False else None
    elif k == "bone_locker":
        box(A, (0.5, 0.45, 1.8), (0, 0, 0.9), "stone_dark", bevel=0.015); box(A, (0.44, 0.02, 1.7), (0, -0.23, 0.9), "iron", bevel=0.004); [box(A, (0.3, 0.012, 0.03), (0, -0.245, 1.4 + i * 0.1), "stone", bevel=0) for i in range(3)]; skull(A, (0, -0.23, 1.0), 0.9); tor(A, 0.03, 0.007, (0.15, -0.25, 0.9), "iron", rot=(PI / 2, 0, 0))
    elif k == "notice_board":
        box(A, (1.0, 0.04, 0.7), (0, 0, 0.35), "wood", bevel=0.008)
        for (x, z, r) in [(-0.3, 0.45, 0.1), (0.0, 0.4, -0.08), (0.3, 0.45, 0.05), (-0.1, 0.18, 0.15), (0.25, 0.2, -0.1)]: box(A, (0.2, 0.01, 0.26), (x, -0.025, z), "parchment", rot=(0, r, 0), bevel=0); sph(A, 0.012, (x, -0.035, z + 0.1), "blood", seg=6)
    elif k == "dormitory_bell":
        box(A, (0.5, 0.05, 0.05), (0, 0, 1.55), "wood"); [box(A, (0.05, 0.05, 1.5), (s * 0.24, 0, 0.75), "wood") for s in (-1, 1)]; lathe(A, [(0.14, 1.2), (0.12, 1.3), (0.08, 1.4), (0.03, 1.48)], (0, 0, 0), "gold", verts=16); cyl(A, 0.012, 0.15, (0, 0, 1.52), "iron", verts=6); sph(A, 0.02, (0, 0, 1.18), "iron", seg=6); box(A, (0.6, 0.4, 0.08), (0, 0, 0.04), "stone")
    elif k == "summoning_stand":
        cyl(A, 0.4, 0.06, (0, 0, 0.03), "stone_dark", verts=24); tor(A, 0.33, 0.012, (0, 0, 0.07), "rune", seg=36); [(cyl(A, 0.04, 0.5, (0.33 * math.cos(a), 0.33 * math.sin(a), 0.31), "stone_light", verts=6), sph(A, 0.045, (0.33 * math.cos(a), 0.33 * math.sin(a), 0.6), "rune", seg=8)) for a in np_range(0, 6.2, 1.2566)]
    elif k == "ritual_circle_stand":
        cyl(A, 0.45, 0.05, (0, 0, 0.025), "stone_dark", verts=24); tor(A, 0.4, 0.01, (0, 0, 0.055), "gold", seg=36); tor(A, 0.25, 0.008, (0, 0, 0.055), "gold", seg=30); [candle(A, (0.42 * math.cos(a), 0.42 * math.sin(a), 0.05), h=0.2) for a in np_range(0, 6.2, 1.57)]
