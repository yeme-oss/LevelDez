"""Generate the academy wall art with Nano Banana (gemini-nano-banana-2.1, Google Interactions API). Resumable.

    python tools/gothic/gen_art.py            # every missing painting
    python tools/gothic/gen_art.py 5          # at most 5 this run
    python tools/gothic/gen_art.py --check    # list what is missing

Images land in assets/gothic/art/<id>.jpg (needs GEMINI_API_KEY, ~$0.034 each). Afterwards re-bake the paintings in Blender: refresh_art().
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from gemini_images import generate, run_parallel, MODEL
from art_prompts import ART, ASPECTS, STYLE

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "gothic", "art")
os.makedirs(OUT, exist_ok=True)


def build(item):
    name, kind, style, subject = item
    open(os.path.join(OUT, name + ".jpg"), "wb").write(generate(f"{subject} {STYLE[style]}", ASPECTS[kind], "1K"))


if __name__ == "__main__":
    todo = [a for a in ART if not os.path.exists(os.path.join(OUT, a[0] + ".jpg"))]
    limit = next((int(a) for a in sys.argv[1:] if a.isdigit()), len(todo))
    todo = todo[:limit]
    print(f"{MODEL}: {len(ART) - len([a for a in ART if not os.path.exists(os.path.join(OUT, a[0] + '.jpg'))])}/{len(ART)} exist, generating {len(todo)} (~${len(todo) * 0.0336:.2f})", flush=True)
    if "--check" in sys.argv: sys.exit(0)
    ok, bad = run_parallel([(a[0], (lambda a=a: build(a))) for a in todo], workers=4)
    print(f"done: {len(ok)} generated, {len(bad)} failed")
