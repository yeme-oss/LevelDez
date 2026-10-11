# ============ SLEEP & STORAGE: bed, nightstand, wardrobe, dresser ============

def _under(A, w, d, x, y, z0, g, t=0.02):
    """Underglow: four thin strips round a base."""
    m = GLOWS[g]
    strip(A, w, t, 0.025, x, y - d / 2 + 0.01, z0, m); strip(A, w, t, 0.025, x, y + d / 2 - 0.01, z0, m)
    strip(A, t, d, 0.025, x - w / 2 + 0.01, y, z0, m); strip(A, t, d, 0.025, x + w / 2 - 0.01, y, z0, m)


@family("bed", "furniture", [{"n": "pod", "glow": "cyan"}, {"n": "float", "glow": "magenta"}, {"n": "ribbed", "glow": "amber"}, {"n": "capsule", "glow": "green"}, {"n": "bunk_cot", "glow": "violet"}, {"n": "hex", "glow": "blue"}],
        cat="sleep", place="floor", tags=["bed", "headwall"], **{"as": "bed"})
def _bed(A, v):
    k, g = v["n"], v["glow"]
    W, D = 1.6, 2.05
    if k == "pod":
        bx(A, W, D, 0.3, 0, 0, 0.0, "hull", 0.05); _under(A, W - 0.1, D - 0.1, 0, 0, 0.02, g)
        pad(A, W - 0.1, D - 0.3, 0.2, 0, -0.05, 0.3, "cloth"); pad(A, W - 0.2, 0.55, 0.12, 0, 0.7, 0.5, "foam", 0.05)
        pad(A, 1.0, 0.6, 0.1, 0, 0.55, 0.52, "cloth2")
        bx(A, W, 0.12, 1.15, 0, D / 2 - 0.06, 0.3, "hull", 0.04); strip(A, W - 0.3, 0.02, 0.05, 0, D / 2 - 0.13, 1.0, GLOWS[g])
        for s in (-1, 1): bx(A, 0.06, D - 0.2, 0.55, s * (W / 2 - 0.03), -0.05, 0.3, "hull", 0.03)
    elif k == "float":
        cy(A, 0.28, 0.1, 0, 0.1, 0.0, "gunmetal", r2=0.22, verts=24); bx(A, W, D, 0.12, 0, 0, 0.12, "hull_dark", 0.04)
        _under(A, W - 0.05, D - 0.05, 0, 0, 0.1, g); pad(A, W - 0.1, D - 0.1, 0.22, 0, 0, 0.24, "foam", 0.06)
        pad(A, W - 0.1, 1.3, 0.04, 0, -0.35, 0.44, "cloth", 0.02); pad(A, 0.65, 0.4, 0.12, -0.35, 0.8, 0.46, "cloth2", 0.05); pad(A, 0.65, 0.4, 0.12, 0.35, 0.8, 0.46, "cloth2", 0.05)
        prism(A, [(-W / 2, 0), (W / 2, 0), (W / 2 - 0.1, 0.7), (-W / 2 + 0.1, 0.7)], 0.08, (0, D / 2 - 0.04, 0.5), "hull", bevel=0.02); strip(A, W - 0.3, 0.02, 0.04, 0, D / 2 - 0.09, 1.0, GLOWS[g])
    elif k == "ribbed":
        bx(A, W, D, 0.35, 0, 0, 0.0, "hull_dark", 0.03); pad(A, W - 0.08, D - 0.1, 0.22, 0, 0, 0.35, "cloth", 0.05)
        for i in range(7): bx(A, W - 0.1, 0.07, 0.07, 0, -D / 2 + 0.2 + i * 0.28, 0.57, "pad", 0.02)
        bx(A, W, 0.2, 1.3, 0, D / 2 - 0.1, 0.0, "hull_dark", 0.04)
        for i in range(5): bx(A, W - 0.2, 0.04, 0.12, 0, D / 2 - 0.22, 0.6 + i * 0.17, "pad", 0.02)
        strip(A, W - 0.3, 0.02, 0.03, 0, D / 2 - 0.205, 1.3, GLOWS[g]); _under(A, W - 0.1, D - 0.1, 0, 0, 0.05, g)
        pad(A, 0.6, 0.4, 0.12, -0.35, 0.75, 0.57, "foam", 0.05); pad(A, 0.6, 0.4, 0.12, 0.35, 0.75, 0.57, "foam", 0.05)
    elif k == "capsule":
        bx(A, W, D, 0.28, 0, 0, 0.0, "hull", 0.06); pad(A, W - 0.2, D - 0.5, 0.16, 0, 0.1, 0.28, "cloth", 0.05)
        hood = [(-W / 2, 0.0), (W / 2, 0.0), (W / 2 - 0.12, 0.75), (0, 0.98), (-W / 2 + 0.12, 0.75)]
        prism(A, hood, D * 0.62, (0, D * 0.19, 0.28), "glass_cyan", bevel=0.04)
        for sy in (-1, 1): prism(A, hood, 0.05, (0, D * 0.19 + sy * D * 0.31, 0.28), "hull", bevel=0.01)
        _under(A, W - 0.05, D - 0.05, 0, 0, 0.02, g); bx(A, 0.5, 0.1, 0.06, 0, -D / 2 + 0.05, 0.28, "hull_dark"); strip(A, 0.3, 0.02, 0.02, 0, -D / 2 + 0.005, 0.3, GLOWS[g])
    elif k == "bunk_cot":
        for s in (-1, 1):
            for sy in (-1, 1): bx(A, 0.07, 0.07, 0.55, s * (W / 2 - 0.04), sy * (D / 2 - 0.04), 0.0, "gunmetal", 0.01)
        bx(A, W, D, 0.07, 0, 0, 0.3, "steel", 0.01); pad(A, W - 0.1, D - 0.15, 0.14, 0, 0, 0.37, "cloth", 0.04); pad(A, 0.55, 0.38, 0.1, 0, 0.78, 0.51, "foam", 0.05)
        pad(A, W - 0.12, 0.85, 0.05, 0, -0.55, 0.51, "cloth2", 0.02); bx(A, W, 0.06, 0.35, 0, D / 2 - 0.03, 0.3, "gunmetal", 0.01); _under(A, W - 0.1, D - 0.1, 0, 0, 0.26, g)
    else:  # hex
        pts = [(-0.4, -1.0), (0.4, -1.0), (0.8, 0.0), (0.4, 1.0), (-0.4, 1.0), (-0.8, 0.0)]
        prism(A, topview(pts), 0.3, (0, 0, 0.15), "hull", rot=(PI / 2, 0, 0), bevel=0.04)
        prism(A, topview([(x * 0.93, y * 0.95) for x, y in pts]), 0.18, (0, 0, 0.38), "cloth", rot=(PI / 2, 0, 0), bevel=0.05)
        prism(A, topview([(x * 0.95, y * 0.95) for x, y in pts]), 0.025, (0, 0, 0.03), GLOWS[g], rot=(PI / 2, 0, 0), bevel=0)
        pad(A, 0.65, 0.4, 0.12, -0.3, 0.75, 0.47, "foam", 0.05); pad(A, 0.65, 0.4, 0.12, 0.3, 0.75, 0.47, "foam", 0.05)
        bx(A, 1.2, 0.1, 0.9, 0, 1.0, 0.3, "hull_dark", 0.03); strip(A, 1.0, 0.02, 0.03, 0, 0.94, 1.0, GLOWS[g])


