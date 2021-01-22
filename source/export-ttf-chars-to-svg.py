"""
    Run from base of repo.
"""

from fontTools.ttLib import TTFont
from drawBot import *
import os

autoOpen = True

fontPath = "source/RecursiveMonoCslSt-Med.ttf"
outputDir = "source/svg-exports"

W,H= 1000,1000
fontSize = W/2

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

with TTFont(fontPath) as f:
    for key, value in f["cmap"].getBestCmap().items():
        newPage(W,H)
        print(chr(key), end=" ")

        try:
            path = BezierPath()

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

            saveTo=f"{outputDir}/{value}.svg"
            
            saveImage(saveTo)

        except TypeError:
            pass


textBox(txt, (0, 0, W, H))


if autoOpen:
    import os
    # os.system(f"open --background -a Preview {path}")
    os.system(f"open -a Preview {saveTo}")
