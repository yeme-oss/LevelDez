# ============ SIGNATURE PROPS: pack-only types that make the place read as sci-fi ============

@family("cryo_pod", "signature", [{"n": "upright", "glow": "cyan"}, {"n": "twin", "glow": "blue"}, {"n": "reclined", "glow": "green"}, {"n": "cracked", "glow": "red"}, {"n": "stasis_tube", "glow": "violet"}],
        cat="scifi", place="floor", tags=["decor", "wall-hug", "light", "glow"], light=0.7)
def _cryo(A, v):
    k, g = v["n"], v["glow"]
    if k == "upright":
        cy(A, 0.5, 0.15, 0, 0, 0.0, "gunmetal", verts=28); cy(A, 0.5, 0.15, 0, 0, 2.05, "gunmetal", verts=28)
        cy(A, 0.42, 1.9, 0, 0, 0.15, "glass_cyan", verts=28); cy(A, 0.28, 0.4, 0, 0, 0.15, "cloth", verts=20, r2=0.2)
        for i in range(4): a = i * PI / 2 + PI / 4; cy(A, 0.03, 1.9, 0.46 * math.cos(a), 0.46 * math.sin(a), 0.15, "steel", verts=8)
        tor(A, 0.5, 0.02, (0, 0, 0.17), GLOWS[g], seg=32, minor=6); tor(A, 0.5, 0.02, (0, 0, 2.03), GLOWS[g], seg=32, minor=6); screen(A, 0.4, 0.2, 0, -0.52, 0.5, SCRS[g], "hull_dark", face=-1)
        cy(A, 0.18, 0.5, 0, 0, 0.55, "foam", r2=0.12, verts=14); sph(A, 0.11, (0, 0, 1.3), "foam", seg=12)
    elif k == "twin":
        for sx in (-1, 1):
            x = sx * 0.5; bx(A, 0.8, 0.8, 0.2, x, 0, 0.0, "hull_dark", 0.03); bx(A, 0.8, 0.8, 0.1, x, 0, 2.05, "hull_dark", 0.03)
            box(A, (0.7, 0.7, 1.85), (x, 0, 1.075), "glass_cyan", bevel=0.03); strip(A, 0.6, 0.012, 0.03, x, -0.4, 0.22, GLOWS[g]); sph(A, 0.14, (x, 0, 1.4), "foam", seg=10); cy(A, 0.16, 0.7, x, 0, 0.5, "foam", r2=0.1, verts=12)
    elif k == "reclined":
        bx(A, 1.0, 2.2, 0.3, 0, 0, 0.0, "hull", 0.06); pad(A, 0.8, 1.9, 0.14, 0, 0, 0.3, "cloth", 0.05)
        prism(A, [(-0.5, 0.0), (0.5, 0.0), (0.42, 0.55), (0, 0.72), (-0.42, 0.55)], 1.6, (0, -0.2, 0.3), "glass_cyan", bevel=0.03); bx(A, 0.6, 0.1, 0.5, 0, 1.05, 0.3, "hull_dark", 0.03)
        strip(A, 0.012, 1.9, 0.02, -0.5, 0.0, 0.32, GLOWS[g]); strip(A, 0.012, 1.9, 0.02, 0.5, 0.0, 0.32, GLOWS[g])
    elif k == "cracked":
        cy(A, 0.5, 0.15, 0, 0, 0.0, "gunmetal", verts=28); cy(A, 0.5, 0.15, 0, 0, 2.05, "gunmetal", verts=28); cy(A, 0.42, 1.9, 0.0, 0.0, 0.15, "glass_cyan", verts=28)
        for i in range(5): limb(A, (0.4, -0.15 + i * 0.05, 0.6 + i * 0.25), (0.15, -0.3, 0.9 + i * 0.2), 0.008, 0.002, "carbon", 4)
        strip(A, 0.3, 0.02, 0.02, 0.0, -0.5, 1.0, "neon_red"); cy(A, 0.3, 0.05, 0, 0, 0.16, "hull_dark", verts=20); screen(A, 0.4, 0.2, 0, -0.52, 0.5, "scr_red", "hull_dark", face=-1)
    else:
        cy(A, 0.35, 0.2, 0, 0, 0.0, "gunmetal", verts=24); cy(A, 0.35, 0.2, 0, 0, 2.0, "gunmetal", verts=24); cy(A, 0.28, 1.8, 0, 0, 0.2, "glass_cyan", verts=24)
        cy(A, 0.2, 1.7, 0, 0, 0.25, GLOWS[g], r2=0.2, verts=20) if False else cy(A, 0.12, 1.6, 0, 0, 0.3, GLOWS[g], verts=16)
        tor(A, 0.3, 0.02, (0, 0, 0.8), "chrome", seg=28, minor=6); tor(A, 0.3, 0.02, (0, 0, 1.4), "chrome", seg=28, minor=6)


@family("command_console", "signature", [{"n": "bridge_main", "glow": "cyan"}, {"n": "nav_station", "glow": "amber"}, {"n": "tactical", "glow": "red"}, {"n": "comms", "glow": "green"}, {"n": "pilot_yoke", "glow": "magenta"}, {"n": "ops_desk", "glow": "blue"}],
        cat="scifi", place="floor", tags=["table", "holds-decor", "wall-hug", "desk"], light=0.5)
def _cmd(A, v):
    k, g = v["n"], v["glow"]
    if k == "bridge_main":
        prism(A, topview([(-1.1, -0.55), (1.1, -0.55), (1.3, 0.0), (0.9, 0.6), (-0.9, 0.6), (-1.3, 0.0)]), 0.9, (0, 0, 0.45), "hull_dark", rot=(PI / 2, 0, 0), bevel=0.03)
        prism(A, topview([(-1.15, -0.6), (1.15, -0.6), (1.35, 0.0), (0.95, 0.65), (-0.95, 0.65), (-1.35, 0.0)]), 0.06, (0, 0, 0.92), "hull", rot=(PI / 2, 0, 0), bevel=0.02)
        for i, x in enumerate((-0.7, 0, 0.7)): box(A, (0.55, 0.3, 0.02), (x, -0.2, 0.96), "scr_cyan" if i == 1 else SCRS[g], (-0.6, 0, 0), 0)
        screen(A, 1.4, 0.7, 0, 0.45, 0.95, "scr_blue", "hull_dark", face=-1)
        strip(A, 2.2, 0.02, 0.02, 0, -0.6, 0.4, GLOWS[g])
    elif k == "nav_station":
        bx(A, 1.2, 0.8, 0.8, 0, 0, 0.0, "hull_dark", 0.03); bx(A, 1.3, 0.9, 0.05, 0, 0, 0.8, "hull", 0.02); cy(A, 0.28, 0.03, 0.0, -0.05, 0.85, "carbon", verts=28)
        tor(A, 0.28, 0.01, (0, -0.05, 0.87), GLOWS[g], seg=36, minor=5); sph(A, 0.12, (0, -0.05, 1.05), GLOWS[g], seg=14); screen(A, 0.5, 0.35, -0.38, 0.32, 0.85, SCRS[g], "hull_dark", face=-1); screen(A, 0.5, 0.35, 0.38, 0.32, 0.85, "scr_green", "hull_dark", face=-1)
    elif k == "tactical":
        bx(A, 1.4, 0.8, 0.75, 0, 0, 0.0, "gunmetal", 0.03); prism(A, [(-0.7, 0), (0.7, 0), (0.7, 0.1), (-0.7, 0.1)], 0.8, (0, 0, 0.85), "carbon", bevel=0.02) if False else bx(A, 1.5, 0.9, 0.1, 0, 0, 0.75, "carbon", 0.02)
        box(A, (1.3, 0.7, 0.01), (0, 0, 0.855), "scr_red", bevel=0); cy(A, 0.1, 0.03, 0.3, 0.1, 0.86, "neon_amber", verts=16); cy(A, 0.06, 0.03, -0.3, -0.1, 0.86, "neon_white", verts=12); strip(A, 1.4, 0.02, 0.02, 0, -0.4, 0.4, GLOWS[g])
    elif k == "comms":
        bx(A, 1.1, 0.7, 0.8, 0, 0, 0.0, "hull", 0.03); bx(A, 1.2, 0.8, 0.04, 0, 0, 0.8, "hull_dark", 0.02); cy(A, 0.02, 0.4, -0.3, 0.25, 0.84, "chrome"); sph(A, 0.05, (-0.3, 0.25, 1.26), "chrome", seg=10)
        for i in range(8): bx(A, 0.06, 0.04, 0.02, -0.1 + i * 0.09, -0.1, 0.84, GLOWS[g] if i % 3 else "hull_grey", 0.003)
        screen(A, 0.6, 0.35, 0.2, 0.3, 0.84, SCRS[g], "hull_dark", face=-1)
    elif k == "pilot_yoke":
        bx(A, 1.0, 0.8, 0.7, 0, 0, 0.0, "hull_dark", 0.04); bx(A, 1.1, 0.9, 0.06, 0, 0, 0.7, "hull", 0.02); cy(A, 0.04, 0.35, 0, -0.05, 0.76, "chrome")
        bx(A, 0.5, 0.06, 0.06, 0, -0.05, 1.1, "gunmetal", 0.02); bx(A, 0.06, 0.06, 0.2, -0.22, -0.05, 1.0, "gunmetal", 0.02); bx(A, 0.06, 0.06, 0.2, 0.22, -0.05, 1.0, "gunmetal", 0.02)
        screen(A, 0.9, 0.5, 0, 0.35, 0.9, SCRS[g], "hull_dark", face=-1); strip(A, 1.0, 0.012, 0.02, 0, -0.41, 0.3, GLOWS[g])
    else:
        bx(A, 1.4, 0.7, 0.05, 0, 0, 0.7, "hull", 0.02); bx(A, 0.08, 0.6, 0.7, -0.6, 0, 0.0, "gunmetal", 0.01); bx(A, 0.08, 0.6, 0.7, 0.6, 0, 0.0, "gunmetal", 0.01); bx(A, 1.2, 0.04, 0.5, 0, 0.3, 0.2, "hull_dark")
        screen(A, 0.5, 0.32, -0.35, 0.25, 0.75, "scr_blue", "hull_dark", face=-1); screen(A, 0.5, 0.32, 0.35, 0.25, 0.75, SCRS[g], "hull_dark", face=-1); strip(A, 1.3, 0.012, 0.014, 0, -0.35, 0.69, GLOWS[g])


