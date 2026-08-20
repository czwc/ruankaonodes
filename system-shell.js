(() => {
  'use strict';

  const MODULES = [
    ['core', '必考考点全攻略', '软考必考考点_可视化.html'],
    ['detail', '软件设计师详细讲义', '1 图像笔记一/软件设计师讲义_可视化.html'],
    ['tricolor', '三色笔记阅读器', '三色笔记阅读器.html'],
    ['notes', '图文笔记速查', '2 图像笔记二/软考-软件设计师-笔记_可视化.html'],
    ['bank', '分类题库标准版', '分类题库/分类题库_标准版_可视化.html'],
    ['drill', '专项练习题集', '考前冲刺三件套/2_专项练习题集_可视化.html'],
    ['formula', '高频公式可视化', '软件设计师高频公式可视化.html'],
    ['code', '代码题与设计模式', '软考代码题全攻略_可视化.html'],
    ['disk', '磁盘调度从零到会', '重点专题/磁盘调度算法_小白从零到会_可视化.html'],
    ['english', '专业英语每日背', '专业英语背诵.html'],
    ['sprintbook', '突击冲刺宝典', '软考突击冲刺宝典_可视化.html'],
    ['frequency', '高频考点统计', '考前冲刺三件套/1_高频考点统计_可视化.html'],
    ['three', '考前 3 天速记', '考前冲刺三件套/3_考前3天速记单页_可视化.html']
  ];
  const VISITS_KEY = 'ruankao_system_visits_v1';
  const currentScript = document.currentScript;
  const rootUrl = currentScript ? new URL('./', currentScript.src) : new URL('./', location.href);
  const normalizedPath = decodeURIComponent(location.pathname).replace(/\\/g, '/');
  const currentIndex = MODULES.findIndex(([, , path]) => normalizedPath.endsWith('/' + path) || normalizedPath.endsWith(path));
  const current = currentIndex >= 0 ? MODULES[currentIndex] : null;

  if (current) {
    try {
      const visits = JSON.parse(localStorage.getItem(VISITS_KEY) || '{}');
      visits[current[0]] = { time: Date.now(), href: current[2], title: current[1] };
      localStorage.setItem(VISITS_KEY, JSON.stringify(visits));
    } catch (_) {}
  }

  const style = document.createElement('style');
  style.textContent = `
    .study-shell{position:fixed;right:18px;bottom:18px;z-index:2147483000;font-family:"Microsoft YaHei UI","PingFang SC",sans-serif;color:#17212b}
    .study-shell button,.study-shell a{font:inherit}
    .study-shell-toggle{height:42px;padding:0 15px;border:1px solid #087f5b;border-radius:6px;background:#087f5b;color:#fff;font-size:13px;font-weight:700;box-shadow:0 8px 24px rgba(23,33,43,.2);cursor:pointer}
    .study-shell-panel{position:absolute;right:0;bottom:50px;width:min(330px,calc(100vw - 28px));display:none;background:#fff;border:1px solid #d9e0e5;border-radius:8px;box-shadow:0 18px 50px rgba(23,33,43,.22);overflow:hidden;text-align:left}
    .study-shell.open .study-shell-panel{display:block}
    .study-shell-head{padding:14px 16px;border-bottom:1px solid #d9e0e5;background:#f5f7f9}
    .study-shell-head strong{display:block;font-size:14px;color:#17212b}.study-shell-head span{display:block;margin-top:2px;font-size:11px;color:#61707d}
    .study-shell-home{display:flex;align-items:center;justify-content:space-between;padding:11px 16px;color:#087f5b!important;text-decoration:none!important;font-size:13px;font-weight:800;border-bottom:1px solid #d9e0e5}
    .study-shell-list{max-height:280px;overflow:auto;padding:6px}
    .study-shell-link{display:block;padding:8px 10px;border-radius:5px;color:#465560!important;text-decoration:none!important;font-size:12px;line-height:1.4}
    .study-shell-link:hover{background:#eef2f5;color:#087f5b!important}.study-shell-link.current{background:#e6f4ef;color:#087f5b!important;font-weight:800}
    .study-shell-nav{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid #d9e0e5}.study-shell-nav a{padding:10px;color:#465560!important;text-decoration:none!important;text-align:center;font-size:12px}.study-shell-nav a+a{border-left:1px solid #d9e0e5}.study-shell-nav a[aria-disabled="true"]{color:#aab4bc!important;pointer-events:none}
    @media(max-width:600px){.study-shell{right:12px;bottom:12px}.study-shell-toggle{height:40px}.study-shell-panel{bottom:48px}}
    @media print{.study-shell{display:none!important}}
  `;
  document.head.appendChild(style);

  const shell = document.createElement('div');
  shell.className = 'study-shell';
  const links = MODULES.map(([id, title, path], index) => {
    const isCurrent = index === currentIndex;
    return `<a class="study-shell-link${isCurrent ? ' current' : ''}" href="${new URL(path, rootUrl).href}"${isCurrent ? ' aria-current="page"' : ''}>${String(index + 1).padStart(2, '0')}　${title}</a>`;
  }).join('');
  const prev = currentIndex > 0 ? MODULES[currentIndex - 1] : null;
  const next = currentIndex >= 0 && currentIndex < MODULES.length - 1 ? MODULES[currentIndex + 1] : null;
  shell.innerHTML = `
    <div class="study-shell-panel" id="studyShellPanel">
      <div class="study-shell-head"><strong>软考软件设计师</strong><span>${current ? '当前：' + current[1] : '统一学习导航'}</span></div>
      <a class="study-shell-home" href="${new URL('index.html', rootUrl).href}"><span>返回学习系统首页</span><span>→</span></a>
      <nav class="study-shell-list" aria-label="学习模块快速导航">${links}</nav>
      <div class="study-shell-nav">
        <a href="${prev ? new URL(prev[2], rootUrl).href : '#'}" aria-disabled="${!prev}">← 上一模块</a>
        <a href="${next ? new URL(next[2], rootUrl).href : '#'}" aria-disabled="${!next}">下一模块 →</a>
      </div>
    </div>
    <button class="study-shell-toggle" type="button" aria-expanded="false" aria-controls="studyShellPanel">学习系统</button>
  `;
  document.body.appendChild(shell);

  const toggle = shell.querySelector('.study-shell-toggle');
  const close = () => {
    shell.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
  };
  toggle.addEventListener('click', () => {
    const open = shell.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('click', event => {
    if (!shell.contains(event.target)) close();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') close();
  });
})();
