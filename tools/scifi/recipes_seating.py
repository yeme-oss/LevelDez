# ============ SEATING: sofa, armchair, dining_chair, office_chair, bench, ottoman ============

@family("sofa", "furniture", [{"n": "modular", "glow": "cyan"}, {"n": "curved", "glow": "magenta"}, {"n": "lounge_low", "glow": "amber"}, {"n": "pod_pair", "glow": "green"}, {"n": "tufted_chrome", "glow": "violet"}, {"n": "bench_sofa", "glow": "blue"}],
        cat="seating", place="floor", tags=["seating", "faces-center"], **{"as": "sofa"})
def _sofa(A, v):
    k, g = v["n"], v["glow"]
    W, D = 2.1, 0.95
    if k == "modular":
        bx(A, W, D, 0.14, 0, 0, 0.1, "hull_dark", 0.02); legs4(A, W, D, 0.1, 0.05, "gunmetal")
        for sx in (-1, 0, 1): pad(A, W / 3 - 0.03, D - 0.25, 0.2, sx * W / 3, -0.1, 0.24, "cloth", 0.05)
        for sx in (-1, 0, 1): pad(A, W / 3 - 0.03, 0.22, 0.4, sx * W / 3, D / 2 - 0.13, 0.4, "cloth", 0.05)
        for sx in (-1, 1): pad(A, 0.12, D, 0.35, sx * (W / 2 - 0.06), 0, 0.24, "hull", 0.03)
        strip(A, W - 0.1, 0.02, 0.02, 0, -D / 2 + 0.02, 0.12, GLOWS[g])
    elif k == "curved":
        arc = []
        for i in range(9):
            a = math.radians(-70 + 140 * i / 8); arc.append((math.sin(a) * 1.05, math.cos(a) * 0.5 - 0.1))
        for i in range(8):
            (x0, y0), (x1, y1) = arc[i], arc[i + 1]
            ang = math.atan2(y1 - y0, x1 - x0)
            box(A, (math.hypot(x1 - x0, y1 - y0) + 0.02, 0.5, 0.22), ((x0 + x1) / 2, (y0 + y1) / 2 - 0.05, 0.25), "cloth", (0, 0, ang), 0.05)
            box(A, (math.hypot(x1 - x0, y1 - y0) + 0.02, 0.16, 0.42), ((x0 + x1) / 2, (y0 + y1) / 2 + 0.3, 0.45), "cloth", (0, 0, ang), 0.05)
        bx(A, 2.0, 0.7, 0.1, 0, 0.0, 0.0, "hull_dark", 0.04); strip(A, 1.7, 0.02, 0.02, 0, -0.48, 0.06, GLOWS[g])
    elif k == "lounge_low":
        bx(A, W, D, 0.22, 0, 0, 0.05, "hull", 0.05); pad(A, W - 0.2, D - 0.3, 0.14, 0, -0.1, 0.27, "cloth", 0.05)
        pad(A, W - 0.1, 0.25, 0.28, 0, D / 2 - 0.15, 0.27, "cloth", 0.06); strip(A, W - 0.1, 0.02, 0.02, 0, -D / 2 + 0.01, 0.06, GLOWS[g])
        for sx in (-1, 1): bx(A, 0.08, D, 0.05, sx * (W / 2 - 0.04), 0, 0.0, "gunmetal")
    elif k == "pod_pair":
        for sx in (-1, 1):
            cx = sx * 0.52
            bx(A, 0.9, 0.85, 0.12, cx, 0, 0.12, "hull_dark", 0.03); pad(A, 0.8, 0.6, 0.18, cx, -0.08, 0.24, "cloth", 0.06)
            prism(A, [(-0.45, 0), (0.45, 0), (0.4, 0.55), (0, 0.72), (-0.4, 0.55)], 0.14, (cx, 0.32, 0.24), "hull", bevel=0.03)
            strip(A, 0.5, 0.02, 0.02, cx, 0.245, 0.7, GLOWS[g]); cy(A, 0.18, 0.12, cx, 0, 0.0, "gunmetal", r2=0.12)
        bx(A, 0.12, 0.6, 0.45, 0, 0.0, 0.0, "hull_grey", 0.03)
    elif k == "tufted_chrome":
        bx(A, W, D, 0.3, 0, 0, 0.08, "chrome", 0.04); legs4(A, W, D, 0.08, 0.05, "chrome")
        pad(A, W - 0.1, D - 0.3, 0.17, 0, -0.1, 0.38, "cloth2", 0.05); pad(A, W - 0.1, 0.22, 0.5, 0, D / 2 - 0.12, 0.38, "cloth2", 0.05)
        for i in range(6): sph(A, 0.022, (-0.85 + i * 0.34, D / 2 - 0.255, 0.62), "chrome", seg=8)
    else:  # bench_sofa
        bx(A, W, D - 0.3, 0.12, 0, 0.0, 0.2, "steel", 0.02); legs4(A, W, D - 0.3, 0.2, 0.06, "gunmetal")
        pad(A, W - 0.1, D - 0.4, 0.12, 0, 0, 0.32, "cloth", 0.04); bx(A, W, 0.1, 0.5, 0, D / 2 - 0.2, 0.32, "hull_grey", 0.02); pad(A, W - 0.2, 0.08, 0.35, 0, D / 2 - 0.27, 0.38, "cloth", 0.03)
        strip(A, W - 0.1, 0.012, 0.014, 0, -D / 2 + 0.16, 0.22, GLOWS[g])


