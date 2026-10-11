# ============ STUDY & LIBRARY (~27) ============

@family("book_stack", "study", ["tall_stack", "scattered_pair", "leaning_row", "tome_pile", "red_stack", "ledger_stack", "bone_bookends", "open_and_stack"], cat="study", place="surface", tags=["decor"])
def _bookstack(A, v):
    k = v["n"]; rng = random.Random(len(k) * 7)
    if k in ("tall_stack", "red_stack", "ledger_stack", "tome_pile"):
        z = 0.0; n = {"tall_stack": 6, "red_stack": 4, "ledger_stack": 5, "tome_pile": 7}[k]
        for i in range(n):
            h = 0.035 + rng.random() * 0.03; w = 0.2 + rng.random() * 0.1 if k != "tome_pile" else 0.28 - i * 0.015; m = "book_a" if k == "red_stack" else "book_c" if k == "ledger_stack" else random.choice(BOOKS)
            book(A, (rng.uniform(-0.012, 0.012), rng.uniform(-0.01, 0.01), z + h / 2), (w, w * 1.3, h), m, rng.uniform(-0.2, 0.2)); z += h
        if k == "tall_stack": candle(A, (0.0, 0.0, z), h=0.08, r=0.015, flame=False)
    elif k == "scattered_pair": book(A, (-0.1, 0, 0.02), (0.2, 0.28, 0.04), "book_b", 0.3); book(A, (0.12, 0.03, 0.02), (0.18, 0.26, 0.04), "book_d", -0.5); book(A, (0.12, 0.03, 0.06), (0.15, 0.22, 0.03), "book_a", 0.2)
    elif k == "leaning_row":
        for i in range(5): h = 0.2 + rng.random() * 0.06; box(A, (0.035, 0.18, h), (-0.1 + i * 0.04, 0, h / 2 + 0.01), random.choice(BOOKS), rot=(0, 0.12 if i == 4 else 0, 0), bevel=0.003)
    elif k == "bone_bookends":
        for s in (-1, 1): box(A, (0.02, 0.1, 0.12), (s * 0.13, 0, 0.06), "bone", bevel=0.004); skull(A, (s * 0.13, 0, 0.12), 0.35, yaw=PI / 2 * -s)
        for i in range(6): h = 0.18 + rng.random() * 0.05; box(A, (0.035, 0.16, h), (-0.1 + i * 0.04, 0, h / 2), random.choice(BOOKS), bevel=0.003)
    elif k == "open_and_stack":
        box(A, (0.38, 0.26, 0.03), (-0.1, 0, 0.015), "book_a", bevel=0.004); [box(A, (0.17, 0.24, 0.02), (-0.1 + s * 0.09, 0, 0.04), "parchment", rot=(0, s * -0.1, 0), bevel=0) for s in (-1, 1)]
        [book(A, (0.2, 0.0, 0.03 + i * 0.05), (0.2, 0.26, 0.05), random.choice(BOOKS), 0.1 * i) for i in range(3)]


@family("globe", "study", ["astral", "world", "star_map", "skull"], cat="study", place="surface", tags=["decor"])
def _globe(A, v):
    k = v["n"]
    cyl(A, 0.1, 0.03, (0, 0, 0.015), "wood_red", r2=0.08, verts=16); cyl(A, 0.012, 0.12, (0, 0, 0.09), "gold", verts=8)
    sph(A, 0.12, (0, 0, 0.27), {"astral": "cloth2", "world": "wood_pale", "star_map": "black", "skull": "bone"}[k], seg=20)
    tor(A, 0.15, 0.008, (0, 0, 0.27), "gold", rot=(0.4, 0, 0), seg=28); tor(A, 0.13, 0.006, (0, 0, 0.27), "gold", rot=(PI / 2, 0, 0.3), seg=24)
    if k == "astral": [sph(A, 0.01, (0.13 * math.cos(a) * math.cos(b), 0.13 * math.sin(a) * math.cos(b), 0.27 + 0.13 * math.sin(b)), "rune", seg=5) for a, b in [(0.3, 0.5), (1.2, -0.4), (2.5, 0.2), (3.8, 0.7), (5.0, -0.2)]]
    if k == "skull": [sph(A, 0.03, (0.1 * s, -0.07, 0.3), "black", seg=8) for s in (-1, 1)]


