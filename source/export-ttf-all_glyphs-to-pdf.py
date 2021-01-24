"""
    Make a PDF to proof all glyphs in an OTF/TTF font binary.
"""

from fontTools.ttLib import TTFont
from drawBot import *
import os

autoOpen = True

fontPath = "source/RecursiveMonoCslSt-Med.ttf"
outputDir = "source/exports/pdf"
filename = "all_glyphs_listed-recursive"

pageSize = "Letter"
border = 20

txt = FormattedString(
    font=fontPath,
    fontSize=20,
    tracking=10,
    lineHeight=30
)
txt.appendGlyph(*txt.listFontGlyphNames())

while txt:
    newPage(pageSize)
    txt = textBox(txt, (border, border, width() - border*2, height() - border*2))

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

saveTo=f"{outputDir}/{filename}.pdf"
saveImage(saveTo)

if autoOpen:
    os.system(f"open -a Preview {saveTo}")
