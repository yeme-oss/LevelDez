# ============ ARCHITECTURE: pillars, pilasters, door/window surrounds, ceiling details, floor decals ============

@family("pillar", "architecture", [{"n": "plain_column", "glow": "cyan"}, {"n": "ribbed_support", "glow": "amber"}, {"n": "hex_strut", "glow": "magenta"}, {"n": "conduit_pillar", "glow": "green"}],
        cat="architecture", place="floor", tags=["arch", "pillar", "decor"])
def _pillar(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]; H = 2.7
    if k == "plain_column":
        cy(A, 0.28, H, 0, 0, 0.0, "hull", verts=24); cy(A, 0.34, 0.15, 0, 0, 0.0, "gunmetal", verts=24); cy(A, 0.34, 0.15, 0, 0, H - 0.15, "gunmetal", verts=24); tor(A, 0.29, 0.015, (0, 0, 0.5), m, seg=28, minor=5); tor(A, 0.29, 0.015, (0, 0, H - 0.5), m, seg=28, minor=5)
    elif k == "ribbed_support":
        bx(A, 0.6, 0.6, H, 0, 0, 0.0, "hull_dark", 0.03)
        for i in range(8): bx(A, 0.64, 0.64, 0.06, 0, 0, 0.2 + i * 0.3, "hull_grey", 0.01)
        for sx in (-1, 1): strip(A, 0.02, 0.02, H - 0.3, sx * 0.31, -0.31, 0.15, m)
    elif k == "hex_strut":
        cy(A, 0.3, H, 0, 0, 0.0, "hull_grey", verts=6); cy(A, 0.36, 0.14, 0, 0, 0.0, "gunmetal", verts=6); cy(A, 0.36, 0.14, 0, 0, H - 0.14, "gunmetal", verts=6)
        for i in range(6): a = i * PI / 3 + PI / 6; strip(A, 0.02, 0.02, H - 0.6, 0.27 * math.cos(a), 0.27 * math.sin(a), 0.3, m) if False else bx(A, 0.025, 0.025, H - 0.6, 0.27 * math.cos(a), 0.27 * math.sin(a), 0.3, m, 0)
    else:
        cy(A, 0.3, H, 0, 0, 0.0, "hull_dark", verts=20)
        for i in range(5): a = i * 2 * PI / 5; cy(A, 0.04, H - 0.2, 0.32 * math.cos(a), 0.32 * math.sin(a), 0.1, "p_orange" if i % 2 else "steel", verts=8)
        tor(A, 0.31, 0.03, (0, 0, 1.0), "gunmetal", seg=28, minor=6); tor(A, 0.31, 0.012, (0, 0, 1.0), m, seg=28, minor=5)


@family("pilaster", "architecture", [{"n": "rib_panel", "glow": "cyan"}, {"n": "strut_light", "glow": "amber"}, {"n": "bulkhead_post", "glow": "red"}],
        cat="architecture", place="wall", y=0.0, tags=["arch", "pilaster", "decor"])
def _pilaster(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]; H = 2.7
    if k == "rib_panel":
        bx(A, 0.4, 0.16, H, 0, 0, 0.0, "hull_grey", 0.02)
        for i in range(10): bx(A, 0.44, 0.18, 0.04, 0, 0, 0.2 + i * 0.25, "hull", 0.008)
        strip(A, 0.03, 0.012, H - 0.4, 0, -0.085, 0.2, m)
    elif k == "strut_light":
        bx(A, 0.3, 0.14, H, 0, 0, 0.0, "hull_dark", 0.02); bx(A, 0.1, 0.02, H - 0.3, 0, -0.08, 0.15, "hull", 0.005); strip(A, 0.04, 0.012, H - 0.4, 0, -0.095, 0.2, m)
    else:
        bx(A, 0.5, 0.2, H, 0, 0, 0.0, "hull_grey", 0.02); bx(A, 0.1, 0.22, H, -0.2, 0, 0.0, "p_yellow", 0.01); bx(A, 0.1, 0.22, H, 0.2, 0, 0.0, "p_yellow", 0.01)
        [bx(A, 0.18, 0.012, 0.04, 0, -0.105, 0.3 + i * 0.5, m, 0) for i in range(5)]


