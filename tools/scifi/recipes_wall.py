# ============ WALL: holo posters (as painting), screens, vents, shelves, pipes, signage, panels ============

def _poster_frame(A, g, w=0.9, h=0.65):
    bx(A, w, 0.05, h, 0, 0, 0.0, "hull_dark", 0.01)
    box(A, (w - 0.06, 0.006, h - 0.06), (0, -0.027, h / 2), "scr_blue" if g in ("blue", "violet") else "screen_off", bevel=0)
    strip(A, w, 0.02, 0.012, 0, -0.03, 0.0, GLOWS[g]); strip(A, w, 0.02, 0.012, 0, -0.03, h - 0.012, GLOWS[g])


@family("holo_poster", "wall", [{"n": "planet", "glow": "cyan"}, {"n": "skyline", "glow": "magenta"}, {"n": "waveform", "glow": "green"}, {"n": "nebula", "glow": "violet"}, {"n": "ship", "glow": "amber"}, {"n": "circuit", "glow": "cyan"}, {"n": "mountains", "glow": "blue"}, {"n": "eye", "glow": "red"}],
        cat="wallart", place="wall", y=1.45, tags=["wallart", "decor", "art", "light", "glow"], light=0.25, lightY=0.35, **{"as": "painting"})
def _poster(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]
    _poster_frame(A, g)
    X = -0.03
    if k == "planet":
        sph(A, 0.2, (0, X, 0.33), "scr_blue", seg=20); tor(A, 0.33, 0.012, (0, X, 0.33), m, rot=(PI / 2 + 0.4, 0, 0.3), seg=40, minor=5)
        for i in range(10): sph(A, 0.008, (-0.38 + (i * 0.37) % 0.76, X, 0.08 + (i * 0.23) % 0.5), "neon_white", seg=5)
    elif k == "skyline":
        for i in range(12): h = 0.1 + ((i * 7) % 5) * 0.08; bx(A, 0.055, 0.012, h, -0.38 + i * 0.07, X, 0.06, "carbon" if i % 2 else "hull_dark", 0); [strip(A, 0.01, 0.012, 0.01, -0.38 + i * 0.07, X - 0.005, 0.08 + j * 0.06, m) for j in range(int(h / 0.06))]
        cyl(A, 0.1, 0.012, (0.25, X, 0.5), "neon_amber", rot=(PI / 2, 0, 0), verts=20)
    elif k == "waveform":
        for i in range(25): h = 0.04 + abs(math.sin(i * 0.45)) * 0.3; bx(A, 0.018, 0.012, h, -0.36 + i * 0.03, X, 0.325 - h / 2, m, 0)
    elif k == "nebula":
        for i in range(40): a = i * 0.5; r = 0.02 + i * 0.008; sph(A, 0.012 + (i % 3) * 0.006, (r * math.cos(a), X, 0.33 + r * 0.7 * math.sin(a)), m if i % 3 else "neon_white", seg=5)
        sph(A, 0.06, (0, X, 0.33), "neon_white", seg=10)
    elif k == "ship":
        prism(A, [(-0.3, 0.0), (0.2, 0.0), (0.38, 0.06), (0.2, 0.12), (-0.3, 0.12), (-0.18, 0.06)], 0.012, (0, X, 0.27), m, bevel=0)
        prism(A, [(-0.1, 0.12), (0.1, 0.12), (0.0, 0.26)], 0.012, (0, X, 0.27), "neon_white", bevel=0); bx(A, 0.5, 0.012, 0.012, 0, X, 0.12, "neon_amber", 0)
    elif k == "circuit":
        for (x0, z0, w, h) in [(-0.35, 0.3, 0.4, 0.012), (0.05, 0.3, 0.012, -0.18), (0.05, 0.12, 0.3, 0.012), (-0.2, 0.3, 0.012, 0.18), (-0.2, 0.48, 0.45, 0.012)]:
            bx(A, abs(w), 0.012, abs(h), x0 + w / 2, X, min(z0, z0 + h), m, 0)
        for x, z in [(-0.35, 0.3), (0.35, 0.12), (0.25, 0.48)]: cyl(A, 0.03, 0.012, (x, X, z), "neon_white", rot=(PI / 2, 0, 0), verts=12)
    elif k == "mountains":
        prism(A, [(-0.4, 0.0), (-0.15, 0.3), (0.0, 0.12), (0.18, 0.36), (0.4, 0.0)], 0.012, (0, X, 0.06), "hull_grey", bevel=0); cyl(A, 0.1, 0.012, (-0.15, X, 0.5), m, rot=(PI / 2, 0, 0), verts=20)
    else:
        for r, mm in ((0.2, m), (0.12, "neon_white")): tor(A, r, 0.012, (0, X, 0.33), mm, rot=(PI / 2, 0, 0), seg=36, minor=5)
        sph(A, 0.05, (0, X, 0.33), "carbon", seg=10); bx(A, 0.7, 0.012, 0.012, 0, X, 0.33, m, 0)


