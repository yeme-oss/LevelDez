# ============ DECOR: small surface items (pack-only types) ============

@family("datapad", "decor", [{"n": "tablet", "glow": "cyan"}, {"n": "stack", "glow": "amber"}, {"n": "folding", "glow": "green"}, {"n": "holo_slate", "glow": "magenta"}],
        cat="decor", place="surface", tags=["decor"])
def _pad(A, v):
    k, g = v["n"], v["glow"]
    if k == "tablet":
        bx(A, 0.22, 0.16, 0.012, 0, 0, 0.0, "hull_dark", 0.004); box(A, (0.2, 0.14, 0.003), (0, 0, 0.013), SCRS[g], bevel=0)
    elif k == "stack":
        for i in range(3): bx(A, 0.22, 0.16, 0.012, 0.01 * (i % 2), 0, i * 0.014, ["hull", "hull_dark", "hull_grey"][i], 0.004)
        box(A, (0.2, 0.14, 0.003), (0.01, 0, 0.044), SCRS[g], bevel=0)
    elif k == "folding":
        bx(A, 0.2, 0.14, 0.01, 0, 0.05, 0.0, "hull_dark", 0.003); bx(A, 0.2, 0.01, 0.14, 0, -0.02, 0.0, "hull_dark", 0.003); box(A, (0.18, 0.003, 0.12), (0, -0.026, 0.07), SCRS[g], bevel=0)
    else:
        bx(A, 0.14, 0.1, 0.01, 0, 0, 0.0, "hull_dark", 0.003); box(A, (0.12, 0.002, 0.09), (0, 0, 0.12), "glass_cyan", (0.2, 0, 0), 0); strip(A, 0.1, 0.01, 0.003, 0, 0, 0.011, GLOWS[g])


@family("cup", "decor", [{"n": "mug", "glow": "amber"}, {"n": "flask", "glow": "cyan"}, {"n": "tumbler", "glow": "magenta"}],
        cat="decor", place="surface", tags=["decor"])
def _cup(A, v):
    k, g = v["n"], v["glow"]
    if k == "mug":
        cy(A, 0.04, 0.09, 0, 0, 0.0, "hull", verts=16); tor(A, 0.03, 0.007, (0.045, 0, 0.05), "hull", rot=(PI / 2, 0, 0), seg=12, minor=5); cy(A, 0.036, 0.004, 0, 0, 0.088, "neon_amber", verts=14)
    elif k == "flask":
        cy(A, 0.035, 0.14, 0, 0, 0.0, "steel", verts=16); cy(A, 0.03, 0.03, 0, 0, 0.14, "gunmetal", verts=12); tor(A, 0.036, 0.004, (0, 0, 0.06), GLOWS[g], seg=18, minor=4)
    else:
        cyl(A, 0.045, 0.12, (0, 0, 0.06), "glass_cyan", r2=0.035, verts=16); cy(A, 0.04, 0.07, 0, 0, 0.01, GLOWS[g], r2=0.03, verts=14)


@family("holo_cube", "decor", [{"n": "rotating", "glow": "cyan"}, {"n": "planet_proj", "glow": "blue"}, {"n": "logo_prism", "glow": "magenta"}],
        cat="decor", place="surface", tags=["decor", "light", "glow"], light=0.3, lightY=0.2)
