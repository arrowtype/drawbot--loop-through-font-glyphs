"""
    Export all glyphs from a OTF/TTF font to indivual SVGs, including glyphs 
    not in character map (e.g. only available via OpenType features).

    Potentially useful in the case of an icon font.
"""

from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.cocoaPen import CocoaPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from drawBot import *
import os
import sys

# using Space Mono because Recursive has wide code ligatures
fontPath = "source/fonts/SpaceMono-Bold.ttf"

outputDir = "source/exports/svg"

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

W,H= 1000, 1000

with TTFont(fontPath) as f:
    glyphSet = f.getGlyphSet()

    yMin, yMax = f["head"].yMin, f["head"].yMax
    xMin, xMax = f["head"].xMin, f["head"].xMax

    for glyphName in glyphSet.keys():
        newPage(W,H)
        fill(0.95)
        rect(0,0,W,H)

        fill(0)

        fontSize(24)
        font(fontPath)

        # set an indent for padding
        indent = 50

        # calculate width of characters
        w = xMax - xMin
        h = yMax - yMin

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
        translate(-xMin, -yMin)
        # translate with height of the path ... but this could use some improvement, still
        translate(-w*0.5, -h*0.5)

        # then, actually draw onto the canvas
        path = BezierPath(glyphSet=glyphSet)
        glyphSet[glyphName].draw(path)
        drawPath(path)

        # make a path like "source/svg-exports/Acircumflex.svg"
        saveTo=f"{outputDir}/{glyphName}.svg"
        
        # save to the path
        saveImage(saveTo)
