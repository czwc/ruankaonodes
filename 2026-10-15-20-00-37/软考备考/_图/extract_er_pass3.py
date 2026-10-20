# -*- coding: utf-8 -*-
import pymupdf, os
src = r"f:\软设笔记\2021-2024历年真题及解析"
out = r"f:\软设笔记\2021-2024历年真题及解析\_提取文本\_图"
jobs = [
    ("2021上", "2021年05月软件设计师下午真题及答案解析.pdf", "lead_bottom", 5),
    ("2021下", "2021年11月软件设计师下午真题及答案解析.pdf", "lead_bottom", 5),
    ("2022上", "2022年05月软件设计师下午真题及答案解析.pdf", "top_to_logic", 4),
    ("2022下", "2022年11月软件设计师下午真题及答案解析.pdf", "whole", 3),
]
for tag, fn, mode, pageno in jobs:
    path = os.path.join(src, fn)
    if not os.path.exists(path):
        print(tag, "PDF缺失"); continue
    doc = pymupdf.open(path)
    page = doc[pageno - 1]
    wms = page.search_for("手机端题库") + page.search_for("PC端题库")
    bottom = page.rect.height
    for w in wms:
        if w.y0 > page.rect.height * 0.6 and w.y0 - 4 < bottom:
            bottom = w.y0 - 4
    if mode == "lead_bottom":
        r = page.search_for("2-1")
        if not r:
            print(tag, "未找到2-1锚点"); continue
        clip = pymupdf.Rect(0, r[0].y1 + 3, page.rect.width, bottom)
    elif mode == "top_to_logic":
        r = page.search_for("逻辑结构设计")
        y1 = r[0].y0 - 4 if r else bottom
        clip = pymupdf.Rect(0, 30, page.rect.width, min(bottom, y1))
    else:
        clip = pymupdf.Rect(0, 20, page.rect.width, bottom)
    pix = page.get_pixmap(matrix=pymupdf.Matrix(2.4, 2.4), clip=clip)
    fp = os.path.join(out, f"{tag}_图2-1.png")
    pix.save(fp)
    print(f"{tag} | 第{pageno}页 | {pix.width}x{pix.height}px | {round(os.path.getsize(fp)/1024)}KB")
