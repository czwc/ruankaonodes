# -*- coding: utf-8 -*-
"""生成《上午题全知识点总复习》可视化 HTML（复用 build_html.py 的模板）"""
import build_html as b

b.build_html(
    r'f:/软设笔记/上午题全知识点总复习.md',
    r'f:/软设笔记/上午题全知识点总复习_可视化.html',
    '上午题全知识点总复习 - 考前一遍过',
    4,
    0
)
