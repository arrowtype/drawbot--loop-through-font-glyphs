"""
    Make an animation to loop through all printable ASCII characters in a font binary (excludes stylistic sets, etc).

    See README.md for usage details.
"""

from fontTools.ttLib import TTFont
from drawBot import *
import os

fontPath = "source/fonts/RecursiveMonoCslSt-Med.ttf"
outputDir = "source/exports/mp4"
filename = "ascii-recursive"

W,H= 1080,1350
# W,H= 1080,1080
fontSize = W/2

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

print(f"\n🤖 Saving SVGs to → {outputDir}.\n")
print("🤖 Depending on the font, this may take a few minutes...\n")

string="0 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z ! \" # $ % & \' ( ) * + , - . / : ; < = > ? @ [ \\ ] ^ _ ` { | } ~"

xMin, yMin, xMax, yMax = 0,0,0,0
print(xMin, yMin, xMax, yMax)
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

# open the font with TTFont
for i in range(1,3):
    with TTFont(fontPath) as f:
        # loop through the character map
        for char in string.split():
            # a try/except to handle characters without paths (like "space"), which will error if you try to draw them as a bezier path
            try:
                newPage(W,H)

                fill(0)
                rect(0,0,W,H)

                fill(1)

                # set up a bezier path
                path = BezierPath()

                # set the current character into the bezier path
                # path.text(chr(key), font=fontPath, fontSize=500)
                path.text(char, font=fontPath, fontSize=W, align="center")

                # set an indent for padding
                indent = 50

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
                # translate with half of the width and height of the path
                # translate(-w*.125, -h*.5)
                translate(-indent, -h*.5)
                # draw the path
                drawPath(path)

            except TypeError:
                pass

saveImage(f"{outputDir}/ascii.mp4")