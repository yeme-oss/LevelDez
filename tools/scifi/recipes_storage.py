# ============ STORAGE & KITCHEN: bookshelf, fridge, kitchen_counter ============

def lt(g, y, i=1.0):
    """Variant meta for a glowing asset."""
    return {"light": i, "lightColor": LIGHTC[g], "lightY": y}


@family("bookshelf", "furniture", [{"n": "data_rack", "glow": "cyan"}, {"n": "open_grid", "glow": "amber"}, {"n": "archive_wall", "glow": "magenta"}, {"n": "slot_tower", "glow": "green"}, {"n": "crate_shelf", "glow": "red"}],
        cat="storage", place="floor", tags=["storage", "wall-hug", "holds-decor"], **{"as": "bookshelf"})
def _bks(A, v):
    k, g = v["n"], v["glow"]
    W, D, H = 0.95, 0.32, 1.9
    bx(A, 0.04, D, H, -W / 2 + 0.02, 0, 0.0, "hull_dark", 0.005); bx(A, 0.04, D, H, W / 2 - 0.02, 0, 0.0, "hull_dark", 0.005); bx(A, W, 0.02, H, 0, D / 2 - 0.01, 0.0, "hull_grey", 0.005)
    n = 5
    for i in range(n + 1): bx(A, W, D, 0.03, 0, 0, 0.0 + i * (H - 0.03) / n, "hull", 0.004)
    for i in range(n):
        z = 0.03 + i * (H - 0.03) / n; sh = (H - 0.03) / n - 0.03
        if k == "data_rack":
            for j in range(3):
                x = -0.28 + j * 0.28; bx(A, 0.24, 0.22, sh - 0.06, x, 0, z + 0.03, "gunmetal", 0.008)
                strip(A, 0.18, 0.012, 0.012, x, -0.115, z + 0.05 + (i + j) % 3 * 0.05, GLOWS[g] if (i + j) % 2 else "neon_white")
        elif k == "open_grid":
            for j in range(4): bx(A, 0.2, 0.2, 0.08 + (j * 7 + i * 3) % 4 * 0.03, -0.3 + j * 0.2, 0, z, ["hull", "p_orange", "hull_grey", "p_teal"][(i + j) % 4], 0.01)
            strip(A, W - 0.1, 0.012, 0.012, 0, -D / 2 + 0.01, z + 0.0, GLOWS[g])
        elif k == "archive_wall":
            for j in range(9): bx(A, 0.08, 0.2, sh - 0.05 - (j % 3) * 0.03, -0.37 + j * 0.092, 0, z, ["hull", "hull_grey", "p_teal", "steel"][(i + j) % 4], 0.006)
        elif k == "slot_tower":
            bx(A, W - 0.1, 0.01, sh - 0.04, 0, -D / 2 + 0.02, z + 0.02, "hull_grey", 0.004); strip(A, 0.012, 0.012, sh - 0.06, -0.3, -D / 2 + 0.01, z + 0.03, GLOWS[g]); strip(A, 0.012, 0.012, sh - 0.06, 0.3, -D / 2 + 0.01, z + 0.03, GLOWS[g])
        else:
            for j in range(2): bx(A, 0.4, 0.26, sh - 0.04, -0.22 + j * 0.44, 0, z + 0.02, "p_yellow" if (i + j) % 3 == 0 else "hull_grey", 0.012)
            strip(A, 0.06, 0.012, 0.012, -0.22, -D / 2 + 0.01, z + 0.1, GLOWS[g])


@family("fridge", "furniture", [{"n": "cryo_unit", "glow": "cyan"}, {"n": "slab_steel", "glow": "amber"}, {"n": "ration_vault", "glow": "green"}],
        cat="kitchen", place="floor", tags=["kitchen", "wall-hug", "tall"], **{"as": "fridge"})
