# -*- coding: utf-8 -*-
"""提取真题 PDF 文本 -> _提取文本/*.txt（UTF-8），并生成摘要"""
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(r"f:\软设笔记\2021-2024历年真题及解析")
OUT = ROOT / "_提取文本"
OUT.mkdir(exist_ok=True)

summary = []
pdfs = sorted(ROOT.rglob("*.pdf"))
def sanitize(s):
    """去掉 PDF 字体映射产生的孤立代理字符，避免 UTF-8 写入失败"""
    return "".join(c for c in s if not (0xD800 <= ord(c) <= 0xDFFF))

for idx, pdf in enumerate(pdfs, 1):
    try:
        reader = PdfReader(str(pdf))
        parts = []
        for i, page in enumerate(reader.pages):
            parts.append(f"\n===== 第{i+1}页 =====\n")
            try:
                parts.append(page.extract_text() or "")
            except Exception as e:
                parts.append(f"[第{i+1}页提取失败: {e}]")
        text = sanitize("".join(parts)).strip()
        target = OUT / (pdf.stem + ".txt")
        target.write_text(text, encoding="utf-8")
        rel = str(pdf.relative_to(ROOT))
        summary.append(f"{idx}. {rel} | 页数={len(reader.pages)} | 字符数={len(text)}")
        print(f"{idx}. OK pages={len(reader.pages)} chars={len(text)}")
    except Exception as e:
        summary.append(f"{idx}. {pdf.name} | FAILED: {e}")
        print(f"{idx}. FAILED {type(e).__name__}")

(OUT / "_summary.txt").write_text("\n".join(summary), encoding="utf-8")
print("DONE, files:", len(pdfs))
