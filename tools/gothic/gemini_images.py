"""Tiny client for Google's Interactions API with Nano Banana (gemini-nano-banana-2.1). Needs GEMINI_API_KEY.
Docs: https://ai.google.dev/gemini-api/docs/image-generation   Price: ~$0.034 per 1K image (no free tier)."""
import base64, json, os, threading, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor

MODEL = os.environ.get("NANO_BANANA_MODEL", "gemini-nano-banana-2.1")
URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
_lock = threading.Lock()
try:  # optional .env at the repo root (KEY=value); real environment variables win
    for _l in open(os.path.join(os.path.dirname(__file__), "..", "..", ".env"), encoding="utf8"):
        _m = __import__("re").match(r"^\s*([A-Za-z0-9_]+)\s*=\s*(.*?)\s*$", _l)
        if _m and _m.group(1) not in os.environ: os.environ[_m.group(1)] = _m.group(2).strip("'\"")
except OSError:
    pass


def generate(prompt, aspect="1:1", size="1K", mime="image/jpeg", retries=4):
    """Return raw image bytes. Retries on 429/5xx with backoff; raises on anything else."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("GEMINI_API_KEY is not set")
    body = {"model": MODEL, "input": prompt, "response_format": {"type": "image", "mime_type": mime, "aspect_ratio": aspect, "image_size": size}}
    for attempt in range(retries):
        req = urllib.request.Request(URL, json.dumps(body).encode(), {"x-goog-api-key": key, "Content-Type": "application/json"})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=300))
            for st in r.get("steps", []):
                for c in st.get("content", []) or []:
                    if c.get("type") == "image" and c.get("data"):
                        return base64.b64decode(c["data"])
            raise RuntimeError("no image in response (status %s)" % r.get("status"))
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:300]
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(4 * (attempt + 1)); continue
            raise RuntimeError(f"HTTP {e.code}: {msg}")
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < retries - 1:
                time.sleep(4 * (attempt + 1)); continue
            raise RuntimeError(str(e))


def run_parallel(jobs, workers=4):
    """jobs: list of (label, callable). Prints progress; returns (ok, failed)."""
    ok, bad = [], []
    def one(j):
        label, fn = j
        try:
            fn();
            with _lock: ok.append(label); print("  ok  ", label, flush=True)
        except Exception as e:
            with _lock: bad.append((label, str(e))); print("  FAIL", label, str(e)[:160], flush=True)
    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(one, jobs))
    return ok, bad
