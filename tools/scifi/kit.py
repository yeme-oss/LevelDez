# Sci-fi materials added to the shared kit (MATS). Names starting with tint_ are recoloured by the editor's style palette.
_S = {
    "hull": ("hull", (0.80, 0.82, 0.86), 0.38, 0.0, None, 0),
    "hull_grey": ("hull_grey", (0.42, 0.44, 0.48), 0.45, 0.0, None, 0),
    "hull_dark": ("hull_dark", (0.11, 0.12, 0.14), 0.4, 0.0, None, 0),
    "gunmetal": ("gunmetal", (0.08, 0.09, 0.11), 0.35, 0.85, None, 0),
    "carbon": ("carbon", (0.015, 0.017, 0.02), 0.28, 0.2, None, 0),
    "steel": ("steel_brushed", (0.6, 0.62, 0.66), 0.32, 1.0, None, 0),
    "chrome": ("chrome", (0.9, 0.92, 0.95), 0.08, 1.0, None, 0),
    "titanium": ("titanium", (0.38, 0.4, 0.44), 0.35, 1.0, None, 0),
    "rubber": ("rubber", (0.02, 0.02, 0.022), 0.9, 0.0, None, 0),
    "foam": ("foam", (0.88, 0.88, 0.9), 0.85, 0.0, None, 0),
    "pad": ("pad_dark", (0.05, 0.05, 0.06), 0.55, 0.0, None, 0),
    "p_orange": ("plastic_orange", (0.9, 0.32, 0.04), 0.5, 0.0, None, 0),
    "p_yellow": ("plastic_yellow", (0.9, 0.7, 0.05), 0.5, 0.0, None, 0),
    "p_red": ("plastic_red", (0.7, 0.05, 0.05), 0.5, 0.0, None, 0),
    "p_teal": ("plastic_teal", (0.05, 0.4, 0.42), 0.5, 0.0, None, 0),
    "screen_off": ("screen_off", (0.01, 0.02, 0.03), 0.06, 0.0, None, 0),
    "leaf": ("tint_plant", (0.08, 0.38, 0.14), 0.7, 0.0, None, 0),
    "leaf2": ("leaf_teal", (0.05, 0.45, 0.35), 0.6, 0.0, None, 0),
    "soil": ("soil", (0.08, 0.06, 0.045), 0.95, 0.0, None, 0),
    "neon_cyan": ("neon_cyan", (0.1, 0.9, 1.0), 0.4, 0, (0.1, 0.9, 1.0), 2.2),
    "neon_magenta": ("neon_magenta", (1.0, 0.1, 0.65), 0.4, 0, (1.0, 0.1, 0.65), 2.2),
    "neon_amber": ("neon_amber", (1.0, 0.55, 0.1), 0.4, 0, (1.0, 0.55, 0.1), 2.2),
    "neon_green": ("neon_green", (0.2, 1.0, 0.3), 0.4, 0, (0.2, 1.0, 0.3), 2.2),
    "neon_red": ("neon_red", (1.0, 0.08, 0.08), 0.4, 0, (1.0, 0.08, 0.08), 2.2),
    "neon_blue": ("neon_blue", (0.2, 0.4, 1.0), 0.4, 0, (0.2, 0.4, 1.0), 2.2),
    "neon_violet": ("neon_violet", (0.6, 0.2, 1.0), 0.4, 0, (0.6, 0.2, 1.0), 2.2),
    "neon_white": ("neon_white", (1.0, 0.96, 0.9), 0.4, 0, (1.0, 0.96, 0.9), 2.2),
    "scr_cyan": ("scr_cyan", (0.05, 0.5, 0.6), 0.2, 0, (0.1, 0.8, 0.95), 1.0),
    "scr_green": ("scr_green", (0.05, 0.5, 0.15), 0.2, 0, (0.15, 1.0, 0.3), 1.0),
    "scr_amber": ("scr_amber", (0.6, 0.3, 0.05), 0.2, 0, (1.0, 0.55, 0.1), 1.0),
    "scr_magenta": ("scr_magenta", (0.55, 0.05, 0.35), 0.2, 0, (1.0, 0.15, 0.7), 1.0),
    "scr_red": ("scr_red", (0.5, 0.04, 0.04), 0.2, 0, (1.0, 0.1, 0.1), 1.0),
    "scr_blue": ("scr_blue", (0.1, 0.2, 0.6), 0.2, 0, (0.25, 0.45, 1.0), 1.0),
}
for _k, (_n, _rgb, _r, _m, _e, _s) in _S.items():
    MATS[_k] = _mat(_n, _rgb, _r, _m, _e, _s)
MATS["glass_cyan"] = _mat("glass_cyan", (0.35, 0.85, 1.0), 0.05, 0.0, None, 0)
_b = next(n for n in MATS["glass_cyan"].node_tree.nodes if n.type == "BSDF_PRINCIPLED")
_b.inputs["Alpha"].default_value = 0.3
for _attr, _val in (("surface_render_method", "BLENDED"), ("blend_method", "BLEND")):
    try:
        setattr(MATS["glass_cyan"], _attr, _val)
    except Exception:
        pass
GLOWS = {"cyan": "neon_cyan", "magenta": "neon_magenta", "amber": "neon_amber", "green": "neon_green", "red": "neon_red", "blue": "neon_blue", "violet": "neon_violet", "white": "neon_white"}
SCRS = {"cyan": "scr_cyan", "magenta": "scr_magenta", "amber": "scr_amber", "green": "scr_green", "red": "scr_red", "blue": "scr_blue", "violet": "scr_blue", "white": "scr_cyan"}
LIGHTC = {"cyan": "#5fe6ff", "magenta": "#ff4fb8", "amber": "#ffb35a", "green": "#6dff8a", "red": "#ff5555", "blue": "#6a8cff", "violet": "#a56bff", "white": "#fff1dc"}
