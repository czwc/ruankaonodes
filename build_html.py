import os

template = '''<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <!-- Marked.js -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <!-- Prism.js -->
    <link href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        :root[data-theme="light"] {
            --bg-color: #ffffff;
            --text-color: #334155;
            --sidebar-bg: #f8fafc;
            --border-color: #e2e8f0;
            --accent-color: #3b82f6;
            --heading-color: #0f172a;
            --code-bg: #f1f5f9;
            --quote-bg: #f8fafc;
            --quote-border: #3b82f6;
            --table-header: #f1f5f9;
        }
        :root[data-theme="dark"] {
            --bg-color: #0f172a;
            --text-color: #cbd5e1;
            --sidebar-bg: #1e293b;
            --border-color: #334155;
            --accent-color: #60a5fa;
            --heading-color: #f8fafc;
            --code-bg: #1e293b;
            --quote-bg: #1e293b;
            --quote-border: #60a5fa;
            --table-header: #1e293b;
        }
        
        body {
            margin: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            display: flex;
            transition: background-color 0.3s, color 0.3s;
            line-height: 1.8;
            font-size: 16px;
        }
        
        /* Sidebar */
        .sidebar {
            width: 320px;
            height: 100vh;
            overflow-y: auto;
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--border-color);
            position: fixed;
            padding: 30px 20px;
            box-sizing: border-box;
            transition: background-color 0.3s, border-color 0.3s, transform 0.3s;
            z-index: 50;
        }
        
        .sidebar::-webkit-scrollbar { width: 6px; }
        .sidebar::-webkit-scrollbar-thumb { background: #94a3b8; border-radius: 3px; }
        
        .sidebar h3 {
            margin-top: 0;
            color: var(--heading-color);
            font-size: 1.2rem;
            padding-bottom: 15px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .theme-toggle {
            background: none;
            border: none;
            cursor: pointer;
            font-size: 1.2rem;
            color: var(--text-color);
            padding: 5px;
            border-radius: 5px;
            transition: background 0.2s;
        }
        .theme-toggle:hover { background: rgba(128,128,128,0.1); }
        
        .sidebar a {
            display: block;
            text-decoration: none;
            color: var(--text-color);
            margin-bottom: 8px;
            font-size: 14px;
            transition: color 0.2s, padding-left 0.2s;
            opacity: 0.8;
            line-height: 1.5;
            padding: 4px 0;
            border-radius: 4px;
        }
        .sidebar a:hover, .sidebar a.active {
            color: var(--accent-color);
            opacity: 1;
            padding-left: 10px;
            background: rgba(59, 130, 246, 0.05);
        }
        
        .toc-h1 { font-weight: 600; margin-top: 15px; font-size: 15px !important; color: var(--heading-color) !important; }
        .toc-h2 { margin-left: 15px; font-weight: 500; }
        .toc-h3 { margin-left: 30px; font-size: 13px !important; }
        .toc-h4 { margin-left: 45px; font-size: 13px !important; opacity: 0.7; }
        
        /* Content */
        .content-wrapper {
            margin-left: 320px;
            width: calc(100% - 320px);
            display: flex;
            justify-content: center;
            min-height: 100vh;
        }
        
        .content {
            padding: 60px 50px;
            max-width: 850px;
            width: 100%;
        }
        
        h1, h2, h3, h4, h5 {
            color: var(--heading-color);
            margin-top: 2em;
            margin-bottom: 0.8em;
            font-weight: 600;
            line-height: 1.3;
        }
        
        h1 { font-size: 2.5rem; border-bottom: 2px solid var(--accent-color); padding-bottom: 10px; margin-top: 0; display: inline-block; }
        h2 { font-size: 1.8rem; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }
        h3 { font-size: 1.4rem; }
        
        p { margin-bottom: 1.2em; }
        
        img {
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            margin: 25px auto;
            display: block;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 25px 0;
            font-size: 0.95rem;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 0 0 1px var(--border-color);
        }
        
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }
        
        th {
            background-color: var(--table-header);
            font-weight: 600;
            color: var(--heading-color);
        }
        
        blockquote {
            border-left: 4px solid var(--quote-border);
            margin: 25px 0;
            padding: 15px 20px;
            background-color: var(--quote-bg);
            border-radius: 0 8px 8px 0;
            font-style: italic;
        }
        
        blockquote p { margin: 0; }
        
        pre {
            border-radius: 8px !important;
            margin: 20px 0 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        
        code {
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            background-color: var(--code-bg);
            padding: 3px 6px;
            border-radius: 4px;
            font-size: 0.9em;
            color: var(--accent-color);
        }
        pre code { background-color: transparent; padding: 0; color: inherit; font-size: 0.85em; }
        
        hr {
            border: 0;
            height: 1px;
            background: var(--border-color);
            margin: 40px 0;
        }
        
        /* Highlight specific markdown features (bold, italics) */
        strong { 
            color: var(--heading-color); 
            font-weight: 600; 
            background: linear-gradient(transparent 50%, rgba(253, 224, 71, 0.6) 50%);
            padding: 0 4px;
            border-radius: 2px;
        }
        
        :root[data-theme="dark"] strong {
            background: linear-gradient(transparent 50%, rgba(234, 179, 8, 0.4) 50%);
            color: #fef08a;
        }

        /* 重点符号高亮 */
        .highlight-icon {
            color: #ef4444;
            font-weight: bold;
            animation: pulse 2s infinite;
            display: inline-block;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        
        /* Floating To Top */
        #totop {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: var(--accent-color);
            color: white;
            width: 45px;
            height: 45px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            opacity: 0;
            transition: opacity 0.3s, transform 0.3s;
            text-decoration: none;
            font-size: 20px;
            z-index: 100;
        }
        #totop:hover { transform: translateY(-3px); }
        #totop.visible { opacity: 1; }
        
        /* Header nav */
        .top-nav {
            margin-bottom: 30px;
            display: flex;
            gap: 15px;
        }
        .top-nav a {
            color: var(--text-color);
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 20px;
            background: var(--sidebar-bg);
            border: 1px solid var(--border-color);
            font-size: 14px;
            transition: all 0.2s;
        }
        .top-nav a:hover, .top-nav a.active-nav {
            background: var(--accent-color);
            color: white;
            border-color: var(--accent-color);
        }

        @media (max-width: 900px) {
            .sidebar { transform: translateX(-100%); }
            .sidebar.open { transform: translateX(0); box-shadow: 4px 0 20px rgba(0,0,0,0.1); }
            .content-wrapper { margin-left: 0; width: 100%; }
            .content { padding: 80px 30px 40px; }
            #menu-btn { display: flex; }
        }
        
        #menu-btn {
            display: none;
            position: fixed;
            top: 15px;
            left: 15px;
            z-index: 101;
            background: var(--bg-color);
            border: 1px solid var(--border-color);
            padding: 8px 12px;
            border-radius: 6px;
            cursor: pointer;
            color: var(--text-color);
            align-items: center;
            gap: 6px;
            font-weight: 500;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
    </style>
</head>
<body>
    <button id="menu-btn">☰ 目录</button>
    
    <div class="sidebar" id="sidebar">
        <h3>目录 <button class="theme-toggle" id="theme-btn" title="切换主题">🌙</button></h3>
        <div id="toc"></div>
    </div>
    
    <div class="content-wrapper">
        <div class="content">
            <div class="top-nav">
                <a href="../1%20图像笔记一/软件设计师讲义_可视化.html" class="{nav1_active}">📔 软件设计师讲义 (详细版)</a>
                <a href="../2%20图像笔记二/软考-软件设计师-笔记_可视化.html" class="{nav2_active}">📝 软件设计师笔记 (速查版)</a>
                <a href="../软考突击冲刺宝典_可视化.html" class="{nav3_active}">🔥 考前冲刺宝典 (必看)</a>
            </div>
            <div id="markdown-content">
                <p>正在渲染内容，请稍候...</p>
            </div>
        </div>
    </div>
    
    <a href="#" id="totop">↑</a>

    <!-- Raw Markdown Data -->
    <script id="raw-markdown" type="text/markdown">
{markdown_content}
    </script>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            // Theme setup
            const themeBtn = document.getElementById('theme-btn');
            const html = document.documentElement;
            
            const savedTheme = localStorage.getItem('theme') || 'light';
            html.setAttribute('data-theme', savedTheme);
            themeBtn.textContent = savedTheme === 'light' ? '🌙' : '☀️';
            
            themeBtn.addEventListener('click', () => {
                const currentTheme = html.getAttribute('data-theme');
                const newTheme = currentTheme === 'light' ? 'dark' : 'light';
                html.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
                themeBtn.textContent = newTheme === 'light' ? '🌙' : '☀️';
            });

            // Mobile menu
            const menuBtn = document.getElementById('menu-btn');
            const sidebar = document.getElementById('sidebar');
            menuBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                sidebar.classList.toggle('open');
            });
            document.addEventListener('click', (e) => {
                if (window.innerWidth <= 900 && !sidebar.contains(e.target) && e.target !== menuBtn) {
                    sidebar.classList.remove('open');
                }
            });

            // Parse markdown
            let rawMd = document.getElementById('raw-markdown').textContent;
            
            const contentDiv = document.getElementById('markdown-content');
            contentDiv.innerHTML = marked.parse(rawMd);
            
            // Syntax highlighting
            if (window.Prism) {
                Prism.highlightAll();
            }

            // Generate TOC
            const tocDiv = document.getElementById('toc');
            const headers = contentDiv.querySelectorAll('h1, h2, h3, h4');
            
            // Highlight specific markers
            const walker = document.createTreeWalker(contentDiv, NodeFilter.SHOW_TEXT, null, false);
            const textNodes = [];
            let node;
            while (node = walker.nextNode()) {
                textNodes.push(node);
            }
            textNodes.forEach(textNode => {
                if (textNode.nodeValue.includes('🔺') || textNode.nodeValue.includes('重点')) {
                    const span = document.createElement('span');
                    span.innerHTML = textNode.nodeValue
                        .replace(/🔺/g, '<span class="highlight-icon">🔺</span>')
                        .replace(/重点/g, '<span style="color: #ef4444; font-weight: bold; border-bottom: 2px dashed #ef4444;">重点</span>');
                    textNode.parentNode.replaceChild(span, textNode);
                }
            });
            
            headers.forEach((h, index) => {
                const id = 'heading-' + index;
                h.id = id;
                const a = document.createElement('a');
                a.href = '#' + id;
                a.textContent = h.textContent;
                a.className = 'toc-' + h.tagName.toLowerCase();
                
                a.addEventListener('click', (e) => {
                    if (window.innerWidth <= 900) {
                        sidebar.classList.remove('open');
                    }
                });
                
                tocDiv.appendChild(a);
            });

            // Scroll to top button
            const toTop = document.getElementById('totop');
            window.addEventListener('scroll', () => {
                if (window.scrollY > 300) {
                    toTop.classList.add('visible');
                } else {
                    toTop.classList.remove('visible');
                }
            });
            
            // Active TOC highlighting
            const tocLinks = document.querySelectorAll('#toc a');
            window.addEventListener('scroll', () => {
                let current = '';
                // Add a small offset to highlight early
                const offset = 100;
                headers.forEach(h => {
                    const top = h.offsetTop;
                    if (scrollY >= top - offset) {
                        current = h.getAttribute('id');
                    }
                });
                
                tocLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + current) {
                        link.classList.add('active');
                    }
                });
            });
            
        });
    </script>
</body>
</html>
'''