@family("armchair", "furniture", [{"n": "egg", "glow": "cyan"}, {"n": "recliner", "glow": "amber"}, {"n": "cube", "glow": "magenta"}, {"n": "swivel_pod", "glow": "green"}, {"n": "gaming", "glow": "red"}, {"n": "lounger", "glow": "violet"}],
        cat="seating", place="floor", tags=["seating", "faces-center"], **{"as": "armchair"})
def _arm(A, v):
    k, g = v["n"], v["glow"]
    if k == "egg":
        cy(A, 0.28, 0.06, 0, 0, 0.0, "gunmetal", verts=24); cy(A, 0.06, 0.2, 0, 0, 0.06, "chrome")
        sph(A, 0.42, (0, 0.04, 0.55), "hull", scale=(1, 1, 1.0), seg=24); sph(A, 0.32, (0, -0.1, 0.5), "cloth", scale=(1, 1, 0.9), seg=20)
        pad(A, 0.5, 0.5, 0.1, 0, -0.12, 0.28, "cloth", 0.04); tor(A, 0.4, 0.012, (0, -0.2, 0.55), GLOWS[g], rot=(PI / 2, 0, 0), seg=32, minor=6)
    elif k == "recliner":
        bx(A, 0.85, 0.85, 0.2, 0, 0, 0.1, "hull_dark", 0.04); pad(A, 0.7, 0.55, 0.2, 0, -0.1, 0.3, "cloth", 0.06)
        prism(A, [(-0.38, 0), (0.38, 0), (0.34, 0.7), (-0.34, 0.7)], 0.16, (0, 0.34, 0.3), "cloth", rot=(0, 0, 0), bevel=0.04)
        for sx in (-1, 1): bx(A, 0.1, 0.7, 0.3, sx * 0.38, -0.02, 0.3, "hull", 0.03)
        pad(A, 0.5, 0.3, 0.1, 0, -0.45, 0.17, "cloth", 0.04); strip(A, 0.7, 0.02, 0.02, 0, -0.43, 0.12, GLOWS[g])
    elif k == "cube":
        bx(A, 0.85, 0.85, 0.12, 0, 0, 0.1, "gunmetal", 0.02); pad(A, 0.85, 0.85, 0.28, 0, 0, 0.22, "cloth", 0.07); pad(A, 0.85, 0.2, 0.45, 0, 0.32, 0.5, "cloth", 0.07)
        for sx in (-1, 1): pad(A, 0.14, 0.7, 0.2, sx * 0.36, -0.05, 0.5, "cloth", 0.05)
        strip(A, 0.8, 0.02, 0.02, 0, -0.43, 0.14, GLOWS[g])
    elif k == "swivel_pod":
        cy(A, 0.3, 0.05, 0, 0, 0.0, "gunmetal", verts=24); cy(A, 0.05, 0.3, 0, 0, 0.05, "steel")
        prism(A, [(-0.42, 0), (0.42, 0), (0.42, 0.28), (0.34, 0.9), (-0.34, 0.9), (-0.42, 0.28)], 0.8, (0, 0, 0.35), "hull", rot=(0, 0, 0), bevel=0.05)
        pad(A, 0.7, 0.6, 0.14, 0, -0.07, 0.34, "cloth", 0.05); pad(A, 0.62, 0.12, 0.5, 0, 0.3, 0.5, "cloth", 0.05)
        tor(A, 0.38, 0.012, (0, 0, 0.35), GLOWS[g], seg=32, minor=6)
    elif k == "gaming":
        cy(A, 0.3, 0.05, 0, 0, 0.0, "gunmetal", verts=5); cy(A, 0.04, 0.25, 0, 0, 0.05, "chrome")
        pad(A, 0.55, 0.5, 0.12, 0, -0.05, 0.3, "pad", 0.05); prism(A, [(-0.27, 0), (0.27, 0), (0.22, 0.75), (-0.22, 0.75)], 0.12, (0, 0.28, 0.35), "pad", bevel=0.04)
        pad(A, 0.5, 0.15, 0.2, 0, 0.3, 1.0, "pad", 0.05); strip(A, 0.03, 0.02, 0.7, -0.2, 0.215, 0.38, GLOWS[g]); strip(A, 0.03, 0.02, 0.7, 0.2, 0.215, 0.38, GLOWS[g])
        for sx in (-1, 1): bx(A, 0.07, 0.35, 0.04, sx * 0.3, -0.02, 0.5, "hull_dark", 0.01)
    else:  # lounger
        prism(A, [(-0.4, 0), (0.4, 0), (0.4, 0.2), (-0.4, 0.4)], 0.95, (0, 0, 0.15), "hull", rot=(0, 0, 0), bevel=0.04) if False else bx(A, 0.8, 0.85, 0.2, 0, 0, 0.12, "hull", 0.05)
        pad(A, 0.7, 0.55, 0.14, 0, -0.1, 0.32, "cloth2", 0.05); pad(A, 0.7, 0.18, 0.55, 0, 0.32, 0.32, "cloth2", 0.06)
        cy(A, 0.06, 0.12, -0.3, -0.3, 0.0, "chrome"); cy(A, 0.06, 0.12, 0.3, -0.3, 0.0, "chrome"); cy(A, 0.06, 0.12, -0.3, 0.3, 0.0, "chrome"); cy(A, 0.06, 0.12, 0.3, 0.3, 0.0, "chrome")
        strip(A, 0.7, 0.02, 0.02, 0, -0.43, 0.14, GLOWS[g])


