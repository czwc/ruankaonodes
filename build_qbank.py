# -*- coding: utf-8 -*-
"""生成《上午真题分类题库》可视化 HTML（复用 build_html.py 模板）"""
import build_html as b

b.build_html(
    r'f:/软设笔记/上午真题分类题库(2021-2024).md',
    r'f:/软设笔记/上午真题分类题库(2021-2024)_可视化.html',
    '上午真题分类题库 (2021-2024) - 按模块刷题',
    3
)
