# Looping through font binaries in DrawBot

A quick exploration of looping through all glyphs in a font binary (TTF or OTF).

Useful in cases such as:
- Exporting an icon font to SVGs or PNGs, etc
- Making a PDF to proofing every glyph in a font

## Usage

Make and activate a `venv`.

```
pip install -r requirements.txt
```

Then run the DrawBot script in a terminal:

```
python source/export-ttf-to-svg.py
```