@family("science", "study", ["orrery", "astrolabe", "armillary", "sundial"], cat="study", place="surface", tags=["decor"])
def _sci(A, v):
    k = v["n"]
    if k == "orrery":
        cyl(A, 0.15, 0.03, (0, 0, 0.015), "wood_red", r2=0.12, verts=18); cyl(A, 0.012, 0.28, (0, 0, 0.17), "gold", verts=8); sph(A, 0.045, (0, 0, 0.18), "flame", seg=10)
        for i, (r, z, c) in enumerate([(0.1, 0.18, "potion_blue"), (0.16, 0.2, "potion_red"), (0.22, 0.17, "potion_amber")]): tor(A, r, 0.003, (0, 0, z), "gold", seg=30, minor=4); a = i * 2; sph(A, 0.022 + 0.004 * i, (r * math.cos(a), r * math.sin(a), z), c, seg=8)
    elif k == "astrolabe":
        cyl(A, 0.14, 0.012, (0, 0, 0.14), "gold", rot=(PI / 2.3, 0, 0), verts=32); tor(A, 0.13, 0.008, (0, 0, 0.14), "gold", rot=(PI / 2.3, 0, 0), seg=32); box(A, (0.26, 0.01, 0.015), (0, 0, 0.14), "gold", rot=(PI / 2.3, 0, 0.5), bevel=0); cyl(A, 0.08, 0.1, (0, 0.04, 0.05), "gold", r2=0.05, verts=12)
    elif k == "armillary":
        cyl(A, 0.1, 0.03, (0, 0, 0.015), "gold", r2=0.08, verts=14); cyl(A, 0.012, 0.1, (0, 0, 0.08), "gold", verts=8)
        for rot in [(0, 0, 0), (PI / 2, 0, 0), (0, PI / 2, 0), (0.6, 0.6, 0)]: tor(A, 0.13, 0.006, (0, 0, 0.26), "gold", rot=rot, seg=30, minor=4)
        sph(A, 0.03, (0, 0, 0.26), "orb", seg=10)
    elif k == "sundial": cyl(A, 0.13, 0.02, (0, 0, 0.01), "stone_light", verts=24); prism(A, [(0, 0), (0.1, 0), (0, 0.1)], 0.01, (0, 0, 0.02), "gold", rot=(PI / 2, 0, 0), bevel=0)


@family("telescope", "study", ["brass_tripod", "star_gazer"], cat="study", place="floor", tags=["decor"])
def _telescope(A, v):
    for i in range(3): a = i * 2 * PI / 3 + 0.3; limb(A, (0.4 * math.cos(a), 0.4 * math.sin(a), 0.0), (0.0, 0.0, 1.1), 0.022, 0.016, "wood")
    cyl(A, 0.05, 1.2 if v["n"] == "brass_tripod" else 1.5, (0, -0.3, 1.45), "gold", r2=0.04, rot=(1.0, 0, 0), verts=14); tor(A, 0.07, 0.01, (0, -0.65, 1.7), "gold", rot=(1.0, 0, 0), seg=16); tor(A, 0.05, 0.01, (0, 0.0, 1.2), "gold", seg=14)
    if v["n"] == "star_gazer": sph(A, 0.04, (0, 0, 1.12), "orb", seg=10)


@family("hourglass", "study", ["sand_small", "bone_frame_big"], cat="study", place="surface", tags=["decor"])
def _hourglass(A, v):
    big = v["n"] != "sand_small"; s = 1.3 if big else 1.0; fr = "bone" if big else "wood_red"
    for z in (0.0, 0.3 * s): cyl(A, 0.07 * s, 0.025, (0, 0, z + 0.0125), fr, verts=14)
    for a in np_range(0, 6.2, PI / 2): cyl(A, 0.008, 0.3 * s, (0.06 * s * math.cos(a), 0.06 * s * math.sin(a), 0.15 * s), fr, verts=6)
    lathe(A, [(0.0, 0.03 * s), (0.05 * s, 0.05 * s), (0.012, 0.15 * s), (0.05 * s, 0.25 * s), (0.0, 0.27 * s)], (0, 0, 0), "glass_clear", verts=14); cyl(A, 0.008, 0.06 * s, (0, 0, 0.1 * s), "potion_amber", verts=6); cone = sph(A, 0.035 * s, (0, 0, 0.055 * s), "potion_amber", scale=(1, 1, 0.5), seg=8)


