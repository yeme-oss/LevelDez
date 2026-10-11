# ============ TABLES: dining_table, desk, coffee_table, side_table, tv_unit ============

@family("dining_table", "furniture", [{"n": "slab", "glow": "cyan"}, {"n": "pedestal", "glow": "magenta"}, {"n": "holo_ring", "glow": "amber"}, {"n": "mess_hall", "glow": "green"}, {"n": "glass_top", "glow": "violet"}],
        cat="table", place="floor", tags=["table", "holds-decor", "center"], **{"as": "dining_table"})
def _dt(A, v):
    k, g = v["n"], v["glow"]
    W, D, H = 1.8, 0.95, 0.75
    if k == "slab":
        for sx in (-1, 1): bx(A, 0.08, D - 0.25, H - 0.06, sx * (W / 2 - 0.2), 0, 0.0, "gunmetal", 0.01)
        bx(A, W, D, 0.06, 0, 0, H - 0.06, "hull", 0.02); strip(A, W - 0.1, 0.012, 0.014, 0, -D / 2 + 0.005, H - 0.075, GLOWS[g]); bx(A, W - 0.5, 0.04, 0.04, 0, 0, 0.15, "gunmetal")
    elif k == "pedestal":
        cy(A, 0.35, 0.05, 0, 0, 0.0, "gunmetal", verts=24); cy(A, 0.1, H - 0.1, 0, 0, 0.05, "chrome", r2=0.07)
        bx(A, W, D, 0.06, 0, 0, H - 0.06, "hull", 0.04); tor(A, 0.33, 0.01, (0, 0, 0.04), GLOWS[g], seg=32, minor=6); strip(A, W - 0.1, D - 0.1, 0.01, 0, 0, H - 0.07, GLOWS[g])
    elif k == "holo_ring":
        bx(A, W, D, 0.06, 0, 0, H - 0.06, "hull_dark", 0.02); legs4(A, W, D, H - 0.06, 0.07, "gunmetal", 0.1)
        cy(A, 0.18, 0.012, 0, 0, H, "hull_grey", verts=28); tor(A, 0.18, 0.01, (0, 0, H + 0.01), GLOWS[g], seg=32, minor=6)
        cy(A, 0.12, 0.28, 0, 0, H + 0.01, "glass_cyan", r2=0.04, verts=20)
    elif k == "mess_hall":
        bx(A, W, D, 0.05, 0, 0, H - 0.05, "steel", 0.015); bx(A, 0.1, D - 0.1, H - 0.05, 0, 0, 0.0, "hull_dark", 0.01)
        for sy in (-1, 1): bx(A, W - 0.2, 0.05, 0.04, 0, sy * (D / 2 - 0.05), H - 0.02, "hull_grey", 0.01)
        bx(A, W - 0.1, 0.012, 0.014, 0, -D / 2 + 0.01, H - 0.07, GLOWS[g] if False else "neon_amber", 0) if False else strip(A, W - 0.1, 0.012, 0.014, 0, -D / 2, H - 0.07, GLOWS[g])
    else:  # glass_top
        legs4(A, W, D, H - 0.03, 0.05, "chrome", 0.08); box(A, (W, D, 0.03), (0, 0, H - 0.015), "glass_cyan", bevel=0.005); bx(A, W - 0.3, D - 0.3, 0.03, 0, 0, 0.3, "hull_dark", 0.005)
        for sx in (-1, 1): bx(A, 0.04, D - 0.2, 0.04, sx * (W / 2 - 0.15), 0, H - 0.06, "chrome"); strip(A, 0.012, D - 0.3, 0.012, sx * (W / 2 - 0.15), 0, H - 0.065, GLOWS[g])


@family("desk", "furniture", [{"n": "console", "glow": "cyan"}, {"n": "drafting", "glow": "amber"}, {"n": "corner_tech", "glow": "magenta"}, {"n": "floating", "glow": "green"}, {"n": "terminal", "glow": "violet"}, {"n": "workbench", "glow": "red"}],
        cat="table", place="floor", tags=["table", "holds-decor", "wall-hug", "desk"], **{"as": "desk"})
