# ============ HOME: rug, mirror, lamps, plants, curtains, bathroom ============

def _rugpat(A, W, D, v, base):
    g = v["glow"]
    box(A, (W, D, 0.02), (0, 0, 0.01), base, bevel=0.004)
    return g


@family("rug", "furniture", [{"n": "neon_grid", "glow": "cyan"}, {"n": "hex_pad", "glow": "magenta"}, {"n": "circuit", "glow": "green"}, {"n": "hazard_border", "glow": "amber"}, {"n": "orbit_rings", "glow": "violet"}, {"n": "landing_pad", "glow": "red"}],
        cat="decor", place="floor", tags=["rug", "flat", "center"], **{"as": "rug"})
def _rug(A, v):
    k, g = v["n"], v["glow"]
    W, D = 2.6, 1.8
    if k == "neon_grid":
        box(A, (W, D, 0.03), (0, 0, 0.015), "hull_dark", bevel=0.005)
        for i in range(-3, 4): strip(A, 0.02, D - 0.1, 0.012, i * 0.38, 0, 0.03, GLOWS[g])
        for j in range(-2, 3): strip(A, W - 0.1, 0.02, 0.012, 0, j * 0.38, 0.03, GLOWS[g])
    elif k == "hex_pad":
        box(A, (W, D, 0.03), (0, 0, 0.015), "pad", bevel=0.005)
        for q in range(-3, 4):
            for r in range(-2, 3):
                x = q * 0.36 + (0.18 if r % 2 else 0); y = r * 0.31
                if abs(x) < W / 2 - 0.2 and abs(y) < D / 2 - 0.15: cyl(A, 0.15, 0.012, (x, y, 0.036), GLOWS[g] if (q + r) % 4 == 0 else "hull_grey", verts=6)
    elif k == "circuit":
        box(A, (W, D, 0.03), (0, 0, 0.015), "carbon", bevel=0.005)
        for i, (x0, y0, w, d) in enumerate([(-0.9, 0.4, 1.2, 0.03), (-0.3, 0.4, 0.03, -0.5), (-0.3, -0.1, 0.9, 0.03), (0.6, -0.1, 0.03, -0.5), (0.2, 0.55, 0.03, 0.2), (0.2, 0.7, 0.7, 0.03), (-0.9, -0.5, 0.03, 0.9)]):
            strip(A, abs(w), abs(d), 0.012, x0 + w / 2, y0 + d / 2, 0.03, GLOWS[g])
        for x, y in [(-0.9, 0.4), (0.6, -0.6), (0.9, 0.7), (-0.3, -0.1)]: cyl(A, 0.06, 0.014, (x, y, 0.037), GLOWS[g], verts=16)
        strip(A, W - 0.1, 0.02, 0.012, 0, D / 2 - 0.08, 0.03, "neon_white"); strip(A, W - 0.1, 0.02, 0.012, 0, -D / 2 + 0.08, 0.03, "neon_white")
    elif k == "hazard_border":
        box(A, (W, D, 0.03), (0, 0, 0.015), "hull_grey", bevel=0.005)
        for i in range(14):
            for sy in (-1, 1): box(A, (0.14, 0.12, 0.012), (-W / 2 + 0.15 + i * 0.185, sy * (D / 2 - 0.1), 0.036), "p_yellow" if i % 2 == 0 else "rubber", (0, 0, 0.5), 0)
        strip(A, W - 0.5, 0.03, 0.012, 0, 0, 0.03, GLOWS[g])
    elif k == "orbit_rings":
        box(A, (W, D, 0.03), (0, 0, 0.015), "hull_dark", bevel=0.005)
        for R, t in ((0.75, 0.018), (0.55, 0.014), (0.35, 0.012)): tor(A, R, t, (0, 0, 0.034), GLOWS[g], seg=48, minor=5)
        sph(A, 0.12, (0, 0, 0.1), GLOWS[g], seg=14); sph(A, 0.04, (0.55, 0, 0.06), "neon_white", seg=8); sph(A, 0.05, (-0.35, 0.0, 0.07), "neon_white", seg=8)
    else:  # landing_pad
        box(A, (W, D, 0.03), (0, 0, 0.015), "hull_grey", bevel=0.005)
        tor(A, 0.7, 0.03, (0, 0, 0.04), "p_yellow", seg=48, minor=6)
        box(A, (0.14, 0.7, 0.012), (0, 0, 0.036), GLOWS[g], bevel=0); box(A, (0.7, 0.14, 0.012), (0, 0, 0.036), GLOWS[g], bevel=0)
        for x in (-1, 1):
            for y in (-1, 1): cyl(A, 0.05, 0.016, (x * (W / 2 - 0.12), y * (D / 2 - 0.12), 0.038), "p_orange", verts=12)


