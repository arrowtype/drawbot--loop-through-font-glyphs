"""
    Run from base of repo.
"""

from fontTools.ttLib import TTFont
from fontTools.pens.cocoaPen import CocoaPen
from drawBot import *
import os

autoOpen = True

# fontPath = "source/RecursiveMonoCslSt-Med.ttf"
fontPath = "source/Grinnell-ExtraBold.ttf"

outputDir = "source/exports/pdf"
filename = "all-glyphs-recursive"

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

W,H= 1000,1000
fontSize = W/40

with TTFont(fontPath) as f:
    glyfTable = f["glyf"]
    glyphSet = f.getGlyphSet()

    for glyphName in glyphSet.keys():

        # use try/except, because some glyphs don’t have paths to draw (e.g. "space")
        try :
            newPage(W,H)

            # Fetch the path of the glyph as a NSBezierPath
            pen = CocoaPen(None)
            glyphSet[glyphName].draw(pen)
            glyphPath = pen.path
            # ...and then convert it to a DrawBot BezierPath
            glyphPath = BezierPath(glyphPath)

            # then, actually draw onto the canvas
            drawPath(glyphPath)

        except TypeError:
            pass

saveTo=f"{outputDir}/{filename}.pdf"
saveImage(saveTo)

if autoOpen:
    import os
    # os.system(f"open --background -a Preview {path}")
    os.system(f"open -a Preview {saveTo}")