@family("holotable", "signature", [{"n": "round_map", "glow": "cyan"}, {"n": "square_grid", "glow": "green"}, {"n": "planet_orrery", "glow": "amber"}, {"n": "ship_blueprint", "glow": "blue"}],
        cat="scifi", place="floor", tags=["table", "center", "holds-decor", "light", "glow"], light=0.9)
def _holo(A, v):
    k, g = v["n"], v["glow"]
    if k == "round_map":
        cy(A, 0.9, 0.7, 0, 0, 0.0, "hull_dark", r2=0.8, verts=32); cy(A, 0.92, 0.06, 0, 0, 0.7, "hull", verts=32); tor(A, 0.8, 0.02, (0, 0, 0.77), GLOWS[g], seg=48, minor=6)
        cyl(A, 0.6, 0.5, (0, 0, 1.05), "glass_cyan", r2=0.2, verts=24); sph(A, 0.15, (0, 0, 1.05), GLOWS[g], seg=14)
    elif k == "square_grid":
        bx(A, 1.6, 1.6, 0.7, 0, 0, 0.0, "hull_dark", 0.03); bx(A, 1.7, 1.7, 0.05, 0, 0, 0.7, "hull", 0.02)
        for i in range(-3, 4): strip(A, 0.01, 1.4, 0.01, i * 0.2, 0, 0.76, GLOWS[g]); strip(A, 1.4, 0.01, 0.01, 0, i * 0.2, 0.76, GLOWS[g])
        for p in [(0.3, 0.2, 0.2), (-0.4, -0.3, 0.3), (0.0, 0.4, 0.15)]: bx(A, 0.15, 0.15, p[2], p[0], p[1], 0.76, "glass_cyan", 0.01)
    elif k == "planet_orrery":
        cy(A, 0.6, 0.6, 0, 0, 0.0, "gunmetal", r2=0.5, verts=28); cy(A, 0.62, 0.05, 0, 0, 0.6, "hull", verts=28)
        sph(A, 0.14, (0, 0, 1.2), GLOWS[g], seg=16); tor(A, 0.4, 0.008, (0, 0, 1.2), "chrome", seg=40, minor=5); tor(A, 0.55, 0.008, (0, 0, 1.2), "chrome", seg=40, minor=5, rot=(0.4, 0, 0)); sph(A, 0.05, (0.4, 0, 1.2), "neon_white", seg=8); sph(A, 0.07, (-0.4, 0.3, 1.3), "scr_blue", seg=8)
        cy(A, 0.015, 0.5, 0, 0, 0.65, "chrome", verts=6)
    else:
        bx(A, 2.0, 1.0, 0.7, 0, 0, 0.0, "hull_dark", 0.03); bx(A, 2.1, 1.1, 0.05, 0, 0, 0.7, "hull", 0.02)
        prism(A, [(-0.7, 0), (0.5, 0), (0.7, 0.1), (0.5, 0.2), (-0.7, 0.2), (-0.8, 0.1)], 0.3, (0, 0, 1.05), "glass_cyan", bevel=0.01) if False else bx(A, 1.4, 0.3, 0.12, 0, 0, 0.95, "glass_cyan", 0.03)
        strip(A, 1.8, 0.01, 0.01, 0, -0.35, 0.76, GLOWS[g]); strip(A, 1.8, 0.01, 0.01, 0, 0.35, 0.76, GLOWS[g]); tor(A, 0.3, 0.008, (0, 0, 0.78), GLOWS[g], seg=32, minor=5)


@family("reactor_core", "signature", [{"n": "plasma_column", "glow": "cyan"}, {"n": "fusion_ring", "glow": "amber"}, {"n": "crystal_heart", "glow": "violet"}],
        cat="scifi", place="floor", tags=["decor", "light", "glow", "focal"], light=1.6)
def _reactor(A, v):
    k, g = v["n"], v["glow"]
    cy(A, 0.8, 0.15, 0, 0, 0.0, "gunmetal", verts=32); tor(A, 0.7, 0.04, (0, 0, 0.18), GLOWS[g], seg=40, minor=6)
    if k == "plasma_column":
        cy(A, 0.5, 2.2, 0, 0, 0.15, "glass_cyan", verts=28); cy(A, 0.18, 2.0, 0, 0, 0.25, GLOWS[g], verts=20)
        for z in (0.5, 1.2, 1.9): tor(A, 0.52, 0.03, (0, 0, z), "chrome", seg=32, minor=6)
        cy(A, 0.6, 0.12, 0, 0, 2.35, "gunmetal", verts=32)
    elif k == "fusion_ring":
        tor(A, 0.7, 0.12, (0, 0, 1.0), "chrome", rot=(PI / 2, 0, 0), seg=48, minor=12); tor(A, 0.7, 0.03, (0, 0, 1.0), GLOWS[g], rot=(PI / 2, 0, 0), seg=48, minor=8); sph(A, 0.25, (0, 0, 1.0), GLOWS[g], seg=18)
        for s in (-1, 1): cy(A, 0.08, 0.9, s * 0.55, 0, 0.15, "steel", verts=12)
    else:
        for i in range(6): a = i * 1.05; limb(A, (0.25 * math.cos(a), 0.25 * math.sin(a), 0.2), (0.0, 0.0, 1.5), 0.1, 0.01, "glass_cyan", 6)
        sph(A, 0.25, (0, 0, 1.0), GLOWS[g], scale=(1, 1, 1.5), seg=14); tor(A, 0.55, 0.03, (0, 0, 1.0), "steel", seg=32, minor=6, rot=(0.3, 0.2, 0))


