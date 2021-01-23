"""
    Print ALL glyphs in a TTF to a PDF, including glyphs not in character map (e.g. only available via OpenType features).

    Decomposes all glyphs in a TTF (https://github.com/fonttools/fonttools/blob/81fa5b5265fe0372a3b0589376d17b4b95d412e3/Snippets/decompose-ttf.py).

    Then prints these to a PDF, one page at a time.
"""

from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.cocoaPen import CocoaPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from drawBot import *
import os
import sys

try:
    import pathops
except ImportError:
    sys.exit(
        "This script requires the skia-pathops module. "
        "`pip install skia-pathops` and then retry."
    )

autoOpen = True

fontPath = "source/RecursiveMonoCslSt-Med.ttf"

outputDir = "source/exports/pdf"
filename = "all-glyphs-recursive"

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

W,H= 1000,1000
fontSize = W/40

# using ASCII to get a good estimate of min & max values in the font
string="0 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z ! \" # $ % & \' ( ) * + , - . / : ; < = > ? @ [ \\ ] ^ _ ` { | } ~"

# setting min/max X/Y values to help size & center glyphs later
# somewhat flawed, because really wide or really tall glyphs are a bit too big
xMin, yMin, xMax, yMax = 0,0,0,0
for char in string.split():
    path = BezierPath()
    path.text(char, font=fontPath, fontSize=W)
    # calculate the width and height of the path
    xMin1, yMin1, xMax1, yMax1 = path.bounds()

    if xMin1 < xMin:
        xMin = xMin1
    if yMin1 < yMin:
        yMin = yMin1
    if xMax1 > xMax:
        xMax = xMax1
    if yMax1 > yMax:
        yMax = yMax1


with TTFont(fontPath) as f:
    glyfTable = f["glyf"]
    glyphSet = f.getGlyphSet()

    for glyphName in glyphSet.keys():
        if not glyfTable[glyphName].isComposite():
            continue

        # record TTGlyph outlines without components
        dcPen = DecomposingRecordingPen(glyphSet)
        glyphSet[glyphName].draw(dcPen)

        # replay recording onto a skia-pathops Path
        path = pathops.Path()
        pathPen = path.getPen()
        dcPen.replay(pathPen)

        # remove overlaps
        path.simplify()

        # create new TTGlyph from Path
        ttPen = TTGlyphPen(None)
        path.draw(ttPen)
        glyfTable[glyphName] = ttPen.glyph()

    for glyphName in glyphSet.keys():

        # get outlines to check if there are any (skip printing whitespace glyphs)
        pen = RecordingPen()
        glyphSet[glyphName].draw(pen)

        if len(pen.value) > 0:

            try:
                newPage(W,H)

                # Fetch the path of the glyph as a NSBezierPath
                pen = CocoaPen(None)
                glyphSet[glyphName].draw(pen)
                glyphPath = pen.path
                # ...and then convert it to a DrawBot BezierPath
                glyphPath = BezierPath(glyphPath)

                # set an indent for padding
                indent = 50

                # print(xMin, yMin, xMax, yMax)

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
                translate(-w * 0.5, -h*.5)

                # then, actually draw onto the canvas
                drawPath(glyphPath)

            except TypeError:
                pass

saveTo=f"{outputDir}/{filename}.pdf"
saveImage(saveTo)

if autoOpen:
    import os
    os.system(f"open -a Preview {saveTo}")