@family("nightstand", "furniture", [{"n": "cube", "glow": "cyan"}, {"n": "drum", "glow": "magenta"}, {"n": "floating", "glow": "amber"}, {"n": "tower", "glow": "green"}, {"n": "charger", "glow": "violet"}],
        cat="storage", place="floor", tags=["holds-decor", "beside"], **{"as": "nightstand"})
def _ns(A, v):
    k, g = v["n"], v["glow"]
    if k == "cube":
        bx(A, 0.45, 0.4, 0.5, 0, 0, 0.0, "hull", 0.03); bx(A, 0.37, 0.01, 0.16, 0, -0.205, 0.28, "hull_dark"); strip(A, 0.2, 0.012, 0.015, 0, -0.208, 0.3, GLOWS[g]); bx(A, 0.37, 0.01, 0.16, 0, -0.205, 0.08, "hull_dark")
    elif k == "drum":
        cy(A, 0.22, 0.5, 0, 0, 0.0, "hull", verts=28); tor(A, 0.22, 0.008, (0, 0, 0.35), GLOWS[g], seg=32, minor=6); cy(A, 0.23, 0.03, 0, 0, 0.47, "gunmetal", verts=28)
    elif k == "floating":
        bx(A, 0.45, 0.4, 0.2, 0, 0, 0.25, "hull", 0.04); bx(A, 0.35, 0.01, 0.08, 0, -0.205, 0.31, "hull_dark"); strip(A, 0.4, 0.38, 0.018, 0, 0, 0.22, GLOWS[g]); bx(A, 0.1, 0.1, 0.22, 0, 0.14, 0.0, "gunmetal")
    elif k == "tower":
        bx(A, 0.34, 0.34, 0.55, 0, 0, 0.0, "hull_dark", 0.025)
        for i in range(3):
            bx(A, 0.3, 0.01, 0.12, 0, -0.176, 0.06 + i * 0.17, "hull_grey"); strip(A, 0.06, 0.012, 0.012, 0.1, -0.18, 0.12 + i * 0.17, GLOWS[g])
        bx(A, 0.4, 0.38, 0.03, 0, 0, 0.55, "hull", 0.015)
    else:
        bx(A, 0.45, 0.4, 0.46, 0, 0, 0.0, "gunmetal", 0.03); cy(A, 0.12, 0.015, 0, 0, 0.46, "hull_dark", verts=24); tor(A, 0.12, 0.006, (0, 0, 0.475), GLOWS[g], seg=28, minor=6); bx(A, 0.37, 0.01, 0.2, 0, -0.205, 0.1, "hull_grey")