@family("dining_chair", "furniture", [{"n": "shell", "glow": "cyan"}, {"n": "stool_back", "glow": "amber"}, {"n": "wire", "glow": "magenta"}, {"n": "block", "glow": "green"}, {"n": "ribbed", "glow": "violet"}, {"n": "hover", "glow": "blue"}],
        cat="seating", place="floor", tags=["seating", "chair"], **{"as": "dining_chair"})
def _dch(A, v):
    k, g = v["n"], v["glow"]
    if k == "shell":
        cy(A, 0.03, 0.4, 0, 0, 0.0, "chrome"); cy(A, 0.22, 0.03, 0, 0, 0.0, "gunmetal", verts=5)
        prism(A, [(-0.22, 0), (0.22, 0), (0.2, 0.52), (-0.2, 0.52)], 0.06, (0, 0.18, 0.4), "hull", bevel=0.02); pad(A, 0.42, 0.42, 0.06, 0, 0, 0.4, "cloth", 0.03)
        strip(A, 0.3, 0.012, 0.02, 0, 0.145, 0.85, GLOWS[g])
    elif k == "stool_back":
        legs4(A, 0.45, 0.45, 0.45, 0.035, "gunmetal", 0.04); bx(A, 0.45, 0.45, 0.05, 0, 0, 0.45, "hull", 0.02); pad(A, 0.4, 0.4, 0.04, 0, 0, 0.5, "cloth", 0.02)
        bx(A, 0.4, 0.04, 0.3, 0, 0.2, 0.62, "hull_grey", 0.015); bx(A, 0.03, 0.03, 0.15, -0.17, 0.2, 0.5, "gunmetal"); bx(A, 0.03, 0.03, 0.15, 0.17, 0.2, 0.5, "gunmetal"); strip(A, 0.3, 0.012, 0.015, 0, 0.18, 0.88, GLOWS[g])
    elif k == "wire":
        for sx in (-1, 1):
            limb(A, (sx * 0.2, -0.2, 0.0), (sx * 0.2, -0.2, 0.46), 0.012, 0.012, "chrome", 6); limb(A, (sx * 0.2, 0.2, 0.0), (sx * 0.2, 0.2, 0.9), 0.012, 0.012, "chrome", 6)
            limb(A, (sx * 0.2, -0.2, 0.46), (sx * 0.2, 0.2, 0.46), 0.012, 0.012, "chrome", 6)
        for i in range(5): limb(A, (-0.2, -0.2 + i * 0.1, 0.46), (0.2, -0.2 + i * 0.1, 0.46), 0.008, 0.008, "chrome", 5)
        pad(A, 0.4, 0.4, 0.04, 0, 0, 0.46, "cloth", 0.02); limb(A, (-0.2, 0.2, 0.9), (0.2, 0.2, 0.9), 0.014, 0.014, GLOWS[g], 6); limb(A, (-0.2, 0.2, 0.7), (0.2, 0.2, 0.7), 0.01, 0.01, "chrome", 5)
    elif k == "block":
        bx(A, 0.45, 0.47, 0.42, 0, 0, 0.0, "hull_dark", 0.03); pad(A, 0.45, 0.47, 0.06, 0, 0, 0.42, "cloth", 0.03); pad(A, 0.45, 0.1, 0.45, 0, 0.18, 0.48, "cloth", 0.03); strip(A, 0.4, 0.012, 0.02, 0, -0.236, 0.05, GLOWS[g])
    elif k == "ribbed":
        legs4(A, 0.44, 0.44, 0.45, 0.03, "chrome", 0.03); pad(A, 0.44, 0.44, 0.06, 0, 0, 0.45, "pad", 0.02)
        for i in range(5): bx(A, 0.42, 0.04, 0.06, 0, 0.2, 0.55 + i * 0.09, "hull", 0.01)
        bx(A, 0.04, 0.04, 0.5, -0.19, 0.2, 0.5, "chrome"); bx(A, 0.04, 0.04, 0.5, 0.19, 0.2, 0.5, "chrome"); strip(A, 0.012, 0.012, 0.35, 0.21, 0.2, 0.56, GLOWS[g])
    else:  # hover
        cy(A, 0.2, 0.05, 0, 0, 0.0, "hull_dark", verts=24); tor(A, 0.2, 0.01, (0, 0, 0.03), GLOWS[g], seg=28, minor=6); cy(A, 0.04, 0.3, 0, 0, 0.05, "chrome")
        pad(A, 0.44, 0.44, 0.07, 0, 0, 0.35, "cloth", 0.04); prism(A, [(-0.22, 0), (0.22, 0), (0.18, 0.5), (-0.18, 0.5)], 0.08, (0, 0.2, 0.42), "cloth", bevel=0.03)


