#!/usr/bin/env python3
"""湯德宗專書五冊（讀秀掃描本）的 OCR 文字層。

五冊每頁嵌一張 JBIG2 一位元影像（205–217 ppi），第 1 頁為彩色封面，末頁為 Anna's Archive
附加的說明頁（無影像、有文字層）。2026-10-05 每冊抽 20 頁比對 pdfimages 抽原圖、pdftoppm、
Ghostscript 三種取法，黑點比例相差在 0.03 個百分點以內；poppler 對每頁報的
「Unknown segment type in JBIG2 stream」不影響內容。故直接抽原圖，不重新渲染。

引擎為 macOS Vision（~/.claude/skills/cjk-print-ocr/ocr_vision）。卷一刊本 18、119、593 頁
逐字核對 2,313 字，認錯率 0.52%，其中漢字認錯 1 處；其餘為行首句號讀成「•」、註號、
拉丁字母（紀錄在該 skill 的 engines.tsv）。原尺寸、放大兩倍、400 dpi 三種輸入的輸出逐字相同。

用法（在倉根目錄）：
    python3 scripts/ocr_tang_books.py --list          # 只列各冊進度，不跑
    python3 scripts/ocr_tang_books.py --book v1       # 跑一冊，已有逐頁稿的頁跳過
    python3 scripts/ocr_tang_books.py --book v1 --build-only

產物在 library/text/<書名>/fulltext.txt，全書一檔：檔頭 # 行記來源、引擎、glyphPolicy、空白頁、
推不出刊本頁的頁、位移分布與取自 PDF 文字層的頁；頁首標 [PDF_PAGE_NNNN]〔刊本頁 M〕，頁文字是 Vision 原始輸出，不改字。
不另產逐頁 JSON（2026-10-12 站主令「禁止停工後保留分頁文本」；檢查 ~/.claude/bin/check-page-fragments.py）。
跑的期間逐頁追加到同目錄的 .progress.jsonl（中斷重跑從這裡接續），組裝完即刪除。
--build-only 沒有 .progress.jsonl 時讀既有的 fulltext.txt 依頁標切回逐頁，重新推刊本頁。

book_page 由每頁讀到的頁碼行推出 PDF 頁序與刊本頁碼的位移，前後兩個讀到的頁碼位移一致
才填；推不出的不標，並列在檔頭的 unresolved_book_pages。text 是原始輸出，
行首的「•」多為「。」，「為」多為原書的「爲」，引用一律回原頁圖核。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = ROOT / "library/books"
TEXT_DIR = ROOT / "library/text"
OCR = Path.home() / ".claude/skills/cjk-print-ocr/ocr_vision"

# 代號, PDF 檔名, 文字層目錄名
BOOKS = [
    ("v1", "湯德宗_權力分立新論卷一_憲法結構與動態平衡_增訂三版_2005.pdf", "湯德宗_權力分立新論卷一"),
    ("v2", "湯德宗_權力分立新論卷二_違憲審查與動態平衡_增訂三版_2005.pdf", "湯德宗_權力分立新論卷二"),
    ("cc5", "湯德宗_廖福特編_憲法解釋之理論與實務第五輯_2007.pdf", "湯德宗_憲法解釋之理論與實務第五輯"),
    ("cs1", "湯德宗_王鵬翔編_2006兩岸四地法律發展上冊_違憲審查與行政訴訟_2007.pdf", "湯德宗_兩岸四地法律發展上冊"),
    ("cs2", "湯德宗_王鵬翔編_2006兩岸四地法律發展下冊_民事訴訟與刑事訴訟_2007.pdf", "湯德宗_兩岸四地法律發展下冊"),
]

ROMAN = re.compile(r"^[ivxlcIVXLC]{1,7}$")
ARABIC = re.compile(r"^\d{1,4}$")


def page_count(pdf: Path) -> int:
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"^Pages:\s+(\d+)", out, re.M).group(1))


def ocr_page(pdf: Path, n: int) -> tuple[str, str]:
    """回傳 (來源, 文字)。來源為 vision 或 textlayer（無影像的頁取 PDF 自帶文字層）。"""
    with tempfile.TemporaryDirectory() as tmp:
        stem = Path(tmp) / "p"
        subprocess.run(["pdfimages", "-png", "-f", str(n), "-l", str(n), str(pdf), str(stem)],
                       capture_output=True, check=True)
        imgs = sorted(Path(tmp).glob("p-*.png"))
        if not imgs:
            txt = subprocess.run(["pdftotext", "-f", str(n), "-l", str(n), str(pdf), "-"],
                                 capture_output=True, text=True, check=True).stdout
            return "textlayer", txt
        if len(imgs) > 1:
            raise SystemExit(f"{pdf.name} 第 {n} 頁有 {len(imgs)} 張影像，與預期的一頁一張不符")
        res = subprocess.run([str(OCR), str(imgs[0])], capture_output=True, text=True)
        if res.returncode != 0 or res.stderr.strip():
            raise SystemExit(f"{pdf.name} 第 {n} 頁 OCR 失敗：{res.stderr.strip()}")
        return "vision", res.stdout


def number_read(text: str):
    """頁碼行：末行或首行只有阿拉伯數字或羅馬數字者。"""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for cand in (lines[-1:] + lines[:1]) if lines else []:
        if ARABIC.match(cand):
            return int(cand)
        if ROMAN.match(cand):
            return cand.lower()
    return None


def assign_book_pages(records):
    """位移取前後最近兩個讀到頁碼的頁（不含本頁），兩者一致才採用。

    本頁自己讀到的數字不替自己作證：書名頁末行的「2005」、註腳末行的註號都會被讀成頁碼。
    本頁讀到的數字與鄰頁推出的不符時，以鄰頁為準並列入 page_number_mismatch。
    """
    total = len(records)
    reads = [(r["pdf_page"], r["pdf_page"] - r["page_number_read"]) for r in records
             if isinstance(r["page_number_read"], int) and 1 <= r["page_number_read"] <= total]
    unresolved, mismatch = [], []
    for r in records:
        n = r["pdf_page"]
        prev = [o for p, o in reads if p < n][-1:]
        nxt = [o for p, o in reads if p > n][:1]
        own = r["page_number_read"]
        if isinstance(own, str):
            r["book_page"] = own
            continue
        if prev and nxt and prev[0] == nxt[0] and n - prev[0] >= 1:
            r["book_page"] = n - prev[0]
            if isinstance(own, int) and own != r["book_page"]:
                mismatch.append(n)
        elif isinstance(own, int) and own in {n - o for o in prev + nxt}:
            r["book_page"] = own
        else:
            r["book_page"] = None
            if r["source"] == "vision" and r["chars"]:
                unresolved.append(n)
    return unresolved, mismatch, Counter(o for _, o in reads)


def build(code, pdf_name, dirname):
    pdf = BOOKS_DIR / pdf_name
    out = TEXT_DIR / dirname
    progress = out / ".progress.jsonl"
    total = page_count(pdf)
    if progress.exists():
        done = load_progress(progress)
    else:
        done = read_fulltext(out / "fulltext.txt")
    missing = [n for n in range(1, total + 1) if n not in done]
    if missing:
        raise SystemExit(f"{code}：尚有 {len(missing)} 頁未辨識（首缺 {missing[0]}），不組裝")
    records = []
    for n in range(1, total + 1):
        src, text = done[n]
        records.append({"pdf_page": n, "source": src,
                        "page_number_read": number_read(text), "chars": len(re.sub(r"\s", "", text)),
                        "text": text})
    unresolved, mismatch, offsets = assign_book_pages(records)
    blank = [r["pdf_page"] for r in records if r["chars"] == 0]
    doc = {"source_pdf": f"library/books/{pdf_name}", "engine": "macOS Vision VNRecognizeTextRequest "
           "(zh-Hant, en-US, accurate)", "glyphPolicy": "未定（原始辨讀輸出，未校訂）",
           "total_pdf_pages": total, "blank_pages": blank, "unresolved_book_pages": unresolved,
           "page_number_mismatch": mismatch,
           "page_offsets": {str(k): v for k, v in offsets.most_common()},
           "textlayer_pages": [r["pdf_page"] for r in records if r["source"] != "vision"],
           "pages": [{k: r[k] for k in ("pdf_page", "book_page", "page_number_read", "source", "chars", "text")}
                     for r in records]}
    head = f"# Source\n{doc['source_pdf']}\n# Total pages\n{total}\n" + "".join(
        f"# {k}: {json.dumps(doc[k], ensure_ascii=False)}\n"
        for k in ("engine", "glyphPolicy", "blank_pages", "unresolved_book_pages", "page_number_mismatch", "page_offsets", "textlayer_pages"))
    body = "".join(
        f"\n[PDF_PAGE_{r['pdf_page']:04d}]" + (f"〔刊本頁 {r['book_page']}〕" if r.get("book_page") not in (None, "") else "")
        + f"\n{r['text'].rstrip()}\n" for r in records)
    (out / "fulltext.txt").write_text(head + body, encoding="utf-8")
    progress.unlink(missing_ok=True)
    print(f"{code}：{total} 頁組裝完成；空白 {len(blank)}；刊本頁推不出 {len(unresolved)}；"
          f"讀到的頁碼與鄰頁不符 {len(mismatch)}；"
          f"位移分布 {offsets.most_common(4)}")


def read_fulltext(path: Path) -> dict:
    """fulltext.txt 依 [PDF_PAGE_NNNN] 切回 {頁: (來源, 文字)}，只在記憶體裡。"""
    t = path.read_text(encoding="utf-8")
    m = re.search(r"^# textlayer_pages: (\[.*\])$", t, re.M)
    tl = set(json.loads(m.group(1))) if m else set()
    parts = re.split(r"^\[PDF_PAGE_(\d+)\](?:〔[^〕]*〕)?$", t, flags=re.M)
    return {int(parts[i]): ("textlayer" if int(parts[i]) in tl else "vision", parts[i + 1].strip("\n"))
            for i in range(1, len(parts), 2)}


def load_progress(path: Path) -> dict:
    """讀進度檔；最後一行若因中斷而寫壞就略過，該頁重跑。"""
    done = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        done[r["pdf_page"]] = (r["source"], r["text"])
    return done


def run(code, pdf_name, dirname):
    pdf = BOOKS_DIR / pdf_name
    out = TEXT_DIR / dirname
    out.mkdir(parents=True, exist_ok=True)
    progress = out / ".progress.jsonl"
    done = load_progress(progress) if progress.exists() else {}
    total = page_count(pdf)
    todo = [n for n in range(1, total + 1) if n not in done]
    print(f"{code}：{total} 頁，待辦 {len(todo)}", flush=True)
    with progress.open("a", encoding="utf-8") as f:
        for i, n in enumerate(todo, 1):
            src, text = ocr_page(pdf, n)
            f.write(json.dumps({"pdf_page": n, "source": src, "text": text}, ensure_ascii=False) + "\n")
            f.flush()
        if i % 25 == 0 or i == len(todo):
                print(f"  {code} {i}/{len(todo)}（PDF 第 {n} 頁）", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", choices=[b[0] for b in BOOKS])
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--build-only", action="store_true")
    a = ap.parse_args()
    if a.list or not a.book:
        for code, pdf_name, dirname in BOOKS:
            out = TEXT_DIR / dirname
            if (out / ".progress.jsonl").exists():
                done = len(load_progress(out / ".progress.jsonl"))
            elif (out / "fulltext.txt").exists():
                done = len(read_fulltext(out / "fulltext.txt"))
            else:
                done = 0
            print(f"{code}\t{done}/{page_count(BOOKS_DIR / pdf_name)}\t{dirname}")
        return
    book = next(b for b in BOOKS if b[0] == a.book)
    if not a.build_only:
        run(*book)
    build(*book)


if __name__ == "__main__":
    sys.exit(main())