@family("wardrobe", "furniture", [{"n": "locker_wall", "glow": "cyan"}, {"n": "sliding", "glow": "amber"}, {"n": "ribbed", "glow": "magenta"}, {"n": "cabinet_tall", "glow": "green"}, {"n": "airlock_closet", "glow": "red"}],
        cat="storage", place="floor", tags=["storage", "wall-hug", "tall"], **{"as": "wardrobe"})
def _wd(A, v):
    k, g = v["n"], v["glow"]
    W, D, H = 1.3, 0.62, 2.1
    if k == "locker_wall":
        bx(A, W, D, H, 0, 0, 0.0, "hull_grey", 0.02)
        for i in range(3):
            x = -W / 3 + i * W / 3; bx(A, W / 3 - 0.04, 0.02, H - 0.2, x, -D / 2 - 0.005, 0.1, "hull", 0.01)
            for j in range(5): bx(A, W / 3 - 0.16, 0.01, 0.02, x, -D / 2 - 0.018, 1.7 + j * 0.05, "hull_dark", 0)
            bx(A, 0.03, 0.03, 0.25, x + 0.12, -D / 2 - 0.03, 1.0, "chrome", 0.005); strip(A, 0.08, 0.012, 0.012, x, -D / 2 - 0.02, 1.95, GLOWS[g])
    elif k == "sliding":
        bx(A, W, D, H, 0, 0, 0.0, "hull_dark", 0.02); bx(A, W / 2 + 0.05, 0.03, H - 0.16, -W / 4 - 0.02, -D / 2 - 0.01, 0.08, "hull", 0.015); bx(A, W / 2 + 0.05, 0.03, H - 0.16, W / 4 + 0.02, -D / 2 - 0.03, 0.08, "hull_grey", 0.015)
        strip(A, 0.02, 0.012, H - 0.3, 0, -D / 2 - 0.05, 0.15, GLOWS[g]); bx(A, 0.04, 0.04, 0.5, -0.05, -D / 2 - 0.06, 0.8, "chrome", 0.005)
    elif k == "ribbed":
        bx(A, W, D, H, 0, 0, 0.0, "hull_dark", 0.02)
        for i in range(12): bx(A, W - 0.1, 0.03, 0.05, 0, -D / 2 - 0.005, 0.15 + i * 0.16, "hull_grey", 0.01)
        strip(A, 0.03, 0.012, H - 0.2, -W / 2 + 0.08, -D / 2 - 0.02, 0.1, GLOWS[g]); strip(A, 0.03, 0.012, H - 0.2, W / 2 - 0.08, -D / 2 - 0.02, 0.1, GLOWS[g])
    elif k == "cabinet_tall":
        bx(A, W, D, H, 0, 0, 0.0, "hull", 0.03)
        for sx in (-1, 1):
            bx(A, W / 2 - 0.05, 0.02, H - 0.25, sx * (W / 4), -D / 2 - 0.005, 0.12, "hull_grey", 0.012); bx(A, 0.025, 0.03, 0.4, sx * 0.05, -D / 2 - 0.03, 1.0, "steel", 0.005)
        bx(A, W, 0.02, 0.14, 0, -D / 2 - 0.01, H - 0.14, "hull_dark"); strip(A, W - 0.2, 0.012, 0.02, 0, -D / 2 - 0.02, H - 0.1, GLOWS[g])
    else:  # airlock_closet: suit locker with porthole
        bx(A, W, D, H, 0, 0, 0.0, "hull", 0.02); bx(A, W - 0.2, 0.05, H - 0.2, 0, -D / 2 - 0.01, 0.1, "hull_grey", 0.02)
        cy(A, 0.28, 0.06, 0, -D / 2 - 0.04, 1.05, "glass_cyan", verts=24, rot=(PI / 2, 0, 0)); tor(A, 0.28, 0.025, (0, -D / 2 - 0.045, 1.35), "steel", rot=(PI / 2, 0, 0), seg=28, minor=8)
        bx(A, 0.05, 0.05, 0.3, W / 2 - 0.2, -D / 2 - 0.06, 0.9, "p_yellow", 0.01); strip(A, 0.4, 0.012, 0.03, 0, -D / 2 - 0.04, 0.45, GLOWS[g])


