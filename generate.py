import json
import os
import urllib.request

MANUAL = {
    "all": {
        "Compressor": {
            "Widget Primary 1": "teal",
            "Widget Primary 2": "text",
            "Widget Secondary 1": "surface1",
            "Widget Secondary 2": "surface2",
        },
        "Preset Browser": {
            "Lighten Screen": "surface0",
            "Widget Primary 1": "surface1",
            "Widget Secondary 2": "surface2",

        }
    },
    "Latte": {
        "Keyboard": {"Widget Secondary 2": "subtext1"},
    },
}

# catppuccin palettes
PALETTES = {
    "Latte": {
        "rosewater": "dc8a78",
        "flamingo": "dd7878",
        "pink": "ea76cb",
        "mauve": "8839ef",
        "red": "d20f39",
        "maroon": "e64553",
        "peach": "fe640b",
        "yellow": "df8e1d",
        "green": "40a02b",
        "teal": "179299",
        "sky": "04a5e5",
        "sapphire": "209fb5",
        "blue": "1e66f5",
        "lavender": "7287fd",
        "text": "4c4f69",
        "subtext1": "5c5f77",
        "subtext0": "6c6f85",
        "overlay2": "7c7f93",
        "overlay1": "8c8fa1",
        "overlay0": "9ca0b0",
        "surface2": "acb0be",
        "surface1": "bcc0cc",
        "surface0": "ccd0da",
        "base": "eff1f5",
        "mantle": "e6e9ef",
        "crust": "dce0e8",
    },
    "Frappé": {
        "rosewater": "f2d5cf",
        "flamingo": "eebebe",
        "pink": "f4b8e4",
        "mauve": "ca9ee6",
        "red": "e78284",
        "maroon": "ea999c",
        "peach": "ef9f76",
        "yellow": "e5c890",
        "green": "a6d189",
        "teal": "81c8be",
        "sky": "99d1db",
        "sapphire": "85c1dc",
        "blue": "8caaee",
        "lavender": "babbf1",
        "text": "c6d0f5",
        "subtext1": "b5bfe2",
        "subtext0": "a5adce",
        "overlay2": "949cbb",
        "overlay1": "838ba7",
        "overlay0": "737994",
        "surface2": "626880",
        "surface1": "51576d",
        "surface0": "414559",
        "base": "303446",
        "mantle": "292c3c",
        "crust": "232634",
    },
    "Macchiato": {
        "rosewater": "f4dbd6",
        "flamingo": "f0c6c6",
        "pink": "f5bde6",
        "mauve": "c6a0f6",
        "red": "ed8796",
        "maroon": "ee99a0",
        "peach": "f5a97f",
        "yellow": "eed49f",
        "green": "a6da95",
        "teal": "8bd5ca",
        "sky": "91d7e3",
        "sapphire": "7dc4e4",
        "blue": "8aadf4",
        "lavender": "b7bdf8",
        "text": "cad3f5",
        "subtext1": "b8c0e0",
        "subtext0": "a5adcb",
        "overlay2": "939ab7",
        "overlay1": "8087a2",
        "overlay0": "6e738d",
        "surface2": "5b6078",
        "surface1": "494d64",
        "surface0": "363a4f",
        "base": "24273a",
        "mantle": "1e2030",
        "crust": "181926",
    },
    "Mocha": {
        "rosewater": "f5e0dc",
        "flamingo": "f2cdcd",
        "pink": "f5c2e7",
        "mauve": "cba6f7",
        "red": "f38ba8",
        "maroon": "eba0ac",
        "peach": "fab387",
        "yellow": "f9e2af",
        "green": "a6e3a1",
        "teal": "94e2d5",
        "sky": "89dceb",
        "sapphire": "74c7ec",
        "blue": "89b4fa",
        "lavender": "b4befe",
        "text": "cdd6f4",
        "subtext1": "bac2de",
        "subtext0": "a6adc8",
        "overlay2": "9399b2",
        "overlay1": "7f849c",
        "overlay0": "6c7086",
        "surface2": "585b70",
        "surface1": "45475a",
        "surface0": "313244",
        "base": "1e1e2e",
        "mantle": "181825",
        "crust": "11111b",
    },
}

