# Wall / floor / wainscot texture library, generated with Nano Banana (gen_textures.py). Pure data.
# (id, kind, tile size in metres, what it shows). Neutral ones are desaturated so the level style can tint them.
HEAD = "Seamless tileable game texture, albedo only, "
TAIL = " Flat orthographic top-down view filling the entire frame, even diffuse lighting, no perspective, no cast shadows, no vignette, no border, no text, no objects, repeating pattern."

TEXTURES = [
    # ---- gothic walls ----
    ("wall_moss_stone", "wall", 2.0, "dark grey gothic castle stone blocks in running bond with green moss in the mortar"),
    ("wall_stone_rough", "wall", 2.0, "rough hewn dark limestone blocks, chipped and weathered, damp stains"),
    ("wall_stone_pale", "wall", 2.0, "pale grey cathedral ashlar stone blocks with fine mortar lines, subtle soot"),
    ("wall_brick_dark", "wall", 2.0, "blackened old dungeon bricks in running bond, soot, crumbling mortar"),
    ("wall_brick_warm", "wall", 2.0, "warm rust-red rough bricks in running bond, worn mortar, kitchen soot"),
    ("wall_obsidian_blocks", "wall", 2.0, "polished black obsidian stone blocks with thin violet glowing seams"),
    ("wall_plaster_bone", "wall", 2.0, "stained bone-white plaster with cracks, damp patches and peeling paint"),
    ("wall_damask_crimson", "wall", 2.0, "crimson and black victorian damask wallpaper with ornate gold fleur motifs, slightly aged"),
    ("wall_damask_green", "wall", 2.0, "deep emerald green damask wallpaper with antique gold ornamental pattern, aged paper"),
    ("wall_damask_purple", "wall", 2.0, "deep violet damask wallpaper with silver ornamental pattern, aged paper"),
    ("wall_damask_noir", "wall", 2.0, "black damask wallpaper with subtle silver-grey baroque pattern, aged"),
    ("wall_stripes_burgundy", "wall", 2.0, "burgundy and dark maroon vertical striped wallpaper with thin gold pinstripes, aged"),
    ("wall_panels_oak", "wall", 2.0, "dark oak wood wall panelling with raised rectangular panels, polished with age"),
    ("wall_tiles_teal", "wall", 2.0, "dark teal glazed ceramic wall tiles with dark grout, some cracked and stained"),
    ("wall_tiles_white", "wall", 2.0, "old white and black glazed bathroom wall tiles with grey grout, cracked and stained"),
    # ---- gothic floors ----
    ("floor_cobble_dark", "floor", 2.0, "dark grey rounded dungeon cobblestones with damp moss between them"),
    ("floor_flagstone_dark", "floor", 2.0, "large dark grey irregular flagstones with narrow grout, worn smooth"),
    ("floor_flagstone_warm", "floor", 2.0, "warm brown-grey flagstone paving, worn, dusty"),
    ("floor_checker_marble", "floor", 2.0, "black and white marble checkerboard floor tiles, polished, veined, slightly scuffed"),
    ("floor_checker_dark", "floor", 2.0, "dark burgundy and black checkerboard floor tiles, glossy, worn"),
    ("floor_plank_dark", "floor", 2.0, "dark ebony wide wooden floorboards with visible grain and nails, aged"),
    ("floor_herringbone_oak", "floor", 2.0, "dark oak herringbone parquet wooden floor, polished with age"),
    ("floor_herringbone_dark", "floor", 2.0, "very dark ebony herringbone parquet floor, subtle shine"),
    ("floor_diamond_teal", "floor", 2.0, "dark teal and charcoal diamond-pattern ceramic floor tiles, cracked, grimy"),
    ("floor_diamond_bw", "floor", 2.0, "black and white diamond-pattern ceramic floor tiles, old, scuffed"),
    ("floor_marble_black", "floor", 2.0, "black marble with violet and silver veins, high polish"),
    ("floor_carpet_crimson", "floor", 2.0, "worn crimson victorian carpet with an ornate gold and black pattern"),
    # ---- wainscot / trim bands ----
    ("wain_oak_dark", "wain", 1.0, "dark oak wainscot panelling with raised rectangular panels"),
    ("wain_stone", "wain", 1.0, "dark carved stone plinth blocks"),
    ("wain_planks", "wain", 1.0, "vertical dark wooden planks, tongue and groove, aged"),
    # ---- neutral (desaturated; tinted by the style palette) ----
    ("n_wall_plaster", "wall", 2.0, "desaturated light grey plastered wall with subtle trowel marks and faint stains, almost no colour"),
    ("n_wall_brick", "wall", 2.0, "desaturated mid grey brick wall in running bond, almost no colour"),
    ("n_wall_stripes", "wall", 2.0, "wall surface painted in wide vertical bands of two very close light grey tones, soft hand-painted look, almost no colour"),
    ("n_wall_damask", "wall", 2.0, "desaturated light grey damask wallpaper with tone-on-tone pattern, almost no colour"),
    ("n_wall_panels", "wall", 2.0, "desaturated mid grey wood wall panelling with raised panels, almost no colour"),
    ("n_wall_tiles", "wall", 2.0, "old plain grey bathroom wall surface made of small square matte tiles in slightly varied pale grey shades, thin dark grout, almost no colour"),
    ("n_floor_plank", "floor", 2.0, "desaturated mid grey wooden floorboards with grain, almost no colour"),
    ("n_floor_herringbone", "floor", 2.0, "desaturated mid grey herringbone parquet floor, almost no colour"),
    ("n_floor_flagstone", "floor", 2.0, "desaturated mid grey flagstone paving, almost no colour"),
    ("n_floor_checker", "floor", 2.0, "desaturated light and dark grey checkerboard floor tiles, almost no colour"),
    ("n_floor_diamond", "floor", 2.0, "desaturated grey diamond-pattern floor tiles, almost no colour"),
    # ---- grayscale detail maps for props (multiplied over their base colour with box mapping) ----
    ("detail_wood", "detail", 0.5, "macro close-up of dark wooden plank grain with fine scratches and pores, strictly grayscale, no colour, mid-grey average tone"),
    ("detail_stone", "detail", 0.5, "macro close-up of rough chiselled stone surface with pits and chips, strictly grayscale, no colour, mid-grey average tone"),
    ("detail_metal", "detail", 0.5, "macro close-up of scratched hammered wrought iron metal with pits and wear, strictly grayscale, no colour, mid-grey average tone"),
    ("detail_fabric", "detail", 0.5, "macro close-up of woven velvet cloth fabric weave texture, strictly grayscale, no colour, mid-grey average tone"),
    ("detail_leather", "detail", 0.5, "macro close-up of worn leather grain with creases, strictly grayscale, no colour, mid-grey average tone"),
    ("detail_bone", "detail", 0.5, "macro close-up of aged ivory bone surface with fine cracks and pores, strictly grayscale, no colour, mid-grey average tone"),
    ("detail_paper", "detail", 0.5, "macro close-up of old parchment paper with fibres, stains and wrinkles, strictly grayscale, no colour, mid-grey average tone"),
    ("detail_grime", "detail", 1.5, "large soft cloudy grime and soot stain mask, blotchy dirt patches, strictly grayscale, no colour, mid-grey average tone"),
]