@family("mirror", "furniture", [{"n": "slim_neon", "glow": "cyan"}, {"n": "round_halo", "glow": "magenta"}, {"n": "smart_panel", "glow": "amber"}, {"n": "hex", "glow": "green"}],
        cat="wallart", place="wall", y=0.9, tags=["wallart", "decor"], **{"as": "mirror"})
def _mir(A, v):
    k, g = v["n"], v["glow"]
    if k == "slim_neon":
        bx(A, 0.6, 0.04, 1.2, 0, 0, 0.0, "hull_dark", 0.01); box(A, (0.52, 0.01, 1.12), (0, -0.022, 0.6), "chrome", bevel=0); strip(A, 0.02, 0.012, 1.2, -0.31, 0.0, 0.0, GLOWS[g]); strip(A, 0.02, 0.012, 1.2, 0.31, 0.0, 0.0, GLOWS[g])
    elif k == "round_halo":
        cyl(A, 0.4, 0.03, (0, 0, 0.6), "chrome", rot=(PI / 2, 0, 0), verts=40); tor(A, 0.42, 0.02, (0, -0.01, 0.6), GLOWS[g], rot=(PI / 2, 0, 0), seg=48, minor=8); cyl(A, 0.42, 0.03, (0, 0.03, 0.6), "gunmetal", rot=(PI / 2, 0, 0), verts=40)
    elif k == "smart_panel":
        bx(A, 0.6, 0.05, 1.2, 0, 0, 0.0, "hull", 0.02); box(A, (0.5, 0.01, 1.0), (0, -0.028, 0.6), "chrome", bevel=0); box(A, (0.4, 0.006, 0.12), (0, -0.034, 1.0), SCRS[g], bevel=0)
    else:
        prism(A, [(-0.3, 0.0), (0.3, 0.0), (0.45, 0.6), (0.3, 1.2), (-0.3, 1.2), (-0.45, 0.6)], 0.04, (0, 0, 0), "hull_dark", rot=(0, 0, 0), bevel=0.01)
        prism(A, [(-0.26, 0.05), (0.26, 0.05), (0.4, 0.6), (0.26, 1.15), (-0.26, 1.15), (-0.4, 0.6)], 0.01, (0, -0.025, 0), "chrome", bevel=0); strip(A, 0.01, 0.012, 1.0, 0.0, 0.0, 0.1, GLOWS[g]) if False else None


@family("floor_lamp", "lighting", [{"n": "stem", "glow": "cyan", "meta": lt("cyan", 1.5, 1.0)}, {"n": "arc", "glow": "amber", "meta": lt("amber", 1.7, 1.1)}, {"n": "tube", "glow": "magenta", "meta": lt("magenta", 1.4, 1.0)}, {"n": "orb", "glow": "green", "meta": lt("green", 1.4, 0.9)}, {"n": "cone", "glow": "violet", "meta": lt("violet", 1.5, 1.0)}],
        cat="light", place="floor", tags=["light", "corner", "glow"], **{"as": "floor_lamp"})
