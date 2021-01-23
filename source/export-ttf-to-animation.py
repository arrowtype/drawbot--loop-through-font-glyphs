"""
    Make an animation to loop through all characters in a font binary (excludes stylistic sets, etc).

    See README.md for usage details.
"""

from fontTools.ttLib import TTFont
from drawBot import *
import os

fontPath = "source/RecursiveMonoCslSt-Med.ttf"
outputDir = "source/exports/mp4"
filename = "chars-recursive"

W,H= 1080,1350

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

print(f"\n🤖 Saving SVGs to → {outputDir}.\n")
print("🤖 Depending on the font, this may take a few minutes...\n")

# using ASCII to get a good estimate of min & max values in the font
string="0 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z ! \" # $ % & \' ( ) * + , - . / : ; < = > ? @ [ \\ ] ^ _ ` { | } ~"

# setting min/max X/Y values to help center animation later
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

# open the font with TTFont
with TTFont(fontPath) as f:
    # loop through the character map
    for key, value in f["cmap"].getBestCmap().items():
        # a try/except to handle characters without paths (like "space"), which will error if you try to draw them as a bezier path
        try:
            # make a new drawbot page
            newPage(W,H)

            fill(0)
            rect(0,0,W,H)

            fill(1)

            # set up a bezier path
            path = BezierPath()

            # set the current character into the bezier path
            path.text(chr(key), font=fontPath, fontSize=W, align="center")
            # path.text(char, font=fontPath, fontSize=W, align="center")

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
            translate(0, -h*.5)
            # draw the path
            drawPath(path)

            # # make a path like "source/svg-exports/Acircumflex.svg"
            # # saveTo=f"{outputDir}/{value}.svg"
            # saveTo=f"{outputDir}/{char}.svg"
            
            # # save to the path
            # saveImage(saveTo)

        except TypeError:
            pass

saveImage(f"{outputDir}/{filename}.mp4")