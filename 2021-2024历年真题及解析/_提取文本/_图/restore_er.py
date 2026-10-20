# -*- coding: utf-8 -*-
import pymupdf, os
src = r"f:\软设笔记\2021-2024历年真题及解析"
out = r"f:\软设笔记\2021-2024历年真题及解析\_提取文本\_图"
def crop(pdf, pageno, mode, fp):
    doc = pymupdf.open(os.path.join(src, pdf))
    page = doc[pageno - 1]
    wms = page.search_for("手机端题库") + page.search_for("PC端题库")
    bottom = page.rect.height
    for w in wms:
        if w.y0 > page.rect.height * 0.6 and w.y0 - 4 < bottom:
            bottom = w.y0 - 4
    if mode == "lead_bottom":
        r = page.search_for("2-1")
        clip = pymupdf.Rect(0, r[0].y1 + 3, page.rect.width, bottom)
    else:  # top_to_q1
        r = page.search_for("【问题 1】") or page.search_for("【问题1】")
        y1 = r[0].y0 - 4 if r else bottom
        clip = pymupdf.Rect(0, 0, page.rect.width, y1)
    pix = page.get_pixmap(matrix=pymupdf.Matrix(2.4, 2.4), clip=clip)
    pix.save(fp)
    print(tag, pix.width, "x", pix.height, round(os.path.getsize(fp)/1024), "KB")

jobs = [
    ("2021上", "2021年05月软件设计师下午真题及答案解析.pdf", 5, "lead_bottom"),
    ("2021下", "2021年11月软件设计师下午真题及答案解析.pdf", 5, "lead_bottom"),
    ("2022上", "2022年05月软件设计师下午真题及答案解析.pdf", 3, "top_to_q1"),
]
for tag, fn, pageno, mode in jobs:
    fp = os.path.join(out, f"{tag}_图2-1.png")
    if os.path.exists(fp):
        print(tag, "已存在跳过"); continue
    crop(fn, pageno, mode, fp)
