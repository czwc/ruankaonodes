# -*- coding: utf-8 -*-
"""给总复习 md 加模块隔离横幅 + 🔺必考标记（幂等，可重复跑）"""
import re
from pathlib import Path

P = Path(r"f:\软设笔记\上午题全知识点总复习.md")
text = P.read_text(encoding="utf-8")

BANNERS = {
    "一": ("5~6", "★★"), "二": ("6", "★★"), "三": ("9", "★★★"),
    "四": ("6", "★★★"), "五": ("6", "★★★"), "六": ("5", "★★"),
    "七": ("13", "★★★"), "八": ("3~4", "★★★"), "九": ("2", "★"),
    "十": ("2", "★"), "十一": ("2~3", "★"), "十二": ("5", "★（考前专项）"),
    "十三": ("偶考", "★"),
}

lines = text.split("\n")
out = []
for ln in lines:
    m = re.match(r"^# 模块([一二三四五六七八九十]+) ", ln)
    if m:
        name = m.group(1)
        if f"模块 {name} 开始" not in text:  # 幂等
            score, stars = BANNERS.get(name, ("?", ""))
            out.append(ln)
            out.append("")
            out.append(f"> 🔺 ━━━ **模块 {name} 开始** ｜ 真题均分 {score} 分 ｜ 必考指数 {stars} ━━━")
            out.append("")
            continue
    out.append(ln)
text = "\n".join(out)

# 🔺 必考点标记（子串唯一匹配；表格行在行首 "| " 后插入）
KEYS = [
    "公式：平均 = h×tc", "Δt（节拍）= 各段", "2ᵏ ≥ n+k+1", "中断向量 = 中断服务程序的入口地址",
    "四种 I/O 方式", "PCI = 并行内总线", "映像方式**（Day5",
    "语法定 2 型", "闭包（0 次或多次", "list 可变有序可重复",
    "n₀ = n₂ + 1", "元素个数 = (rear−front+M)", "新结点放回队列继续参与比较", "DFS 一条道走到黑",
    "Prim 加点", "最短路径 Dijkstra", "ASL(成功)", "快些选堆不稳定", "先接后断",
    "P(S)：S−1", "互斥、请求保持、不可剥夺、循环等待", "一拆二换三拼回", "FIFO 排队走",
    "剩余找", "外菜单内仓库", "变什么，就叫什么独立性", "矩实椭属菱联系",
    "1:1 → 任一方加对方主键", "σ 选行", "执行顺序 FROM 最先", "BCNF：所有决定方",
    "应表会传网数物", "借 n 位分 2ⁿ 网", "TCP 打电话可靠", "协议层次归属",
    "原型** | **需求说不清", "内聚从低到高", "语句→判定→条件", "McCabe 环路复杂度",
    "最长路径定工期", "风险暴露 = 风险概率", "初始混乱可重复",
    "依→关→聚→组", "静类部构署", "创建管生", "收公加密（保密）",
    "图像容量(B)", "颜色数 = 2^位深", "采样频率 ≥ 2×",
    "著自动、专商请", "用公司资源、公司安排开发", "委托开发：无约定", "GB 强制、GB/T 推荐",
]

marked = 0
for k in KEYS:
    # 找包含子串的行，行首加 🔺（表格行加在 "| " 后）
    idx = next((i for i, ln in enumerate(out) if k in ln and not ln.startswith("> 🔺")), None)
    if idx is None:
        print(f"WARN 未找到: {k}")
        continue
    if "🔺" in out[idx]:
        continue
    ln = out[idx]
    out[idx] = "| 🔺" + ln[1:] if ln.startswith("| ") else "🔺 " + ln
    marked += 1

P.write_text(text, encoding="utf-8")
print(f"banners ok, marked {marked}/{len(KEYS)} key lines")
