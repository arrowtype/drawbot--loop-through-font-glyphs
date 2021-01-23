"""
    Make SVGs from all characters in a font binary (excludes stylistic sets, etc).

    Note: this currently sizes each character to fill the canvas. To keep them a 
    similar scale, see size handling of other scripts in this repo.

    See README.md for usage details.
"""

from fontTools.ttLib import TTFont
from drawBot import *
import os

fontPath = "source/RecursiveMonoCslSt-Med.ttf"
outputDir = "source/exports/svg"

W,H= 1000,1000
fontSize = W/2

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

print(f"\n🤖 Saving SVGs to → {outputDir}.\n")
print("🤖 Depending on the font, this may take a few minutes...\n")

# open the font with TTFont
with TTFont(fontPath) as f:
    # loop through the character map
    for key, value in f["cmap"].getBestCmap().items():
        # make a new drawbot page
        newPage(W,H)

        # print characters to the terminal
        print(chr(key), end=" ")

        # a try/except to handle characters without paths (like "space"), which will error if you try to draw them as a bezier path
        try:
            # set up a bezier path
            path = BezierPath()

            # set the current character into the bezier path
            path.text(chr(key), font=fontPath, fontSize=500)

            # set an indent
            indent = 50
            # calculate the width and height of the path
            minx, miny, maxx, maxy = path.bounds()
            w = maxx - minx
            h = maxy - miny
            # calculate the box where we want to draw the path in
            boxWidth = width() - indent * 2
            boxHeight = height() - indent * 2
            # calculate a scale based on the given path bounds and the box
            s = min([boxWidth / float(w), boxHeight / float(h)])
            # translate to the middle
            translate(width()*.5, height()*.5)
            # set the scale
            scale(s)
            # translate the negative offset, letter could have overshoot
            translate(-minx, -miny)
            # translate with half of the width and height of the path
            translate(-w*.5, -h*.5)
            # draw the path
            drawPath(path)

            # make a path like "source/svg-exports/Acircumflex.svg"
            saveTo=f"{outputDir}/{value}.svg"
            
            # save to the path
            saveImage(saveTo)

        except TypeError:
            pass