def build_html(md_path, html_path, title, active_index):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Escape </script> to avoid breaking the HTML template
    md_content = md_content.replace('</script>', '<\/script>')
    
    nav1_active = 'active-nav' if active_index == 1 else ''
    nav2_active = 'active-nav' if active_index == 2 else ''
    nav3_active = 'active-nav' if active_index == 3 else ''
    
    html = template.replace('{title}', title)\
                   .replace('{markdown_content}', md_content)\
                   .replace('{nav1_active}', nav1_active)\
                   .replace('{nav2_active}', nav2_active)\
                   .replace('{nav3_active}', nav3_active)
                   
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Successfully built {html_path}")

build_html(
    r'f:/软设笔记/1 图像笔记一/软件设计师讲义.md',
    r'f:/软设笔记/1 图像笔记一/软件设计师讲义_可视化.html',
    '软件设计师讲义 (详细版) - 学习平台',
    1
)

build_html(
    r'f:/软设笔记/2 图像笔记二/软考-软件设计师-笔记.md',
    r'f:/软设笔记/2 图像笔记二/软考-软件设计师-笔记_可视化.html',
    '软件设计师笔记 (速查版) - 学习平台',
    2
)

build_html(
    r'f:/软设笔记/软考突击冲刺宝典.md',
    r'f:/软设笔记/软考突击冲刺宝典_可视化.html',
    '软考突击冲刺宝典 - 考前必看',
    3
)