@family("server_rack", "signature", [{"n": "blade_full", "glow": "green"}, {"n": "blade_cool", "glow": "cyan"}, {"n": "core_stack", "glow": "magenta"}, {"n": "patch_panel", "glow": "amber"}, {"n": "quantum_cabinet", "glow": "violet"}],
        cat="scifi", place="floor", tags=["storage", "wall-hug", "tall", "light", "glow"], light=0.5)
def _srv(A, v):
    k, g = v["n"], v["glow"]
    W, D, H = 0.7, 0.9, 2.1
    bx(A, W, D, H, 0, 0, 0.0, "hull_dark", 0.02)
    if k in ("blade_full", "blade_cool"):
        for i in range(16):
            z = 0.1 + i * 0.12; bx(A, W - 0.1, 0.03, 0.09, 0, -D / 2 - 0.005, z, "gunmetal", 0.005)
            for j in range(4): strip(A, 0.025, 0.012, 0.012, -0.22 + j * 0.06, -D / 2 - 0.02, z + 0.035, GLOWS[g] if (i * 3 + j) % 3 else "neon_amber")
            strip(A, 0.14, 0.012, 0.012, 0.15, -D / 2 - 0.02, z + 0.035, "neon_white") if k == "blade_cool" else None
    elif k == "core_stack":
        bx(A, W - 0.1, 0.03, H - 0.2, 0, -D / 2 - 0.005, 0.1, "carbon", 0.005)
        for i in range(8): strip(A, W - 0.2, 0.012, 0.02, 0, -D / 2 - 0.02, 0.2 + i * 0.24, GLOWS[g] if i % 2 else "neon_blue")
    elif k == "patch_panel":
        bx(A, W - 0.1, 0.03, H - 0.2, 0, -D / 2 - 0.005, 0.1, "hull_grey", 0.005)
        for i in range(10):
            for j in range(5): cy(A, 0.012, 0.02, -0.22 + j * 0.11, -D / 2 - 0.02, 0.2 + i * 0.17, "neon_amber" if (i + j) % 7 == 0 else "carbon", verts=8, rot=(PI / 2, 0, 0))
        for i in range(6): limb(A, (-0.2 + i * 0.08, -D / 2 - 0.02, 1.0), (-0.2 + i * 0.08 + 0.05, -D / 2 - 0.12, 0.5 - i * 0.05), 0.008, 0.008, GLOWS[g] if i % 2 else "p_teal", 5)
    else:
        bx(A, W - 0.15, 0.03, H - 0.3, 0, -D / 2 - 0.005, 0.15, "hull_dark", 0.005); box(A, (W - 0.3, 0.02, H - 0.5), (0, -D / 2 - 0.02, H / 2), "glass_cyan", bevel=0)
        cy(A, 0.15, 0.3, 0, -0.05, 1.0, GLOWS[g], verts=14); tor(A, 0.2, 0.01, (0, -0.05, 1.3), "chrome", seg=24, minor=5); tor(A, 0.2, 0.01, (0, -0.05, 0.7), "chrome", seg=24, minor=5)
    strip(A, 0.02, 0.012, H - 0.2, W / 2 - 0.03, -D / 2 - 0.01, 0.1, GLOWS[g]); bx(A, W, 0.05, 0.08, 0, -D / 2 - 0.0, H - 0.08, "hull_grey", 0.01)


@family("engineering_station", "signature", [{"n": "diagnostics", "glow": "amber"}, {"n": "power_panel", "glow": "red"}, {"n": "fabricator", "glow": "cyan"}, {"n": "valve_wall", "glow": "green"}],
        cat="scifi", place="floor", tags=["wall-hug", "decor", "holds-decor", "light", "glow"], light=0.5)
def _eng(A, v):
    k, g = v["n"], v["glow"]
    if k == "diagnostics":
        bx(A, 1.2, 0.6, 0.9, 0, 0, 0.0, "hull_dark", 0.03); bx(A, 1.3, 0.7, 0.05, 0, 0, 0.9, "p_orange", 0.02)
        screen(A, 0.9, 0.55, 0, 0.2, 0.95, SCRS[g], "hull_dark", face=-1); [bx(A, 0.08, 0.08, 0.03, -0.4 + i * 0.16, -0.15, 0.95, GLOWS[g] if i % 2 else "p_yellow", 0.01) for i in range(6)]
    elif k == "power_panel":
        bx(A, 1.3, 0.4, 2.0, 0, 0, 0.0, "hull_grey", 0.02)
        for i in range(3): bx(A, 0.36, 0.02, 1.7, -0.42 + i * 0.42, -0.21, 0.15, "hull_dark", 0.01); strip(A, 0.28, 0.012, 0.03, -0.42 + i * 0.42, -0.225, 1.6, GLOWS[g]); [cy(A, 0.03, 0.04, -0.42 + i * 0.42, -0.23, 0.5 + j * 0.3, "p_yellow" if j % 2 else "p_red", verts=10, rot=(PI / 2, 0, 0)) for j in range(4)]
        bx(A, 1.3, 0.1, 0.1, 0, -0.0, 2.0, "p_yellow", 0.01)
    elif k == "fabricator":
        bx(A, 1.2, 0.9, 1.4, 0, 0, 0.0, "hull", 0.04); box(A, (0.9, 0.02, 0.7), (0, -0.46, 0.9), "glass_cyan", bevel=0); bx(A, 0.9, 0.5, 0.05, 0, -0.1, 0.55, "carbon", 0.01)
        limb(A, (0.0, 0.0, 1.35), (0.0, -0.2, 0.9), 0.03, 0.015, "steel", 8); sph(A, 0.04, (0, -0.2, 0.88), GLOWS[g], seg=8); strip(A, 1.0, 0.012, 0.03, 0, -0.455, 0.3, GLOWS[g]); screen(A, 0.35, 0.2, 0.35, -0.45, 1.15, SCRS[g], "hull_dark", face=-1)
    else:
        bx(A, 1.4, 0.2, 2.0, 0, 0, 0.0, "hull_dark", 0.02)
        for i in range(4):
            x = -0.5 + i * 0.33; cy(A, 0.1, 0.06, x, -0.12, 0.7 + (i % 2) * 0.5, "p_red" if i % 2 else "p_yellow", verts=16, rot=(PI / 2, 0, 0)); bx(A, 0.18, 0.05, 0.03, x, -0.15, 0.7 + (i % 2) * 0.5 + 0.09, "steel", 0.005)
        for z in (0.4, 1.3, 1.8): cy(A, 0.05, 1.5, 0, -0.12, z, "steel", verts=10, rot=(0, PI / 2, 0))
        strip(A, 1.2, 0.012, 0.02, 0, -0.105, 0.1, GLOWS[g])


@family("medbay_bed", "signature", [{"n": "scanner_bed", "glow": "cyan"}, {"n": "surgery_table", "glow": "green"}, {"n": "regen_tank", "glow": "blue"}],
        cat="scifi", place="floor", tags=["bed", "decor", "light", "glow"], light=0.6)
def _med(A, v):
    k, g = v["n"], v["glow"]
    if k == "scanner_bed":
        bx(A, 0.8, 2.0, 0.1, 0, 0, 0.55, "hull", 0.03); pad(A, 0.7, 1.9, 0.08, 0, 0, 0.65, "foam", 0.03); cy(A, 0.15, 0.55, 0, 0, 0.0, "gunmetal", r2=0.1); bx(A, 0.6, 0.6, 0.06, 0, 0, 0.0, "gunmetal", 0.02)
        tor(A, 0.6, 0.06, (0, -0.2, 1.0), "hull", rot=(PI / 2, 0, 0), seg=32, minor=10); tor(A, 0.6, 0.015, (0, -0.25, 1.0), GLOWS[g], rot=(PI / 2, 0, 0), seg=32, minor=6)
    elif k == "surgery_table":
        bx(A, 0.7, 1.9, 0.08, 0, 0, 0.85, "steel", 0.02); pad(A, 0.6, 1.7, 0.04, 0, 0, 0.93, "p_teal", 0.015); cy(A, 0.1, 0.85, 0, 0, 0.0, "chrome", r2=0.08); bx(A, 0.7, 0.7, 0.05, 0, 0, 0.0, "gunmetal", 0.02)
        limb(A, (0.5, 0.3, 0.0), (0.5, 0.3, 2.0), 0.03, 0.03, "steel", 8); limb(A, (0.5, 0.3, 2.0), (0.0, 0.0, 1.9), 0.025, 0.025, "steel", 8); cy(A, 0.25, 0.06, 0.0, 0.0, 1.85, "hull", verts=20); cy(A, 0.2, 0.01, 0, 0, 1.84, "neon_white", verts=20)
    else:
        cy(A, 0.55, 0.2, 0, 0, 0.0, "gunmetal", verts=28); cy(A, 0.55, 0.2, 0, 0, 1.9, "gunmetal", verts=28); cy(A, 0.46, 1.7, 0, 0, 0.2, "glass_cyan", verts=28); cy(A, 0.4, 1.0, 0, 0, 0.2, GLOWS[g], verts=24)
        sph(A, 0.15, (0, 0, 1.0), "neon_white", seg=10); bx(A, 0.6, 0.15, 0.25, 0, -0.55, 0.9, "hull_dark", 0.02); screen(A, 0.5, 0.2, 0, -0.64, 0.95, SCRS[g], "hull_dark", face=-1)


