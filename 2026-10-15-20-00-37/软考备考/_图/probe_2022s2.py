# -*- coding: utf-8 -*-
import pymupdf, os
src = r"f:\软设笔记\2021-2024历年真题及解析"
out = r"f:\软设笔记\2021-2024历年真题及解析\_提取文本\_图"
doc = pymupdf.open(os.path.join(src, "2022年05月软件设计师下午真题及答案解析.pdf"))
page = doc[2]
r = page.search_for("【问题 1】") or page.search_for("【问题1】")
y1 = r[0].y0 - 4 if r else page.rect.height * 0.5
pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=pymupdf.Rect(0, 0, page.rect.width, y1))
pix.save(os.path.join(out, "2022上_图2-1.png"))
print("2022上 定稿", pix.width, pix.height, round(os.path.getsize(os.path.join(out,"2022上_图2-1.png"))/1024), "KB")