def _fr(A, v):
    k, g = v["n"], v["glow"]
    W, D, H = 0.72, 0.7, 1.85
    if k == "cryo_unit":
        bx(A, W, D, H, 0, 0, 0.0, "hull", 0.04); bx(A, W - 0.1, 0.03, 0.9, 0, -D / 2 - 0.005, 0.9, "glass_cyan", 0.01); bx(A, W - 0.1, 0.02, 0.7, 0, -D / 2 - 0.005, 0.1, "hull_grey", 0.01)
        strip(A, 0.02, 0.012, 1.4, W / 2 - 0.06, -D / 2 - 0.015, 0.2, GLOWS[g]); screen(A, 0.2, 0.1, 0, -D / 2 - 0.02, 1.7, SCRS[g], "hull_dark", face=-1)
    elif k == "slab_steel":
        bx(A, W, D, H, 0, 0, 0.0, "steel", 0.03); bx(A, 0.02, 0.03, 0.5, W / 2 - 0.1, -D / 2 - 0.02, 0.9, "chrome"); bx(A, W - 0.06, 0.012, 0.01, 0, -D / 2 - 0.006, 1.0, "hull_dark")
        strip(A, 0.2, 0.012, 0.014, -0.15, -D / 2 - 0.01, 1.65, GLOWS[g]); bx(A, W - 0.06, 0.04, 0.1, 0, -D / 2 - 0.01, 0.0, "hull_dark")
    else:
        bx(A, W, D, H, 0, 0, 0.0, "hull_grey", 0.02); bx(A, W - 0.12, 0.05, H - 0.2, 0, -D / 2 - 0.01, 0.1, "hull", 0.02)
        cy(A, 0.08, 0.05, 0, -D / 2 - 0.05, 1.0, "steel", rot=(PI / 2, 0, 0)); bx(A, 0.3, 0.012, 0.06, 0, -D / 2 - 0.04, 1.5, "hull_dark"); strip(A, 0.2, 0.012, 0.014, 0, -D / 2 - 0.047, 1.52, GLOWS[g])


@family("kitchen_counter", "furniture", [{"n": "prep_unit", "glow": "cyan"}, {"n": "galley_run", "glow": "amber"}, {"n": "nutri_synth", "glow": "green"}, {"n": "island_block", "glow": "magenta"}],
        cat="kitchen", place="floor", tags=["kitchen", "wall-hug", "holds-decor", "run"], **{"as": "kitchen_counter"})
def _kc(A, v):
    k, g = v["n"], v["glow"]
    W, D, H = 1.2, 0.62, 0.92
    bx(A, W, D - 0.04, H - 0.06, 0, 0.02, 0.0, "hull", 0.02); bx(A, W - 0.06, 0.04, 0.1, 0, -D / 2 + 0.02, 0.0, "hull_dark")
    bx(A, W + 0.02, D, 0.05, 0, 0, H - 0.05, "steel" if k != "island_block" else "hull_dark", 0.01)
    if k == "prep_unit":
        for i in range(2): bx(A, W / 2 - 0.06, 0.02, H - 0.25, -W / 4 + i * W / 2, -D / 2 + 0.0, 0.14, "hull_grey", 0.01)
        cy(A, 0.02, 0.01, 0.3, 0, H, "chrome"); bx(A, 0.35, 0.3, 0.03, -0.25, 0.0, H - 0.01, "hull_dark"); strip(A, W - 0.1, 0.012, 0.014, 0, -D / 2 - 0.005, H - 0.07, GLOWS[g])
    elif k == "galley_run":
        for i in range(3): bx(A, W / 3 - 0.05, 0.02, H - 0.25, -W / 3 + i * W / 3, -D / 2, 0.14, "hull_grey" if i != 1 else "p_orange", 0.01)
        for i in range(2): cy(A, 0.07, 0.01, -0.3 + i * 0.3, 0.0, H, "gunmetal"); tor(A, 0.07, 0.008, (-0.3 + i * 0.3, 0, H + 0.01), GLOWS[g], seg=20, minor=5)
    elif k == "nutri_synth":
        bx(A, 0.5, 0.4, 0.4, 0, 0.1, H, "hull_grey", 0.03); screen(A, 0.3, 0.2, 0, -0.1, H + 0.12, SCRS[g], "hull_dark", face=-1); bx(A, 0.2, 0.2, 0.01, 0, -0.05, H, "glass_cyan"); strip(A, 0.4, 0.012, 0.014, 0, -D / 2 - 0.005, H - 0.07, GLOWS[g])
        for i in range(2): bx(A, W / 2 - 0.06, 0.02, H - 0.25, -W / 4 + i * W / 2, -D / 2, 0.14, "hull_grey", 0.01)
    else:
        bx(A, W - 0.1, 0.03, H - 0.3, 0, -D / 2 - 0.01, 0.15, "hull_dark", 0.01); strip(A, W - 0.1, 0.012, 0.018, 0, -D / 2 - 0.02, 0.05, GLOWS[g]); strip(A, W - 0.1, D - 0.1, 0.01, 0, 0, H, GLOWS[g])
