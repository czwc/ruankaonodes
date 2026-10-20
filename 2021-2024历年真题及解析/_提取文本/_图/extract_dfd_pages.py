# -*- coding: utf-8 -*-
import pymupdf, os
src = r"f:\软设笔记\2021-2024历年真题及解析"
out = r"f:\软设笔记\2021-2024历年真题及解析\_提取文本\_图"
# (标签, 文件, 页码, 裁剪模式 full/top_q1)
jobs = [
    ("2021上_试题一", "2021年05月软件设计师下午真题及答案解析.pdf", 3, "full"),
    ("2021下_试题一", "2021年11月软件设计师下午真题及答案解析.pdf", 3, "full"),
    ("2022上_试题一0层", "2022年05月软件设计师下午真题及答案解析.pdf", 3, "top_q1"),
    ("2022上_试题一顶层", "2022年05月软件设计师下午真题及答案解析.pdf", 2, "full"),
    ("2022下_试题一", "2022年11月软件设计师下午真题及答案解析.pdf", 2, "full"),
    ("2023上_试题一", "2023年上半年软件设计师下午真题及参考答案.pdf", 1, "full"),
]
for tag, fn, pageno, mode in jobs:
    fp = os.path.join(out, f"{tag}.png")
    if os.path.exists(fp):
        print(tag, "已有跳过"); continue
    doc = pymupdf.open(os.path.join(src, fn))
    page = doc[pageno - 1]
    wms = page.search_for("手机端题库") + page.search_for("PC端题库")
    bottom = page.rect.height
    for w in wms:
        if w.y0 > page.rect.height * 0.6 and w.y0 - 4 < bottom:
            bottom = w.y0 - 4
    if mode == "top_q1":
        r = page.search_for("【问题 1】") or page.search_for("【问题1】")
        if r: bottom = min(bottom, r[0].y0 - 4)
    clip = pymupdf.Rect(0, 26, page.rect.width, bottom)
    pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=clip)
    pix.save(fp)
    print(f"{tag} | 第{pageno}页 | {pix.width}x{pix.height}px | {round(os.path.getsize(fp)/1024)}KB")
