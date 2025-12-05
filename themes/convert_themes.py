import os
import tomllib

THEMES_DIR = "/home/kevin/Work/omarchy/themes"

TEMPLATE_SCOPES = {
    "type": "yellow",
    "constant": "fg",
    "constant.builtin": { "fg": "purple", "modifiers": ["italic"] },
    "constant.builtin.boolean": "purple",
    "constant.numeric": "purple",
    "constant.character.escape": "green",
    "string": "aqua",
    "string.regexp": "green",
    "string.special": "yellow",
    "comment": { "fg": "grey1", "modifiers": ["italic"] },
    "variable": "fg",
    "variable.builtin": { "fg": "purple", "modifiers": ["italic"] },
    "variable.parameter": "fg",
    "variable.other.member": "blue",
    "label": "orange",
    "punctuation": "grey2",
    "punctuation.delimiter": "grey1",
    "punctuation.bracket": "fg",
    "punctuation.special": "blue",
    "keyword": "red",
    "keyword.operator": "orange",
    "keyword.directive": "purple",
    "keyword.storage": "red",
    "operator": "orange",
    "function": "green",
    "function.macro": "green",
    "tag": "orange",
    "namespace": { "fg": "yellow", "modifiers": ["italic"] },
    "attribute": { "fg": "purple", "modifiers": ["italic"] },
    "constructor": "green",
    "module": "yellow",
    "special": "blue",
    "ui.virtual.jump-label": { "fg": "#00dfff", "modifiers": ["bold"] },

    "markup.heading.marker": "grey1",
    "markup.heading.1": { "fg": "red", "modifiers": ["bold"] },
    "markup.heading.2": { "fg": "orange", "modifiers": ["bold"] },
    "markup.heading.3": { "fg": "yellow", "modifiers": ["bold"] },
    "markup.heading.4": { "fg": "green", "modifiers": ["bold"] },
    "markup.heading.5": { "fg": "blue", "modifiers": ["bold"] },
    "markup.heading.6": { "fg": "purple", "modifiers": ["bold"] },
    "markup.list": "red",
    "markup.bold": { "modifiers": ["bold"] },
    "markup.italic": { "modifiers": ["italic"] },
    "markup.strikethrough": { "modifiers": ["crossed_out"] },
    "markup.link.url": { "fg": "blue", "underline": { "style": "line" } },
    "markup.link.label": "orange",
    "markup.link.text": "purple",
    "markup.quote": "grey1",
    "markup.raw.inline": "green",
    "markup.raw.block": "aqua",

    "diff.plus": "green",
    "diff.delta": "blue",
    "diff.minus": "red",

    "ui.background": {}, # Transparent as requested
    "ui.background.separator": "grey0",
    "ui.cursor": { "fg": "bg1", "bg": "grey2" },
    "ui.cursor.insert": { "fg": "bg0", "bg": "grey1" },
    "ui.cursor.select": { "fg": "bg0", "bg": "blue" },
    "ui.cursor.match": { "fg": "orange", "bg": "bg_yellow" },
    "ui.cursor.primary": { "fg": "bg0", "bg": "fg" },
    "ui.cursorline.primary": { "bg": "bg1" },
    "ui.cursorline.secondary": { "bg": "bg2" },
    "ui.selection": { "bg": "bg3" },
    "ui.linenr": "grey0",
    "ui.linenr.selected": "grey2",
    "ui.statusline": { "fg": "grey2", "bg": "bg3" },
    "ui.statusline.inactive": { "fg": "grey0", "bg": "bg1" },
    "ui.statusline.normal": { "fg": "bg0", "bg": "statusline1", "modifiers": ["bold"] },
    "ui.statusline.insert": { "fg": "bg0", "bg": "statusline2", "modifiers": ["bold"] },
    "ui.statusline.select": { "fg": "bg0", "bg": "blue", "modifiers": ["bold"] },
    "ui.bufferline": { "fg": "grey2", "bg": "bg3" },
    "ui.bufferline.active": { "fg": "bg0", "bg": "statusline1", "modifiers": ["bold"] },
    "ui.popup": { "fg": "grey2", "bg": "bg2" },
    "ui.picker.header": { "modifiers": ["bold", "underlined"] },
    "ui.window": { "fg": "bg4", "bg": "bg_dim" },
    "ui.help": { "fg": "fg", "bg": "bg2" },
    "ui.text": "fg",
    "ui.text.directory": { "fg": "green" },
    "ui.text.focus": "fg",
    "ui.menu": { "fg": "fg", "bg": "bg3" },
    "ui.menu.selected": { "fg": "bg0", "bg": "green" },
    "ui.virtual.ruler": { "bg": "bg3" },
    "ui.virtual.whitespace": { "fg": "bg4" },
    "ui.virtual.indent-guide": { "fg": "bg4" },
    "ui.virtual.inlay-hint": { "fg": "grey0" },
    "ui.virtual.wrap": { "fg": "grey0" },

    "hint": "green",
    "info": "blue",
    "warning": "yellow",
    "error": "red",

    "diagnostic.hint": { "underline": { "color": "green", "style": "curl" } },
    "diagnostic.info": { "underline": { "color": "blue", "style": "curl" } },
    "diagnostic.warning": { "underline": { "color": "yellow", "style": "curl" } },
    "diagnostic.error": { "underline": { "color": "red", "style": "curl" } },
    "diagnostic.unnecessary": { "modifiers": ["dim"] },
    "diagnostic.deprecated": { "modifiers": ["crossed_out"] },
}

