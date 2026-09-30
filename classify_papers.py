# -*- coding: utf-8 -*-
"""把 6 套上午真题按模块分类整合为题库 md（子代理已完成题号→模块映射，本脚本负责切题落盘）"""
import re
from pathlib import Path

SRC = Path(r"f:\软设笔记\2021-2024历年真题及解析\_提取文本")
OUT = Path(r"f:\软设笔记\上午真题分类题库(2021-2024).md")

MODULES = ["一、计算机组成与体系结构", "二、操作系统", "三、数据库", "四、数据结构与算法",
           "五、程序设计语言（含 Python）", "六、计算机网络", "七、软件工程",
           "八、面向对象与设计模式", "九、多媒体", "十、信息安全",
           "十一、知识产权与标准化", "十二、专业英语", "十三、其他"]

# 各卷映射：模块序号 -> [(起始题号, 结束题号), ...]
MAPS = {
    "2021.05": ("2021年05月软件设计师上午真题及答案解析.txt",
                {0: [(1, 6)], 9: [(7, 11)], 10: [(12, 14)], 6: [(15, 19), (29, 36)],
                 4: [(20, 22), (48, 50)], 1: [(24, 28)], 7: [(37, 47)], 2: [(51, 56)],
                 3: [(57, 65)], 5: [(66, 70)], 11: [(71, 75)], 12: [(23, 23)]}),
    "2021.11": ("2021年11月软件设计师上午真题+答案解析.txt",
                {0: [(1, 6)], 9: [(7, 11)], 10: [(12, 14)], 6: [(15, 19), (29, 36)],
                 3: [(20, 20), (57, 65)], 1: [(23, 28)], 7: [(37, 47)],
                 4: [(21, 22), (48, 50)], 2: [(51, 56)], 5: [(66, 70)], 11: [(71, 75)]}),
    "2022.05": ("2022年05月软件设计师上午真题及答案解析.txt",
                {0: [(1, 6)], 9: [(7, 11)], 10: [(12, 13)], 6: [(14, 15)], 7: [(16, 19)],
                 4: [(20, 22)], 2: [(23, 25)], 3: [(26, 30)], 5: [(31, 34)]}),
    "2022.11": ("2022年11月软件设计师上午真题及答案解析.txt",
                {0: [(1, 6)], 9: [(7, 11)], 10: [(12, 14)], 6: [(15, 19), (29, 36)],
                 4: [(20, 22), (48, 50)], 1: [(23, 28)], 7: [(37, 47)], 2: [(51, 56)],
                 3: [(57, 65)], 5: [(66, 70)], 11: [(71, 75)]}),
    "2023.05": ("2023年上半年软件设计师上午真题及答案解析.txt",
                {0: [(1, 6)], 5: [(7, 7)], 9: [(8, 11)], 10: [(12, 14)],
                 6: [(15, 19), (29, 36), (39, 39)], 4: [(20, 22), (48, 50)],
                 1: [(23, 28)], 7: [(37, 38), (40, 47)], 2: [(51, 56)],
                 3: [(57, 65)], 5: [(66, 70)], 11: [(71, 75)]}),
    "2024.05": ("2024年上半年软件设计师综合知识（空白试卷）.txt",
                {0: [(1, 6), (9, 9)], 9: [(7, 8), (48, 49)], 4: [(10, 15)],
                 3: [(16, 22)], 1: [(23, 26)], 6: [(27, 37), (40, 40)],
                 7: [(38, 39), (41, 42)], 2: [(43, 47)], 5: [(50, 55)],
                 10: [(56, 58)], 12: [(59, 70)], 11: [(71, 75)]}),
}

ADS = ["手机端题库", "内部资料", "禁止传播", "希赛网", "客服热线", "软考达人",
       "ruankaodaren", "富国", "淘宝", "QQ", "专业的在线教育平台", "微信搜索"]
EXACT_AD = {"搜索", "考达", "微信搜索", "软考达人－高效提分的软考题库"}

QSTART = re.compile(r"^[\(（]?(\d{1,2})[\)）]?(?:\s*[、．.，])?\s*\S")
GROUP = re.compile(r"^(\d{1,2})\s*[-—–]\s*(\d{1,2})\s*题")
INLINE = re.compile(r"[（(](\d{1,2})[）)](?!\d)|[（(](\d{1,2})$")   # 2024 卷：题号嵌在题干中/行尾无右括号

def is_ad(line):
    s = line.strip()
    return (any(a in line for a in ADS) or s in EXACT_AD
            or re.match(r"^\d+\s*/\s*\d+\s*$", s) or re.match(r"^\d{1,3}\s*/?\s*$", s)
            or not s)

def module_of(mapping, q):
    for idx, ranges in mapping.items():
        for a, b in ranges:
            if a <= q <= b:
                return idx
    return None