@family("wall_screen", "wall", [{"n": "wide_blue", "glow": "blue"}, {"n": "tall_cyan", "glow": "cyan"}, {"n": "triple", "glow": "green"}, {"n": "status_board", "glow": "amber"}, {"n": "data_ticker", "glow": "magenta"}, {"n": "radar", "glow": "green"}],
        cat="wallart", place="wall", y=1.3, tags=["wallart", "decor", "light", "glow"], light=0.35, lightY=0.4)
def _wscr(A, v):
    k, g = v["n"], v["glow"]
    if k == "wide_blue":
        screen(A, 1.6, 0.9, 0, 0, 0.0, "scr_blue", "hull_dark", face=-1, t=0.05)
    elif k == "tall_cyan":
        screen(A, 0.6, 1.3, 0, 0, 0.0, SCRS[g], "hull_dark", face=-1, t=0.05)
    elif k == "triple":
        for i in range(3): screen(A, 0.6, 0.45, -0.65 + i * 0.65, 0, 0.0, SCRS[g] if i != 1 else "scr_cyan", "hull_dark", face=-1, t=0.05)
    elif k == "status_board":
        bx(A, 1.2, 0.05, 0.8, 0, 0, 0.0, "hull_dark", 0.01)
        for i in range(5): box(A, (1.0, 0.01, 0.07), (0, -0.03, 0.1 + i * 0.14), SCRS[g] if i % 2 else "scr_green", bevel=0)
        for i in range(5): bx(A, 0.06, 0.012, 0.06, -0.52, -0.03, 0.065 + i * 0.14, "neon_red" if i == 2 else "neon_green", 0)
    elif k == "data_ticker":
        bx(A, 1.6, 0.05, 0.22, 0, 0, 0.0, "hull_dark", 0.01); box(A, (1.52, 0.01, 0.14), (0, -0.03, 0.11), SCRS[g], bevel=0)
        for i in range(12): bx(A, 0.04 + (i % 3) * 0.02, 0.012, 0.08, -0.7 + i * 0.12, -0.035, 0.07, "neon_white", 0)
    else:
        cyl(A, 0.4, 0.05, (0, 0, 0.4), "hull_dark", rot=(PI / 2, 0, 0), verts=36); cyl(A, 0.36, 0.01, (0, -0.03, 0.4), "scr_green", rot=(PI / 2, 0, 0), verts=36)
        for r in (0.12, 0.24): tor(A, r, 0.004, (0, -0.036, 0.4), "neon_green", rot=(PI / 2, 0, 0), seg=32, minor=4)
        bx(A, 0.72, 0.01, 0.006, 0, -0.036, 0.4, "neon_green", 0); bx(A, 0.006, 0.01, 0.72, 0, -0.036, 0.04, "neon_green", 0); limb(A, (0, -0.037, 0.4), (0.2, -0.037, 0.55), 0.006, 0.006, "neon_white", 4)


@family("wall_vent", "wall", [{"n": "grille_square", "glow": "cyan"}, {"n": "louver_wide", "glow": "amber"}, {"n": "fan_round", "glow": "green"}, {"n": "duct_port", "glow": "red"}],
        cat="decor", place="wall", y=0.5, tags=["decor", "wallart"])
def _vent(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]
    if k == "grille_square":
        bx(A, 0.6, 0.06, 0.6, 0, 0, 0.0, "hull_grey", 0.01)
        for i in range(8): bx(A, 0.5, 0.02, 0.02, 0, -0.035, 0.07 + i * 0.065, "carbon", 0)
        strip(A, 0.5, 0.012, 0.012, 0, -0.04, 0.02, m)
    elif k == "louver_wide":
        bx(A, 1.2, 0.06, 0.35, 0, 0, 0.0, "hull_dark", 0.01)
        for i in range(5): bx(A, 1.1, 0.04, 0.025, 0, -0.04, 0.05 + i * 0.06, "hull_grey", 0, rot=(0.4, 0, 0))
        strip(A, 1.1, 0.012, 0.012, 0, -0.04, 0.01, m)
    elif k == "fan_round":
        cyl(A, 0.3, 0.08, (0, 0, 0.3), "hull_grey", rot=(PI / 2, 0, 0), verts=32); cyl(A, 0.26, 0.02, (0, -0.045, 0.3), "carbon", rot=(PI / 2, 0, 0), verts=32)
        for i in range(5): a = i * 2 * PI / 5; limb(A, (0, -0.06, 0.3), (0.22 * math.cos(a), -0.06, 0.3 + 0.22 * math.sin(a)), 0.03, 0.01, "steel", 5)
        tor(A, 0.3, 0.012, (0, -0.045, 0.3), m, rot=(PI / 2, 0, 0), seg=32, minor=5)
    else:
        bx(A, 0.5, 0.2, 0.5, 0, 0.0, 0.0, "hull_grey", 0.03); cyl(A, 0.2, 0.2, (0, -0.1, 0.25), "carbon", rot=(PI / 2, 0, 0), verts=24); tor(A, 0.21, 0.012, (0, -0.2, 0.25), m, rot=(PI / 2, 0, 0), seg=28, minor=5)


