# -*- coding: utf-8 -*-
import pymupdf, os
src = r"f:\软设笔记\2021-2024历年真题及解析"
out = r"f:\软设笔记\2021-2024历年真题及解析\_提取文本\_图"
files = {
    "2021下": "2021年11月软件设计师下午真题及答案解析.pdf",
    "2022上": "2022年05月软件设计师下午真题及答案解析.pdf",
    "2022下": "2022年11月软件设计师下午真题及答案解析.pdf",
}
for tag, fn in files.items():
    fp = os.path.join(out, f"{tag}_图2-1.png")
    if os.path.exists(fp):
        print(tag, "已有，跳过"); continue
    path = os.path.join(src, fn)
    if not os.path.exists(path):
        print(tag, "PDF缺失:", fn); continue
    doc = pymupdf.open(path)
    hit = None
    for i, page in enumerate(doc):
        t = page.get_text()
        if "逻辑结构设计" in t:
            hit = (i, page); break
    if not hit:
        print(tag, "未找到逻辑结构设计页"); continue
    i, page = hit
    r2 = page.search_for("逻辑结构设计")
    y1 = r2[0].y0 - 2 if r2 else page.rect.height * 0.75
    clip = pymupdf.Rect(0, 0, page.rect.width, max(120, y1))
    pix = page.get_pixmap(matrix=pymupdf.Matrix(2.2, 2.2), clip=clip)
    pix.save(fp)
    print(f"{tag} | 第{i+1}页 | 兜底裁剪 | {pix.width}x{pix.height}px | {round(os.path.getsize(fp)/1024)}KB")