def _hcube(A, v):
    k, g = v["n"], v["glow"]
    cy(A, 0.07, 0.025, 0, 0, 0.0, "gunmetal", verts=20); tor(A, 0.06, 0.005, (0, 0, 0.026), GLOWS[g], seg=20, minor=4)
    if k == "rotating":
        box(A, (0.1, 0.1, 0.1), (0, 0, 0.13), "glass_cyan", (0.6, 0.6, 0.3), 0); box(A, (0.05, 0.05, 0.05), (0, 0, 0.13), GLOWS[g], (0.3, 0.2, 0.6), 0)
    elif k == "planet_proj":
        sph(A, 0.06, (0, 0, 0.14), "scr_blue", seg=14); tor(A, 0.1, 0.004, (0, 0, 0.14), GLOWS[g], seg=28, minor=4, rot=(0.4, 0, 0))
    else:
        prism(A, [(-0.06, 0), (0.06, 0), (0, 0.11)], 0.04, (0, 0, 0.1), GLOWS[g], rot=(0, 0, 0), bevel=0) if False else cyl(A, 0.06, 0.12, (0, 0, 0.1), GLOWS[g], r2=0.0, verts=3)


@family("minibot", "decor", [{"n": "crawler", "glow": "cyan"}, {"n": "ball", "glow": "amber"}, {"n": "desk_buddy", "glow": "green"}],
        cat="decor", place="surface", tags=["decor"])
def _mbot(A, v):
    k, g = v["n"], v["glow"]
    if k == "crawler":
        bx(A, 0.14, 0.2, 0.05, 0, 0, 0.03, "hull", 0.015); [cy(A, 0.03, 0.03, s * 0.09, y, 0.0, "rubber", verts=10, rot=(0, PI / 2, 0)) for s in (-1, 1) for y in (-0.07, 0.07)]; sph(A, 0.02, (0, -0.09, 0.07), GLOWS[g], seg=6)
    elif k == "ball":
        sph(A, 0.07, (0, 0, 0.07), "p_orange", seg=14); tor(A, 0.07, 0.004, (0, 0, 0.07), "gunmetal", seg=24, minor=4); sph(A, 0.02, (0, -0.065, 0.09), GLOWS[g], seg=6)
    else:
        cy(A, 0.05, 0.02, 0, 0, 0.0, "gunmetal", verts=12); bx(A, 0.08, 0.06, 0.07, 0, 0, 0.02, "hull", 0.01); bx(A, 0.1, 0.08, 0.07, 0, 0, 0.09, "hull", 0.015); bx(A, 0.07, 0.01, 0.02, 0, -0.045, 0.12, GLOWS[g], 0)
        [limb(A, (s * 0.05, 0, 0.07), (s * 0.08, -0.03, 0.04), 0.008, 0.006, "gunmetal", 5) for s in (-1, 1)]


@family("vial_set", "decor", [{"n": "rack_of_four", "glow": "green"}, {"n": "sample_tray", "glow": "cyan"}, {"n": "single_ampoule", "glow": "magenta"}],
        cat="decor", place="surface", tags=["decor"])
def _vial(A, v):
    k, g = v["n"], v["glow"]
    if k == "rack_of_four":
        bx(A, 0.22, 0.07, 0.025, 0, 0, 0.0, "hull_dark", 0.005)
        for i in range(4): cy(A, 0.012, 0.09, -0.08 + i * 0.054, 0, 0.025, "glass_cyan", verts=8); cy(A, 0.009, 0.05, -0.08 + i * 0.054, 0, 0.03, [GLOWS[g], "neon_amber", "neon_cyan", "neon_magenta"][i], verts=8)
    elif k == "sample_tray":
        bx(A, 0.24, 0.16, 0.02, 0, 0, 0.0, "hull", 0.004)
        for i in range(3):
            for j in range(2): cy(A, 0.02, 0.025, -0.07 + i * 0.07, -0.04 + j * 0.08, 0.02, "glass_cyan", verts=10); cy(A, 0.015, 0.012, -0.07 + i * 0.07, -0.04 + j * 0.08, 0.025, GLOWS[g] if (i + j) % 2 else "neon_white", verts=8)
    else:
        cy(A, 0.02, 0.1, 0, 0, 0.0, "glass_cyan", verts=10); cy(A, 0.016, 0.06, 0, 0, 0.005, GLOWS[g], verts=8); cy(A, 0.008, 0.03, 0, 0, 0.1, "glass_cyan", r2=0.003, verts=8)


