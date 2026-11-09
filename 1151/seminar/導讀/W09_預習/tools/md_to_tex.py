#!/usr/bin/env python3
"""W09 預習頁 md 轉 tex 的單次轉換（2026-11-09）。

來源：notes/docs/1151/seminar/W09_1109_預習.md（87808f3 提交版）。轉完後 Teile/*.tex 為正本，md 頁凍結；
輸出檔已存在時拒絕寫入，除非加 --force（重跑會蓋掉人工修改）。

層級：md 的「## 一、」各節 → \\chapter（一節一部，各寫一個 Teile 檔）；### → \\section；#### → \\subsection。
### 標題開頭的「甲、」「（一）」去掉，由章節編號代替；#### 的「（一）」保留（secnumdepth 為 1，該層無自動編號）。
頁碼括號：含「頁」字的全形括號改寫成 \\pg{…}，括號內文字不動，供 tools/build_sources.py 收出處。
表題：沿用課程問答書 tools/md_to_tex.py 的 convert_tables（表格上一行「表 N　說明」→ longtable 的 \\caption）。
用法：python3 -I tools/md_to_tex.py <W09_1109_預習.md> [--force]
"""
import argparse
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
BASE = BOOK.parent.parent / "課程問答" / "tools" / "md_to_tex.py"
spec = importlib.util.spec_from_file_location("base", BASE)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

# md 的「## 」節 → 輸出檔與部名
PARTS = [
    ("一、導論", "10_intro", "導論：三篇的出處與問題"),
    ("二、Alexander", "20_AS", None),
    ("三、Kramer", "30_Kramer", None),
    ("四、Ferejohn", "40_FP", None),
    ("五、主要用語", "A3_terms", "主要用語對照"),
    ("六、與前後幾週", "50_relations", "與前後幾週的關係及課前問題"),
]

PG = re.compile(r"（([^（）]*?\d[^（）]*?頁[^（）]*?)）")


def to_tex(md):
    md = re.sub(r"^(### )(?:[甲乙丙丁戊己庚辛壬癸]、|（[一二三四五六七八九十]+）)", r"\1", md, flags=re.M)
    lines, tables, nocap = base.convert_tables(md.split("\n"))
    tex = base.pandoc("\n".join(lines), shift=-2)
    tex = tex.replace("\\emph{", "\\en{")
    # 頁碼括號（標題裡的也改：\pg 在標題中展開為同樣的全形括號）
    tex = PG.sub(lambda m: "\\pg{" + m.group(1) + "}", tex)
    return tex, tables, nocap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    md = Path(a.src).read_text()
    body = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.S)
    chunks = re.split(r"^## ", body, flags=re.M)
    head = chunks[0]
    # 卷首說明（# 題之後、## 一之前）→ Teile/00_note.tex，主檔放進凡例
    note = "\n".join(l for l in head.split("\n") if not l.startswith("# ")).strip()
    out = {"00_note": ("", note)}
    for c in chunks[1:]:
        title_line, rest = c.split("\n", 1)
        hit = next((p for p in PARTS if title_line.startswith(p[0])), None)
        if not hit:
            sys.exit(f"未對應的節：{title_line}")
        title = hit[2] or re.sub(r"^[一二三四五六七八九十]+、", "", title_line).strip()
        out[hit[1]] = (title, rest)
    for name, (title, md_part) in out.items():
        dst = BOOK / "Teile" / f"{name}.tex"
        if dst.exists() and not a.force:
            sys.exit(f"{dst} 已存在；確定要覆蓋再加 --force")
        tex, tables, nocap = to_tex(md_part)
        if title:
            title = PG.sub(lambda m: "\\pg{" + m.group(1) + "}", title.replace("*", ""))
        hdr = (f"% 自 notes/docs/1151/seminar/W09_1109_預習.md（87808f3）由 tools/md_to_tex.py 於 2026-11-09 轉出一次；"
               f"此後本檔為正本。\n")
        if title:
            hdr += f"\\chapter{{{title}}}\n\n"
        dst.write_text(hdr + tex)
        print(f"{name}: 表 {tables}（無表題 {nocap}）section {tex.count(chr(92)+'section{')} "
              f"subsection {tex.count(chr(92)+'subsection{')} pg {tex.count(chr(92)+'pg{')}")


if __name__ == "__main__":
    main()