def _fl(A, v):
    k, g = v["n"], v["glow"]
    cy(A, 0.16, 0.04, 0, 0, 0.0, "gunmetal", verts=24)
    if k == "stem":
        cy(A, 0.02, 1.4, 0, 0, 0.04, "chrome"); cy(A, 0.1, 0.3, 0, 0, 1.3, GLOWS[g], verts=16); cy(A, 0.11, 0.03, 0, 0, 1.6, "gunmetal", verts=16)
    elif k == "arc":
        cy(A, 0.02, 1.3, -0.1, 0, 0.04, "chrome")
        for i in range(8):
            a0, a1 = math.radians(i * 14), math.radians((i + 1) * 14); limb(A, (-0.1 + 0.35 * (1 - math.cos(a0)) * 0 + 0.4 * math.sin(a0) - 0.0, 0, 1.3 + 0.3 * (1 - math.cos(a0))), (-0.1 + 0.4 * math.sin(a1), 0, 1.3 + 0.3 * (1 - math.cos(a1))), 0.016, 0.016, "chrome", 6)
        sph(A, 0.1, (0.3, 0, 1.55), GLOWS[g], seg=14)
    elif k == "tube":
        cy(A, 0.03, 1.55, 0, 0, 0.04, GLOWS[g], verts=14); cy(A, 0.05, 0.05, 0, 0, 0.04, "chrome"); cy(A, 0.05, 0.05, 0, 0, 1.58, "chrome")
    elif k == "orb":
        cy(A, 0.025, 1.0, 0, 0, 0.04, "chrome"); sph(A, 0.17, (0, 0, 1.25), GLOWS[g], seg=18); tor(A, 0.19, 0.01, (0, 0, 1.25), "chrome", seg=28, minor=6)
    else:
        cy(A, 0.02, 1.2, 0, 0, 0.04, "chrome"); cyl(A, 0.2, 0.28, (0, 0, 1.4), "hull", r2=0.05, verts=20); cyl(A, 0.17, 0.02, (0, 0, 1.28), GLOWS[g], verts=20)


@family("table_lamp", "lighting", [{"n": "cone", "glow": "cyan", "meta": lt("cyan", 0.3, 0.5)}, {"n": "orb", "glow": "magenta", "meta": lt("magenta", 0.28, 0.5)}, {"n": "cube", "glow": "amber", "meta": lt("amber", 0.25, 0.5)}, {"n": "desk_arm", "glow": "green", "meta": lt("green", 0.4, 0.5)}, {"n": "crystal", "glow": "violet", "meta": lt("violet", 0.3, 0.5)}],
        cat="light", place="surface", tags=["light", "glow", "decor"], **{"as": "table_lamp"})
def _tl(A, v):
    k, g = v["n"], v["glow"]
    cy(A, 0.1, 0.025, 0, 0, 0.0, "gunmetal", verts=20)
    if k == "cone":
        cy(A, 0.012, 0.2, 0, 0, 0.02, "chrome"); cyl(A, 0.11, 0.17, (0, 0, 0.3), "hull", r2=0.04, verts=18); cyl(A, 0.09, 0.015, (0, 0, 0.22), GLOWS[g], verts=18)
    elif k == "orb":
        cy(A, 0.012, 0.12, 0, 0, 0.02, "chrome"); sph(A, 0.1, (0, 0, 0.26), GLOWS[g], seg=16)
    elif k == "cube":
        bx(A, 0.14, 0.14, 0.2, 0, 0, 0.02, GLOWS[g], 0.015); bx(A, 0.16, 0.16, 0.025, 0, 0, 0.0, "hull_dark")
    elif k == "desk_arm":
        limb(A, (0, 0, 0.02), (0.06, 0, 0.28), 0.01, 0.01, "chrome", 6); limb(A, (0.06, 0, 0.28), (-0.08, 0, 0.4), 0.01, 0.01, "chrome", 6); cyl(A, 0.07, 0.07, (-0.1, 0, 0.38), "hull", r2=0.03, rot=(0, 0.5, 0), verts=14); sph(A, 0.03, (-0.115, 0, 0.35), GLOWS[g], seg=8)
    else:
        cyl(A, 0.07, 0.3, (0, 0, 0.18), GLOWS[g], r2=0.01, verts=6); cy(A, 0.03, 0.03, 0, 0, 0.02, "chrome")


