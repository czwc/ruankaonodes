# -*- coding: utf-8 -*-
import pymupdf, os
src = r"f:\软设笔记\2021-2024历年真题及解析\2022年11月软件设计师下午真题及答案解析.pdf"
out = r"f:\软设笔记\2021-2024历年真题及解析\_提取文本\_图\2022下_图2-1.png"
doc = pymupdf.open(src)
page = doc[2]
r = page.search_for("试题三")
y1 = r[0].y0 - 6 if r else page.rect.height
pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=pymupdf.Rect(0, 0, page.rect.width, y1))
pix.save(out)
print("2022下 定稿", pix.width, pix.height, round(os.path.getsize(out)/1024), "KB")
