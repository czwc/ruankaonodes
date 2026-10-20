# -*- coding: utf-8 -*-
import pymupdf, os
src = r"f:\软设笔记\2021-2024历年真题及解析"
out = r"f:\软设笔记\2021-2024历年真题及解析\_提取文本\_图"
os.makedirs(out, exist_ok=True)
files = {
    "2021上": "2021年05月软件设计师下午真题及答案解析.pdf",
    "2021下": "2021年11月软件设计师下午真题+答案解析.pdf",
    "2022上": "2022年05月软件设计师下午真题及答案解析.pdf",
    "2022下": "2022年11月软件设计师下午真题及答案解析.pdf",
    "2023上": "2023年上半年软件设计师下午真题及参考答案.pdf",
}
for tag, fn in files.items():
    path = os.path.join(src, fn)
    if not os.path.exists(path):
        print(tag, "PDF缺失:", fn); continue
    doc = pymupdf.open(path)
    hit = None
    for i, page in enumerate(doc):
        t = page.get_text()
        if ("实体联系图" in t) or ("概念模型设计" in t and "逻辑结构" in t) or ("概念结构设计" in t and "逻辑结构" in t):
            if "图2-1" in t or "图 2-1" in t or "实体联系图" in t:
                hit = (i, page, t); break
    if not hit:
        print(tag, "未找到图2-1所在页"); continue
    i, page, t = hit
    r1 = page.search_for("概念模型设计") or page.search_for("概念结构设计")
    r2 = page.search_for("逻辑结构设计")
    clip = None
    if r1 and r2 and r2[0].y0 > r1[0].y1:
        y0, y1 = r1[0].y1 + 2, r2[0].y0 - 2
        clip = pymupdf.Rect(0, y0, page.rect.width, y1)
        mode = "标题间裁剪"
    else:
        cap = page.search_for("图2-1") or page.search_for("图 2-1")
        if cap:
            y = cap[0].y0
            clip = pymupdf.Rect(0, max(0, y-500), page.rect.width, min(page.rect.height, y+16))
            mode = "题注上方裁剪"
        else:
            clip = page.rect; mode = "整页"
    pix = page.get_pixmap(matrix=pymupdf.Matrix(2.2, 2.2), clip=clip)
    fp = os.path.join(out, f"{tag}_图2-1.png")
    pix.save(fp)
    print(f"{tag} | 第{i+1}页 | {mode} | {pix.width}x{pix.height}px | {round(os.path.getsize(fp)/1024)}KB")