@family("ceiling_light", "lighting", [{"n": "disc", "glow": "white", "meta": lt("white", 0.1, 1.4)}, {"n": "ring", "glow": "cyan", "meta": lt("cyan", 0.1, 1.4)}, {"n": "panel", "glow": "white", "meta": lt("white", 0.08, 1.5)}, {"n": "pendant_orb", "glow": "amber", "meta": lt("amber", 0.2, 1.4)}, {"n": "lantern_tube", "glow": "magenta", "meta": lt("magenta", 0.2, 1.4)}, {"n": "cluster", "glow": "violet", "meta": lt("violet", 0.25, 1.4)}],
        cat="light", place="ceiling", tags=["light", "glow"], **{"as": "ceiling_light"})
def _cl(A, v):
    k, g = v["n"], v["glow"]
    H = 0.45  # object spans z 0..H, hangs from the top (z = H)
    if k == "disc":
        cy(A, 0.28, 0.06, 0, 0, H - 0.06, "hull", verts=32); cy(A, 0.24, 0.02, 0, 0, H - 0.075, GLOWS[g], verts=32)
    elif k == "ring":
        cy(A, 0.28, 0.04, 0, 0, H - 0.04, "hull_dark", verts=32); tor(A, 0.24, 0.025, (0, 0, H - 0.07), GLOWS[g], seg=40, minor=8); cy(A, 0.05, 0.05, 0, 0, H - 0.09, "chrome")
    elif k == "panel":
        bx(A, 0.6, 0.6, 0.04, 0, 0, H - 0.04, "hull", 0.01); bx(A, 0.54, 0.54, 0.012, 0, 0, H - 0.05, GLOWS[g], 0)
    elif k == "pendant_orb":
        cy(A, 0.012, 0.2, 0, 0, H - 0.2, "chrome"); cy(A, 0.06, 0.03, 0, 0, H - 0.03, "gunmetal"); sph(A, 0.16, (0, 0, 0.17), GLOWS[g], seg=18)
    elif k == "lantern_tube":
        for sx in (-1, 1): cy(A, 0.008, 0.2, sx * 0.2, 0, H - 0.2, "chrome", verts=6)
        cy(A, 0.035, 0.48, 0, 0, 0.0, GLOWS[g], verts=14, rot=(0, PI / 2, 0)) if False else box(A, (0.5, 0.06, 0.06), (0, 0, 0.2), GLOWS[g], bevel=0.01)
        bx(A, 0.54, 0.1, 0.04, 0, 0, H - 0.04, "gunmetal", 0.01)
    else:
        cy(A, 0.15, 0.035, 0, 0, H - 0.035, "gunmetal", verts=24)
        for i, (x, y, l) in enumerate([(0, 0, 0.3), (0.12, 0.06, 0.2), (-0.1, 0.08, 0.25), (0.02, -0.12, 0.15)]):
            cy(A, 0.006, l, x, y, H - 0.035 - l, "chrome", verts=6); sph(A, 0.05, (x, y, H - 0.035 - l), GLOWS[g], seg=10)


@family("plant", "decor", [{"n": "hydro_tower"}, {"n": "fern_pod"}, {"n": "bonsai_dome"}, {"n": "vine_column"}, {"n": "cactus_neon"}, {"n": "ficus_planter"}],
        cat="decor", place="floor", tags=["plant", "corner", "decor"], **{"as": "plant"})
