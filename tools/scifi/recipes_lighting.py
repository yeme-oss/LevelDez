# ============ LIGHTING: neon signs, strips, wall lights, beacons (pack-only types) ============

@family("neon_sign", "lighting", [{"n": "arrow", "glow": "magenta"}, {"n": "bowl", "glow": "red"}, {"n": "ring", "glow": "cyan"}, {"n": "triangle", "glow": "amber"}, {"n": "hex", "glow": "green"}, {"n": "bars", "glow": "violet"}, {"n": "glyphs", "glow": "cyan"}, {"n": "cross", "glow": "red"}],
        cat="light", place="wall", y=2.0, tags=["decor", "light", "glow", "wallart"], light=0.7, lightY=0.0)
def _neon(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]; t = 0.025
    bx(A, 1.0, 0.04, 0.6, 0, 0.0, 0.0, "hull_dark", 0.01)  # backing plate
    def seg(x0, z0, x1, z1): limb(A, (x0, -0.04, z0), (x1, -0.04, z1), t, t, m, 6)
    if k == "arrow":
        seg(-0.4, 0.3, 0.3, 0.3); seg(0.3, 0.3, 0.1, 0.5); seg(0.3, 0.3, 0.1, 0.1); seg(-0.4, 0.15, 0.0, 0.15)
    elif k == "bowl":
        for i in range(12): a = math.radians(180 + i * 15); b = math.radians(180 + (i + 1) * 15); seg(0.3 * math.cos(a), 0.4 + 0.25 * math.sin(a), 0.3 * math.cos(b), 0.4 + 0.25 * math.sin(b))
        seg(-0.3, 0.4, 0.3, 0.4); seg(0.1, 0.4, 0.3, 0.55); seg(0.05, 0.4, 0.2, 0.55)
    elif k == "ring":
        tor(A, 0.22, t, (0, -0.04, 0.3), m, rot=(PI / 2, 0, 0), seg=32, minor=6); tor(A, 0.1, t, (0, -0.04, 0.3), "neon_white", rot=(PI / 2, 0, 0), seg=24, minor=6); seg(-0.45, 0.3, -0.28, 0.3); seg(0.28, 0.3, 0.45, 0.3)
    elif k == "triangle":
        seg(-0.25, 0.1, 0.25, 0.1); seg(0.25, 0.1, 0.0, 0.52); seg(0.0, 0.52, -0.25, 0.1); seg(0.0, 0.2, 0.0, 0.34); sph(A, 0.025, (0, -0.04, 0.16), m, seg=6)
    elif k == "hex":
        for i in range(6): a = math.radians(i * 60); b = math.radians((i + 1) * 60); seg(0.25 * math.cos(a), 0.3 + 0.25 * math.sin(a), 0.25 * math.cos(b), 0.3 + 0.25 * math.sin(b))
        seg(-0.1, 0.3, 0.1, 0.3); seg(0.0, 0.2, 0.0, 0.4)
    elif k == "bars":
        for i in range(7): h = 0.15 + ((i * 5) % 4) * 0.1; bx(A, 0.08, 0.03, h, -0.36 + i * 0.12, -0.035, 0.05, m, 0)
    elif k == "glyphs":
        for i in range(3):
            x = -0.3 + i * 0.3; seg(x - 0.08, 0.5, x + 0.08, 0.5); seg(x, 0.5, x, 0.1); seg(x - 0.08, 0.3, x + 0.08, 0.3) if i != 1 else seg(x - 0.08, 0.1, x + 0.08, 0.3)
    else:
        seg(0, 0.1, 0, 0.5); seg(-0.2, 0.3, 0.2, 0.3); tor(A, 0.28, t, (0, -0.04, 0.3), m, rot=(PI / 2, 0, 0), seg=32, minor=6)


@family("light_strip", "lighting", [{"n": "ceiling_bar", "glow": "white", "meta": {"place": "ceiling"}}, {"n": "ceiling_cross", "glow": "cyan", "meta": {"place": "ceiling"}}, {"n": "wall_run", "glow": "cyan", "meta": {"place": "wall", "y": 0.4}}, {"n": "wall_stairs", "glow": "magenta", "meta": {"place": "wall", "y": 1.0}}, {"n": "ceiling_panel_row", "glow": "white", "meta": {"place": "ceiling"}}],
        cat="light", tags=["decor", "light", "glow", "ceiling-decor"], light=0.9)
