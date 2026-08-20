# -*- coding: utf-8 -*-
"""把分类题库 MD 转成 HTML 可视化版(复用三件套模板)"""
import os
import sys

sys.path.insert(0, r"f:\软设笔记\考前冲刺三件套")
from build_html import HTML_TEMPLATE

BASE_DIR = r"f:\软设笔记\分类题库"

f = {
    "md": "分类题库_标准版.md",
    "html": "分类题库_标准版_可视化.html",
    "title": "分类题库(标准版) - 软考软件设计师",
    "sidebar_title": "📝 分类题库",
}

md_path = os.path.join(BASE_DIR, f["md"])
html_path = os.path.join(BASE_DIR, f["html"])
with open(md_path, encoding="utf-8") as fp:
    md_content = fp.read()
html = HTML_TEMPLATE.format(
    title=f["title"],
    sidebar_title=f["sidebar_title"],
    markdown=md_content,
)
with open(html_path, "w", encoding="utf-8") as fp:
    fp.write(html)
size = os.path.getsize(html_path)
print("OK " + f["html"] + " (" + str(size) + " bytes)")
