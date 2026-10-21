# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import pymupdf, os
src = r"f:\软设笔记\2021-2024历年真题及解析"
out = r"f:\软设笔记\2021-2024历年真题及解析\_提取文本\_图"

# 1) 官方解析段
for tag, fn in [("2021上", "2021年05月软件设计师下午真题及答案解析.txt"),
                ("2023上", "2023年上半年软件设计师下午真题及参考答案.txt")]:
    c = open(os.path.join(src, "_提取文本", fn), encoding="utf-8").read()
    i = c.rfind("试题三")
    print(f"████ {tag} 试题三解析 ████")
    print(c[i:i+1500])

# 2) 裁图
jobs = [
    ("2021上_试题三", "2021年05月软件设计师下午真题及答案解析.pdf", 9),
    ("2022下_试题三", "2022年11月软件设计师下午真题及答案解析.pdf", 4),
]
for tag, fn, pageno in jobs:
    doc = pymupdf.open(os.path.join(src, fn))
    page = doc[pageno - 1]
    wms = page.search_for("手机端题库") + page.search_for("PC端题库")
    bottom = page.rect.height
    for w in wms:
        if w.y0 > page.rect.height * 0.6 and w.y0 - 4 < bottom:
            bottom = w.y0 - 4
    pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=pymupdf.Rect(0, 26, page.rect.width, bottom))
    fp = os.path.join(out, f"{tag}.png")
    pix.save(fp)
    print(f"{tag} | 第{pageno}页 | {pix.width}x{pix.height}px | {round(os.path.getsize(fp)/1024)}KB")

# 2023上：定位试题三图所在页
doc = pymupdf.open(os.path.join(src, "2023年上半年软件设计师下午真题及参考答案.pdf"))
target = None
for i, page in enumerate(doc):
    t = page.get_text()
    if ("图3-2" in t or "图 3-2" in t or ("用例图" in t and "类图" in t)) and i >= 3:
        target = (i, page); break
if target:
    i, page = target
    wms = page.search_for("手机端题库") + page.search_for("PC端题库")
    bottom = page.rect.height
    for w in wms:
        if w.y0 > page.rect.height * 0.6 and w.y0 - 4 < bottom:
            bottom = w.y0 - 4
    pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), clip=pymupdf.Rect(0, 26, page.rect.width, bottom))
    fp = os.path.join(out, "2023上_试题三.png")
    pix.save(fp)
    print(f"2023上_试题三 | 第{i+1}页 | {pix.width}x{pix.height}px | {round(os.path.getsize(fp)/1024)}KB")
else:
    print("2023上 未定位到图页，尝试渲染第5、6页")
    for pi in (4, 5):
        page = doc[pi]
        pix = page.get_pixmap(matrix=pymupdf.Matrix(1.6, 1.6))
        fp = os.path.join(out, f"probe_2023上_p{pi+1}.png")
        pix.save(fp)
        print("probe:", fp)
