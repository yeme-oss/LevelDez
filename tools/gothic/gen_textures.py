"""Generate the wall/floor texture library with Nano Banana, make each tile seamless, write assets/textures/manifest.json. Resumable.

    python tools/gothic/gen_textures.py          # every missing texture
    python tools/gothic/gen_textures.py 6        # at most 6 this run
    python tools/gothic/gen_textures.py wall_    # only ids containing this text
"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from gemini_images import generate, run_parallel, MODEL
from texture_prompts import TEXTURES, HEAD, TAIL
from PIL import Image
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "textures")
os.makedirs(OUT, exist_ok=True)
SIZE = 768


def make_seamless(img):
    """Cross-fade the image with a half-rolled copy through a cosine window: borders then come from the (continuous) centre of the roll."""
    a = np.asarray(img, dtype=np.float32)
    h, w, _ = a.shape
    # only bother when the wrap-around seam is clearly worse than a normal neighbouring column/row
    seam = np.abs(a[:, 0] - a[:, -1]).mean() + np.abs(a[0] - a[-1]).mean()
    base = np.abs(a[:, 1:] - a[:, :-1]).mean() + np.abs(a[1:] - a[:-1]).mean()
    if seam < base * 1.35:
        return img, False
    rolled = np.roll(a, (h // 2, w // 2), axis=(0, 1))
    wx = np.sin(np.linspace(0, np.pi, w)) ** 1.5
    wy = np.sin(np.linspace(0, np.pi, h)) ** 1.5
    m = (wy[:, None] * wx[None, :])[..., None]
    return Image.fromarray(np.clip(a * m + rolled * (1 - m), 0, 255).astype(np.uint8)), True


def build(tid, kind, tile, what):
    raw = generate(HEAD + what + "." + TAIL, "1:1", "1K")
    img = Image.open(io.BytesIO(raw)).convert("RGB").resize((SIZE, SIZE), Image.LANCZOS)
    img, fixed = make_seamless(img)
    if tid.startswith("detail_"):  # neutral grayscale, auto-levelled to a mid-grey mean so multiplying never changes the base colour much
        g = np.asarray(img.convert("L"), dtype=np.float32)
        lo, hi = np.percentile(g, 2), np.percentile(g, 98)
        g = np.clip((g - lo) / max(hi - lo, 1) , 0, 1) * 0.7 + 0.15
        g = np.clip(g + (0.5 - g.mean()), 0, 1)
        img = Image.fromarray((g * 255).astype(np.uint8)).convert("RGB")
    img.save(os.path.join(OUT, tid + ".jpg"), quality=88)
    write_manifest()


def write_manifest():
    man = {}
    for tid, kind, tile, what in TEXTURES:
        if os.path.exists(os.path.join(OUT, tid + ".jpg")):
            man[tid] = {"file": tid + ".jpg", "kind": kind, "tile": tile, "neutral": tid.startswith("n_"), "desc": what}
    json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)


if __name__ == "__main__":
    args = sys.argv[1:]
    limit = next((int(a) for a in args if a.isdigit()), None)
    pat = next((a for a in args if not a.isdigit() and not a.startswith("-")), "")
    todo = [t for t in TEXTURES if pat in t[0] and not os.path.exists(os.path.join(OUT, t[0] + ".jpg"))]
    if limit: todo = todo[:limit]
    print(f"{MODEL}: {len(todo)} textures to generate (~${len(todo) * 0.0336:.2f})", flush=True)
    ok, bad = run_parallel([(t[0], (lambda t=t: build(*t))) for t in todo], workers=4)
    write_manifest()
    print(f"done: {len(ok)} generated, {len(bad)} failed, {sum(1 for t in TEXTURES if os.path.exists(os.path.join(OUT, t[0] + '.jpg')))}/{len(TEXTURES)} on disk")