@family("ship_model", "decor", [{"n": "cruiser", "glow": "cyan"}, {"n": "fighter", "glow": "red"}, {"n": "station_ring", "glow": "amber"}],
        cat="decor", place="surface", tags=["decor"])
def _sm(A, v):
    k, g = v["n"], v["glow"]
    cy(A, 0.07, 0.02, 0, 0, 0.0, "gunmetal", verts=16); cy(A, 0.008, 0.07, 0, 0, 0.02, "chrome", verts=6)
    if k == "cruiser":
        bx(A, 0.06, 0.28, 0.04, 0, 0, 0.09, "hull", 0.01); prism(A, [(-0.1, -0.02), (0.1, -0.02), (0.0, 0.07)], 0.03, (0, 0.04, 0.1), "hull_grey", rot=(PI / 2, 0, 0), bevel=0.003) if False else bx(A, 0.2, 0.06, 0.012, 0, 0.06, 0.1, "hull_grey", 0.003)
        strip(A, 0.012, 0.02, 0.012, -0.015, 0.14, 0.1, GLOWS[g]); strip(A, 0.012, 0.02, 0.012, 0.015, 0.14, 0.1, GLOWS[g])
    elif k == "fighter":
        bx(A, 0.04, 0.2, 0.03, 0, 0, 0.09, "hull", 0.008); prism(A, [(-0.1, 0), (0.1, 0), (0.03, 0.12), (-0.03, 0.12)], 0.01, (0, 0.0, 0.1), "hull_grey", rot=(PI / 2, 0, 0), bevel=0.002); strip(A, 0.02, 0.01, 0.01, 0, 0.11, 0.09, GLOWS[g])
    else:
        tor(A, 0.11, 0.012, (0, 0, 0.11), "steel", seg=32, minor=6); cy(A, 0.02, 0.1, 0, 0, 0.06, "hull", verts=10); [limb(A, (0, 0, 0.11), (0.11 * math.cos(a), 0.11 * math.sin(a), 0.11), 0.004, 0.004, "chrome", 4) for a in (0, 1.57, 3.14, 4.71)]
        sph(A, 0.025, (0, 0, 0.11), GLOWS[g], seg=8)


@family("cable_bundle", "decor", [{"n": "coil", "glow": "cyan"}, {"n": "tangle_floor", "glow": "magenta"}, {"n": "spool", "glow": "amber"}],
        cat="decor", place="floor", tags=["decor", "flat"])
def _cab(A, v):
    k, g = v["n"], v["glow"]
    if k == "coil":
        for i in range(4): tor(A, 0.18 - i * 0.02, 0.014, (0, 0, 0.014 + i * 0.026), "rubber", seg=24, minor=6)
        limb(A, (0.18, 0, 0.014), (0.5, 0.05, 0.014), 0.014, 0.014, GLOWS[g], 5)
    elif k == "tangle_floor":
        pts = [(-0.4, -0.1), (-0.2, 0.1), (0.0, -0.1), (0.2, 0.1), (0.4, -0.05)]
        for (a, b), (c, d) in zip(pts[:-1], pts[1:]): limb(A, (a, b, 0.014), (c, d, 0.014), 0.014, 0.014, "rubber", 5)
        for (a, b), (c, d) in zip(pts[:-1], pts[1:]): limb(A, (a, b + 0.04, 0.014), (c, d + 0.04, 0.014), 0.01, 0.01, GLOWS[g], 5)
    else:
        cy(A, 0.2, 0.04, 0, 0, 0.0, "hull_grey", verts=24); cy(A, 0.2, 0.04, 0, 0, 0.26, "hull_grey", verts=24); cy(A, 0.12, 0.22, 0, 0, 0.04, "rubber", verts=20); tor(A, 0.12, 0.01, (0, 0, 0.15), GLOWS[g], seg=24, minor=4)
