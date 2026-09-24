# -*- coding: utf-8 -*-
"""OCR 扫描版真题 PDF：渲染页面 -> rapidocr 识别 -> _提取文本/*.txt
用法: python ocr_pdfs.py <序号0-4>   （不传参数则跑全部）
"""
import sys
from pathlib import Path
import numpy as np
import fitz  # PyMuPDF
from rapidocr_onnxruntime import RapidOCR

ROOT = Path(r"f:\软设笔记\2021-2024历年真题及解析")
OUT = ROOT / "_提取文本"
OUT.mkdir(exist_ok=True)

TARGETS = [
    "2022年11月软件设计师下午真题及答案解析",
    "2023年上半年软件设计师上午真题及答案解析",
    r"2024上半年软考中级软件设计师试题及答案解析/2024年上半年软件设计师 综合知识 答案解析",
    r"2024上半年软考中级软件设计师试题及答案解析/2024年上半年软件设计师案例分析（空白试卷）",
    r"2024上半年软考中级软件设计师试题及答案解析/2024年上半年软件设计师综合知识（空白试卷）",
]

def sanitize(s):
    return "".join(c for c in s if not (0xD800 <= ord(c) <= 0xDFFF))

def run(idx):
    name = TARGETS[idx]
    pdf_path = ROOT / (name + ".pdf")
    doc = fitz.open(str(pdf_path))
    engine = RapidOCR()
    parts = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        if pix.n == 4:
            img = img[:, :, :3]
        result, _ = engine(img)
        page_text = "\n".join(item[1] for item in result) if result else ""
        parts.append(f"\n===== 第{i+1}页 =====\n{page_text}")
        print(f"page {i+1}/{len(doc)}")
    doc.close()
    text = sanitize("\n".join(parts)).strip()
    (OUT / (Path(name).stem + ".txt")).write_text(text, encoding="utf-8")
    print(f"DONE chars={len(text)} idx={idx}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(int(sys.argv[1]))
    else:
        for i in range(len(TARGETS)):
            run(i)
