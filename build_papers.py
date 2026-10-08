# -*- coding: utf-8 -*-
"""把 2021-2024历年真题及解析/_提取文本/*.txt 转成带目录导航的可视化 HTML，
并在根目录生成《真题阅读器.html》门户。用法：python build_papers.py"""
import os
import re
import glob
import urllib.parse
import build_html as b

SRC = r'f:/软设笔记/2021-2024历年真题及解析/_提取文本'
ROOT = r'f:/软设笔记'
MD_DIR = os.path.join(SRC, '_md')
os.makedirs(MD_DIR, exist_ok=True)


def read_text(fp):
    for enc in ('utf-8', 'gb18030'):
        try:
            with open(fp, 'r', encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise RuntimeError('无法解码: ' + fp)


def to_md(text):
    """轻量结构化：试题/答案解析 → ##，问题 → ###；转义 < 防止被 marked 当 HTML 吞掉"""
    text = text.replace('<', '＜')
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        if re.match(r'^试题[一二三四五六七八九十]', s):
            out.append('## ' + s)
        elif re.match(r'^【问题', s) or re.match(r'^问题[一二三四五六]', s):
            out.append('### ' + s)
        elif re.match(r'^(参考答案|答案解析|答案及解析|试题答案与解析)', s):
            out.append('## ' + s)
        else:
            out.append(ln)
    return '\n'.join(out)


papers = []
for fp in sorted(glob.glob(os.path.join(SRC, '*.txt'))):
    name = os.path.splitext(os.path.basename(fp))[0]
    if name.startswith('_'):
        continue
    md = to_md(read_text(fp))
    md_path = os.path.join(MD_DIR, name + '.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md)
    title = name.replace('软件设计师', '·') + ' - 真题阅读'
    html_name = name + '_可视化.html'
    b.build_html(md_path, os.path.join(SRC, html_name), title, 0, 2)
    papers.append((name, html_name))
    print('paper done:', name)

am = [(n, h) for n, h in papers if ('上午' in n or '综合知识' in n)]
pm = [(n, h) for n, h in papers if ('上午' not in n and '综合知识' not in n)]


def links(lst):
    return '\n'.join(
        '- [{}](2021-2024历年真题及解析/_提取文本/{})'.format(n, urllib.parse.quote(h))
        for n, h in lst
    )


hub_md = '# 历年真题阅读器（2021-2024）\n\n' \
    '> 13 份真题的完整提取文本，带目录导航，含答案解析。\n' \
    '> **做题纪律：限时独立做完，再对答案——先看答案题就废了。**\n\n' \
    '## 上午卷（{} 份）\n\n{}\n\n' \
    '## 下午卷（{} 份）\n\n{}\n'.format(len(am), links(am), len(pm), links(pm))

hub_md_path = os.path.join(MD_DIR, '_真题阅读器.md')
with open(hub_md_path, 'w', encoding='utf-8') as f:
    f.write(hub_md)
b.build_html(hub_md_path, os.path.join(ROOT, '真题阅读器.html'),
             '历年真题阅读器 (2021-2024)', 0, 0)
print('hub done: 真题阅读器.html (上午 {} 份 / 下午 {} 份)'.format(len(am), len(pm)))