@family("scanner_arch", "signature", [{"n": "security_gate", "glow": "green"}, {"n": "body_scanner", "glow": "cyan"}],
        cat="scifi", place="floor", tags=["decor", "light", "glow"], light=0.6)
def _arch(A, v):
    k, g = v["n"], v["glow"]
    for s in (-1, 1): bx(A, 0.2, 1.0, 2.4, s * 0.65, 0, 0.0, "hull", 0.03); strip(A, 0.012, 0.9, 2.0, s * 0.545, 0, 0.2, GLOWS[g])
    bx(A, 1.5, 1.0, 0.25, 0, 0, 2.4, "hull", 0.03); strip(A, 1.0, 0.012, 0.03, 0, -0.505, 2.5, GLOWS[g]); bx(A, 1.5, 1.0, 0.04, 0, 0, 0.0, "hull_dark", 0.01)
    if k == "body_scanner": box(A, (1.1, 0.02, 2.3), (0, 0.4, 1.2), "glass_cyan", bevel=0)
    else:
        screen(A, 0.3, 0.2, 0, -0.5, 2.38, SCRS[g], "hull_dark", face=-1)


@family("robot_arm", "signature", [{"n": "assembly", "glow": "amber"}, {"n": "ceiling_rail", "glow": "cyan"}, {"n": "bar_arm", "glow": "magenta"}],
        cat="scifi", place="floor", tags=["decor", "light", "glow"], light=0.4)
def _rarm(A, v):
    k, g = v["n"], v["glow"]
    cy(A, 0.3, 0.2, 0, 0, 0.0, "hull_dark", verts=24); cy(A, 0.2, 0.15, 0, 0, 0.2, "p_orange" if k == "assembly" else "hull", verts=20)
    limb(A, (0, 0, 0.35), (0.3, 0, 1.2), 0.1, 0.08, "hull", 10); sph(A, 0.1, (0.3, 0, 1.2), "gunmetal", seg=12); limb(A, (0.3, 0, 1.2), (0.8, 0, 1.0), 0.07, 0.05, "hull", 10); sph(A, 0.07, (0.8, 0, 1.0), "gunmetal", seg=10)
    limb(A, (0.8, 0, 1.0), (0.95, 0, 0.6), 0.04, 0.03, "steel", 8); [bx(A, 0.02, 0.1, 0.12, 0.95 + s * 0.04, 0, 0.5, "steel", 0.003) for s in (-1, 1)]
    tor(A, 0.2, 0.01, (0, 0, 0.3), GLOWS[g], seg=24, minor=5)


@family("drone_dock", "signature", [{"n": "quad", "glow": "cyan"}, {"n": "orb_bot", "glow": "magenta"}, {"n": "wall_charger", "glow": "green"}, {"n": "cleaner", "glow": "amber"}],
        cat="scifi", place="floor", tags=["decor", "light", "glow"], light=0.4)
def _drone(A, v):
    k, g = v["n"], v["glow"]
    cy(A, 0.3, 0.06, 0, 0, 0.0, "gunmetal", verts=24); tor(A, 0.3, 0.012, (0, 0, 0.05), GLOWS[g], seg=32, minor=5)
    if k == "quad":
        sph(A, 0.12, (0, 0, 0.6), "hull", scale=(1, 1, 0.6), seg=14)
        for sx in (-1, 1):
            for sy in (-1, 1): limb(A, (0, 0, 0.6), (sx * 0.22, sy * 0.22, 0.62), 0.015, 0.015, "gunmetal", 6); cy(A, 0.1, 0.01, sx * 0.22, sy * 0.22, 0.64, "hull_grey", verts=16); cy(A, 0.02, 0.02, sx * 0.22, sy * 0.22, 0.62, "chrome")
        sph(A, 0.035, (0, -0.1, 0.58), GLOWS[g], seg=8)
    elif k == "orb_bot":
        sph(A, 0.18, (0, 0, 0.55), "hull", seg=18); tor(A, 0.18, 0.01, (0, 0, 0.55), "gunmetal", seg=28, minor=5); sph(A, 0.06, (0, -0.15, 0.58), GLOWS[g], seg=10)
    elif k == "wall_charger":
        bx(A, 0.5, 0.15, 0.8, 0, 0.25, 0.0, "hull", 0.03); cy(A, 0.18, 0.04, 0, 0, 0.8, "gunmetal", verts=20); sph(A, 0.1, (0, 0, 0.9), "hull", seg=12); strip(A, 0.3, 0.012, 0.02, 0, 0.17, 0.5, GLOWS[g])
    else:
        cy(A, 0.28, 0.14, 0, 0, 0.06, "p_orange", verts=28); cy(A, 0.08, 0.04, 0, 0, 0.2, "gunmetal", verts=14); strip(A, 0.3, 0.012, 0.02, 0, -0.27, 0.1, GLOWS[g]); sph(A, 0.03, (0.15, -0.2, 0.17), "neon_white", seg=6)


@family("vending_machine", "signature", [{"n": "snack_hex", "glow": "magenta"}, {"n": "drink_cooler", "glow": "cyan"}, {"n": "gear_vendor", "glow": "amber"}, {"n": "noodle_dispenser", "glow": "red"}],
        cat="scifi", place="floor", tags=["decor", "wall-hug", "tall", "light", "glow"], light=0.9)
def _vend(A, v):
    k, g = v["n"], v["glow"]
    W, D, H = 1.0, 0.8, 1.9
    bx(A, W, D, H, 0, 0, 0.0, "hull_dark", 0.03); box(A, (W - 0.3, 0.02, H - 0.5), (-0.07, -D / 2 - 0.01, 1.0), "glass_cyan", bevel=0); bx(A, 0.2, 0.03, H - 0.5, W / 2 - 0.13, -D / 2 - 0.01, 0.75, "carbon", 0.005)
    for i in range(5):
        z = 0.35 + i * 0.28; strip(A, W - 0.34, 0.02, 0.014, -0.07, -D / 2 - 0.02, z, GLOWS[g])
        for j in range(5): bx(A, 0.09, 0.08, 0.14, -0.3 + j * 0.13, -D / 2 + 0.1, z + 0.014, ["p_orange", "p_teal", "p_red", "hull", "p_yellow"][(i + j + len(k)) % 5], 0.01)
    box(A, (W - 0.1, 0.012, 0.2), (0, -D / 2 - 0.01, H - 0.15), GLOWS[g], bevel=0); bx(A, 0.5, 0.1, 0.18, -0.07, -D / 2 - 0.04, 0.04, "carbon", 0.01); screen(A, 0.14, 0.12, W / 2 - 0.13, -D / 2 - 0.02, 1.35, SCRS[g], "hull_dark", face=-1)


@family("hydroponic_bed", "signature", [{"n": "rack_tall", "glow": "magenta"}, {"n": "trough_long", "glow": "magenta"}, {"n": "tower_ring", "glow": "violet"}, {"n": "herb_wall", "glow": "magenta"}, {"n": "algae_tank", "glow": "green"}],
        cat="scifi", place="floor", tags=["decor", "plant", "light", "glow"], light=0.8)
