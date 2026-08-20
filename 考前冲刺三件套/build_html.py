#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把三件套 MD 转成 HTML 可视化版"""
import os
import sys

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#3b82f6">
<title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script>
if(typeof marked==='undefined'){{
window.marked={{parse:function(md){{
var h=md;
h=h.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
h=h.replace(/```([\\s\\S]*?)```/g,function(m,c){{return'<pre><code>'+c+'</code></pre>';}});
h=h.replace(/^#### (.*)$/gm,'<h4>$1</h4>');
h=h.replace(/^### (.*)$/gm,'<h3>$1</h3>');
h=h.replace(/^## (.*)$/gm,'<h2>$1</h2>');
h=h.replace(/^# (.*)$/gm,'<h1>$1</h1>');
h=h.replace(/^&gt; (.*)$/gm,'<blockquote><p>$1</p></blockquote>');
h=h.replace(/^---$/gm,'<hr>');
h=h.replace(/\\*\\*(.*?)\\*\\*/g,'<strong>$1</strong>');
h=h.replace(/`([^`]+)`/g,'<code>$1</code>');
h=h.replace(/^- (.*)$/gm,'<li>$1</li>');
h=h.replace(/^\\* (.*)$/gm,'<li>$1</li>');
h=h.replace(/(<li>[\\s\\S]*?<\\/li>)/g,'<ul>$1</ul>');
h=h.replace(/^\\|(.*)\\|$/gm,function(m,r){{
var cells=r.split('|').filter(function(c){{return c.trim();}});
if(cells[0]&&cells[0].indexOf('-')>=0&&cells[0].indexOf(':')<0)return'';
return'<tr>'+cells.map(function(c){{return'<td>'+c.trim()+'</td>';}}).join('')+'</tr>';
}});
h=h.replace(/(<tr>[\\s\\S]*?<\\/tr>)/g,'<table>$1</table>');
h=h.replace(/\\n\\n/g,'</p><p>');
h='<div><p>'+h+'</p></div>';
h=h.replace(/<p><\\/p>/g,'');
h=h.replace(/<p>(<h[1-4]>)/g,'$1');
h=h.replace(/(<\\/h[1-4]>)<\\/p>/g,'$1');
h=h.replace(/<p>(<blockquote>)/g,'$1');
h=h.replace(/(<\\/blockquote>)<\\/p>/g,'$1');
h=h.replace(/<p>(<hr>)/g,'$1');
h=h.replace(/<p>(<pre>)/g,'$1');
h=h.replace(/(<\\/pre>)<\\/p>/g,'$1');
h=h.replace(/<p>(<table>)/g,'$1');
h=h.replace(/(<\\/table>)<\\/p>/g,'$1');
h=h.replace(/<p>(<ul>)/g,'$1');
h=h.replace(/(<\\/ul>)<\\/p>/g,'$1');
return h;
}}}};
}}
</script>
<style>
:root[data-theme="light"]{{--bg:#ffffff;--text:#1e293b;--sidebar-bg:#f8fafc;--accent:#3b82f6;--border:#e2e8f0;--code-bg:#f1f5f9;--block-bg:#eff6ff;--table-head:#3b82f6;}}
:root[data-theme="dark"]{{--bg:#0f172a;--text:#e2e8f0;--sidebar-bg:#1e293b;--accent:#60a5fa;--border:#334155;--code-bg:#1e293b;--block-bg:#1e3a5f;--table-head:#1e40af;}}
*{{box-sizing:border-box;-webkit-tap-highlight-color:transparent;}}
body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--text);line-height:1.8;font-size:16px;transition:background .3s,color .3s;}}
.sidebar{{position:fixed;top:0;left:0;width:280px;height:100vh;background:var(--sidebar-bg);border-right:1px solid var(--border);overflow-y:auto;padding:20px 16px;z-index:100;transition:transform .3s;}}
.sidebar::-webkit-scrollbar{{width:6px;}}
.sidebar::-webkit-scrollbar-thumb{{background:#94a3b8;border-radius:3px;}}
.sidebar h3{{font-size:16px;margin:0 0 12px;display:flex;justify-content:space-between;align-items:center;color:var(--accent);}}
.theme-toggle{{background:none;border:none;font-size:18px;cursor:pointer;padding:4px 8px;border-radius:6px;color:var(--text);}}
.theme-toggle:hover{{background:rgba(128,128,128,.1);}}
.search-box{{width:100%;padding:8px 12px;border:1px solid var(--border);border-radius:8px;font-size:14px;background:var(--bg);color:var(--text);margin-bottom:12px;}}
#toc{{font-size:14px;}}
#toc a{{display:block;padding:6px 10px;color:var(--text);text-decoration:none;border-radius:6px;margin-bottom:2px;transition:all .2s;border-left:3px solid transparent;}}
#toc a:hover,#toc a.active{{background:rgba(59,130,246,.1);color:var(--accent);border-left-color:var(--accent);}}
#toc a.h2{{font-weight:600;margin-top:8px;}}
#toc a.h3{{padding-left:24px;font-size:13px;color:#64748b;}}
:root[data-theme="dark"] #toc a.h3{{color:#94a3b8;}}
.content-wrapper{{margin-left:280px;min-height:100vh;transition:margin .3s;}}
.content{{max-width:900px;margin:0 auto;padding:24px 28px 80px;}}
.content h1{{font-size:26px;border-bottom:3px solid var(--accent);padding-bottom:10px;margin-top:8px;color:var(--accent);}}
.content h2{{font-size:22px;margin-top:36px;padding:10px 14px;background:var(--block-bg);border-left:4px solid var(--accent);border-radius:6px;}}
.content h3{{font-size:18px;margin-top:28px;color:var(--accent);}}
.content h4{{font-size:16px;margin-top:20px;}}
.content p{{margin:12px 0;}}
.content strong{{color:var(--accent);}}
:root[data-theme="dark"] .content strong{{color:#fbbf24;}}
.content code{{background:var(--code-bg);padding:2px 6px;border-radius:4px;font-family:"Consolas","Monaco",monospace;font-size:14px;color:#dc2626;}}
:root[data-theme="dark"] .content code{{color:#f87171;}}
.content pre{{background:var(--code-bg);padding:14px;border-radius:8px;overflow-x:auto;border:1px solid var(--border);}}
.content pre code{{background:none;padding:0;color:var(--text);}}
.content table{{border-collapse:collapse;width:100%;margin:14px 0;font-size:14px;}}
.content th{{background:var(--table-head);color:#fff;padding:10px 12px;text-align:left;border:1px solid var(--border);}}
.content td{{padding:8px 12px;border:1px solid var(--border);}}
.content tr:nth-child(even){{background:var(--code-bg);}}
.content blockquote{{background:var(--block-bg);border-left:4px solid var(--accent);padding:12px 16px;margin:14px 0;border-radius:0 8px 8px 0;}}
.content blockquote p{{margin:6px 0;}}
.content hr{{border:none;border-top:2px dashed var(--border);margin:28px 0;}}
.content ul{{padding-left:22px;}}
.content li{{margin-bottom:6px;}}
.content details{{margin:14px 0;border:1px solid var(--border);border-radius:8px;overflow:hidden;background:var(--code-bg);}}
.content summary{{padding:12px 16px;cursor:pointer;font-weight:600;color:var(--accent);background:var(--block-bg);}}
.content details[open] summary{{border-bottom:1px solid var(--border);}}
.content details .rk-detail-body{{padding:14px 16px;}}
#menu-btn{{display:none;position:fixed;top:12px;left:12px;z-index:200;background:var(--accent);color:#fff;border:none;padding:8px 14px;border-radius:8px;font-size:14px;cursor:pointer;}}
.progress-bar{{position:fixed;top:0;left:0;height:3px;background:var(--accent);z-index:300;transition:width .1s;width:0;}}
.float-btn{{position:fixed;right:20px;bottom:20px;width:44px;height:44px;border-radius:50%;background:var(--accent);color:#fff;border:none;cursor:pointer;font-size:18px;box-shadow:0 2px 8px rgba(0,0,0,.2);z-index:150;display:flex;align-items:center;justify-content:center;text-decoration:none;}}
#menu-close{{display:none;}}
@media(max-width:900px){{
.sidebar{{transform:translateX(-100%);}}
.sidebar.open{{transform:translateX(0);box-shadow:4px 0 20px rgba(0,0,0,.15);}}
.content-wrapper{{margin-left:0;}}
#menu-btn{{display:flex;}}
#menu-close{{display:block;position:absolute;top:12px;right:12px;background:none;border:none;font-size:20px;cursor:pointer;color:var(--text);}}
}}
.search-hide{{display:none!important;}}
mark{{background:#fde047;color:#1e293b;border-radius:2px;}}
</style>
</head>
<body>
<div class="progress-bar" id="progressBar"></div>
<button id="menu-btn">☰ 目录</button>
<div class="sidebar" id="sidebar">
<h3>{sidebar_title} <button class="theme-toggle" id="theme-btn">🌙</button></h3>
<input type="text" class="search-box" id="searchBox" placeholder="🔍 搜索考点...">
<button id="menu-close">✕</button>
<div id="toc"></div>
</div>
<div class="content-wrapper">
<div class="content">
<div id="markdown-content"><p>正在渲染内容,请稍候...</p></div>
</div>
</div>
<a href="#" class="float-btn" id="totop" title="回到顶部">↑</a>
<script id="raw-markdown" type="text/markdown">
{markdown}
</script>
<script>
var md=document.getElementById('raw-markdown').textContent;
var html=marked.parse(md);
// 把 <details> 内部包一层 div,便于样式
document.getElementById('markdown-content').innerHTML=html;
var htmlEl=document.documentElement;
var savedTheme=localStorage.getItem('rk-theme');
if(savedTheme){{htmlEl.setAttribute('data-theme',savedTheme);document.getElementById('theme-btn').textContent=savedTheme==='dark'?'☀️':'🌙';}}
document.getElementById('theme-btn').addEventListener('click',function(){{
var currentTheme=htmlEl.getAttribute('data-theme');
var newTheme=currentTheme==='dark'?'light':'dark';
htmlEl.setAttribute('data-theme',newTheme);
this.textContent=newTheme==='dark'?'☀️':'🌙';
localStorage.setItem('rk-theme',newTheme);
}});
var toc=document.getElementById('toc');
var headers=document.querySelectorAll('.content h1, .content h2, .content h3');
headers.forEach(function(h){{
if(!h.id){{h.id='h-'+Math.random().toString(36).substr(2,9);}}
var level=parseInt(h.tagName[1]);
var cls=level===2?'h2':(level===3?'h3':'');
var a=document.createElement('a');
a.href='#'+h.id;
a.textContent=h.textContent;
a.className=cls+' rk-toc-link';
a.dataset.target=h.id;
toc.appendChild(a);
}});
document.getElementById('menu-btn').addEventListener('click',function(){{
document.getElementById('sidebar').classList.toggle('open');
}});
document.getElementById('menu-close').addEventListener('click',function(){{
document.getElementById('sidebar').classList.remove('open');
}});
document.addEventListener('click',function(e){{
var sidebar=document.getElementById('sidebar');
if(window.innerWidth<=900&&!sidebar.contains(e.target)&&e.target.id!=='menu-btn'){{
sidebar.classList.remove('open');
}}
if(e.target.classList.contains('rk-toc-link')){{
if(window.innerWidth<=900){{sidebar.classList.remove('open');}}
}}
}});
var tocLinks=document.querySelectorAll('.rk-toc-link');
function updateActiveToc(){{
var scrollPos=window.scrollY+100;
var current=null;
headers.forEach(function(h){{
if(h.offsetTop<=scrollPos){{current=h;}}
}});
if(current){{
tocLinks.forEach(function(l){{l.classList.remove('active');}});
var activeLink=document.querySelector('.rk-toc-link[data-target="'+current.id+'"]');
if(activeLink){{activeLink.classList.add('active');}}
}}
}}
window.addEventListener('scroll',function(){{
var scrollTop=window.scrollY;
var docHeight=document.documentElement.scrollHeight-window.innerHeight;
var percent=Math.min(100,(scrollTop/docHeight)*100);
document.getElementById('progressBar').style.width=percent+'%';
updateActiveToc();
}});
document.getElementById('totop').addEventListener('click',function(e){{
e.preventDefault();window.scrollTo({{top:0,behavior:'smooth'}});
}});
var searchBox=document.getElementById('searchBox');
searchBox.addEventListener('input',function(){{
var q=this.value.trim().toLowerCase();
var blocks=document.querySelectorAll('#markdown-content > *');
if(!q){{
blocks.forEach(function(b){{b.classList.remove('search-hide');}});
return;
}}
blocks.forEach(function(b){{
var text=b.textContent.toLowerCase();
if(text.indexOf(q)>=0){{b.classList.remove('search-hide');}}
else{{b.classList.add('search-hide');}}
}});
}});
</script>
</body>
</html>
"""

BASE_DIR = r"f:\软设笔记\考前冲刺三件套"

FILES = [
    {
        "md": "1_高频考点统计(2021-2024).md",
        "html": "1_高频考点统计_可视化.html",
        "title": "高频考点统计(2021-2024) - 软考软件设计师",
        "sidebar_title": "📊 高频统计",
    },
    {
        "md": "2_专项练习题集.md",
        "html": "2_专项练习题集_可视化.html",
        "title": "专项练习题集 - 软考软件设计师",
        "sidebar_title": "✏️ 专项练习",
    },
    {
        "md": "3_考前3天速记单页.md",
        "html": "3_考前3天速记单页_可视化.html",
        "title": "考前3天速记单页 - 软考软件设计师",
        "sidebar_title": "⚡ 考前速记",
    },
]

for f in FILES:
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
    print(f"OK {f['html']} ({size} bytes)")

print("---")
print("三件套 HTML 生成完成")