def _plant(A, v):
    k = v["n"]
    if k == "hydro_tower":
        cy(A, 0.2, 0.08, 0, 0, 0.0, "gunmetal", verts=20); cy(A, 0.08, 1.0, 0, 0, 0.08, "hull", verts=16); strip(A, 0.02, 0.02, 0.9, 0.0, -0.085, 0.12, "neon_magenta")
        for i in range(6):
            a = i * 1.1; z = 0.25 + i * 0.15; x, y = 0.12 * math.cos(a), 0.12 * math.sin(a)
            cy(A, 0.06, 0.04, x, y, z, "hull_grey", verts=10)
            for j in range(4): limb(A, (x, y, z + 0.04), (x + 0.12 * math.cos(a + j * 1.6), y + 0.12 * math.sin(a + j * 1.6), z + 0.14), 0.012, 0.004, "leaf", 5); sph(A, 0.04, (x + 0.12 * math.cos(a + j * 1.6), y + 0.12 * math.sin(a + j * 1.6), z + 0.14), "leaf", scale=(1, 1, 0.5), seg=8)
    elif k == "fern_pod":
        cy(A, 0.25, 0.3, 0, 0, 0.0, "hull", r2=0.2, verts=24); cy(A, 0.24, 0.02, 0, 0, 0.3, "soil", verts=24); tor(A, 0.23, 0.01, (0, 0, 0.1), "neon_cyan", seg=28, minor=5)
        for i in range(14):
            a = i * 0.45; t = 0.5 + (i % 4) * 0.2; limb(A, (0.03 * math.cos(a), 0.03 * math.sin(a), 0.3), (0.5 * math.cos(a) * 0.7, 0.5 * math.sin(a) * 0.7, 0.3 + t), 0.015, 0.003, "leaf", 5)
            sph(A, 0.07, (0.35 * math.cos(a), 0.35 * math.sin(a), 0.3 + t), "leaf" if i % 3 else "leaf2", scale=(1, 1, 0.4), seg=8)
    elif k == "bonsai_dome":
        cy(A, 0.28, 0.35, 0, 0, 0.0, "hull_dark", r2=0.24, verts=24); cy(A, 0.26, 0.02, 0, 0, 0.35, "soil", verts=24); limb(A, (0, 0, 0.35), (0.05, 0, 0.8), 0.04, 0.025, "hull_grey", 8)
        for p in [(0.0, 0, 0.95), (0.2, 0.05, 0.85), (-0.15, 0.1, 0.88), (0.1, -0.15, 0.82)]: sph(A, 0.17, p, "leaf", seg=10)
        sph(A, 0.5, (0, 0, 0.9), "glass_cyan", scale=(1, 1, 1.2), seg=24)
    elif k == "vine_column":
        cy(A, 0.18, 0.06, 0, 0, 0.0, "gunmetal", verts=20); cy(A, 0.04, 1.8, 0, 0, 0.06, "chrome", verts=10)
        for i in range(24):
            z = 0.2 + i * 0.07; a = i * 0.9; x, y = 0.07 * math.cos(a), 0.07 * math.sin(a); sph(A, 0.05, (x, y, z), "leaf" if i % 2 else "leaf2", scale=(1, 1, 0.5), seg=6)
        cy(A, 0.1, 0.25, 0, 0, 0.0, "hull", verts=16)
    elif k == "cactus_neon":
        cy(A, 0.2, 0.25, 0, 0, 0.0, "hull_dark", r2=0.17, verts=20); cy(A, 0.19, 0.02, 0, 0, 0.25, "soil", verts=20); cy(A, 0.1, 0.9, 0, 0, 0.27, "leaf2", verts=14); sph(A, 0.1, (0, 0, 1.17), "leaf2", seg=14)
        for s, z, l in ((-1, 0.7, 0.3), (1, 0.55, 0.25)):
            limb(A, (s * 0.1, 0, z), (s * 0.28, 0, z), 0.06, 0.06, "leaf2", 10); limb(A, (s * 0.28, 0, z), (s * 0.28, 0, z + l), 0.06, 0.06, "leaf2", 10); sph(A, 0.06, (s * 0.28, 0, z + l), "leaf2", seg=10)
        strip(A, 0.012, 0.012, 0.8, 0.0, -0.105, 0.3, "neon_magenta")
    else:  # ficus_planter
        bx(A, 0.5, 0.5, 0.3, 0, 0, 0.0, "hull", 0.04); bx(A, 0.44, 0.44, 0.02, 0, 0, 0.3, "soil", 0); strip(A, 0.46, 0.012, 0.012, 0, -0.255, 0.03, "neon_green")
        limb(A, (0, 0, 0.3), (0, 0, 0.9), 0.03, 0.02, "hull_grey", 8)
        for i, (x, y, z) in enumerate([(0, 0, 1.15), (0.2, 0.1, 0.95), (-0.2, 0.05, 1.0), (0.1, -0.2, 0.9), (-0.1, 0.2, 1.05), (0.05, 0.15, 1.2)]): sph(A, 0.2, (x, y, z), "leaf", scale=(1, 1, 0.9), seg=12)