def _hyd(A, v):
    k, g = v["n"], v["glow"]
    if k == "rack_tall":
        bx(A, 1.2, 0.6, 2.0, 0, 0, 0.0, "hull_dark", 0.02) if False else None
        for sx in (-1, 1): bx(A, 0.05, 0.6, 2.0, sx * 0.58, 0, 0.0, "gunmetal", 0.01)
        for i in range(4):
            z = 0.15 + i * 0.5; bx(A, 1.2, 0.55, 0.06, 0, 0, z, "hull", 0.01); bx(A, 1.1, 0.45, 0.08, 0, 0, z + 0.06, "soil", 0.01); strip(A, 1.1, 0.04, 0.02, 0, 0, z + 0.4, "neon_magenta")
            for j in range(6): sph(A, 0.07, (-0.45 + j * 0.18, 0, z + 0.2), "leaf" if j % 2 else "leaf2", scale=(1, 1, 1.2), seg=8)
    elif k == "trough_long":
        bx(A, 1.8, 0.6, 0.35, 0, 0, 0.0, "hull", 0.03); bx(A, 1.7, 0.5, 0.04, 0, 0, 0.35, "soil", 0.0); strip(A, 1.7, 0.012, 0.02, 0, -0.305, 0.1, "neon_magenta")
        for j in range(8): sph(A, 0.1, (-0.7 + j * 0.2, 0, 0.5), "leaf" if j % 2 else "leaf2", scale=(1, 1, 1.2), seg=8)
        bx(A, 1.8, 0.05, 0.05, 0, 0, 1.2, "gunmetal", 0.01); strip(A, 1.7, 0.04, 0.02, 0, 0, 1.17, "neon_magenta")
        for sx in (-1, 1): cy(A, 0.02, 1.2, sx * 0.88, 0, 0.0, "steel", verts=8)
    elif k == "tower_ring":
        cy(A, 0.35, 0.1, 0, 0, 0.0, "gunmetal", verts=24); cy(A, 0.12, 1.9, 0, 0, 0.1, "hull", verts=16)
        for i in range(7): z = 0.3 + i * 0.25; tor(A, 0.3, 0.05, (0, 0, z), "hull_grey", seg=24, minor=8); sph(A, 0.1, (0.3 * math.cos(i), 0.3 * math.sin(i), z + 0.1), "leaf" if i % 2 else "leaf2", seg=8)
        strip(A, 0.02, 0.02, 1.8, 0, -0.125, 0.15, GLOWS[g])
    elif k == "herb_wall":
        bx(A, 1.4, 0.25, 1.6, 0, 0, 0.0, "hull_dark", 0.02)
        for i in range(4):
            for j in range(4): bx(A, 0.28, 0.2, 0.2, -0.45 + j * 0.3, -0.05, 0.1 + i * 0.38, "hull", 0.02); sph(A, 0.1, (-0.45 + j * 0.3, -0.05, 0.38 + i * 0.38), "leaf" if (i + j) % 2 else "leaf2", seg=8)
        strip(A, 1.3, 0.02, 0.02, 0, -0.14, 1.65, "neon_magenta")
    else:
        bx(A, 1.2, 0.6, 0.15, 0, 0, 0.0, "gunmetal", 0.02); box(A, (1.1, 0.5, 1.1), (0, 0, 0.7), "glass_cyan", bevel=0.02); box(A, (1.05, 0.45, 0.9), (0, 0, 0.62), GLOWS[g], bevel=0.02); bx(A, 1.2, 0.6, 0.08, 0, 0, 1.25, "gunmetal", 0.02)
        for i in range(5): sph(A, 0.03 + (i % 3) * 0.01, (-0.4 + i * 0.2, 0, 0.3 + (i * 0.17) % 0.7), "neon_white", seg=6)


@family("teleporter_pad", "signature", [{"n": "ring_pad", "glow": "cyan"}, {"n": "booth", "glow": "violet"}],
        cat="scifi", place="floor", tags=["decor", "light", "glow", "focal"], light=1.0)
def _tele(A, v):
    k, g = v["n"], v["glow"]
    cy(A, 0.9, 0.12, 0, 0, 0.0, "gunmetal", verts=32); tor(A, 0.8, 0.03, (0, 0, 0.13), GLOWS[g], seg=48, minor=6); tor(A, 0.5, 0.02, (0, 0, 0.13), GLOWS[g], seg=40, minor=6); cy(A, 0.78, 0.01, 0, 0, 0.12, "scr_cyan", verts=32)
    if k == "ring_pad":
        for i in range(4): a = i * PI / 2 + PI / 4; cy(A, 0.06, 1.8, 0.85 * math.cos(a), 0.85 * math.sin(a), 0.12, "hull", verts=10); sph(A, 0.07, (0.85 * math.cos(a), 0.85 * math.sin(a), 1.95), GLOWS[g], seg=8)
        tor(A, 0.85, 0.04, (0, 0, 1.9), "chrome", seg=48, minor=8)
    else:
        for i in range(8): a = i * PI / 4; bx(A, 0.18, 0.05, 2.2, 0.82 * math.cos(a), 0.82 * math.sin(a), 0.12, "hull_dark", 0.01, rot=(0, 0, a + PI / 2))
        cy(A, 0.95, 0.12, 0, 0, 2.3, "gunmetal", verts=32); tor(A, 0.8, 0.03, (0, 0, 2.28), GLOWS[g], seg=48, minor=6)


@family("captain_chair", "signature", [{"n": "command_throne", "glow": "amber"}, {"n": "pilot_seat", "glow": "cyan"}, {"n": "gunner_seat", "glow": "red"}],
        cat="scifi", place="floor", tags=["seating", "faces-center", "focal", "light", "glow"], light=0.4)
def _cap(A, v):
    k, g = v["n"], v["glow"]
    cy(A, 0.4, 0.2, 0, 0, 0.0, "gunmetal", r2=0.3, verts=24); cy(A, 0.07, 0.3, 0, 0, 0.2, "chrome")
    pad(A, 0.65, 0.65, 0.14, 0, -0.02, 0.45, "pad", 0.05); prism(A, [(-0.34, 0), (0.34, 0), (0.3, 1.0), (-0.3, 1.0)], 0.14, (0, 0.3, 0.55), "pad", bevel=0.05)
    for s in (-1, 1): bx(A, 0.12, 0.6, 0.06, s * 0.4, -0.05, 0.7, "hull", 0.02); bx(A, 0.08, 0.08, 0.2, s * 0.4, 0.0, 0.5, "gunmetal", 0.01)
    if k == "command_throne":
        pad(A, 0.5, 0.2, 0.3, 0, 0.3, 1.5, "pad", 0.05); prism(A, [(-0.45, 0), (0.45, 0), (0.3, 0.5), (-0.3, 0.5)], 0.06, (0, 0.38, 1.55), "hull", bevel=0.02); strip(A, 0.7, 0.012, 0.02, 0, 0.345, 1.55, GLOWS[g])
        for s in (-1, 1): screen(A, 0.16, 0.12, s * 0.4, -0.2, 0.76, SCRS[g], "hull_dark", face=-1)
    elif k == "pilot_seat":
        strip(A, 0.03, 0.012, 0.8, -0.3, 0.37, 0.6, GLOWS[g]); strip(A, 0.03, 0.012, 0.8, 0.3, 0.37, 0.6, GLOWS[g]); bx(A, 0.3, 0.12, 0.2, 0, 0.3, 1.6, "pad", 0.04)
    else:
        bx(A, 0.9, 0.06, 0.2, 0, -0.45, 0.9, "hull_dark", 0.01); limb(A, (0.4, -0.05, 0.7), (0.4, -0.5, 0.95), 0.02, 0.02, "steel", 6); limb(A, (-0.4, -0.05, 0.7), (-0.4, -0.5, 0.95), 0.02, 0.02, "steel", 6); strip(A, 0.8, 0.012, 0.02, 0, -0.485, 0.98, GLOWS[g])


