# -*- coding: utf-8 -*-
import pymupdf, os
src = r"f:\软设笔记\2021-2024历年真题及解析\2022年11月软件设计师下午真题及答案解析.pdf"
out = r"f:\软设笔记\2021-2024历年真题及解析\_提取文本\_图\2022下_图6-1.png"
doc = pymupdf.open(src)
page = doc[7]  # 第8页：类图+Java代码开头
r = page.search_for("图6-1")
if not r:
    r = page.search_for("图 6-1")
cap = r[0]
clip = pymupdf.Rect(0, max(26, cap.y0 - 460), page.rect.width, cap.y1 + 6)
pix = page.get_pixmap(matrix=pymupdf.Matrix(2.4, 2.4), clip=clip)
pix.save(out)
print("图6-1:", pix.width, "x", pix.height, round(os.path.getsize(out)/1024), "KB")
