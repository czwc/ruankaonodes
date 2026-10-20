# -*- coding: utf-8 -*-
import pymupdf, os
src = r"f:\软设笔记\2021-2024历年真题及解析"
out = r"f:\软设笔记\2021-2024历年真题及解析\_提取文本\_图"
files = {
    "2021上": "2021年05月软件设计师下午真题及答案解析.pdf",
    "2021下": "2021年11月软件设计师下午真题及答案解析.pdf",
    "2022上": "2022年05月软件设计师下午真题及答案解析.pdf",
    "2022下": "2022年11月软件设计师下午真题及答案解析.pdf",
    "2023上": "2023年上半年软件设计师下午真题及参考答案.pdf",
}
for tag, fn in files.items():
    doc = pymupdf.open(os.path.join(src, fn))
    # 找试题一起始页
    start = None
    for i, page in enumerate(doc):
        if "试题一" in page.get_text():
            start = i; break
    if start is None:
        print(tag, "未找到试题一"); continue
    end = len(doc)
    for i in range(start + 1, len(doc)):
        if "试题二" in doc[i].get_text():
            end = i; break
    for cap, name in (("图1-1", "t"), ("图1-2", "l")):
        done = False
        for i in range(start, end):
            page = doc[i]
            wms = page.search_for("手机端题库") + page.search_for("PC端题库")
            bottom = page.rect.height
            for w in wms:
                if w.y0 > page.rect.height * 0.6 and w.y0 - 4 < bottom:
                    bottom = w.y0 - 4
            rs = page.search_for(cap)
            if not rs:
                continue
            r = rs[0]
            y0 = max(28, r.y0 - 500)
            clip = pymupdf.Rect(0, y0, page.rect.width, min(bottom, r.y1 + 8))
            pix = page.get_pixmap(matrix=pymupdf.Matrix(2.2, 2.2), clip=clip)
            fp = os.path.join(out, f"{tag}_图{cap[-3:]}.png")
            pix.save(fp)
            print(f"{tag} {cap} | 第{i+1}页 | {pix.width}x{pix.height}px | {round(os.path.getsize(fp)/1024)}KB")
            done = True
        if not done:
            print(f"{tag} {cap} 未找到")
