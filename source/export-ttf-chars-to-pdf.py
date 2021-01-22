"""
    Run from base of repo.
"""

from fontTools.ttLib import TTFont
from drawBot import *

autoOpen = True

fontPath = "source/RecursiveMonoCslSt-Med.ttf"

W,H= 1000,1000
fontSize = W/40

newPage(W,H)

txt = FormattedString()
txt.font(fontPath)
txt.fontSize(fontSize)
txt.lineHeight(fontSize * 1.5)

with TTFont(fontPath) as f:
    for key, value in f["cmap"].getBestCmap().items():
        print(chr(key), end=" ")
        txt.append(chr(key) + " ")

textBox(txt, (0, 0, W, H))

saveTo="test.pdf"
saveImage(saveTo)

if autoOpen:
    import os
    # os.system(f"open --background -a Preview {path}")
    os.system(f"open -a Preview {saveTo}")