def _lstrip(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]
    if k == "ceiling_bar":
        bx(A, 1.8, 0.14, 0.05, 0, 0, 0.0, "hull_dark", 0.01); bx(A, 1.7, 0.08, 0.02, 0, 0, -0.01, m, 0); [bx(A, 0.04, 0.16, 0.06, x, 0, 0.0, "gunmetal", 0.005) for x in (-0.85, 0.85)]
    elif k == "ceiling_cross":
        bx(A, 1.6, 0.12, 0.05, 0, 0, 0.0, "hull_dark", 0.01); bx(A, 0.12, 1.6, 0.05, 0, 0, 0.0, "hull_dark", 0.01); bx(A, 1.5, 0.05, 0.02, 0, 0, -0.01, m, 0); bx(A, 0.05, 1.5, 0.02, 0, 0, -0.01, m, 0)
    elif k == "wall_run":
        bx(A, 2.0, 0.05, 0.1, 0, 0, 0.0, "hull_dark", 0.01); bx(A, 1.9, 0.02, 0.03, 0, -0.03, 0.035, m, 0)
    elif k == "wall_stairs":
        for i in range(6): bx(A, 0.5, 0.04, 0.03, -0.9 + i * 0.36, 0.0, i * 0.12, m, 0); bx(A, 0.1, 0.03, 0.03, -0.62 + i * 0.36, 0.0, i * 0.12, "hull_dark", 0)
    else:
        for i in range(4): bx(A, 0.5, 0.5, 0.04, -0.9 + i * 0.6, 0, 0.0, "hull", 0.01); bx(A, 0.44, 0.44, 0.012, -0.9 + i * 0.6, 0, -0.01, m, 0)


@family("wall_light", "lighting", [{"n": "box_sconce", "glow": "amber"}, {"n": "round_lamp", "glow": "cyan"}, {"n": "tube_pair", "glow": "white"}, {"n": "uplight_wing", "glow": "magenta"}, {"n": "porthole_glow", "glow": "green"}, {"n": "slit", "glow": "red"}],
        cat="light", place="wall", y=1.8, tags=["decor", "light", "glow"], light=0.8, lightY=0.0)
def _wlight(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]
    if k == "box_sconce":
        bx(A, 0.2, 0.1, 0.3, 0, 0, 0.0, "hull_dark", 0.02); bx(A, 0.14, 0.02, 0.22, 0, -0.06, 0.04, m, 0)
    elif k == "round_lamp":
        cyl(A, 0.12, 0.05, (0, 0, 0.12), "hull", rot=(PI / 2, 0, 0), verts=24); sph(A, 0.09, (0, -0.04, 0.12), m, scale=(1, 0.5, 1), seg=14)
    elif k == "tube_pair":
        for s in (-1, 1): bx(A, 0.04, 0.04, 0.5, s * 0.05, 0, 0.0, m, 0.0)
        bx(A, 0.18, 0.04, 0.05, 0, 0.02, 0.0, "gunmetal", 0.005); bx(A, 0.18, 0.04, 0.05, 0, 0.02, 0.45, "gunmetal", 0.005)
    elif k == "uplight_wing":
        prism(A, [(-0.25, 0), (0.25, 0), (0.18, 0.15), (-0.18, 0.15)], 0.1, (0, 0, 0.1), "hull_dark", bevel=0.01); bx(A, 0.4, 0.03, 0.02, 0, -0.01, 0.2, m, 0); bx(A, 0.1, 0.1, 0.1, 0, 0.0, 0.0, "gunmetal")
    elif k == "porthole_glow":
        tor(A, 0.14, 0.03, (0, 0, 0.15), "steel", rot=(PI / 2, 0, 0), seg=28, minor=8); cyl(A, 0.13, 0.03, (0, 0.0, 0.15), m, rot=(PI / 2, 0, 0), verts=24)
    else:
        bx(A, 0.6, 0.06, 0.09, 0, 0, 0.0, "hull_dark", 0.01); bx(A, 0.56, 0.02, 0.03, 0, -0.035, 0.03, m, 0)


