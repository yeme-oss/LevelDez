# Small helpers for the scifi recipes. All dimensions in metres, z up, front = -Y.
def bx(A, w, d, h, x, y, z0, m="hull", bv=0.012, rot=(0, 0, 0)):
    """Box by width/depth/height, centre x,y and BOTTOM z0."""
    return box(A, (w, d, h), (x, y, z0 + h / 2), m, rot, bv)


def cy(A, r, h, x, y, z0, m="hull", r2=None, verts=20, rot=(0, 0, 0)):
    return cyl(A, r, h, (x, y, z0 + h / 2), m, r2=r2, verts=verts, rot=rot)


def glow(v, default="cyan"):
    return v.get("glow", default)


def gm(v, default="cyan"):
    return GLOWS[v.get("glow", default)]


def sm(v, default="cyan"):
    return SCRS[v.get("glow", default)]


def strip(A, w, d, h, x, y, z0, m="neon_cyan"):
    """Emissive light strip (no bevel)."""
    return box(A, (w, d, h), (x, y, z0 + h / 2), m, bevel=0)


def legs4(A, w, d, h, t=0.05, m="gunmetal", inset=0.06, z0=0.0):
    for sx in (-1, 1):
        for sy in (-1, 1):
            bx(A, t, t, h, sx * (w / 2 - inset), sy * (d / 2 - inset), z0, m, 0.004)


def screen(A, w, h, x, y, z0, m="scr_cyan", frame="gunmetal", face=-1, t=0.025):
    """Framed display facing -Y (face=-1) or +Y: frame box + emissive panel proud of it."""
    bx(A, w, t, h, x, y, z0, frame, 0.006)
    box(A, (w - 0.04, 0.004, h - 0.04), (x, y + face * (t / 2 + 0.001), z0 + h / 2), m, bevel=0)


def pad(A, w, d, h, x, y, z0, m="cloth", bv=0.035):
    return box(A, (w, d, h), (x, y, z0 + h / 2), m, bevel=bv)


def pedestal(A, r, h, x, y, z0=0.0, m="gunmetal"):
    cy(A, r, h, x, y, z0, m, r2=r * 0.7, verts=24)


_entry_for_base = entry_for


def entry_for(it):
    """Generic entry plus defaults for glowing assets: light colour from the variant's glow, light height from the placement."""
    m = _entry_for_base(it)
    g = it["v"].get("glow")
    if m.get("light"):
        m["light"] = round(m["light"] * 0.6, 2)  # the editor adds one point light per glowing prop; keep rooms from blowing out
        m.setdefault("lightColor", LIGHTC.get(g, "#bfe8ff"))
        m.setdefault("lightY", {"floor": 1.2, "ceiling": 0.15, "surface": 0.25, "wall": 0.3}.get(m.get("place"), 1.0))
    return m