@family("door_surround", "architecture", [{"n": "airlock_frame", "glow": "amber"}, {"n": "slim_trim", "glow": "cyan"}, {"n": "bulkhead_arch", "glow": "red"}],
        cat="architecture", place="wall", y=0.0, tags=["arch", "door-deco", "decor"])
def _door(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]; W, H = 1.1, 2.1
    if k == "airlock_frame":
        for s in (-1, 1): bx(A, 0.16, 0.14, H, s * (W / 2 + 0.08), 0, 0.0, "hull_grey", 0.02); bx(A, 0.04, 0.012, H - 0.2, s * (W / 2 + 0.02), -0.075, 0.1, m, 0)
        bx(A, W + 0.32, 0.14, 0.2, 0, 0, H, "hull_grey", 0.02); strip(A, W, 0.012, 0.03, 0, -0.075, H + 0.1, m)
        for i in range(8): box(A, (0.09, 0.012, 0.2), (-W / 2 - 0.08 + i * 0.001, -0.075, 0.1 + i * 0.1), "p_yellow" if i % 2 == 0 else "rubber", (0, 0, 0), 0) if False else None
        [bx(A, 0.14, 0.012, 0.05, s * (W / 2 + 0.08), -0.075, 0.05 + i * 0.1, "p_yellow" if i % 2 == 0 else "rubber", 0) for s in (-1, 1) for i in range(3)]
    elif k == "slim_trim":
        for s in (-1, 1): bx(A, 0.06, 0.08, H, s * (W / 2 + 0.03), 0, 0.0, "hull_dark", 0.01); strip(A, 0.012, 0.012, H, s * (W / 2 + 0.03), -0.045, 0.0, m)
        bx(A, W + 0.12, 0.08, 0.06, 0, 0, H, "hull_dark", 0.01); strip(A, W + 0.12, 0.012, 0.012, 0, -0.045, H + 0.02, m)
    else:
        for s in (-1, 1): bx(A, 0.2, 0.16, H - 0.4, s * (W / 2 + 0.1), 0, 0.0, "hull", 0.03)
        prism(A, [(-W / 2 - 0.2, 0), (W / 2 + 0.2, 0), (W / 2 + 0.2, 0.2), (W / 4, 0.4), (-W / 4, 0.4), (-W / 2 - 0.2, 0.2)], 0.16, (0, 0, H - 0.4), "hull", bevel=0.02)
        strip(A, W, 0.012, 0.03, 0, -0.085, H - 0.15, m)


@family("window_surround", "architecture", [{"n": "porthole_ring", "glow": "cyan"}, {"n": "slit_frame", "glow": "amber"}, {"n": "panoramic_trim", "glow": "violet"}],
        cat="architecture", place="wall", y=0.9, tags=["arch", "window-deco", "decor"])
def _win(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]; W, H = 1.55, 1.3
    if k == "porthole_ring":
        tor(A, 0.55, 0.06, (0, 0, H / 2), "steel", rot=(PI / 2, 0, 0), seg=40, minor=10); tor(A, 0.62, 0.015, (0, -0.03, H / 2), m, rot=(PI / 2, 0, 0), seg=40, minor=6)
        for i in range(8): a = i * PI / 4; cy(A, 0.025, 0.04, 0.6 * math.cos(a), 0, H / 2 + 0.6 * math.sin(a), "gunmetal", verts=8, rot=(PI / 2, 0, 0))
    elif k == "slit_frame":
        for s in (-1, 1): bx(A, 0.1, 0.1, H, s * (W / 2 + 0.05), 0, 0.0, "hull_dark", 0.01)
        bx(A, W + 0.2, 0.1, 0.1, 0, 0, H, "hull_dark", 0.01); bx(A, W + 0.2, 0.1, 0.1, 0, 0, -0.1, "hull_dark", 0.01); strip(A, W, 0.012, 0.015, 0, -0.055, H + 0.02, m); strip(A, W, 0.012, 0.015, 0, -0.055, -0.07, m)
    else:
        for s in (-1, 1): bx(A, 0.14, 0.12, H + 0.1, s * (W / 2 + 0.07), 0, -0.05, "hull_grey", 0.02); strip(A, 0.02, 0.012, H, s * (W / 2 + 0.07), -0.065, 0.0, m)
        for z in (-0.08, H): bx(A, W + 0.28, 0.12, 0.08, 0, 0, z, "hull_grey", 0.015)
        [bx(A, 0.03, 0.05, H, -W / 2 + i * W / 4, 0, 0.0, "steel", 0.005) for i in range(1, 4)]


