#!/usr/bin/env python3
"""把逐頁 JSON 與逐頁索引併回一篇一檔的 fulltext，然後刪掉分頁檔。

2026-10-12 站主明令「全局底層禁止停工後保留分頁文本」。檢查在 ~/.claude/bin/check-page-fragments.py。

處理三種形狀：
  X_pages.json（＋X_fulltext.txt、X_page_index.csv）  extract_pdf_text.py 的舊產物
  <目錄>/pages.json（＋fulltext.txt）                 library/text 底下整本書
  兩者的頁文字都寫成 fulltext 裡的 ===== [PDF_PAGE_NNNN] ===== 或 [PDF_PAGE_NNNN] 標記

規則：
  fulltext 已存在且逐頁文字（去空白後）與 JSON 相同 → fulltext 不動，只刪分頁檔。
  不同或不存在 → 以 JSON 的頁文字重寫 fulltext（JSON 是未經清理的原文，2026-10-12 查
    113 年憲判字第 9 號判決 332 頁有 400 頁的 fulltext 被重複字合併規則刪掉字）。
  JSON 帶刊本頁（book_page）時，標記寫成 [PDF_PAGE_NNNN]〔刊本頁 M〕；
    帶書層的後設資料（引擎、glyphPolicy、未解的頁碼）時寫進檔頭的 # 行。
  EPUB 只有 book_page 而無 pdf_page 時，標記寫成 [BOOK_PAGE_NNNN]。

用法：python3 scripts/merge_page_files.py <根目錄> [--write]
不帶 --write 只報告會怎麼做；帶 --write 才寫檔並刪除分頁檔（git 追蹤的檔請之後 git add -A 該目錄）。
"""
import json
import re
import sys
from pathlib import Path

SKIP = {".git", ".venv", "node_modules"}
MARK = re.compile(r"^(?:===== )?\[(?:PDF|BOOK)_PAGE_(\d+)\](?:〔[^〕]*〕)?(?: =====)?$", re.M)


def norm(s: str) -> str:
    s = re.sub(r"^#+ .*$", "", s or "", flags=re.M)
    return re.sub(r"\s+", "", s)


def split_fulltext(t: str):
    parts = MARK.split(t)
    return [parts[i + 1] for i in range(1, len(parts), 2)]


def page_label(p: dict):
    if "pdf_page" in p:
        lab = f"[PDF_PAGE_{p['pdf_page']:04d}]"
        if p.get("book_page") not in (None, ""):
            lab += f"〔刊本頁 {p['book_page']}〕"
        return lab
    return f"[BOOK_PAGE_{int(p['book_page']):04d}]"


def render(doc: dict, pages: list, old_header: str, old_body: str = "") -> str:
    if old_header.strip():
        head = old_header.rstrip() + "\n"
    else:
        src = doc.get("source_pdf") or doc.get("source_epub") or ""
        total = doc.get("total_pages") or doc.get("total_pdf_pages") or doc.get("total_book_pages") or len(pages)
        head = f"# Source\n{src}\n# Total pages\n{total}\n"
    meta = {k: v for k, v in doc.items()
            if k not in ("pages", "source_pdf", "source_epub", "total_pages", "total_pdf_pages", "total_book_pages")}
    for k, v in meta.items():
        line = f"# {k}: {json.dumps(v, ensure_ascii=False)}"
        if line not in head:
            head += line + "\n"
    heads = carry_headings(old_body, pages)
    body = "".join(f"\n{page_label(p)}\n{heads.get(i, '')}{(p.get('text') or '').rstrip()}\n"
                   for i, p in enumerate(pages))
    return head + body


def carry_headings(old_body: str, pages: list) -> dict:
    """無頁界標記的舊 fulltext 若有 # 章名，按其後的文字找到起頁，章名放在該頁開頭。"""
    out = {}
    if MARK.search(old_body):
        return out
    for m in re.finditer(r"^(#+ .+)\n+(.{1,200})", old_body, re.M):
        snippet = norm(m.group(2))[:30]
        for i, p in enumerate(pages):
            if norm(p.get("text")).startswith(snippet):
                out[i] = out.get(i, "") + m.group(1) + "\n\n"
                break
    return out


def jobs(root: Path):
    for j in sorted(root.rglob("*pages.json")):
        if any(part in SKIP for part in j.parts):
            continue
        if j.name == "pages.json":
            yield j, j.parent / "fulltext.txt", None
        elif j.name.endswith("_pages.json"):
            stem = j.name[: -len("_pages.json")]
            yield j, j.parent / f"{stem}_fulltext.txt", j.parent / f"{stem}_page_index.csv"


def main(argv):
    root = Path(argv[0]).resolve()
    write = "--write" in argv
    stats = {"不動": 0, "重寫": 0, "新建": 0}
    removed = 0
    problems = []
    for j, full, idx in jobs(root):
        doc = json.loads(j.read_text(encoding="utf-8"))
        pages = doc["pages"] if isinstance(doc, dict) else doc
        doc = doc if isinstance(doc, dict) else {}
        if not pages:
            problems.append(f"空的 pages：{j}")
            continue
        has_book = any(p.get("book_page") not in (None, "") for p in pages)
        old = full.read_text(encoding="utf-8") if full.exists() else ""
        secs = split_fulltext(old)
        meta_keys = [k for k in doc if k not in ("pages", "source_pdf", "source_epub", "total_pages",
                                                  "total_pdf_pages", "total_book_pages")]
        same = (len(secs) == len(pages)
                and all(norm(a.get("text")) == norm(b) for a, b in zip(pages, secs))
                and not (has_book and "〔刊本頁" not in old and "pdf_page" in pages[0])
                and all(f"# {k}:" in old for k in meta_keys))
        if same:
            stats["不動"] += 1
        else:
            m = MARK.search(old)
            header = old[: m.start()] if m else ""
            new = render(doc, pages, header, old if not m else "")
            got = split_fulltext(new)
            if len(got) != len(pages) or any(norm(a.get("text")) != norm(b) for a, b in zip(pages, got)):
                problems.append(f"重寫後逐頁文字不符：{full}")
                continue
            stats["重寫" if old else "新建"] += 1
            if write:
                full.write_text(new, encoding="utf-8")
        for f in (j, idx):
            if f is not None and f.exists():
                removed += 1
                if write:
                    f.unlink()
    print(f"{root}：fulltext 不動 {stats['不動']}、重寫 {stats['重寫']}、新建 {stats['新建']}；"
          f"{'已刪' if write else '將刪'}分頁檔 {removed}")
    for p in problems:
        print("  ", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