def generate_palette(alacritty_colors):
    """Maps Alacritty colors to the specific variable set required by the template."""

    primary = alacritty_colors.get('primary', {})
    normal = alacritty_colors.get('normal', {})
    bright = alacritty_colors.get('bright', {})
    selection = alacritty_colors.get('selection', {})

    # Base Colors
    p_bg = primary.get('background', '#1e1e2e')
    p_fg = primary.get('foreground', '#cdd6f4')

    # Map ANSI colors
    # Use normal as base, fallback to bright or safe defaults
    red = normal.get('red', bright.get('red', '#ff5555'))
    green = normal.get('green', bright.get('green', '#50fa7b'))
    yellow = normal.get('yellow', bright.get('yellow', '#f1fa8c'))
    blue = normal.get('blue', bright.get('blue', '#bd93f9'))
    magenta = normal.get('magenta', bright.get('magenta', '#ff79c6'))
    cyan = normal.get('cyan', bright.get('cyan', '#8be9fd'))

    # Aliases
    purple = magenta
    aqua = cyan

    # Orange assumption: Often 'bright red' or 'yellow' acts as orange in 16-color themes
    # if not explicitly indexed.
    # Let's try to find an indexed color if possible, but reading raw indexed array is hard
    # without robust parsing. We'll use bright red as a proxy for orange or yellow mix.
    # Actually, yellow is often earthy, bright red is often orange-ish.
    # Let's use bright red for orange.
    orange = bright.get('red', red)
    if orange == red:
         # If they are distinct, use yellow? No, let's stick to bright red or use a mix if we could.
         pass

    # Blacks / Greys
    # bg0 is main background
    bg0 = p_bg
    # We need variations for bg1..bg5.
    # In a flat conversion, we might map them all to bg0 or slightly different if we had HSL logic.
    # Since we can't easily darken/lighten without dependencies, we will map them:
    # bg_dim (darker), bg1..5 (lighter)
    # Mapping strategy: use 'black' and 'bright_black' from palette for UI elements
    # to create some contrast if possible.

    c_black = normal.get('black', '#000000')
    c_bright_black = bright.get('black', '#444444')

    # Construct the specific palette keys
    palette = {
        "bg_dim": p_bg, # Map to bg0 for safety, or black if darker? Let's use bg0
        "bg0": p_bg,
        "bg1": c_black, # Use ANSI black which is usually lighter than bg in modern themes (e.g. curr line)
        "bg2": c_black,
        "bg3": c_bright_black, # Even lighter
        "bg4": c_bright_black,
        "bg5": c_bright_black,

        "bg_visual": selection.get('background', c_bright_black),
        "bg_red": red,   # These are usually backgrounds for diffs?
        "bg_green": green,
        "bg_blue": blue,
        "bg_yellow": yellow,

        "fg": p_fg,
        "red": red,
        "orange": orange,
        "yellow": yellow,
        "green": green,
        "aqua": aqua,
        "blue": blue,
        "purple": purple,

        "grey0": c_bright_black,
        "grey1": c_bright_black, # Fallback, maybe we don't have enough shades
        "grey2": p_fg, # Highest grey is close to fg

        "statusline1": green,
        "statusline2": p_fg,
        "statusline3": red,
    }

    return palette

def dump_toml(theme_dict, f):
    """Simple TOML dumper."""

    # Write Scopes first (Root table)
    for k, v in theme_dict.items():
        if k == "palette":
            continue

        if isinstance(v, str):
            f.write(f'"{k}" = "{v}"\n')
        elif isinstance(v, dict):
            # Inline dict
            if not v:
                f.write(f'"{k}" = {{}}\n')
                continue

            entries = []
            for subk, subv in v.items():
                if isinstance(subv, list):
                    # array ["a", "b"]
                    val = str(subv).replace("'", '"')
                    entries.append(f'{subk} = {val}')
                elif isinstance(subv, dict):
                    # nested
                    subentries = []
                    for ssk, ssv in subv.items():
                         subentries.append(f'{ssk} = "{ssv}"')
                    sub_val = "{ " + ", ".join(subentries) + " }"
                    entries.append(f'{subk} = {sub_val}')
                else:
                    entries.append(f'{subk} = "{subv}"')

            inline_str = ", ".join(entries)
            f.write(f'"{k}" = {{ {inline_str} }}\n')

    # Write palette last
    palette = theme_dict.get("palette", {})
    if palette:
        f.write("\n[palette]\n")
        for k, v in palette.items():
            f.write(f'{k} = "{v}"\n')
        f.write("\n")

def convert_theme(theme_name):
    theme_path = os.path.join(THEMES_DIR, theme_name)
    alacritty_file = os.path.join(theme_path, "alacritty.toml")

    if not os.path.exists(alacritty_file):
        return

    try:
        with open(alacritty_file, 'rb') as f:
            data = tomllib.load(f)

        colors = data.get('colors', {})
        if not colors:
            print(f"Skipping {theme_name}: No colors found")
            return

        palette = generate_palette(colors)

        # Merge key-values
        full_theme = TEMPLATE_SCOPES.copy()
        full_theme["palette"] = palette

        output_path = os.path.join(theme_path, "helix.toml")
        with open(output_path, 'w') as f:
            dump_toml(full_theme, f)

        print(f"Converted {theme_name}")

    except Exception as e:
        print(f"Error {theme_name}: {e}")

def main():
    if not os.path.exists(THEMES_DIR):
        return
    for item in os.listdir(THEMES_DIR):
        if os.path.isdir(os.path.join(THEMES_DIR, item)):
            convert_theme(item)

if __name__ == "__main__":
    main()