def _desk(A, v):
    k, g = v["n"], v["glow"]
    W, D, H = 1.4, 0.7, 0.75
    if k == "console":
        bx(A, W, D, 0.05, 0, 0, H - 0.05, "hull", 0.02); bx(A, 0.5, D - 0.1, H - 0.05, W / 2 - 0.3, 0, 0.0, "hull_dark", 0.02)
        for i in range(3): bx(A, 0.42, 0.012, 0.15, W / 2 - 0.3, -D / 2 + 0.04, 0.1 + i * 0.2, "hull_grey", 0.01)
        bx(A, 0.06, D - 0.1, H - 0.05, -W / 2 + 0.1, 0, 0.0, "gunmetal", 0.01); strip(A, W - 0.1, 0.012, 0.014, 0, -D / 2 + 0.005, H - 0.065, GLOWS[g])
        screen(A, 0.6, 0.36, -0.15, D / 2 - 0.12, H, SCRS[g], "hull_dark", face=-1)
    elif k == "drafting":
        legs4(A, W, D, H - 0.05, 0.05, "gunmetal", 0.05); prism(A, [(-W / 2, 0), (W / 2, 0), (W / 2, 0.04), (-W / 2, 0.04)], D, (0, 0, H - 0.04), "hull", bevel=0.01) if False else bx(A, W, D, 0.04, 0, 0, H - 0.04, "hull", 0.015)
        box(A, (W - 0.2, D - 0.2, 0.01), (0, 0, H + 0.005), "scr_blue", bevel=0); tor(A, 0.02, 0.01, (0, 0, H + 0.02), "chrome", seg=10, minor=6)
        strip(A, W - 0.1, 0.012, 0.014, 0, -D / 2 + 0.005, H - 0.055, GLOWS[g])
    elif k == "corner_tech":
        bx(A, W, D, 0.05, 0, 0, H - 0.05, "hull_dark", 0.02); legs4(A, W, D, H - 0.05, 0.05, "chrome", 0.05)
        for sx in (-1, 0, 1): screen(A, 0.4, 0.28, sx * 0.42, D / 2 - 0.1, H + 0.02, SCRS[g] if sx else "scr_green", "hull_dark", face=-1) if False else screen(A, 0.4, 0.28, sx * 0.44, D / 2 - 0.1, H + 0.04, SCRS[g] if sx else "scr_green", "hull_dark", face=-1)
        bx(A, 0.5, 0.18, 0.015, 0, -0.15, H, "carbon", 0.005); strip(A, W - 0.1, 0.012, 0.014, 0, -D / 2 + 0.005, H - 0.065, GLOWS[g])
    elif k == "floating":
        bx(A, W, D, 0.05, 0, 0.0, H - 0.05, "hull", 0.02); bx(A, 0.12, 0.12, H - 0.05, 0, D / 2 - 0.1, 0.0, "gunmetal", 0.01); strip(A, W - 0.1, D - 0.1, 0.012, 0, 0, H - 0.062, GLOWS[g])
        bx(A, 0.35, 0.02, 0.2, 0.3, 0, H, "glass_cyan", 0.0) if False else box(A, (0.5, 0.01, 0.3), (0.3, 0.1, H + 0.3), "glass_cyan", (0.2, 0, 0), 0)
    elif k == "terminal":
        bx(A, W, D, 0.05, 0, 0, H - 0.05, "hull_grey", 0.02); bx(A, W - 0.1, D - 0.1, H - 0.05, 0, 0, 0.0, "hull_dark", 0.02)
        prism(A, [(-0.45, 0), (0.45, 0), (0.45, 0.45), (0.3, 0.55), (-0.3, 0.55), (-0.45, 0.45)], 0.06, (0, D / 2 - 0.08, H), "hull", bevel=0.02)
        box(A, (0.78, 0.004, 0.38), (0, D / 2 - 0.112, H + 0.28), SCRS[g], bevel=0); bx(A, 0.6, 0.2, 0.01, 0, -0.1, H, "carbon", 0.003)
    else:  # workbench
        bx(A, W, D, 0.06, 0, 0, H - 0.06, "steel", 0.015); legs4(A, W, D, H - 0.06, 0.07, "p_orange", 0.04); bx(A, W - 0.2, D - 0.2, 0.03, 0, 0, 0.2, "hull_grey", 0.01)
        bx(A, W, 0.03, 0.4, 0, D / 2 - 0.015, H, "hull_dark", 0.01)
        for i in range(5): bx(A, 0.03, 0.02, 0.2, -0.5 + i * 0.25, D / 2 - 0.04, H + 0.05, "chrome", 0.005)
        strip(A, W - 0.1, 0.012, 0.014, 0, -D / 2 + 0.005, H - 0.075, GLOWS[g])


@family("coffee_table", "furniture", [{"n": "glass_ring", "glow": "cyan"}, {"n": "monolith", "glow": "magenta"}, {"n": "hover_disc", "glow": "amber"}, {"n": "nested", "glow": "green"}],
        cat="table", place="floor", tags=["table", "holds-decor", "center"], **{"as": "coffee_table"})
def _ct(A, v):
    k, g = v["n"], v["glow"]
    if k == "glass_ring":
        cy(A, 0.4, 0.03, 0, 0, 0.39, "glass_cyan", verts=32); tor(A, 0.4, 0.015, (0, 0, 0.4), "chrome", seg=32, minor=8)
        for i in range(3):
            a = 2 * PI * i / 3; cy(A, 0.025, 0.4, 0.32 * math.cos(a), 0.32 * math.sin(a), 0.0, "chrome")
        tor(A, 0.3, 0.008, (0, 0, 0.05), GLOWS[g], seg=32, minor=6)
    elif k == "monolith":
        bx(A, 1.0, 0.6, 0.38, 0, 0, 0.0, "hull_dark", 0.03); bx(A, 1.06, 0.66, 0.04, 0, 0, 0.38, "hull", 0.02); strip(A, 0.96, 0.012, 0.02, 0, -0.306, 0.18, GLOWS[g])
    elif k == "hover_disc":
        cy(A, 0.4, 0.04, 0, 0, 0.36, "hull", verts=32); cy(A, 0.3, 0.012, 0, 0, 0.34, GLOWS[g], verts=32); cy(A, 0.12, 0.1, 0, 0, 0.0, "gunmetal", verts=20); cy(A, 0.06, 0.3, 0, 0, 0.05, "chrome")
    else:
        bx(A, 1.0, 0.6, 0.04, 0, 0, 0.38, "hull", 0.015); bx(A, 0.6, 0.4, 0.04, 0.1, 0, 0.26, "hull_grey", 0.015); legs4(A, 1.0, 0.6, 0.38, 0.04, "gunmetal", 0.04); strip(A, 0.9, 0.012, 0.012, 0, -0.3, 0.37, GLOWS[g])