@family("plant_small", "decor", [{"n": "mini_pod"}, {"n": "glow_succulent"}, {"n": "moss_cube"}, {"n": "bonsai_mini"}],
        cat="decor", place="surface", tags=["plant", "decor"], **{"as": "plant_small"})
def _ps(A, v):
    k = v["n"]
    if k == "mini_pod":
        cy(A, 0.09, 0.1, 0, 0, 0.0, "hull", r2=0.07, verts=16); cy(A, 0.085, 0.01, 0, 0, 0.1, "soil", verts=16)
        for i in range(5): a = i * 1.25; limb(A, (0, 0, 0.1), (0.06 * math.cos(a), 0.06 * math.sin(a), 0.26), 0.008, 0.003, "leaf", 5); sph(A, 0.035, (0.07 * math.cos(a), 0.07 * math.sin(a), 0.27), "leaf", scale=(1, 1, 0.5), seg=6)
    elif k == "glow_succulent":
        cy(A, 0.08, 0.07, 0, 0, 0.0, "gunmetal", verts=14); tor(A, 0.08, 0.006, (0, 0, 0.05), "neon_cyan", seg=20, minor=5)
        for i in range(8): a = i * 0.8; limb(A, (0, 0, 0.08), (0.07 * math.cos(a), 0.07 * math.sin(a), 0.17), 0.018, 0.006, "leaf2", 6)
    elif k == "moss_cube":
        bx(A, 0.14, 0.14, 0.14, 0, 0, 0.0, "hull_dark", 0.015); sph(A, 0.09, (0, 0, 0.15), "leaf", scale=(1, 1, 0.6), seg=10); strip(A, 0.12, 0.012, 0.012, 0, -0.072, 0.02, "neon_green")
    else:
        cy(A, 0.07, 0.05, 0, 0, 0.0, "hull_grey", verts=14); limb(A, (0, 0, 0.05), (0.02, 0, 0.2), 0.012, 0.008, "hull_dark", 6)
        for p in [(0.02, 0, 0.24), (0.07, 0.02, 0.2), (-0.04, 0.03, 0.21)]: sph(A, 0.05, p, "leaf", seg=8)


@family("curtains", "furniture", [{"n": "privacy_shutter", "glow": "cyan"}, {"n": "light_blind", "glow": "amber"}, {"n": "slat_panel", "glow": "magenta"}, {"n": "smart_glass", "glow": "violet"}],
        cat="wallart", place="wall", y=0.05, tags=["curtain"], **{"as": "curtains"})