@family("wall_shelf", "wall", [{"n": "floating_plank", "glow": "cyan"}, {"n": "bracket_rack", "glow": "amber"}, {"n": "glass_shelf", "glow": "magenta"}, {"n": "cargo_net", "glow": "green"}],
        cat="wallart", place="wall", y=1.4, tags=["wallart", "decor", "holds-decor"], **{"as": "wall_shelf"})
def _wshelf(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]
    if k == "floating_plank":
        bx(A, 0.9, 0.2, 0.04, 0, 0.0, 0.0, "hull", 0.01); strip(A, 0.9, 0.012, 0.012, 0, -0.1, 0.0, m)
    elif k == "bracket_rack":
        bx(A, 0.9, 0.2, 0.03, 0, 0, 0.12, "steel", 0.005); [bx(A, 0.03, 0.2, 0.14, x, 0, 0.0, "gunmetal", 0.005) for x in (-0.35, 0.35)]; strip(A, 0.8, 0.012, 0.012, 0, -0.1, 0.12, m)
    elif k == "glass_shelf":
        box(A, (0.9, 0.2, 0.025), (0, 0, 0.1), "glass_cyan", bevel=0); [cy(A, 0.012, 0.1, x, -0.0, 0.0, "chrome", verts=8) for x in (-0.4, 0.4)]; strip(A, 0.9, 0.012, 0.012, 0, -0.1, 0.09, m)
    else:
        bx(A, 0.9, 0.2, 0.03, 0, 0, 0.0, "hull_grey", 0.005); [limb(A, (-0.4 + i * 0.1, -0.1, 0.0), (-0.4 + i * 0.1, -0.1, 0.22), 0.006, 0.006, "p_teal", 4) for i in range(9)]; bx(A, 0.9, 0.012, 0.012, 0, -0.1, 0.1, m, 0)


@family("pipe_run", "wall", [{"n": "horizontal_pair", "glow": "amber"}, {"n": "vertical_trunk", "glow": "cyan"}, {"n": "corner_manifold", "glow": "red"}, {"n": "valve_bank", "glow": "green"}],
        cat="decor", place="wall", y=0.2, tags=["decor", "wallart", "wall-hug"])
def _pipe(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]
    if k == "horizontal_pair":
        for z in (0.0, 0.16): cyl(A, 0.05, 2.0, (0, 0, 0.05 + z), "steel" if z else "p_orange", rot=(0, PI / 2, 0), verts=14)
        for x in (-0.8, 0.0, 0.8): bx(A, 0.04, 0.06, 0.26, x, 0.03, 0.0, "gunmetal", 0.005)
        tor(A, 0.055, 0.01, (0.4, 0, 0.05), m, rot=(0, PI / 2, 0), seg=14, minor=5)
    elif k == "vertical_trunk":
        for x in (-0.08, 0.08): cy(A, 0.06, 2.4, x, 0, 0.0, "steel" if x < 0 else "p_teal", verts=14)
        for z in (0.3, 1.2, 2.1): bx(A, 0.3, 0.04, 0.04, 0, 0.04, z, "gunmetal", 0.005)
        tor(A, 0.07, 0.012, (-0.08, 0, 1.2), m, seg=14, minor=5)
    elif k == "corner_manifold":
        cy(A, 0.06, 1.2, 0, 0, 0.0, "p_orange", verts=14); cyl(A, 0.06, 1.0, (0.5, 0, 1.2), "p_orange", rot=(0, PI / 2, 0), verts=14); sph(A, 0.075, (0, 0, 1.2), "p_orange", seg=12); tor(A, 0.07, 0.012, (0, 0, 0.5), m, seg=14, minor=5)
    else:
        cyl(A, 0.05, 1.4, (0, 0, 0.5), "steel", rot=(0, PI / 2, 0), verts=12)
        for i in range(4): x = -0.5 + i * 0.33; cy(A, 0.03, 0.2, x, -0.05, 0.5, "gunmetal", verts=8, rot=(PI / 2, 0, 0)); cy(A, 0.07, 0.03, x, -0.15, 0.5, "p_red" if i % 2 else "p_yellow", verts=12, rot=(PI / 2, 0, 0))
        strip(A, 1.2, 0.012, 0.012, 0, -0.01, 0.4, m)