def parse_paper(path, tag, mapping, cut_at_answer=False, inline_qnum=False):
    lines = Path(path).read_text(encoding="utf-8").split("\n")
    blocks = {}   # qnum -> [lines]
    order = []
    cur_q, cur_lines = None, None
    for line in lines:
        if is_ad(line):
            continue
        if "=====" in line:
            continue
        if cut_at_answer and "参考答案" in line:
            cur_q, cur_lines = None, None
            continue
        if inline_qnum:
            m_i = INLINE.search(line)
            m_f = None if m_i else re.search(r"(\d{1,2})）\s*$", line)
            if m_i or m_f:
                raw = m_i.group(1) or m_i.group(2) if m_i else m_f.group(1)
                q = int(raw)
                mod = module_of(mapping, q)
                if mod is None or q in blocks:
                    cur_q, cur_lines = None, None
                    continue
                cur_q, cur_lines = q, [line]
                blocks[q] = cur_lines
                order.append(q)
                continue
            if cur_q is not None:
                cur_lines.append(line)
            continue
        m_q = QSTART.match(line)
        m_g = GROUP.match(line)
        if m_q or m_g:
            q = int(m_g.group(1)) if m_g else int(m_q.group(1))
            mod = module_of(mapping, q)
            if mod is None:
                cur_q, cur_lines = None, None   # 答案解析区的"伪题号"直接丢弃
                continue
            if cur_q is not None and cur_q in blocks:
                blocks[cur_q].extend(cur_lines)
            cur_q, cur_lines = q, [line]
            if q not in blocks:
                blocks[q] = cur_lines
                order.append(q)
            continue
        if cur_q is not None:
            cur_lines.append(line)
    if cur_q is not None and cur_q in blocks:
        blocks[cur_q].extend(cur_lines)
    result = {}
    for q in order:
        body = "\n".join(l for l in blocks[q]).strip()
        if body:
            result[q] = body
    return result

def main():
    banks = {i: [] for i in range(13)}
    stats = {}
    total = 0
    for tag, (fname, mapping) in MAPS.items():
        inline = (tag == "2024.05")
        qs = parse_paper(SRC / fname, tag, mapping, cut_at_answer=(tag == "2023.05"), inline_qnum=inline)
        # 缺号诊断：映射范围内的题号哪些没有解析出块
        expected = sorted({q for ranges in mapping.values() for a, b in ranges for q in range(a, b + 1)})
        missing = [q for q in expected if q not in qs]
        if missing:
            print(f"{tag}: 缺块题号 {missing}")
        year = tag.split(".")[0]
        month = tag.split(".")[1]
        stats[tag] = {}
        for mod in range(13):
            got = []
            for q in sorted(qs):
                if module_of(mapping, q) == mod:
                    got.append((year, month, q, qs[q]))
            banks[mod].extend(got)
            stats[tag][mod] = len(got)
        total += len(qs)
        print(f"{tag}: 解析出 {len(qs)} 题")

    out = ["# 上午真题分类题库（2021~2024，6 套卷按模块整合）",
           "",
           "> 来源：2021.05 / 2021.11 / 2022.05 / 2022.11 / 2023.05 / 2024.05 六套上午卷。",
           "> 按模块重组，方便按专题刷题；题干选项为原文（OCR 卷可能有少量识别噪声，已标〔提取不清〕或保留原样）。",
           "> 已知缺陷：2021.11 第 8 题原卷题干缺失；2022.05 原文件只有 1~34 题；2024 第 59~70 题两份源文件均无题干、第 20/74/75 题 OCR 题号丢失（这三题请对照原 PDF），第 17 题题号残缺已尽力恢复。",
           "> 配套：知识点讲解见《上午题全知识点总复习_可视化.html》。", "",
           "## 各模块题量分布", ""]
    hdr = "| 模块 | " + " | ".join(MAPS.keys()) + " | 合计 |"
    out.append(hdr)
    out.append("|---|" + "---|" * (len(MAPS) + 1))
    for mod in range(13):
        row = [str(len([q for q in banks[mod] if q[0] == y and q[1] == m])) for y, m in
               [(t.split(".")[0], t.split(".")[1]) for t in MAPS]]
        name = MODULES[mod].split("、")[0] + "、" + MODULES[mod].split("、")[1] if "、" in MODULES[mod] else MODULES[mod]
        out.append(f"| {MODULES[mod]} | " + " | ".join(row) + f" | {len(banks[mod])} |")
    out.append("")
    for mod in range(13):
        if not banks[mod]:
            continue
        out.append(f"# {MODULES[mod]}")
        out.append("")
        for year, month, q, body in banks[mod]:
            out.append(f"**【{year}.{month} · 第{q}题】**")
            out.append("")
            out.append(body)
            out.append("")
        out.append("---")
        out.append("")
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"TOTAL {total} 题 -> {OUT} ({len(OUT.read_text(encoding='utf-8'))} chars)")

if __name__ == "__main__":
    main()