@family("office_chair", "furniture", [{"n": "task", "glow": "cyan"}, {"n": "command", "glow": "amber"}, {"n": "mesh_high", "glow": "magenta"}, {"n": "stool_swivel", "glow": "green"}],
        cat="seating", place="floor", tags=["seating", "chair"], **{"as": "office_chair"})
def _och(A, v):
    k, g = v["n"], v["glow"]
    for i in range(5):
        a = 2 * PI * i / 5; limb(A, (0, 0, 0.1), (0.28 * math.cos(a), 0.28 * math.sin(a), 0.03), 0.025, 0.018, "gunmetal", 6); sph(A, 0.03, (0.28 * math.cos(a), 0.28 * math.sin(a), 0.03), "rubber", seg=6)
    cy(A, 0.04, 0.32, 0, 0, 0.1, "chrome")
    if k == "task":
        pad(A, 0.5, 0.5, 0.08, 0, 0, 0.42, "cloth", 0.04); prism(A, [(-0.25, 0), (0.25, 0), (0.22, 0.55), (-0.22, 0.55)], 0.07, (0, 0.24, 0.55), "cloth", bevel=0.03); strip(A, 0.3, 0.012, 0.02, 0, 0.205, 1.05, GLOWS[g])
        for sx in (-1, 1): bx(A, 0.04, 0.3, 0.04, sx * 0.28, 0, 0.62, "hull_dark")
    elif k == "command":
        pad(A, 0.58, 0.55, 0.12, 0, 0, 0.42, "pad", 0.05); prism(A, [(-0.3, 0), (0.3, 0), (0.26, 0.75), (-0.26, 0.75)], 0.12, (0, 0.27, 0.55), "pad", bevel=0.05)
        for sx in (-1, 1): bx(A, 0.1, 0.45, 0.05, sx * 0.34, -0.05, 0.62, "hull_dark", 0.015); bx(A, 0.04, 0.04, 0.16, sx * 0.34, 0.1, 0.5, "gunmetal")
        strip(A, 0.5, 0.012, 0.03, 0, 0.205, 1.1, GLOWS[g]); strip(A, 0.03, 0.012, 0.45, -0.22, 0.205, 0.65, GLOWS[g]); strip(A, 0.03, 0.012, 0.45, 0.22, 0.205, 0.65, GLOWS[g])
    elif k == "mesh_high":
        pad(A, 0.5, 0.5, 0.07, 0, 0, 0.42, "pad", 0.03); prism(A, [(-0.24, 0), (0.24, 0), (0.2, 0.78), (-0.2, 0.78)], 0.05, (0, 0.24, 0.55), "pad", bevel=0.02)
        pad(A, 0.3, 0.08, 0.16, 0, 0.27, 1.25, "hull", 0.03); strip(A, 0.012, 0.012, 0.7, -0.19, 0.22, 0.6, GLOWS[g])
    else:
        cy(A, 0.27, 0.1, 0, 0, 0.42, "cloth", verts=24); tor(A, 0.27, 0.01, (0, 0, 0.45), GLOWS[g], seg=32, minor=6)