@family("signage", "wall", [{"n": "exit_arrow", "glow": "green"}, {"n": "hazard_plate", "glow": "amber"}, {"n": "deck_number", "glow": "cyan"}, {"n": "no_entry", "glow": "red"}, {"n": "restricted_zone", "glow": "red"}],
        cat="wallart", place="wall", y=2.0, tags=["decor", "wallart", "light", "glow"], light=0.3, lightY=0.0)
def _sign(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]
    if k == "exit_arrow":
        bx(A, 0.6, 0.04, 0.22, 0, 0, 0.0, "hull_dark", 0.01); strip(A, 0.4, 0.012, 0.03, -0.05, -0.025, 0.095, m); limb(A, (0.15, -0.026, 0.11), (0.05, -0.026, 0.17), 0.012, 0.012, m, 5); limb(A, (0.15, -0.026, 0.11), (0.05, -0.026, 0.05), 0.012, 0.012, m, 5)
    elif k == "hazard_plate":
        bx(A, 0.5, 0.03, 0.5, 0, 0, 0.0, "p_yellow", 0.01); prism(A, [(-0.18, 0), (0.18, 0), (0, 0.31)], 0.012, (0, -0.02, 0.1), "carbon", bevel=0); bx(A, 0.03, 0.012, 0.12, 0, -0.03, 0.2, m, 0); sph(A, 0.02, (0, -0.03, 0.15), m, seg=6)
    elif k == "deck_number":
        bx(A, 0.5, 0.04, 0.3, 0, 0, 0.0, "hull_dark", 0.01); [bx(A, 0.06, 0.012, 0.18, -0.12 + i * 0.12, -0.026, 0.06, m, 0) for i in range(3)]; bx(A, 0.4, 0.012, 0.02, 0, -0.026, 0.25, m, 0)
    elif k == "no_entry":
        cyl(A, 0.2, 0.04, (0, 0, 0.2), "hull_dark", rot=(PI / 2, 0, 0), verts=28); tor(A, 0.17, 0.02, (0, -0.025, 0.2), m, rot=(PI / 2, 0, 0), seg=28, minor=6); bx(A, 0.28, 0.012, 0.04, 0, -0.03, 0.18, m, 0)
    else:
        bx(A, 0.9, 0.04, 0.3, 0, 0, 0.0, "hull_dark", 0.01)
        for i in range(6): box(A, (0.06, 0.012, 0.34), (-0.37 + i * 0.15, -0.026, 0.15), "p_yellow", (0, 0.6, 0), 0)
        bx(A, 0.8, 0.012, 0.06, 0, -0.03, 0.12, m, 0)


@family("control_panel", "wall", [{"n": "switch_bank", "glow": "amber"}, {"n": "touch_slab", "glow": "cyan"}, {"n": "door_keypad", "glow": "green"}],
        cat="wallart", place="wall", y=1.1, tags=["decor", "wallart", "light", "glow"], light=0.3, lightY=0.2)
def _cpan(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]
    if k == "switch_bank":
        bx(A, 0.6, 0.06, 0.4, 0, 0, 0.0, "hull_grey", 0.015)
        for i in range(6): bx(A, 0.04, 0.04, 0.1, -0.22 + i * 0.09, -0.04, 0.2, "chrome", 0.005); bx(A, 0.025, 0.012, 0.025, -0.22 + i * 0.09, -0.04, 0.1, m if i % 2 else "neon_red", 0)
        screen(A, 0.4, 0.1, 0, -0.03, 0.3, SCRS[g], "hull_dark", face=-1) if False else None
    elif k == "touch_slab":
        bx(A, 0.5, 0.04, 0.7, 0, 0, 0.0, "hull_dark", 0.015); box(A, (0.44, 0.006, 0.6), (0, -0.023, 0.35), SCRS[g], bevel=0); strip(A, 0.5, 0.012, 0.012, 0, -0.025, 0.0, m)
    else:
        bx(A, 0.22, 0.05, 0.34, 0, 0, 0.0, "hull_dark", 0.015); [bx(A, 0.045, 0.012, 0.045, -0.055 + (i % 3) * 0.055, -0.03, 0.04 + (i // 3) * 0.055, "hull_grey", 0.003) for i in range(9)]; strip(A, 0.16, 0.012, 0.02, 0, -0.03, 0.28, m)
