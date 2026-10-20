# -*- coding: utf-8 -*-
import pymupdf, os
src = r"f:\软设笔记\2021-2024历年真题及解析"
out = r"f:\软设笔记\2021-2024历年真题及解析\_提取文本\_图"
doc = pymupdf.open(os.path.join(src, "2022年05月软件设计师下午真题及答案解析.pdf"))
page = doc[2]  # 第3页
r = page.search_for("概念模型设计")
wms = page.search_for("手机端题库")
bottom = page.rect.height
for w in wms:
    if w.y0 > page.rect.height * 0.6: bottom = w.y0 - 4
y0 = r[0].y1 + 2 if r else page.rect.height * 0.5
pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=pymupdf.Rect(0, y0, page.rect.width, bottom))
pix.save(os.path.join(out, "probe_2022上_p3底.png"))
print("p3底", pix.width, pix.height)
page = doc[3]  # 第4页
pix = page.get_pixmap(matrix=pymupdf.Matrix(1.6, 1.6), clip=pymupdf.Rect(0, 0, page.rect.width, page.rect.height * 0.55))
pix.save(os.path.join(out, "probe_2022上_p4上.png"))
print("p4上", pix.width, pix.height)