# default vital color -> catppuccin role
COLOR_MAP = {
    "262a2d": "mantle",
    "262a2e": "crust",
    "14181b": "crust",
    "161718": "crust",
    "000000": "crust",
    "2c3033": "mantle",
    "1d2125": "crust",
    "2c2e2f": "mantle",
    "3e4245": "base",
    "4c4f52": "surface0",
    "333333": "surface0",
    "393636": "surface1",
    "4c4c4c": "surface1",
    "545454": "surface1",
    "606265": "surface2",
    "666666": "surface2",
    "6b6b6b": "surface2",
    "848789": "overlay1",
    "848686": "overlay1",
    "939699": "overlay2",
    "aaacad": "subtext0",
    "aaabab": "subtext0",
    "d3d6d6": "subtext1",
    "d1cab7": "subtext1",
    "eeeeee": "subtext1",
    "dfdfdf": "text",
    "ffffff": "text",
    "111111": "text",
    "aa88ff": "mauve",
    "906de9": "mauve",
    "8464d2": "mauve",
    "9f88ff": "mauve",
    "bda3ff": "lavender",
    "ba9fff": "lavender",
    "1de9b6": "teal",
    "64ffda": "teal",
    "10735b": "teal",
    "0b4039": "teal",
    "11cbb2": "teal",
    "00bfa5": "teal",
    "32d6bf": "teal",
    "37beac": "teal",
    "b6e6e6": "teal",
    "1de952": "green",
    "00e686": "green",
    "1dc2e9": "sapphire",
    "40c4ff": "blue",
    "00b0ff": "blue",
    "0086e6": "blue",
    "40cfff": "sky",
    "80d8ff": "sky",
    "8fa0ff": "lavender",
    "9898ff": "lavender",
    "ea1616": "red",
    "ff5252": "red",
    "ff1744": "red",
    "ff99e9": "pink",
    "ffb74d": "peach",
    "ff8180": "maroon",
    "ff8a80": "maroon",
    "ffd740": "yellow",
    "ffc900": "yellow",
    "fff6e1": "rosewater",
}

SKIP_KEYS = {
    "Overlay Screen",
    "Shadow",
    # "Lighten Screen",
    "Border",
    "Text Editor Border",
    "Text Editor Selection",
}

COLOR_KEYS = {
    "Background",
    "Body",
    "Body Heading Background",
    "Heading Text",
    "Preset Text",
    "Body Text",
    "Border",
    "Label Background",
    "Label Connection",
    "Power Button On",
    "Power Button Off",
    "Overlay Screen",
    "Lighten Screen",
    "Shadow",
    "Popup Selector Background",
    "Popup Background",
    "Popup Border",
    "Text Component Background",
    "Text Component Text",
    "Rotary Arc",
    "Rotary Arc Disabled",
    "Rotary Arc Unselected",
    "Rotary Arc Unselected Disabled",
    "Rotary Hand",
    "Rotary Body",
    "Rotary Body Border",
    "Linear Slider",
    "Linear Slider Disabled",
    "Linear Slider Unselected",
    "Linear Slider Thumb",
    "Linear Slider Thumb Disabled",
    "Widget Center Line",
    "Widget Primary 1",
    "Widget Primary 2",
    "Widget Primary Disabled",
    "Widget Secondary 1",
    "Widget Secondary 2",
    "Widget Secondary Disabled",
    "Widget Accent 1",
    "Widget Accent 2",
    "Widget Background",
    "Modulation Meter",
    "Modulation Meter Left",
    "Modulation Meter Right",
    "Modulation Meter Control",
    "Modulation Button Selected",
    "Modulation Button Dragging",
    "Modulation Button Unselected",
    "Icon Selector Icon",
    "Icon Button Off",
    "Icon Button Off Hover",
    "Icon Button Off Pressed",
    "Icon Button On",
    "Icon Button On Hover",
    "Icon Button On Pressed",
    "UI Button",
    "UI Button Text",
    "UI Button Hover",
    "UI Button Press",
    "UI Action Button",
    "UI Action Button Hover",
    "UI Action Button Press",
    "Text Editor Background",
    "Text Editor Border",
    "Text Editor Caret",
    "Text Editor Selection",
}


def recolor(value, pal):
    if not isinstance(value, str) or value.lower() in ("0", "00000000"):
        return value

    s = value.lower()

    if len(s) == 8:
        alpha, rgb = s[:2], s[2:]
    elif len(s) == 6:
        alpha, rgb = "ff", s
    elif len(s) == 7:
        alpha, rgb = "0" + s[0], s[1:]
    else:
        return value

    role = COLOR_MAP.get(rgb)
    return value if role is None else alpha + pal[role]


def resolve_spec(spec, pal):
    if isinstance(spec, (int, float)):
        return spec

    s = str(spec).lower()

    if ":" in s and s.split(":", 1)[1] in pal:
        alpha, role = s.split(":", 1)
        return alpha + pal[role]

    if s in pal:
        return "ff" + pal[s]

    h = s.lstrip("#")
    return "ff" + h if len(h) == 6 else h


def build_theme(base, flavor, pal):

    def convert(obj):
        return {
            k: (
                convert(v)
                if isinstance(v, dict)
                else recolor(v, pal) if k in COLOR_KEYS and k not in SKIP_KEYS else v
            )
            for k, v in obj.items()
        }

    skin = convert(base)

    for scope in ("all", flavor):
        for section, entries in MANUAL.get(scope, {}).items():

            if section == "global":
                target = skin
            else:
                ov = skin.setdefault("overrides", {})
                if not isinstance(ov.get(section), dict):
                    ov[section] = {}
                target = ov[section]

            for key, spec in entries.items():
                target[key] = resolve_spec(spec, pal)

    return skin


def load_default():
    if os.path.exists("default.vitalskin"):
        with open("default.vitalskin") as f:
            return json.load(f)

    url = "https://raw.githubusercontent.com/mtytel/vital/main/default.vitalskin"
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read().decode())


if __name__ == "__main__":

    base = load_default()
    for name, pal in PALETTES.items():
        with open(f"Catppuccin {name}.vitaltheme", "w") as f:
            json.dump(build_theme(base, name, pal), f)
        print("wrote Catppuccin", name)