@family("star_map", "signature", [{"n": "wall_globe", "glow": "blue"}, {"n": "floor_sphere", "glow": "cyan"}],
        cat="scifi", place="floor", tags=["decor", "light", "glow", "focal"], light=0.9)
def _smap(A, v):
    k, g = v["n"], v["glow"]
    if k == "wall_globe":
        cy(A, 0.4, 0.1, 0, 0, 0.0, "gunmetal", verts=24); cy(A, 0.06, 0.8, 0, 0, 0.1, "chrome"); sph(A, 0.45, (0, 0, 1.4), "glass_cyan", seg=24); tor(A, 0.46, 0.012, (0, 0, 1.4), "chrome", seg=40, minor=5, rot=(0.3, 0, 0))
        for i in range(20): a = i * 2.4; b = (i * 0.37) % 1.2 - 0.6; sph(A, 0.015, (0.28 * math.cos(a) * math.cos(b), 0.28 * math.sin(a) * math.cos(b), 1.4 + 0.28 * math.sin(b)), "neon_white" if i % 3 else GLOWS[g], seg=6)
        sph(A, 0.07, (0, 0, 1.4), GLOWS[g], seg=10)
    else:
        cy(A, 0.5, 0.15, 0, 0, 0.0, "gunmetal", r2=0.4, verts=28); sph(A, 0.6, (0, 0, 1.0), "glass_cyan", seg=28)
        for R, rot in ((0.62, (0, 0, 0)), (0.62, (PI / 2, 0, 0)), (0.62, (0.6, 0.5, 0))): tor(A, R, 0.01, (0, 0, 1.0), "steel", seg=48, minor=5, rot=rot)
        for i in range(30): a = i * 2.4; b = (i * 0.29) % 1.6 - 0.8; sph(A, 0.02, (0.4 * math.cos(a) * math.cos(b), 0.4 * math.sin(a) * math.cos(b), 1.0 + 0.4 * math.sin(b)), "neon_white" if i % 3 else GLOWS[g], seg=6)


@family("cargo_crate", "signature", [{"n": "standard", "glow": "amber"}, {"n": "ribbed_large", "glow": "cyan"}, {"n": "hazard", "glow": "red"}, {"n": "medical", "glow": "green"}, {"n": "stack_two", "glow": "amber"}, {"n": "cryo_case", "glow": "blue"}, {"n": "ammo_box", "glow": "amber"}, {"n": "open_loot", "glow": "magenta"}],
        cat="scifi", place="floor", tags=["decor", "wall-hug"])
def _crate(A, v):
    k, g = v["n"], v["glow"]
    if k == "standard":
        bx(A, 0.8, 0.8, 0.8, 0, 0, 0.0, "hull_grey", 0.03)
        for z in (0.05, 0.7): bx(A, 0.84, 0.84, 0.06, 0, 0, z, "gunmetal", 0.01)
        for sx in (-1, 1): bx(A, 0.06, 0.84, 0.8, sx * 0.4, 0, 0.0, "gunmetal", 0.01)
        strip(A, 0.3, 0.012, 0.04, 0, -0.42, 0.4, GLOWS[g])
    elif k == "ribbed_large":
        bx(A, 1.2, 0.8, 1.0, 0, 0, 0.0, "hull", 0.03)
        for i in range(6): bx(A, 0.04, 0.84, 1.0, -0.5 + i * 0.2, 0, 0.0, "hull_grey", 0.01)
        bx(A, 0.5, 0.012, 0.18, 0, -0.41, 0.7, "hull_dark"); strip(A, 0.4, 0.012, 0.02, 0, -0.415, 0.7, GLOWS[g])
    elif k == "hazard":
        bx(A, 0.8, 0.8, 0.7, 0, 0, 0.0, "p_yellow", 0.03)
        for i in range(5): box(A, (0.1, 0.012, 0.9), (-0.32 + i * 0.16, -0.405, 0.35), "rubber", (0, 0.7, 0), 0)
        bx(A, 0.84, 0.84, 0.06, 0, 0, 0.0, "gunmetal", 0.01); strip(A, 0.2, 0.012, 0.04, 0, -0.42, 0.55, GLOWS[g])
    elif k == "medical":
        bx(A, 0.8, 0.6, 0.6, 0, 0, 0.0, "hull", 0.04); bx(A, 0.14, 0.012, 0.35, 0, -0.307, 0.15, "p_red"); bx(A, 0.35, 0.012, 0.14, 0, -0.307, 0.25, "p_red"); bx(A, 0.84, 0.64, 0.05, 0, 0, 0.55, "hull_grey", 0.01); strip(A, 0.5, 0.012, 0.02, 0, -0.31, 0.5, GLOWS[g])
    elif k == "stack_two":
        bx(A, 0.8, 0.8, 0.6, 0, 0, 0.0, "hull_grey", 0.03); bx(A, 0.6, 0.6, 0.5, 0.05, 0.02, 0.6, "p_orange", 0.03); strip(A, 0.3, 0.012, 0.03, 0, -0.41, 0.3, GLOWS[g])
    elif k == "cryo_case":
        bx(A, 1.0, 0.5, 0.5, 0, 0, 0.0, "hull_dark", 0.04); bx(A, 0.9, 0.4, 0.05, 0, 0, 0.5, "glass_cyan", 0.02); strip(A, 0.8, 0.012, 0.03, 0, -0.255, 0.2, GLOWS[g]); screen(A, 0.2, 0.1, 0.35, -0.26, 0.28, SCRS[g], "hull_dark", face=-1)
    elif k == "ammo_box":
        bx(A, 0.6, 0.35, 0.3, 0, 0, 0.0, "hull_grey", 0.025); bx(A, 0.62, 0.37, 0.05, 0, 0, 0.25, "gunmetal", 0.01); bx(A, 0.1, 0.04, 0.04, 0, -0.19, 0.3, "chrome"); strip(A, 0.2, 0.012, 0.03, 0, -0.18, 0.12, GLOWS[g])
    else:
        bx(A, 0.8, 0.7, 0.5, 0, 0, 0.0, "hull_grey", 0.03); bx(A, 0.8, 0.05, 0.4, 0, 0.35, 0.5, "hull_grey", 0.02, rot=(-0.9, 0, 0)); sph(A, 0.16, (0, 0, 0.62), GLOWS[g], seg=12)
        for p in [(-0.2, 0.1), (0.2, -0.1), (0.0, 0.2)]: bx(A, 0.14, 0.1, 0.07, p[0], p[1], 0.5, "gold" if False else "titanium", 0.01)


@family("canister", "signature", [{"n": "gas_tall", "glow": "cyan"}, {"n": "fuel_drum", "glow": "amber"}, {"n": "coolant", "glow": "blue"}, {"n": "toxic", "glow": "green"}],
        cat="scifi", place="floor", tags=["decor", "wall-hug"])
def _can(A, v):
    k, g = v["n"], v["glow"]
    if k == "gas_tall":
        cy(A, 0.18, 1.2, 0, 0, 0.0, "hull", verts=20); sph(A, 0.18, (0, 0, 1.2), "hull", scale=(1, 1, 0.6), seg=16); cy(A, 0.04, 0.12, 0, 0, 1.32, "chrome"); cy(A, 0.19, 0.12, 0, 0, 0.5, "hull_dark", verts=20); tor(A, 0.19, 0.01, (0, 0, 0.8), GLOWS[g], seg=24, minor=5)
    elif k == "fuel_drum":
        cy(A, 0.3, 0.9, 0, 0, 0.0, "p_orange", verts=24)
        for z in (0.15, 0.45, 0.75): tor(A, 0.3, 0.015, (0, 0, z), "gunmetal", seg=28, minor=5)
        cy(A, 0.07, 0.04, 0.1, 0.1, 0.9, "gunmetal"); strip(A, 0.2, 0.012, 0.04, 0, -0.305, 0.45, GLOWS[g])
    elif k == "coolant":
        cy(A, 0.28, 0.9, 0, 0, 0.0, "steel", verts=24); cy(A, 0.2, 0.6, 0, 0, 0.15, "glass_cyan", verts=20); cy(A, 0.17, 0.5, 0, 0, 0.2, GLOWS[g], verts=18); cy(A, 0.3, 0.06, 0, 0, 0.9, "gunmetal", verts=24)
    else:
        cy(A, 0.27, 0.8, 0, 0, 0.0, "p_yellow", verts=20); cy(A, 0.28, 0.05, 0, 0, 0.1, "rubber", verts=20); cy(A, 0.28, 0.05, 0, 0, 0.7, "rubber", verts=20); cy(A, 0.1, 0.03, 0, -0.27, 0.45, GLOWS[g], verts=12, rot=(PI / 2, 0, 0))
        bx(A, 0.18, 0.012, 0.18, 0, -0.27, 0.45, "rubber", 0.0)


