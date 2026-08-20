# -*- coding: utf-8 -*-
"""把重点专题 MD 转成 HTML 可视化版(复用三件套模板)"""
import os
import sys

sys.path.insert(0, r"f:\软设笔记\考前冲刺三件套")
from build_html import HTML_TEMPLATE

BASE_DIR = r"f:\软设笔记\重点专题"

for f in os.listdir(BASE_DIR):
    if f.endswith(".md"):
        name = f[:-3]
        md_path = os.path.join(BASE_DIR, f)
        html_path = os.path.join(BASE_DIR, name + "_可视化.html")
        with open(md_path, encoding="utf-8") as fp:
            md_content = fp.read()
        html = HTML_TEMPLATE.format(
            title=name + " - 软考软件设计师重点专题",
            sidebar_title="📌 重点专题",
            markdown=md_content,
        )
        with open(html_path, "w", encoding="utf-8") as fp:
            fp.write(html)
        print("OK " + name + "_可视化.html (" + str(os.path.getsize(html_path)) + " bytes)")
