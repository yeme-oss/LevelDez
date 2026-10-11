# Shared builders for the recipes (masonry arches, tracery, columns...). Loaded after the kit.

def arch_ring(A, w, hs, squash, thick, depth, loc, mat="stone_light", n=7):
    """Pointed arch built from voussoir blocks (hollow). Spring height hs, opening width w; loc = (x, y, z of the spring-line base)."""
    cx, cy, cz = loc
    def pt(side, t):  # t in 0..1 along the arc
        a = math.radians(60 * t)
        if side > 0:   # right arc centred at (-w/2, hs)
            return (-w / 2 + w * math.cos(a), hs + w * math.sin(a) * squash)
        return (w / 2 - w * math.cos(a), hs + w * math.sin(a) * squash)
    for side in (1, -1):
        for i in range(n):
            p0, p1 = pt(side, i / n), pt(side, (i + 1) / n)
            dx, dz = p1[0] - p0[0], p1[1] - p0[1]
            ln = math.hypot(dx, dz)
            ang = -math.atan2(dz, dx)
            box(A, (ln + 0.012, depth, thick), (cx + (p0[0] + p1[0]) / 2, cy, cz + (p0[1] + p1[1]) / 2), mat, rot=(0, ang, 0), bevel=0.006)
    sph(A, thick * 0.55, (cx, cy, cz + hs + w * 0.866 * squash), mat, seg=8)  # keystone knob


def jambs(A, w, h, thick, depth, loc, mat="stone_light"):
    cx, cy, cz = loc
    for s in (-1, 1):
        box(A, (thick, depth, h), (cx + s * (w / 2 + thick / 2), cy, cz + h / 2), mat, bevel=0.01)


def column_shaft(A, kind, H, r=0.2, loc=(0, 0, 0), mat="stone_light"):
    x, y, z0 = loc
    if kind == "fluted":
        cyl(A, r * 0.85, H, (x, y, z0 + H / 2), mat, verts=16)
        for i in range(10):
            a = 2 * PI * i / 10
            cyl(A, 0.022, H, (x + r * 0.92 * math.cos(a), y + r * 0.92 * math.sin(a), z0 + H / 2), mat, verts=6)
    elif kind == "clustered":
        cyl(A, r * 0.55, H, (x, y, z0 + H / 2), mat, verts=12)
        for px, py, _, _a in ring_of(6, r * 0.75):
            cyl(A, r * 0.32, H, (x + px, y + py, z0 + H / 2), mat, verts=10)
    elif kind == "twisted":
        steps = 18
        for i in range(steps):
            box(A, (r * 1.5, r * 0.85, H / steps + 0.01), (x, y, z0 + (i + 0.5) * H / steps), mat, rot=(0, 0, i * 0.2), bevel=0.01)
            box(A, (r * 0.85, r * 1.5, H / steps + 0.01), (x, y, z0 + (i + 0.5) * H / steps), mat, rot=(0, 0, i * 0.2), bevel=0.01)
    else:
        lathe(A, [(r * 1.05, 0), (r, H * 0.1), (r * 0.92, H * 0.5), (r, H * 0.9), (r * 1.05, H)], (x, y, z0), mat, verts=20)
