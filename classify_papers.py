# -*- coding: utf-8 -*-
"""把 6 套上午真题按模块分类整合为题库 md
v3：每题引用卡片框 + <details> 折叠答案解析；修复块重复与答案区污染"""
import re
from pathlib import Path

SRC = Path(r"f:\软设笔记\2021-2024历年真题及解析\_提取文本")
OUT = Path(r"f:\软设笔记\上午真题分类题库(2021-2024).md")

MODULES = ["一、计算机组成与体系结构", "二、操作系统", "三、数据库", "四、数据结构与算法",
           "五、程序设计语言（含 Python）", "六、计算机网络", "七、软件工程",
           "八、面向对象与设计模式", "九、多媒体", "十、信息安全",
           "十一、知识产权与标准化", "十二、专业英语", "十三、其他"]

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

ANSWER_MARKERS = {"2022.05": "答案：", "2023.05": "参考答案"}
STOP_MARK = "答案解析"

ADS = ["手机端题库", "内部资料", "禁止传播", "希赛网", "客服热线", "软考达人",
       "ruankaodaren", "富国", "淘宝", "QQ", "专业的在线教育平台", "微信搜索"]
EXACT_AD = {"搜索", "考达", "微信搜索", "软考达人－高效提分的软考题库"}

QSTART = re.compile(r"^[\(（]?(\d{1,2})[\)）]?(?:\s*[、．.，])?\s*\S")
GROUP = re.compile(r"^(\d{1,2})\s*[-—–]\s*(\d{1,2})\s*题")
INLINE = re.compile(r"[（(](\d{1,2})[）)](?!\d)|[（(](\d{1,2})$")

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

def parse_paper(path, mapping, inline_qnum=False, ans_marker=None):
    """返回 {q: (题干行列表, 答案行列表或None)}；块列表与 blocks 字典不再共享引用"""
    lines = Path(path).read_text(encoding="utf-8").split("\n")
    blocks = {}
    order = []
    cur_q, cur_lines = None, None

    def finalize():
        nonlocal cur_q, cur_lines
        if cur_q is not None and cur_q not in blocks:
            blocks[cur_q] = cur_lines
            order.append(cur_q)
        cur_q, cur_lines = None, None

    for line in lines:
        if is_ad(line) or "=====" in line:
            continue
        if STOP_MARK in line and len(order) >= 40:   # 卷尾答案解析区，停止
            finalize()
            break
        started = False
        if inline_qnum:
            m_i = INLINE.search(line)
            m_f = None if m_i else re.search(r"(\d{1,2})）\s*$", line)
            if m_i or m_f:
                q = int((m_i.group(1) or m_i.group(2)) if m_i else m_f.group(1))
                started = True
        else:
            m_g = GROUP.match(line)
            m_q = None if m_g else QSTART.match(line)
            if m_g or m_q:
                q = int(m_g.group(1)) if m_g else int(m_q.group(1))
                started = True
        if started:
            finalize()
            mod = module_of(mapping, q)
            if mod is None or q in blocks:      # 答案区伪题号 / 重复题号：丢弃后续行
                continue
            blocks[q] = [line]
            order.append(q)
            cur_q, cur_lines = q, blocks[q]
            continue
        if cur_q is not None:
            cur_lines.append(line)
    finalize()

    result = {}
    for q in order:
        body = [l for l in blocks[q] if l.strip()]
        if not body:
            continue
        qtext, ans = body, None
        if ans_marker:
            for i, ln in enumerate(body):
                if ans_marker in ln:
                    qtext, ans = body[:i], body[i:]
                    break
        result[q] = (qtext, ans)
    return result

def parse_2021_11_letters(path):
    letters = {}
    for line in Path(path).read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^(\d{1,2})\s*[．.]\s*([A-D])\s*$", line.strip())
        if m:
            letters[int(m.group(1))] = m.group(2)
    return letters

def parse_2024_answers(path):
    ans = {}
    cur, cur_lines = None, None
    for line in Path(path).read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^[（(](\d{1,2})[）)]\s*答案\s*[:：]", line.strip())
        if m:
            if cur is not None:
                ans[cur] = "\n".join(cur_lines).strip()
            cur = int(m.group(1))
            cur_lines = [line]
        elif cur is not None:
            if is_ad(line) or "=====" in line:
                continue
            cur_lines.append(line)
    if cur is not None:
        ans[cur] = "\n".join(cur_lines).strip()
    return ans

