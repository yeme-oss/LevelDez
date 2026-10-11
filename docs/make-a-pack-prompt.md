# Make-a-pack prompt

Paste this into an LLM agent that can run code **and** drive Blender (for example Claude Code with a BlenderMCP server, started in the LevelDez folder). Replace the two `{{...}}` lines first. Anything goes for the genre: *cyberpunk noodle bar, sunlit Mediterranean villa, haunted 1980s motel, alien hive, cosy hobbit burrows*.

---

````text
You are building a new asset pack for LevelDez, a browser interior level editor. Work inside this repository.

GENRE / STYLE:  {{describe the genre, mood, palette, materials and era in 2-3 sentences}}
PACK NAME:      {{short_lowercase_name}}      (folder: assets/<PACK NAME>/)
SIZE:           {{e.g. 120 assets}}

STEP 0 - READ FIRST (do not skip)
- README.md, section "Asset packs" (manifest fields).
- assets/gothic/manifest.json: look at 10 entries to see real examples.
- tools/blender_kit.py: reuse its helpers (materials, box/cyl/lathe/prism, finish()) if you drive Blender with Python. Skip tools/gothic/ recipes; they are specific to the gothic pack.

STEP 1 - PLAN BEFORE BUILDING
Write assets/<PACK NAME>/PLAN.md: a checklist of every asset with id, label, category, placement (floor / wall / ceiling / surface), approximate size in metres and tags. Aim for variety across these groups, scaled to SIZE:
 1. Variants of base types so existing layout logic keeps working: bed, nightstand, sofa, armchair, dining_table, dining_chair, desk, bookshelf, wardrobe, dresser, rug, painting, mirror, floor_lamp, table_lamp, ceiling_light, plant, curtains, bench, toilet, bathtub, sink_vanity, kitchen_counter, fridge (give each several genre-specific looks).
 2. Pack-only types that only exist in this genre (the signature props that make the place recognisable).
 3. Lighting with a glow (lamps, neon, candles, lanterns, fires).
 4. Wall pieces: art frames, signs, shelves, trophies, banners.
 5. Small surface decor: items that sit on tables and shelves, plus floor clutter (crates, bins, boxes).
 6. Architecture accents: pillars, window or door surrounds, ceiling details.
Stop and show me the plan summary (counts per group). Continue unless I object.

STEP 2 - BUILD EACH ASSET AS A GLB
Conventions (the editor depends on these):
- Metres. Origin at the centre of the footprint, on the floor (bottom of the object at y = 0). Export Y-up.
- The FRONT of the object faces -Y in Blender (+Z in glTF).
- One GLB per asset, saved as assets/<PACK NAME>/<id>.glb. Few meshes (merge by material), under ~15k triangles, no external textures except images embedded as JPEG.
- Name materials with a tint_ prefix (for example tint_fabric) on surfaces the editor may recolour; keep other materials fixed.
- Emissive materials for anything that glows.
- Build in small batches (about 20), look at a rendered gallery of each batch, fix proportions, then continue. Make it resumable: record finished ids in assets/<PACK NAME>/_progress.json so you can stop and continue later.

STEP 3 - MANIFEST
Write assets/<PACK NAME>/manifest.json, one entry per GLB:
{ "<id>": { "file": "<id>.glb", "label": "Human name", "cat": "furniture|decor|lighting|architecture|...",
            "as": "bed",                       // ONLY for variants of a base type listed in step 1.1
            "place": "floor|wall|ceiling|surface", "y": 1.5,        // y = mount height for wall items
            "tags": ["wall-hug","holds-decor","light","decor","seating","curtain","altar","flat","arch","faces-center"],
            "light": 1.2, "lightColor": "#ffb070", "lightY": 1.6,     // only if it glows
            "tint": "fabric", "bbox": [w, d, h] } }
Tag meaning: wall-hug = stands against a wall; holds-decor = small items may be placed on top; light = emits light; seating / decor = used by the fill buttons; flat = rug-like, walkable; arch = doorway-like architecture. Pack-only types (no "as") must have a "label", "cat", "place" and a believable bbox. The server measures the bbox if you omit it.

STEP 4 - OPTIONAL: WALL ART
If I have set GEMINI_API_KEY in .env, generate paintings/posters/signs in this genre with tools/gothic/gemini_images.py (generate(prompt, aspect, size)) and bake them onto flat frame GLBs. Skip this step if the key is missing.

STEP 5 - VERIFY
- Start the editor (npm start), open http://localhost:5173, choose "pack: <PACK NAME>", press "Generate layout", then run Autopilot.
- Screenshot the result. Check: props face the right way, sit on the floor, are the right scale next to a door (about 2.0 m tall), glow where intended, and nothing is missing or floating.
- Fix the worst offenders and repeat once.
- Finish with a short report: counts per group, anything skipped, and the three assets you are least happy with.
````