@family("dresser", "furniture", [{"n": "drawer_stack", "glow": "cyan"}, {"n": "crate_low", "glow": "amber"}, {"n": "console_chest", "glow": "magenta"}, {"n": "modular", "glow": "green"}],
        cat="storage", place="floor", tags=["storage", "wall-hug", "holds-decor"], **{"as": "dresser"})
def _dr(A, v):
    k, g = v["n"], v["glow"]
    W, D, H = 1.2, 0.46, 0.85
    if k == "drawer_stack":
        legs4(A, W, D, 0.12, 0.05, "gunmetal"); bx(A, W, D, H - 0.12, 0, 0, 0.12, "hull", 0.025)
        for i in range(4):
            bx(A, W - 0.1, 0.02, 0.15, 0, -D / 2 - 0.005, 0.2 + i * 0.17, "hull_grey", 0.01); strip(A, 0.3, 0.012, 0.012, 0, -D / 2 - 0.02, 0.3 + i * 0.17, GLOWS[g])
    elif k == "crate_low":
        bx(A, W, D, H, 0, 0, 0.0, "hull_dark", 0.02)
        for i in range(2):
            for j in range(3): bx(A, W / 3 - 0.06, 0.02, H / 2 - 0.08, -W / 3 + j * W / 3, -D / 2 - 0.005, 0.05 + i * H / 2, "p_orange" if (i + j) % 3 == 0 else "hull_grey", 0.012)
        strip(A, W - 0.1, 0.012, 0.015, 0, -D / 2 - 0.02, 0.02, GLOWS[g])
    elif k == "console_chest":
        bx(A, W, D, 0.5, 0, 0, 0.2, "hull", 0.03); cy(A, 0.06, 0.2, -W / 2 + 0.1, 0, 0.0, "gunmetal"); cy(A, 0.06, 0.2, W / 2 - 0.1, 0, 0.0, "gunmetal")
        bx(A, W - 0.1, 0.02, 0.16, 0, -D / 2 - 0.005, 0.5, "hull_grey", 0.01); screen(A, 0.5, 0.3, 0, D / 2 - 0.05, 0.7, SCRS[g], "hull_dark", face=-1)
        strip(A, W - 0.1, 0.012, 0.015, 0, -D / 2 - 0.02, 0.22, GLOWS[g])
    else:  # modular
        for i in range(3):
            bx(A, W / 3 - 0.02, D, H, -W / 3 + i * W / 3, 0, 0.0, ["hull", "hull_grey", "hull"][i], 0.03)
            bx(A, W / 3 - 0.1, 0.02, 0.1 + 0.05 * i, -W / 3 + i * W / 3, -D / 2 - 0.005, 0.5, "hull_dark", 0.01)
            strip(A, W / 3 - 0.12, 0.012, 0.015, -W / 3 + i * W / 3, -D / 2 - 0.02, 0.15 + i * 0.1, GLOWS[g])