def _cur(A, v):
    k, g = v["n"], v["glow"]
    W, H = 1.8, 2.4
    bx(A, W + 0.1, 0.1, 0.1, 0, 0, H - 0.1, "gunmetal", 0.01)
    if k == "privacy_shutter":
        for i in range(18): bx(A, W, 0.03, 0.1, 0, 0.0, 0.1 + i * 0.12, "hull" if i % 2 else "hull_grey", 0.005)
        strip(A, 0.02, 0.02, H - 0.2, -W / 2 - 0.02, 0, 0.1, GLOWS[g]); strip(A, 0.02, 0.02, H - 0.2, W / 2 + 0.02, 0, 0.1, GLOWS[g])
    elif k == "light_blind":
        bx(A, W, 0.03, H - 0.3, 0, 0, 0.3, "hull_grey", 0.005); bx(A, W, 0.05, 0.05, 0, 0, 0.25, "gunmetal", 0.01); strip(A, W - 0.1, 0.02, 0.012, 0, -0.03, 0.27, GLOWS[g])
    elif k == "slat_panel":
        for i in range(16): bx(A, 0.09, 0.05, H - 0.15, -W / 2 + 0.06 + i * 0.115, 0.0, 0.05, "cloth2" if i % 4 == 0 else "hull_dark", 0.01)
        strip(A, W, 0.02, 0.014, 0, -0.04, 0.04, GLOWS[g])
    else:
        box(A, (W, 0.03, H - 0.2), (0, 0, H / 2 - 0.05), "glass_cyan", bevel=0); bx(A, W, 0.05, 0.04, 0, 0, 0.02, "gunmetal", 0.005); strip(A, W - 0.1, 0.02, 0.012, 0, -0.03, 0.06, GLOWS[g])


@family("toilet", "furniture", [{"n": "sleek", "glow": "cyan"}, {"n": "wall_hung", "glow": "green"}, {"n": "zero_g", "glow": "amber"}],
        cat="bath", place="floor", tags=["bath", "wall-hug"], **{"as": "toilet"})
def _toi(A, v):
    k, g = v["n"], v["glow"]
    if k == "sleek":
        bx(A, 0.4, 0.2, 0.75, 0, 0.25, 0.0, "hull", 0.04); sph(A, 0.2, (0, -0.05, 0.25), "hull", scale=(1, 1.4, 0.8), seg=16); bx(A, 0.36, 0.5, 0.04, 0, -0.05, 0.42, "hull_grey", 0.02); strip(A, 0.2, 0.012, 0.02, 0, 0.14, 0.6, GLOWS[g])
    elif k == "wall_hung":
        bx(A, 0.4, 0.14, 0.8, 0, 0.3, 0.0, "hull_dark", 0.02); sph(A, 0.2, (0, 0.0, 0.35), "hull", scale=(1, 1.6, 0.7), seg=16); strip(A, 0.3, 0.012, 0.014, 0, -0.2, 0.2, GLOWS[g]); cy(A, 0.04, 0.02, 0, 0.225, 0.62, "steel", rot=(PI / 2, 0, 0))
    else:
        cy(A, 0.2, 0.4, 0, 0.05, 0.0, "hull", r2=0.17, verts=24); cy(A, 0.19, 0.06, 0, 0.05, 0.4, "hull_grey", verts=24); cy(A, 0.12, 0.01, 0, 0.05, 0.46, "screen_off", verts=24); bx(A, 0.3, 0.1, 0.75, 0, 0.3, 0.0, "hull_dark", 0.02); tor(A, 0.2, 0.01, (0, 0.05, 0.05), GLOWS[g], seg=28, minor=5)


@family("bathtub", "furniture", [{"n": "soak_capsule", "glow": "cyan"}, {"n": "oval_tub", "glow": "magenta"}, {"n": "sonic_bay", "glow": "green"}],
        cat="bath", place="floor", tags=["bath", "wall-hug", "long"], **{"as": "bathtub"})