@family("ceiling_detail", "architecture", [{"n": "rib_vault", "glow": "cyan"}, {"n": "cable_tray", "glow": "amber"}, {"n": "light_grid", "glow": "white"}, {"n": "duct_run", "glow": "green"}],
        cat="architecture", place="ceiling", tags=["arch", "ceiling-decor", "decor"])
def _ceil(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]
    if k == "rib_vault":
        for i in range(5): bx(A, 3.0, 0.14, 0.12, 0, -1.2 + i * 0.6, 0.0, "hull_grey", 0.015); bx(A, 0.14, 0.14, 0.2, -1.5, -1.2 + i * 0.6, -0.08, "hull_dark", 0.01)
        bx(A, 0.14, 3.0, 0.12, 0, 0, 0.0, "hull_grey", 0.015); strip(A, 2.8, 0.03, 0.012, 0, 0, -0.01, m)
    elif k == "cable_tray":
        bx(A, 0.4, 3.0, 0.06, 0, 0, 0.08, "gunmetal", 0.01); [bx(A, 0.4, 0.03, 0.14, 0, -1.4 + i * 0.4, 0.0, "hull_dark", 0.005) for i in range(8)]; [limb(A, (-0.1 + s * 0.08, -1.4, 0.1), (-0.1 + s * 0.08, 1.4, 0.1), 0.02, 0.02, [m, "rubber", "p_orange"][s + 1], 5) for s in (-1, 0, 1)]
    elif k == "light_grid":
        for i in range(3):
            for j in range(3): bx(A, 0.8, 0.8, 0.05, -1.0 + i * 1.0, -1.0 + j * 1.0, 0.0, "hull_grey", 0.01); bx(A, 0.7, 0.7, 0.012, -1.0 + i * 1.0, -1.0 + j * 1.0, -0.005, m, 0)
    else:
        cyl(A, 0.2, 3.0, (0, 0, 0.2), "hull", rot=(PI / 2, 0, 0), verts=20); [tor(A, 0.21, 0.03, (0, -1.2 + i * 0.6, 0.2), "gunmetal", rot=(PI / 2, 0, 0), seg=24, minor=6) for i in range(5)]; strip(A, 0.02, 2.8, 0.02, 0, 0, 0.0, m)


@family("floor_decal", "architecture", [{"n": "hazard_stripes", "glow": "amber", "meta": {"size": [1.2, 0.5, 0.02]}}, {"n": "path_arrows", "glow": "cyan", "meta": {"size": [1.4, 0.3, 0.02]}}, {"n": "deck_ring", "glow": "magenta", "meta": {"size": [1.0, 1.0, 0.03]}}],
        cat="architecture", place="floor", tags=["arch", "decal", "flat", "decor"])
def _decal(A, v):
    k, g = v["n"], v["glow"]; m = GLOWS[g]
    if k == "hazard_stripes":
        for i in range(12): box(A, (0.16, 0.5, 0.012), (-1.1 + i * 0.2, 0, 0.006), "p_yellow" if i % 2 == 0 else "rubber", (0, 0, 0.6), 0)
    elif k == "path_arrows":
        for i in range(3): x = -0.8 + i * 0.8; prism(A, [(-0.2, 0), (0.2, 0), (0.2, 0.0), (0, 0.0)], 0.01, (0, 0, 0), m, bevel=0) if False else box(A, (0.3, 0.06, 0.012), (x, 0.0, 0.006), m, (0, 0, 0.0), 0); limb(A, (x + 0.15, 0, 0.008), (x + 0.04, 0.1, 0.008), 0.03, 0.03, m, 4); limb(A, (x + 0.15, 0, 0.008), (x + 0.04, -0.1, 0.008), 0.03, 0.03, m, 4)
    else:
        tor(A, 0.9, 0.03, (0, 0, 0.02), m, seg=48, minor=5); tor(A, 0.7, 0.015, (0, 0, 0.02), "neon_white", seg=48, minor=4); [box(A, (0.04, 0.3, 0.012), (0.8 * math.cos(a), 0.8 * math.sin(a), 0.01), m, (0, 0, a), 0) for a in (0, PI / 2, PI, 3 * PI / 2)]
