#!/usr/bin/env python3
"""Extract full text and page metadata from a PDF.

Usage:
  . .venv/bin/activate
  python scripts/extract_pdf_text.py --pdf "path/to/file.pdf" --out-dir "path/to/output"
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from pypdf import PdfReader


def shortest_repeating_unit(token: str) -> str:
    n = len(token)
    for unit_len in range(1, (n // 2) + 1):
        if n % unit_len != 0:
            continue
        unit = token[:unit_len]
        if unit * (n // unit_len) == token:
            return unit
    return token


def normalize_token(token: str) -> str:
    token = shortest_repeating_unit(token)
    while True:
        new_token = re.sub(r"^([\u4e00-\u9fffA-Za-z])\1+(.*)$", r"\1\2", token)
        if new_token == token:
            break
        token = new_token
    return token


def collapse_spaced_character_repeats(text: str) -> str:
    patterns = [
        re.compile(r"([\u4e00-\u9fffA-Za-z])(?:\s*\1){1,}"),
        re.compile(r"([\u4e00-\u9fffA-Za-z]{2})(?:\s*\1){1,}"),
    ]
    changed = True
    while changed:
        changed = False
        for pattern in patterns:
            new_text = pattern.sub(r"\1", text)
            if new_text != text:
                text = new_text
                changed = True
    return text


def dedupe_repeated_tokens(line: str) -> str:
    tokens = line.split()
    if not tokens:
        return ""

    normalized: list[str] = []
    for token in tokens:
        token = normalize_token(token)
        if not token:
            continue

        if normalized:
            prev = normalized[-1]
            if token == prev:
                continue
            if len(prev) >= 2 and token.startswith(prev):
                token = normalize_token(token[len(prev) :])
                if not token or token == prev:
                    continue

        normalized.append(token)

    changed = True
    while changed and normalized:
        changed = False
        for seq_len in range(min(6, len(normalized) // 2), 0, -1):
            i = 0
            collapsed: list[str] = []
            while i < len(normalized):
                left = normalized[i : i + seq_len]
                right = normalized[i + seq_len : i + (2 * seq_len)]
                if left and left == right:
                    collapsed.extend(left)
                    i += 2 * seq_len
                    changed = True
                    while normalized[i : i + seq_len] == left:
                        i += seq_len
                    continue
                collapsed.append(normalized[i])
                i += 1
            normalized = collapsed
    return " ".join(normalized)


def collapse_adjacent_phrase_repeats(text: str) -> str:
    text = collapse_spaced_character_repeats(text)
    patterns = [
        re.compile(r"([\u4e00-\u9fffA-Za-z0-9]{2,30})(?:\s+\1)+"),
        re.compile(r"([\u4e00-\u9fffA-Za-z])(?:\s+\1)+"),
        re.compile(r"([，。、「」『』（）〔〕［］《》；：？！,.!?;:]{1,4})(?:\s*\1)+"),
    ]
    changed = True
    while changed:
        changed = False
        for pattern in patterns:
            new_text = pattern.sub(r"\1", text)
            if new_text != text:
                text = new_text
                changed = True
    return text


def clean_extracted_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = collapse_spaced_character_repeats(text)

    cleaned_lines: list[str] = []
    for raw_line in text.splitlines():
        line = dedupe_repeated_tokens(raw_line.strip())
        line = collapse_spaced_character_repeats(line)
        line = collapse_adjacent_phrase_repeats(line)
        cleaned_lines.append(line)

    cleaned = "\n".join(cleaned_lines)

    cleaned = collapse_spaced_character_repeats(cleaned)
    cleaned = collapse_adjacent_phrase_repeats(cleaned)
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip() + ("\n" if cleaned.strip() else "")


def merge_line_fragments(fragments: list[str]) -> str:
    merged: list[str] = []
    for frag in fragments:
        frag = clean_extracted_text(frag).strip()
        if not frag:
            continue
        if not merged:
            merged.append(frag)
            continue

        prev = merged[-1]
        if frag == prev:
            continue
        if len(prev) >= 2 and frag.startswith(prev):
            merged[-1] = frag
            continue
        if len(frag) >= 2 and prev.endswith(frag):
            continue
        merged.append(frag)

    line = " ".join(merged)
    line = collapse_adjacent_phrase_repeats(line)
    line = dedupe_repeated_tokens(line)
    line = collapse_adjacent_phrase_repeats(line)
    return line.strip()


def extract_page_text(page: Any) -> str:
    fragments: list[dict[str, Any]] = []

    def visitor(text: str, cm: list[float], tm: list[float], font_dict: Any, font_size: float) -> None:
        stripped = text.strip()
        if not stripped:
            return
        fragments.append(
            {
                "text": text.replace("\r\n", "\n").replace("\r", "\n").strip(),
                "x": float(tm[4]),
                "y": float(tm[5]),
                "font_size": float(font_size),
            }
        )

    page.extract_text(visitor_text=visitor)
    if not fragments:
        return ""

    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, int, int, int]] = set()
    for frag in fragments:
        key = (
            frag["text"],
            round(frag["x"]),
            round(frag["y"]),
            round(frag["font_size"]),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(frag)

    deduped.sort(key=lambda item: (-item["y"], item["x"]))

    line_groups: list[dict[str, Any]] = []
    for frag in deduped:
        target = None
        for group in line_groups:
            if abs(group["y"] - frag["y"]) <= max(2.5, frag["font_size"] * 0.25):
                target = group
                break
        if target is None:
            target = {"y": frag["y"], "items": []}
            line_groups.append(target)
        target["items"].append(frag)

    body_groups: list[dict[str, Any]] = []
    footnote_groups: list[dict[str, Any]] = []
    for group in line_groups:
        max_font = max(item["font_size"] for item in group["items"])
        if max_font <= 12.5:
            footnote_groups.append(group)
        else:
            body_groups.append(group)

    def groups_to_lines(groups: list[dict[str, Any]]) -> list[str]:
        groups.sort(key=lambda group: -group["y"])
        result: list[str] = []
        for group in groups:
            items = sorted(group["items"], key=lambda item: item["x"])
            line = merge_line_fragments([item["text"] for item in items])
            if line:
                result.append(line)
        return result

    lines = groups_to_lines(body_groups)
    footnotes = groups_to_lines(footnote_groups)

    text_parts: list[str] = []
    if lines:
        text_parts.append("\n".join(lines))
    if footnotes:
        text_parts.append("\n".join(footnotes))
    return clean_extracted_text("\n\n".join(text_parts))


def split_lines(text: str) -> list[str]:
    return [line for line in (ln.strip() for ln in text.splitlines()) if line]


def split_paragraphs(text: str) -> list[str]:
    parts: list[str] = []
    for chunk in re.split(r"\n\s*\n", text):
        para = " ".join(chunk.split()).strip()
        if para:
            parts.append(para)
    return parts


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--pdf", required=True, help="Path to input PDF")
    p.add_argument("--out-dir", required=True, help="Directory to write outputs")
    p.add_argument("--prefix", default=None, help="Output filename prefix")
    p.add_argument(
        "--write-page-files",
        action="store_true",
        help="Also write one text file per PDF page under out-dir/pages",
    )
    return p.parse_args()


def slugify(name: str) -> str:
    s = name.strip().lower().replace(" ", "_")
    s = re.sub(r"[^a-z0-9_\-.]+", "", s)
    return s or "pdf"


def main() -> None:
    args = parse_args()
    pdf_path = Path(args.pdf).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    prefix = args.prefix or slugify(pdf_path.stem)
    pages_dir = out_dir / "pages"
    if args.write_page_files:
        pages_dir.mkdir(exist_ok=True)

    reader = PdfReader(str(pdf_path))

    fulltext_file = out_dir / f"{prefix}_fulltext.txt"
    index_file = out_dir / f"{prefix}_page_index.csv"
    pages_json_file = out_dir / f"{prefix}_pages.json"

    chunks: list[str] = []
    chunks.append(f"# Source PDF\n{pdf_path.name}\n")
    chunks.append(f"# Total PDF pages\n{len(reader.pages)}\n")

    index_lines = ["pdf_page,chars,preview"]
    pages_payload: list[dict[str, object]] = []

    for i, page in enumerate(reader.pages, start=1):
        text = extract_page_text(page)

        if args.write_page_files:
            (pages_dir / f"page_{i:04d}.txt").write_text(text, encoding="utf-8")

        chunks.append(f"\n\n===== [PDF_PAGE_{i:04d}] =====\n\n")
        chunks.append(text)

        preview = " ".join(text.split())[:140].replace('"', "'")
        index_lines.append(f'{i},{len(text)},"{preview}"')
        page_item = {
            "pdf_page": i,
            "chars": len(text),
            "preview": preview,
            "text": text,
            "lines": split_lines(text),
            "paragraphs": split_paragraphs(text),
        }
        if args.write_page_files:
            page_item["source_file"] = f"page_{i:04d}.txt"
        pages_payload.append(page_item)

    fulltext_file.write_text("".join(chunks), encoding="utf-8")
    index_file.write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    pages_json_file.write_text(
        json.dumps(
            {
                "source_pdf": pdf_path.name,
                "total_pages": len(reader.pages),
                "pages": pages_payload,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"WROTE {fulltext_file}")
    print(f"WROTE {index_file}")
    print(f"WROTE {pages_json_file}")
    print(f"WROTE_PAGES {len(reader.pages)}")


if __name__ == "__main__":
    main()
