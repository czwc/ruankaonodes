# -*- coding: utf-8 -*-
"""生成《下午题全题型总复习》可视化 HTML（复用 build_html.py 模板）"""
import build_html as b

b.build_html(
    r'f:/软设笔记/下午题全题型总复习.md',
    r'f:/软设笔记/下午题全题型总复习_可视化.html',
    '下午题全题型总复习 - 五大题型套路与骨架',
    5,
    0
)