@family("noodle_stall", "signature", [{"n": "street_cart", "glow": "red"}, {"n": "counter_bar", "glow": "magenta"}, {"n": "ramen_booth", "glow": "amber"}],
        cat="scifi", place="floor", tags=["decor", "wall-hug", "light", "glow", "holds-decor"], light=1.2)
def _noodle(A, v):
    k, g = v["n"], v["glow"]
    if k == "street_cart":
        bx(A, 1.4, 0.8, 0.9, 0, 0, 0.15, "hull_dark", 0.03); bx(A, 1.5, 0.9, 0.05, 0, 0, 1.05, "steel", 0.02); cy(A, 0.1, 0.1, -0.55, -0.35, 0.0, "rubber", verts=14, rot=(0, PI / 2, 0)); cy(A, 0.1, 0.1, 0.55, -0.35, 0.0, "rubber", verts=14, rot=(0, PI / 2, 0))
        for sx in (-1, 1): cy(A, 0.02, 1.0, sx * 0.7, -0.4, 1.1, "gunmetal", verts=8)
        bx(A, 1.6, 1.0, 0.06, 0, 0, 2.05, GLOWS[g] if False else "p_red", 0.02); strip(A, 1.4, 0.03, 0.04, 0, -0.5, 1.95, GLOWS[g]); cy(A, 0.18, 0.2, 0.3, 0.0, 1.1, "steel", verts=16); cy(A, 0.16, 0.01, 0.3, 0.0, 1.3, "neon_amber", verts=16)
    elif k == "counter_bar":
        bx(A, 2.0, 0.6, 1.0, 0, 0, 0.0, "hull_dark", 0.03); bx(A, 2.1, 0.7, 0.06, 0, 0, 1.0, "hull", 0.02); strip(A, 2.0, 0.012, 0.03, 0, -0.305, 0.2, GLOWS[g]); bx(A, 2.1, 0.06, 0.4, 0, 0.3, 1.06, "glass_cyan", 0.01)
        for i in range(3): cy(A, 0.1, 0.1, -0.6 + i * 0.6, -0.05, 1.06, "steel", verts=16); cy(A, 0.09, 0.01, -0.6 + i * 0.6, -0.05, 1.16, "neon_amber", verts=16)
    else:
        bx(A, 2.0, 1.0, 0.1, 0, 0, 0.0, "hull_grey", 0.02)
        for sx in (-1, 1): bx(A, 0.08, 1.0, 2.2, sx * 0.96, 0, 0.0, "hull_dark", 0.01)
        bx(A, 2.0, 1.0, 0.1, 0, 0, 2.2, "p_red", 0.02); strip(A, 1.6, 0.04, 0.06, 0, -0.52, 2.1, GLOWS[g]); bx(A, 1.8, 0.4, 0.9, 0, 0.3, 0.1, "hull_dark", 0.02); bx(A, 1.8, 0.45, 0.05, 0, 0.3, 1.0, "hull", 0.01)
        for sx in (-1, 1): cy(A, 0.18, 0.04, sx * 0.6, -0.3, 0.45, "p_red", verts=16); cy(A, 0.03, 0.4, sx * 0.6, -0.3, 0.05, "chrome")


@family("suit_rack", "signature", [{"n": "eva_rack", "glow": "cyan"}, {"n": "armor_stand", "glow": "red"}, {"n": "helmet_shelf", "glow": "green"}],
        cat="scifi", place="floor", tags=["decor", "wall-hug", "light", "glow"], light=0.5)
def _suit(A, v):
    k, g = v["n"], v["glow"]
    def suit(x, mat="hull", y=0.0):
        bx(A, 0.45, 0.25, 0.6, x, y, 0.9, mat, 0.06); sph(A, 0.14, (x, y - 0.02, 1.68), "hull_grey", seg=14); sph(A, 0.1, (x, y - 0.1, 1.68), "glass_cyan", scale=(1, 0.5, 0.9), seg=10)
        for s in (-1, 1): limb(A, (x + s * 0.25, y, 1.45), (x + s * 0.3, y, 0.95), 0.07, 0.06, mat, 8); limb(A, (x + s * 0.12, y, 0.9), (x + s * 0.12, y, 0.1), 0.09, 0.07, mat, 8); bx(A, 0.12, 0.2, 0.06, x + s * 0.12, y - 0.04, 0.0, "gunmetal", 0.01)
        bx(A, 0.25, 0.1, 0.25, x, y + 0.15, 1.1, "hull_dark", 0.03)
    if k == "eva_rack":
        bx(A, 1.4, 0.1, 2.0, 0, 0.3, 0.0, "hull_dark", 0.02); suit(-0.35); suit(0.35, "p_orange"); strip(A, 1.3, 0.012, 0.02, 0, 0.245, 1.95, GLOWS[g])
    elif k == "armor_stand":
        cy(A, 0.3, 0.06, 0, 0, 0.0, "gunmetal", verts=20); suit(0.0, "hull_dark"); strip(A, 0.3, 0.012, 0.03, 0, -0.14, 1.2, GLOWS[g])
    else:
        bx(A, 1.2, 0.3, 0.05, 0, 0, 1.2, "hull_dark", 0.01); bx(A, 1.2, 0.3, 0.05, 0, 0, 0.8, "hull_dark", 0.01); bx(A, 0.05, 0.3, 0.7, -0.6, 0, 0.6, "gunmetal"); bx(A, 0.05, 0.3, 0.7, 0.6, 0, 0.6, "gunmetal")
        for i in range(3):
            for z in (1.25, 0.85): sph(A, 0.11, (-0.4 + i * 0.4, 0, z + 0.11), "hull_grey" if i % 2 else "hull", seg=12); sph(A, 0.07, (-0.4 + i * 0.4, -0.07, z + 0.12), "glass_cyan", scale=(1, 0.5, 0.8), seg=8)
        strip(A, 1.1, 0.012, 0.02, 0, -0.155, 1.2, GLOWS[g])


@family("locker_bank", "signature", [{"n": "gym_row", "glow": "cyan"}, {"n": "crew_cubbies", "glow": "amber"}, {"n": "security_lockers", "glow": "red"}, {"n": "mail_wall", "glow": "green"}, {"n": "bio_vault", "glow": "violet"}],
        cat="scifi", place="floor", tags=["storage", "wall-hug", "tall"])