@family("writing_set", "study", ["inkwell_quill", "quill_stand", "seal_press"], cat="study", place="surface", tags=["decor"])
def _writing(A, v):
    k = v["n"]
    if k == "inkwell_quill": lathe(A, [(0.0, 0), (0.04, 0.0), (0.045, 0.05), (0.025, 0.07), (0.0, 0.07)], (0, 0, 0), "glass_clear", verts=12); cyl(A, 0.03, 0.01, (0, 0, 0.05), "black", verts=10); limb(A, (0.01, 0, 0.06), (0.08, 0.0, 0.2), 0.004, 0.002, "ivory", 5); prism(A, [(0, 0), (0.03, 0.06), (0.0, 0.12), (-0.01, 0.05)], 0.002, (0.06, 0, 0.12), "ivory", rot=(PI / 2, 0, 0.4), bevel=0)
    elif k == "quill_stand":
        cyl(A, 0.05, 0.02, (0, 0, 0.01), "gold", verts=12); cyl(A, 0.03, 0.08, (0, 0, 0.06), "gold", r2=0.04, verts=12); [limb(A, (0, 0, 0.1), (0.05 * math.cos(a), 0.05 * math.sin(a), 0.28), 0.003, 0.002, c, 5) for a, c in [(0, "ivory"), (2.1, "black"), (4.2, "ivory")]]
    elif k == "seal_press": cyl(A, 0.05, 0.02, (0, 0, 0.01), "iron", verts=12); cyl(A, 0.012, 0.1, (0, 0, 0.07), "iron", verts=8); sph(A, 0.03, (0, 0, 0.13), "wood", seg=8); cyl(A, 0.035, 0.01, (0.1, 0, 0.005), "book_a", verts=12)


@family("study_furniture", "study", [{"n": "map_table", "meta": {"size": [1.6, 1.0, 0.9]}}, {"n": "scroll_rack_a"}, {"n": "scroll_rack_b"}, {"n": "library_ladder"}],
        cat="study", place="floor", tags=["wall-hug"])
def _studyf(A, v):
    k = v["n"]
    if k == "map_table":
        box(A, (1.6, 1.0, 0.07), (0, 0, 0.865), "wood", bevel=0.012); box(A, (1.5, 0.9, 0.01), (0, 0, 0.905), "parchment", bevel=0)
        for sx in (-1, 1):
            for sy in (-1, 1): box(A, (0.1, 0.1, 0.83), (sx * 0.7, sy * 0.4, 0.415), "wood")
        for (x, y) in [(-0.5, 0.2), (0.4, -0.2)]: cyl(A, 0.02, 0.05, (x, y, 0.93), "bone", verts=8)
        limb(A, (-0.2, -0.1, 0.915), (0.3, 0.2, 0.915), 0.004, 0.004, "blood", 4)
    elif k.startswith("scroll_rack"):
        box(A, (0.9, 0.3, 0.06), (0, 0, 0.03), "wood"); box(A, (0.9, 0.3, 0.06), (0, 0, 1.2), "wood")
        for sx in (-1, 1): box(A, (0.05, 0.3, 1.2), (sx * 0.43, 0, 0.6), "wood")
        for r in range(3 if k.endswith("a") else 4):
            for c in range(6): cyl(A, 0.03, 0.26, (-0.35 + c * 0.14, 0, 0.15 + r * 0.26), "parchment", rot=(PI / 2, 0, 0), verts=8)
    elif k == "library_ladder":
        for sx in (-1, 1): box(A, (0.05, 0.05, 2.2), (sx * 0.22, 0.0, 1.1), "wood", rot=(0.1, 0, 0), bevel=0.005)
        for i in range(8): box(A, (0.44, 0.06, 0.03), (0, 0.0 - i * 0.02 + 0.18, 0.2 + i * 0.25), "wood", bevel=0.003)
        for sx in (-1, 1): cyl(A, 0.04, 0.03, (sx * 0.22, -0.2, 0.02), "iron", rot=(0, PI / 2, 0), verts=10); box(A, (0.04, 0.06, 0.08), (sx * 0.22, 0.18, 2.2), "iron", bevel=0)