def _bath(A, v):
    k, g = v["n"], v["glow"]
    W, D = 1.7, 0.78
    if k == "soak_capsule":
        bx(A, W, D, 0.5, 0, 0, 0.0, "hull", 0.12); bx(A, W - 0.2, D - 0.2, 0.06, 0, 0, 0.5, "glass_cyan", 0.05); strip(A, W - 0.1, 0.012, 0.02, 0, -D / 2 - 0.005, 0.25, GLOWS[g]); bx(A, 0.3, 0.1, 0.06, -W / 2 + 0.3, D / 2 - 0.1, 0.5, "steel", 0.01)
    elif k == "oval_tub":
        cy(A, 0.5, 0.5, 0, 0, 0.0, "hull", verts=32) if False else sph(A, 0.5, (0, 0, 0.28), "hull", scale=(W / 1.0, D / 1.0, 0.55), seg=24)
        sph(A, 0.45, (0, 0, 0.36), "glass_cyan", scale=(W / 1.0 - 0.18, D / 1.0 - 0.15, 0.4), seg=24); tor(A, 0.5, 0.012, (0, -0.0, 0.05), GLOWS[g], seg=36, minor=5) if False else strip(A, W - 0.4, 0.012, 0.02, 0, -D / 2 + 0.02, 0.04, GLOWS[g])
    else:
        bx(A, W, D, 0.12, 0, 0, 0.0, "hull_dark", 0.02); bx(A, W - 0.1, D - 0.1, 0.4, 0, 0, 0.12, "hull", 0.06); bx(A, W - 0.3, D - 0.3, 0.02, 0, 0, 0.5, "steel", 0.01)
        for i in range(8): bx(A, 0.012, 0.012, 0.1, -0.5 + i * 0.14, 0.1, 0.5, GLOWS[g], 0)
        screen(A, 0.3, 0.12, W / 2 - 0.3, D / 2 - 0.08, 0.2, SCRS[g], "hull_dark", face=-1)


@family("sink_vanity", "furniture", [{"n": "basin_unit", "glow": "cyan"}, {"n": "pedestal", "glow": "magenta"}, {"n": "wash_station", "glow": "green"}, {"n": "mirror_vanity", "glow": "amber"}],
        cat="bath", place="floor", tags=["bath", "wall-hug", "holds-decor"], **{"as": "sink_vanity"})
def _sink(A, v):
    k, g = v["n"], v["glow"]
    W, D, H = 0.8, 0.5, 0.9
    if k == "basin_unit":
        bx(A, W, D, 0.75, 0, 0, 0.0, "hull", 0.03); bx(A, W, D, 0.04, 0, 0, 0.75, "hull_grey", 0.01); sph(A, 0.18, (0, -0.02, 0.76), "chrome", scale=(1.3, 1.1, 0.4), seg=14); cy(A, 0.015, 0.2, 0, 0.15, 0.78, "chrome"); strip(A, W - 0.1, 0.012, 0.014, 0, -D / 2 - 0.005, 0.05, GLOWS[g])
    elif k == "pedestal":
        cy(A, 0.12, 0.7, 0, 0.05, 0.0, "hull", r2=0.1, verts=20); sph(A, 0.3, (0, -0.0, 0.8), "hull", scale=(1.2, 0.9, 0.35), seg=16); cy(A, 0.015, 0.2, 0, 0.18, 0.85, "chrome"); tor(A, 0.14, 0.008, (0, 0.05, 0.04), GLOWS[g], seg=24, minor=5)
    elif k == "wash_station":
        bx(A, W, D, 0.82, 0, 0, 0.0, "hull_dark", 0.02); bx(A, W - 0.1, D - 0.1, 0.04, 0, 0, 0.82, "steel", 0.01); bx(A, 0.35, 0.28, 0.02, 0, 0, 0.855, "hull_dark")
        cy(A, 0.02, 0.15, 0, 0.12, 0.86, "chrome"); strip(A, 0.3, 0.012, 0.012, 0, -D / 2 - 0.005, 0.6, GLOWS[g]); screen(A, 0.2, 0.1, 0.25, -D / 2 - 0.01, 0.3, SCRS[g], "hull_grey", face=-1)
    else:
        bx(A, W, D, 0.72, 0, 0, 0.0, "hull", 0.03); bx(A, W, D, 0.04, 0, 0, 0.72, "hull_grey", 0.01); sph(A, 0.17, (0, 0, 0.73), "chrome", scale=(1.3, 1.1, 0.4), seg=14)
        bx(A, W - 0.1, 0.04, 0.5, 0, D / 2 - 0.02, 0.8, "hull_dark", 0.01); box(A, (W - 0.2, 0.01, 0.4), (0, D / 2 - 0.045, 1.05), "chrome", bevel=0); strip(A, W - 0.1, 0.012, 0.014, 0, D / 2 - 0.045, 1.3, GLOWS[g])