@family("holo_lamp", "lighting", [{"n": "cube", "glow": "cyan"}, {"n": "orbit", "glow": "magenta"}, {"n": "cone_beam", "glow": "green"}],
        cat="light", place="surface", tags=["decor", "light", "glow"], light=0.5, lightY=0.3)
def _hlamp(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]
    cy(A, 0.1, 0.03, 0, 0, 0.0, "gunmetal", verts=20); tor(A, 0.08, 0.006, (0, 0, 0.035), m, seg=24, minor=5)
    if k == "cube":
        box(A, (0.14, 0.14, 0.14), (0, 0, 0.17), "glass_cyan", (0.5, 0.5, 0.0), 0); sph(A, 0.03, (0, 0, 0.17), m, seg=8)
    elif k == "orbit":
        sph(A, 0.05, (0, 0, 0.2), m, seg=12); tor(A, 0.1, 0.004, (0, 0, 0.2), "chrome", seg=28, minor=4, rot=(0.5, 0, 0)); sph(A, 0.015, (0.1, 0, 0.2), "neon_white", seg=6)
    else:
        cyl(A, 0.08, 0.25, (0, 0, 0.17), "glass_cyan", r2=0.01, verts=16); cy(A, 0.02, 0.2, 0, 0, 0.04, m)


@family("floor_uplight", "lighting", [{"n": "wedge", "glow": "cyan"}, {"n": "column", "glow": "magenta"}, {"n": "ground_pod", "glow": "amber"}],
        cat="light", place="floor", tags=["decor", "light", "glow", "corner"], light=1.0, lightY=1.2)
def _upl(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]
    if k == "wedge":
        prism(A, [(-0.15, 0), (0.15, 0), (0.1, 1.6), (-0.1, 1.6)], 0.12, (0, 0, 0.0), "hull_dark", bevel=0.01); bx(A, 0.06, 0.02, 1.4, 0, -0.07, 0.1, m, 0)
    elif k == "column":
        cy(A, 0.1, 1.8, 0, 0, 0.0, "hull_dark", verts=16); cy(A, 0.06, 1.6, 0, 0, 0.1, m, verts=12); cy(A, 0.12, 0.05, 0, 0, 0.0, "gunmetal", verts=16); cy(A, 0.12, 0.05, 0, 0, 1.8, "gunmetal", verts=16)
    else:
        cy(A, 0.25, 0.18, 0, 0, 0.0, "hull_dark", r2=0.2, verts=24); cy(A, 0.2, 0.02, 0, 0, 0.18, m, verts=24); tor(A, 0.22, 0.01, (0, 0, 0.1), "steel", seg=28, minor=5)


@family("beacon", "lighting", [{"n": "warning_red", "glow": "red", "meta": {"place": "wall", "y": 2.3}}, {"n": "rotary_amber", "glow": "amber", "meta": {"place": "ceiling"}}, {"n": "status_ring", "glow": "green", "meta": {"place": "wall", "y": 1.9}}, {"n": "alarm_panel", "glow": "red", "meta": {"place": "wall", "y": 2.0}}],
        cat="light", tags=["decor", "light", "glow"], light=0.6)
def _beacon(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]
    if k == "warning_red":
        bx(A, 0.14, 0.06, 0.14, 0, 0, 0.0, "hull_dark", 0.01); sph(A, 0.07, (0, -0.06, 0.07), m, seg=12)
    elif k == "rotary_amber":
        cy(A, 0.1, 0.05, 0, 0, 0.12, "gunmetal", verts=18); cy(A, 0.08, 0.12, 0, 0, 0.0, m, verts=16); bx(A, 0.12, 0.01, 0.01, 0, 0, 0.06, "hull_dark")
    elif k == "status_ring":
        tor(A, 0.1, 0.02, (0, 0, 0.1), m, rot=(PI / 2, 0, 0), seg=28, minor=6); cyl(A, 0.12, 0.04, (0, 0.02, 0.1), "hull_dark", rot=(PI / 2, 0, 0), verts=24)
    else:
        bx(A, 0.35, 0.05, 0.25, 0, 0, 0.0, "hull", 0.015); bx(A, 0.3, 0.02, 0.08, 0, -0.03, 0.14, m, 0); [cyl(A, 0.025, 0.02, (-0.1 + i * 0.1, -0.03, 0.06), "p_red" if i != 1 else "p_yellow", rot=(PI / 2, 0, 0), verts=10) for i in range(3)]
