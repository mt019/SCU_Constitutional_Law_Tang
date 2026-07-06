#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import zipfile
from dataclasses import dataclass
from html import unescape
from pathlib import Path
from typing import Iterable
import xml.etree.ElementTree as ET


XHTML_NS = {"xhtml": "http://www.w3.org/1999/xhtml", "ncx": "http://www.daisy.org/z3986/2005/ncx/"}


def normalize_ws(text: str) -> str:
    text = unescape(text).replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def title_to_slug(title: str, fallback: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", title).strip("_").lower()
    return slug or fallback


@dataclass
class TocItem:
    title: str
    src: str
    href: str
    anchor: str | None
    children: list["TocItem"]


def parse_ncx(zf: zipfile.ZipFile) -> list[TocItem]:
    root = ET.fromstring(zf.read("OEBPS/toc.ncx"))

    def build(node: ET.Element) -> TocItem:
        title = normalize_ws("".join(node.find("ncx:navLabel/ncx:text", XHTML_NS).itertext()))
        src = node.find("ncx:content", XHTML_NS).attrib["src"]
        href, _, anchor = src.partition("#")
        children = [build(child) for child in node.findall("ncx:navPoint", XHTML_NS)]
        return TocItem(title=title, src=src, href=f"OEBPS/{href}", anchor=anchor or None, children=children)

    return [build(node) for node in root.findall(".//ncx:navMap/ncx:navPoint", XHTML_NS)]


def flatten_toc(nodes: Iterable[TocItem]) -> list[TocItem]:
    out: list[TocItem] = []
    for node in nodes:
        out.append(node)
        out.extend(flatten_toc(node.children))
    return out


def is_note_anchor(el: ET.Element) -> bool:
    href = el.attrib.get("href", "")
    return "note-" in href or "note-" in el.attrib.get("id", "")


def is_page_marker(el: ET.Element) -> bool:
    cls = el.attrib.get("class", "")
    return "pageNumber" in cls


def extract_page_number(text: str) -> int | None:
    m = re.search(r"\(p\.(\d+)\)", text)
    return int(m.group(1)) if m else None


def inline_chunks(el: ET.Element) -> list[tuple[str, object]]:
    chunks: list[tuple[str, object]] = []
    if el.text:
        chunks.append(("text", el.text))
    for child in list(el):
        if is_note_anchor(child):
            pass
        elif is_page_marker(child):
            page_num = extract_page_number("".join(child.itertext()))
            if page_num is not None:
                chunks.append(("page", page_num))
        else:
            chunks.extend(inline_chunks(child))
        if child.tail:
            chunks.append(("text", child.tail))
    return chunks


def element_text_with_pages(el: ET.Element, initial_page: int) -> tuple[list[tuple[int, str]], str]:
    current_page = initial_page
    pieces: list[str] = []
    segments: list[tuple[int, str]] = []
    raw_parts: list[str] = []
    for kind, value in inline_chunks(el):
        if kind == "page":
            page_num = int(value)
            text = normalize_ws("".join(pieces))
            if text:
                segments.append((current_page, text))
                raw_parts.append(text)
            pieces = []
            current_page = page_num
        else:
            pieces.append(str(value))
    text = normalize_ws("".join(pieces))
    if text:
        segments.append((current_page, text))
        raw_parts.append(text)
    return segments, "\n".join(raw_parts)


def parse_xhtml(zf: zipfile.ZipFile, path: str) -> ET.Element:
    raw = zf.read(path).decode("utf-8", "ignore")
    raw = raw.replace("&nbsp;", "&#160;")
    return ET.fromstring(raw)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("epub_path")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--basename", default="the_ultimate_rule_of_law")
    args = parser.parse_args()

    epub_path = Path(args.epub_path)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(epub_path) as zf:
        toc_tree = parse_ncx(zf)
        toc_items = flatten_toc(toc_tree)
        title_lookup = {(item.href, item.anchor): item.title for item in toc_items if item.anchor}

        pages: dict[int, list[str]] = {}
        chapters: list[dict[str, object]] = []
        fulltext_parts: list[str] = []

        chapter_counter = 0
        for item in toc_tree:
            if not item.href.endswith(".xhtml") or "chapter-" not in item.href:
                continue

            chapter_counter += 1
            root = parse_xhtml(zf, item.href)
            body = root.find("xhtml:body", XHTML_NS)
            if body is None:
                continue

            chapter_title = item.title
            chapter_id = f"ch{chapter_counter}"
            sections: list[dict[str, object]] = []
            current_section: dict[str, object] | None = None
            paragraph_counter = 0
            chapter_pages: set[int] = set()
            raw_xhtml = zf.read(item.href).decode("utf-8", "ignore")
            marker_nums = [int(x) for x in re.findall(r"pageid_(\d+)", raw_xhtml)]
            initial_page = max(1, min(marker_nums) - 1) if marker_nums else 1

            for el in body.iter():
                tag = el.tag.split("}")[-1]
                if tag not in {"h1", "h2", "h3", "p"}:
                    continue

                el_id = el.attrib.get("id")
                text_segments, raw_text = element_text_with_pages(el, initial_page)
                if not raw_text:
                    continue

                if tag in {"h1", "h2", "h3"} and el_id and (item.href, el_id) in title_lookup:
                    section_title = title_lookup[(item.href, el_id)]
                    current_section = {
                        "id": title_to_slug(section_title, f"sec_{len(sections)+1}"),
                        "title": section_title,
                        "paragraphs": [],
                    }
                    sections.append(current_section)
                    continue

                if tag == "h1" and el_id == "pagetitle":
                    fulltext_parts.append(f"\n# {raw_text}\n")
                    continue

                if current_section is None:
                    current_section = {
                        "id": "opening",
                        "title": "Opening",
                        "paragraphs": [],
                    }
                    sections.append(current_section)

                paragraph_counter += 1
                para_id = f"{chapter_id}_p{paragraph_counter:03d}"
                para_pages = sorted({page for page, _ in text_segments})
                chapter_pages.update(para_pages)
                para_entry = {
                    "paragraph_id": para_id,
                    "book_pages": para_pages,
                    "text": raw_text,
                    "segments": [{"book_page": p, "text": t} for p, t in text_segments],
                }
                current_section["paragraphs"].append(para_entry)

                for page_num, segment_text in text_segments:
                    pages.setdefault(page_num, []).append(segment_text)
                fulltext_parts.append(raw_text)

            chapters.append(
                {
                    "id": chapter_id,
                    "title": chapter_title,
                    "book_page_start": min(chapter_pages) if chapter_pages else None,
                    "book_page_end": max(chapter_pages) if chapter_pages else None,
                    "sections": sections,
                }
            )

        page_entries = []
        for page_num in sorted(pages):
            text = "\n\n".join(pages[page_num]).strip()
            page_entries.append(
                {
                    "book_page": page_num,
                    "chars": len(text),
                    "preview": text[:200],
                    "text": text,
                }
            )

        pages_json = {
            "source_epub": str(epub_path),
            "total_book_pages": len(page_entries),
            "pages": page_entries,
        }
        structured_json = {
            "source_epub": str(epub_path),
            "toc": [
                {"title": item.title, "src": item.src, "children": [{"title": c.title, "src": c.src} for c in item.children]}
                for item in toc_tree
            ],
            "chapters": chapters,
        }
        fulltext = "\n\n".join(part for part in fulltext_parts if part).strip() + "\n"

    (out_dir / f"{args.basename}_pages.json").write_text(json.dumps(pages_json, ensure_ascii=False, indent=2))
    (out_dir / f"{args.basename}_structured.json").write_text(json.dumps(structured_json, ensure_ascii=False, indent=2))
    (out_dir / f"{args.basename}_fulltext.txt").write_text(fulltext)


if __name__ == "__main__":
    main()