@family("side_table", "furniture", [{"n": "cylinder", "glow": "cyan"}, {"n": "cube_pad", "glow": "magenta"}, {"n": "tripod", "glow": "amber"}, {"n": "terminal_stand", "glow": "green"}],
        cat="table", place="floor", tags=["table", "holds-decor", "beside"], **{"as": "side_table"})
def _st(A, v):
    k, g = v["n"], v["glow"]
    if k == "cylinder":
        cy(A, 0.22, 0.55, 0, 0, 0.0, "hull", verts=28); tor(A, 0.22, 0.008, (0, 0, 0.05), GLOWS[g], seg=32, minor=6); cy(A, 0.23, 0.03, 0, 0, 0.52, "gunmetal", verts=28)
    elif k == "cube_pad":
        bx(A, 0.45, 0.45, 0.55, 0, 0, 0.0, "hull_dark", 0.04); strip(A, 0.4, 0.4, 0.012, 0, 0, 0.0, GLOWS[g]); bx(A, 0.39, 0.39, 0.02, 0, 0, 0.55, "hull", 0.01)
    elif k == "tripod":
        for i in range(3):
            a = 2 * PI * i / 3 + 0.5; limb(A, (0.2 * math.cos(a), 0.2 * math.sin(a), 0.0), (0.05 * math.cos(a), 0.05 * math.sin(a), 0.52), 0.014, 0.012, "chrome", 6)
        cy(A, 0.23, 0.03, 0, 0, 0.52, "hull", verts=28); tor(A, 0.2, 0.006, (0, 0, 0.545), GLOWS[g], seg=28, minor=6)
    else:
        cy(A, 0.18, 0.04, 0, 0, 0.0, "gunmetal", verts=20); cy(A, 0.04, 0.4, 0, 0, 0.04, "chrome"); bx(A, 0.45, 0.45, 0.04, 0, 0, 0.51, "hull", 0.015); screen(A, 0.28, 0.14, 0, 0.05, 0.56, SCRS[g], "hull_dark", face=-1)


@family("tv_unit", "furniture", [{"n": "wall_screen", "glow": "cyan"}, {"n": "media_console", "glow": "magenta"}, {"n": "holo_stand", "glow": "amber"}],
        cat="media", place="floor", tags=["media", "wall-hug", "faces-center", "focal"], **{"as": "tv_unit"})
def _tv(A, v):
    k, g = v["n"], v["glow"]
    W, D = 1.6, 0.42
    if k == "wall_screen":
        bx(A, W, D, 0.4, 0, 0, 0.0, "hull", 0.03); bx(A, 1.5, 0.05, 0.8, 0, 0.1, 0.4, "hull_dark", 0.02); box(A, (1.46, 0.004, 0.76), (0, 0.073, 0.8), "scr_blue", bevel=0)
        strip(A, W - 0.1, 0.012, 0.016, 0, -D / 2 - 0.005, 0.03, GLOWS[g]); bx(A, 0.5, 0.012, 0.1, 0, -D / 2 - 0.005, 0.18, "hull_grey")
    elif k == "media_console":
        legs4(A, W, D, 0.12, 0.05, "gunmetal"); bx(A, W, D, 0.28, 0, 0, 0.12, "hull_dark", 0.025); bx(A, W - 0.1, 0.012, 0.18, 0, -D / 2 - 0.005, 0.17, "hull_grey")
        screen(A, 1.2, 0.68, 0, 0.08, 0.4, "scr_cyan" if g == "cyan" else SCRS[g], "hull_dark", face=-1); strip(A, W - 0.1, 0.012, 0.014, 0, -D / 2 - 0.012, 0.13, GLOWS[g])
    else:
        bx(A, W, D, 0.35, 0, 0, 0.0, "hull", 0.04); cy(A, 0.28, 0.02, 0, 0, 0.35, "hull_grey", verts=28); tor(A, 0.28, 0.01, (0, 0, 0.37), GLOWS[g], seg=32, minor=6)
        box(A, (0.9, 0.01, 0.55), (0, 0.0, 0.95), "glass_cyan", bevel=0); strip(A, 0.9, 0.012, 0.012, 0, 0.0, 0.66, GLOWS[g]); strip(A, 0.9, 0.012, 0.012, 0, 0.0, 1.22, GLOWS[g])