def _lockers(A, v):
    k, g = v["n"], v["glow"]
    W, D, H = 1.6, 0.5, 1.9
    bx(A, W, D, H, 0, 0, 0.0, "hull_grey" if k != "security_lockers" else "gunmetal", 0.02)
    if k in ("gym_row", "security_lockers"):
        for i in range(4):
            x = -0.6 + i * 0.4; bx(A, 0.36, 0.02, H - 0.1, x, -D / 2 - 0.005, 0.05, "hull" if k == "gym_row" else "hull_dark", 0.01); strip(A, 0.02, 0.012, 0.15, x + 0.12, -D / 2 - 0.02, 1.0, GLOWS[g]); [bx(A, 0.2, 0.01, 0.015, x, -D / 2 - 0.015, 1.65 + j * 0.04, "hull_dark") for j in range(3)]
    elif k == "crew_cubbies":
        for i in range(4):
            for j in range(4): bx(A, 0.34, 0.4, 0.4, -0.6 + i * 0.4, -0.05, 0.05 + j * 0.46, "hull_dark", 0.01); strip(A, 0.2, 0.012, 0.012, -0.6 + i * 0.4, -D / 2 - 0.0, 0.1 + j * 0.46, GLOWS[g])
    elif k == "mail_wall":
        for i in range(8):
            for j in range(5): bx(A, 0.17, 0.02, 0.3, -0.7 + i * 0.2, -D / 2 - 0.005, 0.1 + j * 0.35, "hull", 0.006); strip(A, 0.03, 0.012, 0.03, -0.7 + i * 0.2, -D / 2 - 0.02, 0.35 + j * 0.35, GLOWS[g] if (i + j) % 3 else "neon_amber")
    else:
        for i in range(2): bx(A, 0.7, 0.03, H - 0.2, -0.4 + i * 0.8, -D / 2 - 0.01, 0.1, "hull_dark", 0.01); box(A, (0.5, 0.01, 0.6), (-0.4 + i * 0.8, -D / 2 - 0.03, 1.2), "glass_cyan", bevel=0); cy(A, 0.12, 0.3, -0.4 + i * 0.8, -0.1, 0.9, GLOWS[g], verts=14)
        screen(A, 0.2, 0.1, 0, -D / 2 - 0.01, 1.7, SCRS[g], "hull_dark", face=-1)


@family("android", "signature", [{"n": "service_bot", "glow": "cyan"}, {"n": "bartender", "glow": "magenta"}, {"n": "guard_mech", "glow": "red"}, {"n": "display_mannequin", "glow": "violet"}],
        cat="scifi", place="floor", tags=["decor", "light", "glow"], light=0.4)
def _andr(A, v):
    k, g = v["n"], v["glow"]
    if k == "service_bot":
        cy(A, 0.28, 0.1, 0, 0, 0.0, "gunmetal", verts=24); cyl(A, 0.22, 0.9, (0, 0, 0.55), "hull", r2=0.15, verts=20); sph(A, 0.15, (0, 0, 1.15), "hull", seg=14); sph(A, 0.08, (0, -0.1, 1.17), GLOWS[g], scale=(1.3, 0.4, 0.6), seg=10)
        for s in (-1, 1): limb(A, (s * 0.2, 0, 0.9), (s * 0.3, -0.1, 0.5), 0.04, 0.03, "gunmetal", 8)
        tor(A, 0.21, 0.01, (0, 0, 0.7), GLOWS[g], seg=24, minor=5)
    elif k == "bartender":
        bx(A, 0.5, 0.35, 0.7, 0, 0, 0.9, "hull", 0.06); bx(A, 0.35, 0.3, 0.9, 0, 0, 0.0, "hull_dark", 0.04); sph(A, 0.14, (0, 0, 1.75), "chrome", seg=14); sph(A, 0.1, (0, -0.1, 1.75), GLOWS[g], scale=(1.4, 0.4, 0.5), seg=10)
        for s in (-1, 1): limb(A, (s * 0.3, 0, 1.5), (s * 0.35, -0.2, 1.0), 0.05, 0.04, "chrome", 8); sph(A, 0.05, (s * 0.35, -0.2, 1.0), "chrome", seg=8)
        bx(A, 0.4, 0.015, 0.2, 0, -0.18, 1.2, GLOWS[g], 0)
    elif k == "guard_mech":
        for s in (-1, 1): bx(A, 0.25, 0.3, 0.2, s * 0.25, 0, 0.0, "gunmetal", 0.03); limb(A, (s * 0.25, 0, 0.2), (s * 0.25, 0.05, 1.0), 0.09, 0.08, "hull_dark", 8); limb(A, (s * 0.55, 0, 1.8), (s * 0.6, -0.15, 1.1), 0.09, 0.07, "hull_dark", 8); sph(A, 0.15, (s * 0.55, 0, 1.85), "p_red", seg=10)
        bx(A, 0.9, 0.5, 0.9, 0, 0, 1.0, "hull_dark", 0.05); bx(A, 0.35, 0.3, 0.3, 0, 0, 1.95, "hull_dark", 0.05); bx(A, 0.25, 0.02, 0.06, 0, -0.16, 2.05, GLOWS[g], 0)
        for s in (-1, 1): bx(A, 0.1, 0.1, 0.5, s * 0.63, -0.15, 0.6, "carbon", 0.02)
    else:
        cy(A, 0.3, 0.05, 0, 0, 0.0, "hull_dark", verts=20); cy(A, 0.03, 0.4, 0, 0, 0.05, "chrome")
        limb(A, (0, 0, 0.45), (0, 0, 1.0), 0.14, 0.17, "hull", 10); sph(A, 0.18, (0, 0, 1.15), "hull", scale=(1, 0.8, 1.2), seg=12); sph(A, 0.12, (0, 0, 1.55), "hull", seg=12); cy(A, 0.04, 0.12, 0, 0, 1.4, "hull", verts=8)
        for s in (-1, 1): limb(A, (s * 0.2, 0, 1.25), (s * 0.35, 0, 0.8), 0.05, 0.04, "hull", 8); tor(A, 0.2, 0.008, (0, 0, 1.0), GLOWS[g], seg=24, minor=5)


@family("terminal_kiosk", "signature", [{"n": "info_pillar", "glow": "cyan"}, {"n": "ticket_booth", "glow": "amber"}, {"n": "map_kiosk", "glow": "green"}, {"n": "hack_deck", "glow": "magenta"}],
        cat="scifi", place="floor", tags=["decor", "light", "glow"], light=0.6)
def _kiosk(A, v):
    k, g = v["n"], v["glow"]
    if k == "info_pillar":
        bx(A, 0.5, 0.35, 1.7, 0, 0, 0.0, "hull_dark", 0.04); screen(A, 0.42, 0.7, 0, -0.18, 0.9, SCRS[g], "hull", face=-1); strip(A, 0.4, 0.012, 0.03, 0, -0.18, 0.15, GLOWS[g]); bx(A, 0.56, 0.4, 0.08, 0, 0, 1.7, "hull", 0.02)
    elif k == "ticket_booth":
        bx(A, 1.0, 0.7, 1.1, 0, 0, 0.0, "hull", 0.04); bx(A, 1.1, 0.8, 0.05, 0, 0, 1.1, "hull_dark", 0.02); bx(A, 0.06, 0.7, 1.2, -0.5, 0, 1.1, "glass_cyan", 0.0) if False else box(A, (1.0, 0.02, 0.9), (0, -0.4, 1.6), "glass_cyan", bevel=0)
        screen(A, 0.4, 0.28, 0, -0.35, 0.8, SCRS[g], "hull_dark", face=-1); strip(A, 0.9, 0.012, 0.03, 0, -0.355, 0.1, GLOWS[g]); bx(A, 1.1, 0.8, 0.06, 0, 0, 2.05, "hull_dark", 0.02)
    elif k == "map_kiosk":
        cy(A, 0.3, 0.1, 0, 0, 0.0, "gunmetal", verts=24); cy(A, 0.07, 1.0, 0, 0, 0.1, "chrome"); prism(A, [(-0.5, 0), (0.5, 0), (0.5, 0.7), (-0.5, 0.7)], 0.05, (0, -0.05, 1.45), "hull_dark", rot=(0.2, 0, 0), bevel=0.02)
        box(A, (0.9, 0.01, 0.6), (0, -0.075, 1.45), SCRS[g], (0.2, 0, 0), 0); strip(A, 1.0, 0.012, 0.02, 0, -0.08, 1.12, GLOWS[g])
    else:
        bx(A, 1.0, 0.6, 0.75, 0, 0, 0.0, "carbon", 0.03); bx(A, 1.0, 0.5, 0.06, 0, -0.05, 0.75, "hull_dark", 0.02, rot=(0.2, 0, 0))
        box(A, (0.9, 0.01, 0.4), (0, 0.2, 1.1), SCRS[g], (-0.2, 0, 0), 0); box(A, (0.7, 0.01, 0.2), (0, -0.05, 0.93), GLOWS[g], (0.2, 0, 0), 0); strip(A, 0.9, 0.012, 0.02, 0, -0.305, 0.1, GLOWS[g])