def md_blockquote(lines):
    return "\n".join("> " + l.strip() if l.strip() else ">" for l in lines)

def md_details(ans_lines, note=""):
    body = "<br>".join(l.strip() for l in ans_lines if l.strip())
    if note:
        body = (body + "<br>" if body else "") + f"<i>{note}</i>"
    return (f"<details><summary><b>👉 点击展开答案与解析</b></summary>\n\n"
            f"<p>{body}</p>\n\n</details>")

def main():
    ans_2021_11 = parse_2021_11_letters(SRC / "2021年11月软件设计师上午真题+答案解析.txt")
    ans_2024 = parse_2024_answers(SRC / "2024年上半年软件设计师 综合知识 答案解析.txt")

    banks = {i: [] for i in range(13)}
    total = 0
    for tag, (fname, mapping) in MAPS.items():
        inline = (tag == "2024.05")
        ans_marker = ANSWER_MARKERS.get(tag)
        qs = parse_paper(SRC / fname, mapping, inline_qnum=inline, ans_marker=ans_marker)
        year, month = tag.split(".")[0], tag.split(".")[1]
        for mod in range(13):
            for q in sorted(qs):
                if module_of(mapping, q) != mod:
                    continue
                qtext, ans = qs[q]
                details = None
                if tag == "2022.05" and ans:
                    details = md_details(ans)
                elif tag == "2023.05" and ans:
                    details = md_details(ans)
                elif tag == "2024.05" and q in ans_2024:
                    details = md_details(ans_2024[q].split("\n"))
                elif tag == "2021.11" and q in ans_2021_11:
                    details = md_details([f"答案：{ans_2021_11[q]}"],
                                         "原卷解析为图片未提取；要听讲解把这题发我")
                banks[mod].append((year, month, q, qtext, details))
        total += len(qs)
        print(f"{tag}: {len(qs)} 块")

    out = ["# 上午真题分类题库（2021~2024，6 套卷按模块整合 · 答案折叠版）",
           "",
           "> **用法**：先做题 → 点每题下方『👉 点击展开答案与解析』对答案。题干选项为原文。",
           "> **答案覆盖**：2022.05 / 2023.05 / 2024 有完整答案+解析（折叠块）；2021.11 只有答案字母（解析为图片未提取）；**2021.05 / 2022.11 原卷未含解析**——不会的题直接发我，我定位知识点补讲。",
           "> **已知缺陷**：2021.11 第 8 题原卷题干缺失；2022.05 原文件只有 1~34 题；2024 第 59~70 题源文件无题干、第 20/74/75 题 OCR 题号丢失、第 17 题题号残缺已恢复；OCR 卷可能有少量识别噪声。",
           "> **配合**：知识点讲解见《上午题全知识点总复习_可视化.html》。", "",
           "## 各模块题量分布（块数）", ""]
    years = list(MAPS.keys())
    out.append("| 模块 | " + " | ".join(years) + " | 合计 |")
    out.append("|---|" + "---|" * (len(years) + 1))
    for mod in range(13):
        row = [str(len([b for b in banks[mod] if b[0] == y and b[1] == m])) for y, m in
               [(t.split(".")[0], t.split(".")[1]) for t in MAPS]]
        out.append(f"| {MODULES[mod]} | " + " | ".join(row) + f" | {len(banks[mod])} |")
    out.append("")
    for mod in range(13):
        if not banks[mod]:
            continue
        out.append(f"# {MODULES[mod]}")
        out.append("")
        for year, month, q, qtext, details in banks[mod]:
            out.append(f"**【{year}.{month} · 第{q}题】**")
            out.append("")
            out.append(md_blockquote(qtext))
            out.append("")
            if details:
                out.append(details)
                out.append("")
        out.append("---")
        out.append("")
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"TOTAL {total} 块 -> {OUT} ({len(OUT.read_text(encoding='utf-8'))} chars)")

if __name__ == "__main__":
    main()
