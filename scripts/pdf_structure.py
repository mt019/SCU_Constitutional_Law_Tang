#!/usr/bin/env python3
"""替課件 PDF 補上刊本頁碼標籤與層級書籤。

期刊論文的 PDF 多半只帶數位化系統自動產的書籤（JSTOR 的逐頁清單、典藏庫的封面頁），
在閱讀器上跳不到節次，頁碼也顯示成第 1 頁而非刊本的第 525 頁。這支分兩步處理：

  detect  讀 PDF 與同目錄 text/ 底下的 fulltext 文字層，產一份 <stem>.structure.json 草稿
  apply   把該 json 寫回 PDF 的 /PageLabels 與 /Outlines

草稿是給人改的：偵測不到或偵測錯的，直接編輯 json 再 apply。

頁碼基準：json 裡的 page 一律是 PDF 的第幾頁，從 1 起算；label 是刊本印的頁碼。
寫入時才轉成 pypdf 的 0 起算。

已知會出錯的地方：
  - JSTOR 的逐頁書籤是權威對照，有就用，不要從頁眉猜。
  - 頁眉裡的卷號與年份（115:1346、1998）會混進頁碼的候選，偵測以「每頁對同一偏移量
    只投一票」計覆蓋率，覆蓋率低於七成的標成待核，不要當成已知。
  - 節標題的層級依編號樣式首次出現的先後指派，不假定羅馬數字一定是第一層。
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import warnings
from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Any

warnings.filterwarnings("ignore")

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

PAGE_BOOKMARK = re.compile(r"^(?:p\.\s*)?\[?(\d{1,4})\]?$")
NUM = re.compile(r"(?<!\d)(\d{1,4})(?!\d)")

# 節標題的編號樣式。鍵是樣式名，值是判斷用的 regex。
HEADING_STYLES = {
    "roman": re.compile(r"^([IVXL]{1,5})\.\s+([A-Z][^.]{2,70})$"),
    "digit": re.compile(r"^(\d{1,2})\.\s+([A-Z][^.]{2,70})$"),
    "alpha": re.compile(r"^([A-Z])\.\s+([A-Z][^.]{2,70})$"),
    "paren": re.compile(r"^\((\d{1,2}|[a-z])\)\s+([A-Z][^.]{2,70})$"),
}


def pages_for(pdf: Path) -> list[dict]:
    """讀 text/<slug>_fulltext.txt，依 ===== [PDF_PAGE_NNNN] ===== 標記切回逐頁（只在記憶體裡）。"""
    slug = re.sub(r"[^a-z0-9_\-.]+", "", pdf.stem.strip().lower().replace(" ", "_"))
    f = pdf.parent / "text" / f"{slug}_fulltext.txt"
    if not f.exists():
        return []
    parts = re.split(r"^===== \[PDF_PAGE_(\d+)\] =====$", f.read_text(encoding="utf-8"), flags=re.M)
    return [{"pdf_page": int(parts[i]), "lines": [ln.strip() for ln in parts[i + 1].splitlines() if ln.strip()]}
            for i in range(1, len(parts), 2)]


def labels_from_bookmarks(reader: PdfReader) -> list[tuple[int, int]]:
    """從 JSTOR 那種逐頁書籤讀出「PDF 頁 → 刊本頁」的對照。"""
    pairs: list[tuple[int, int]] = []

    def walk(items: Any) -> None:
        for it in items:
            if isinstance(it, list):
                walk(it)
                continue
            m = PAGE_BOOKMARK.match(it.title.strip())
            if not m:
                continue
            try:
                pairs.append((reader.get_destination_page_number(it) + 1, int(m.group(1))))
            except Exception:
                pass

    try:
        walk(reader.outline)
    except Exception:
        return []
    pairs.sort()
    return pairs


def labels_from_headers(pages: list[dict]) -> tuple[int | None, float]:
    """從頁眉與頁尾的數字推偏移量，回傳（偏移量, 覆蓋率）。"""
    votes: collections.Counter[int] = collections.Counter()
    for pg in pages:
        lines = [l.strip() for l in pg.get("lines", []) if l.strip()]
        if not lines:
            continue
        seen: set[int] = set()
        for cand in (lines[0], lines[-1]):
            for m in NUM.finditer(cand[:90]):
                v = int(m.group(1))
                if 1 <= v <= 3000:
                    seen.add(v - pg["pdf_page"])
        for off in seen:
            votes[off] += 1
    if not votes:
        return None, 0.0
    off, n = votes.most_common(1)[0]
    return off, n / max(1, len(pages))


def font_blocks(pdf: Path) -> list[dict]:
    """用 poppler 的 pdftohtml -xml 取每塊文字的字型與座標。

    pypdf 的 visitor 逐片段重組，遇到調過字距或 small caps 的標題會散成
    「So cio log i cal」；poppler 這條把整塊文字連同字型大小一起給出來。
    反過來，JSTOR 那種把文字藏在影像底下的掃描件，poppler 讀不到而 pypdf 讀得到，
    兩者互補，判斷標題用這支、核對頁碼兩支都要試。
    """
    try:
        xml = subprocess.run(
            ["pdftohtml", "-xml", "-i", "-stdout", str(pdf)], capture_output=True
        ).stdout
        root = ET.fromstring(xml)
    except Exception:
        return []
    specs: dict[str, tuple[float, str]] = {}
    out: list[dict] = []
    for page in root.iter("page"):
        pno = int(page.get("number"))
        for f in page.iter("fontspec"):
            specs[f.get("id")] = (float(f.get("size")), f.get("family") or "")
        for t in page.findall("text"):
            txt = " ".join("".join(t.itertext()).split())
            if not txt:
                continue
            size, fam = specs.get(t.get("font"), (0.0, "?"))
            out.append(
                {"page": pno, "text": txt, "size": size, "family": fam, "top": int(t.get("top"))}
            )
    return out


def headings_by_font(pdf: Path) -> list[dict]:
    """字型與正文不同、且不在頁眉位置的短文字塊，就是標題的候選。"""
    bs = font_blocks(pdf)
    if not bs:
        return []
    weight: collections.Counter = collections.Counter()
    for b in bs:
        weight[(b["size"], b["family"])] += len(b["text"])
    body = weight.most_common(1)[0][0]
    npages = len({b["page"] for b in bs})
    tops = collections.Counter(b["top"] for b in bs)
    header_tops = {t for t, n in tops.items() if n > npages * 0.4}
    out: list[dict] = []
    for b in bs:
        if b["top"] in header_tops or (b["size"], b["family"]) == body:
            continue
        if b["size"] < body[0] or not (3 <= len(b["text"]) <= 90):
            continue
        if re.fullmatch(r"[\d\s.,;:\u2022\-\u2013]+", b["text"]):
            continue
        out.append(
            {"page": b["page"], "title": b["text"], "size": b["size"], "family": b["family"]}
        )
    return out


def normalize_title(t: str) -> str:
    """修掉抽取造成的字距與黏字，並去掉目次行尾端的引導點與頁碼。"""
    t = re.sub(r"[.\u00b7\u2022\s]{3,}\d{1,4}\s*$", "", t)          # ". . . . 680"
    t = re.sub(r"\b([A-Z])\s+(?=[A-Z]{2,})", r"\1", t)                # "T HE" -> "THE"
    t = re.sub(r"\b([A-Z]{2,})([A-Z][a-z])", r"\1 \2", t)             # "THEJudge" -> "THE Judge"
    return " ".join(t.split()).strip()


def heading_hits(pages: list[dict]) -> list[dict]:
    hits: list[dict] = []
    for pg in pages:
        for line in pg.get("lines", []):
            t = " ".join(line.split())
            if not (4 <= len(t) <= 110) or " v. " in t:
                continue
            for style, pat in HEADING_STYLES.items():
                m = pat.match(normalize_title(t))
                if m:
                    hits.append(
                        {
                            "page": pg["pdf_page"],
                            "style": style,
                            "num": m.group(1),
                            "title": normalize_title(t),
                        }
                    )
                    break
    return hits


def detect_outline(pages: list[dict]) -> tuple[list[dict], dict]:
    """回傳（書籤清單, 診斷）。

    文章開頭的目次頁每一行都長得像節標題，一頁會命中好幾條。這種頁不進書籤，
    改拿它當作者自己列的節次清單：標題文字取目次那份（完整），頁碼取正文那份。
    """
    hits = heading_hits(pages)
    per_page = collections.Counter(h["page"] for h in hits)
    toc_pages = {pg for pg, n in per_page.items() if n >= 4 and pg <= max(4, len(pages) // 10)}

    toc = [h for h in hits if h["page"] in toc_pages]
    body = [h for h in hits if h["page"] not in toc_pages]

    # 同一個編號在正文出現多次時取最先那次（後面多半是頁眉或交互參照）
    chosen: dict[tuple[str, str], dict] = {}
    for h in body:
        key = (h["style"], h["num"])
        if key not in chosen or h["page"] < chosen[key]["page"]:
            chosen[key] = h

    for key, h in chosen.items():
        for t in toc:
            if (t["style"], t["num"]) == key and len(t["title"]) > len(h["title"]):
                h["title"] = t["title"]
                break

    items = sorted(chosen.values(), key=lambda h: (h["page"], h["num"]))
    order: list[str] = []
    for h in items:
        if h["style"] not in order:
            order.append(h["style"])
    out = [
        {"level": order.index(h["style"]) + 1, "page": h["page"], "title": h["title"]}
        for h in items
    ]
    diag = {
        "toc_pages": sorted(toc_pages),
        "toc_entries": len(toc),
        "body_headings": len(out),
        "missing_from_body": sorted(
            {t["title"] for t in toc} - {h["title"] for h in items}
        )[:20],
    }
    return out, diag


def detect(pdf: Path) -> dict:
    reader = PdfReader(str(pdf))
    total = len(reader.pages)
    pages = pages_for(pdf)

    outline, diag = detect_outline(pages)
    by_font = headings_by_font(pdf)
    diag["font_candidates"] = by_font[:60]
    diag["font_candidate_count"] = len(by_font)

    pairs = labels_from_bookmarks(reader)
    offsets = {b - a for a, b in pairs}
    if len(pairs) >= 5 and len(offsets) == 1:
        off = offsets.pop()
        first = pairs[0][0]
        source, confidence = "jstor-bookmarks", 1.0
    else:
        off, confidence = labels_from_headers(pages)
        # 典藏庫會在正文前面塞一兩頁封面，正文的起始頁不一定是第 1 頁：
        # 取第一個「頁眉抽到的數字剛好等於 頁次＋偏移量」的頁。
        first = None
        if off is not None:
            for pg in pages:
                lines = [l.strip() for l in pg.get("lines", []) if l.strip()]
                zone = " ".join(lines[:3] + lines[-3:])
                if str(pg["pdf_page"] + off) in zone:
                    first = pg["pdf_page"]
                    break
            if first is None:
                first = 1
        source = "page-headers"

    labels: list[dict] = []
    if off is not None and first is not None:
        if first > 1:
            labels.append({"from": 1, "to": first - 1, "style": "/r"})
        labels.append({"from": first, "to": total, "style": "/D", "start": first + off})

    return {
        "source_pdf": pdf.name,
        "total_pages": total,
        "page_base": 1,
        "page_labels": labels,
        "page_labels_source": source,
        "page_labels_confidence": round(confidence, 2),
        "needs_review": confidence < 0.7,
        "outline": outline,
        "outline_diagnostics": diag,
    }


def apply(spec_path: Path, pdf: Path | None = None, labels_only: bool = False) -> int:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    pdf = pdf or spec_path.parent / spec["source_pdf"]
    reader = PdfReader(str(pdf))
    writer = PdfWriter(clone_from=str(pdf))
    root = writer._root_object
    for key in ("/Outlines", "/PageMode"):
        if key in root:
            del root[NameObject(key)]

    for lb in spec.get("page_labels", []):
        writer.set_page_label(
            lb["from"] - 1, lb["to"] - 1, style=lb.get("style", "/D"), start=lb.get("start", 1)
        )

    outline = [] if labels_only else spec.get("outline", [])
    parents: dict[int, Any] = {}
    for item in outline:
        level = int(item.get("level", 1))
        parent = parents.get(level - 1) if level > 1 else None
        node = writer.add_outline_item(item["title"], item["page"] - 1, parent=parent)
        parents[level] = node
        for deeper in [k for k in parents if k > level]:
            del parents[deeper]

    if outline:
        root[NameObject("/PageMode")] = NameObject("/UseOutlines")

    writer.write(str(pdf))

    check = PdfReader(str(pdf))
    ok = len(check.pages) == len(reader.pages)
    print(
        "%s  頁數 %d %s  頁碼標籤 %d 段  書籤 %d 條"
        % (pdf.name, len(check.pages), "不變" if ok else "改變了", len(spec.get("page_labels", [])), len(outline))
    )
    return 0 if ok else 1


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    pd = sub.add_parser("detect")
    pd.add_argument("pdf", nargs="+")
    pd.add_argument("--out-suffix", default=".structure.json")
    pa = sub.add_parser("apply")
    pa.add_argument("spec", nargs="+")
    pa.add_argument("--labels-only", action="store_true", help="只寫頁碼標籤，不動書籤")
    a = p.parse_args()

    if a.cmd == "detect":
        for s in a.pdf:
            f = Path(s)
            spec = detect(f)
            out = f.with_suffix(a.out_suffix)
            out.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(
                "%-46s 頁碼 %-16s 覆蓋 %.0f%%%s  書籤 %d 條"
                % (
                    f.name[:46],
                    spec["page_labels_source"] if spec["page_labels"] else "偵測不到",
                    100 * spec["page_labels_confidence"],
                    "  待核" if spec["needs_review"] else "",
                    len(spec["outline"]),
                )
            )
        return 0

    rc = 0
    for s in a.spec:
        rc |= apply(Path(s), labels_only=a.labels_only)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