@family("bench", "furniture", [{"n": "slab", "glow": "cyan"}, {"n": "locker_room", "glow": "amber"}, {"n": "cushioned", "glow": "magenta"}, {"n": "lit_block", "glow": "green"}, {"n": "airlock", "glow": "red"}],
        cat="seating", place="floor", tags=["seating", "wall-hug"], **{"as": "bench"})
def _bench(A, v):
    k, g = v["n"], v["glow"]
    W, D = 1.2, 0.4
    if k == "slab":
        for sx in (-1, 1): bx(A, 0.06, D - 0.05, 0.4, sx * (W / 2 - 0.12), 0, 0.0, "gunmetal", 0.01)
        bx(A, W, D, 0.06, 0, 0, 0.4, "hull", 0.02); strip(A, W - 0.1, 0.012, 0.016, 0, -D / 2 + 0.01, 0.39, GLOWS[g])
    elif k == "locker_room":
        bx(A, W, 0.06, 0.4, 0, D / 2 - 0.03, 0.0, "hull_grey", 0.01)
        for sx in (-1, 1): bx(A, 0.05, D, 0.4, sx * (W / 2 - 0.1), 0, 0.0, "hull_dark", 0.01)
        bx(A, W, D, 0.05, 0, 0, 0.4, "wood_pale" if False else "hull", 0.015); bx(A, W - 0.1, 0.03, 0.02, 0, -D / 2 + 0.03, 0.435, GLOWS[g] if False else "p_orange", 0)
        bx(A, W - 0.1, 0.3, 0.2, 0, -0.0, 0.15, "pad", 0.02)
    elif k == "cushioned":
        for sx in (-1, 1): cy(A, 0.03, 0.38, sx * (W / 2 - 0.1), 0, 0.0, "chrome")
        pad(A, W, D, 0.1, 0, 0, 0.36, "cloth", 0.04); strip(A, W - 0.2, 0.012, 0.014, 0, 0, 0.35, GLOWS[g])
    elif k == "lit_block":
        bx(A, W, D, 0.44, 0, 0, 0.0, "hull", 0.04); strip(A, W - 0.05, D - 0.05, 0.012, 0, 0, 0.0, GLOWS[g]); pad(A, W - 0.1, D - 0.1, 0.05, 0, 0, 0.44, "cloth", 0.03)
    else:  # airlock bench with storage hatch
        bx(A, W, D, 0.45, 0, 0, 0.0, "hull_grey", 0.025); bx(A, W - 0.2, 0.02, 0.28, 0, -D / 2 - 0.005, 0.07, "hull", 0.01); bx(A, 0.2, 0.025, 0.04, 0, -D / 2 - 0.02, 0.2, "p_yellow", 0.005)
        pad(A, W, D, 0.05, 0, 0, 0.45, "pad", 0.02); strip(A, 0.3, 0.012, 0.012, 0.35, -D / 2 - 0.015, 0.4, GLOWS[g])


@family("ottoman", "furniture", [{"n": "puck", "glow": "cyan"}, {"n": "cube_glow", "glow": "magenta"}, {"n": "pouf", "glow": "amber"}],
        cat="seating", place="floor", tags=["seating"], **{"as": "ottoman"})
def _ott(A, v):
    k, g = v["n"], v["glow"]
    if k == "puck":
        cy(A, 0.3, 0.3, 0, 0, 0.05, "cloth", verts=28); cy(A, 0.28, 0.05, 0, 0, 0.0, "gunmetal", verts=28); tor(A, 0.3, 0.008, (0, 0, 0.06), GLOWS[g], seg=32, minor=6)
    elif k == "cube_glow":
        bx(A, 0.6, 0.6, 0.4, 0, 0, 0.0, "hull", 0.06); strip(A, 0.5, 0.5, 0.012, 0, 0, 0.0, GLOWS[g]); pad(A, 0.56, 0.56, 0.06, 0, 0, 0.4, "cloth", 0.03)
    else:
        sph(A, 0.3, (0, 0, 0.22), "cloth", scale=(1, 1, 0.75), seg=20); cy(A, 0.18, 0.05, 0, 0, 0.0, "gunmetal", verts=20); tor(A, 0.2, 0.008, (0, 0, 0.05), GLOWS[g], seg=28, minor=6)
