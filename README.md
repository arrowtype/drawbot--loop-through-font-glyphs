# Looping through font binaries in DrawBot

A quick exploration of looping through all glyphs in a font binary (TTF or OTF). Probably a WIP.

Useful in cases such as:
- Exporting an icon font to SVGs or PNGs, etc
- Making a PDF to proofing every glyph in a font

## Usage

### Set up the environment

To build, set up the virtual environment

```bash
virtualenv -p python3 venv
```

Then activate it:

```bash
source venv/bin/activate
```

Then install requirements:

```bash
pip install -U -r requirements.txt
```

### Run the scripts

Run the desired DrawBot script in a terminal:

```bash
python source/export-ttf-to-svg.py
```

```bash
python source/export-ttf-chars-to-svg.py # warning: this one can take a while for a large font!
```

To alter the font, replace `source/RecursiveMonoCslSt-Med.ttf` with any ttf or otf font, then update the drawbot scripts to point to that new file path.
