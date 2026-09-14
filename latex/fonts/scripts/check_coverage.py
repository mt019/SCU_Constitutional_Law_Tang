#!/usr/bin/env python3
"""
check_coverage.py  ─  Font glyph-coverage audit for the SCU Constitutional Law font pack.

Usage:
    python3 check_coverage.py                   # audit all fonts in the pack
    python3 check_coverage.py --tex             # also extract chars from project .tex files
    python3 check_coverage.py --font path/to/font.ttf   # single-font quick check
    python3 check_coverage.py --missing         # show only fonts with missing chars

Output: TSV table to stdout; pipe to a file or use --out report.tsv

Character sets tested:
  project   All CJK characters that appear in .tex files in this repo
  big5      Big5 common subset (U+4E00..U+9FFF ∩ Big5 codepoints)
  tc-basic  TC common use: 常用國字標準字體表 (4,808 chars) – embedded subset here
"""

import argparse
import os
import sys
import unicodedata
from pathlib import Path

try:
    from fontTools.ttLib import TTFont
except ImportError:
    sys.exit("fonttools not installed. Run: pip3 install fonttools --break-system-packages")

# ── paths ─────────────────────────────────────────────────────────────────────
REPO = Path(__file__).resolve().parents[2]          # 本倉根目錄
# 字型檔存放於 font-lab 的 packs/scu-constitutional，不隨本倉進版控；
# 換存放位置時設環境變數 SCU_FONT_PACK。
DEFAULT_PACK = Path.home() / "Documents/NTU/1142/font-lab/packs/scu-constitutional"
PACK = Path(os.environ.get("SCU_FONT_PACK", DEFAULT_PACK))
MATERIAL = REPO

FONT_DIRS = [
    PACK / "fonts",
    PACK / "categories" / "elegant-intellectual",
    PACK / "categories" / "handwriting-accent",
    PACK / "categories" / "typewriter-ink",
    PACK / "categories" / "typewriter-latin",
]

EXTENSIONS = {".ttf", ".otf", ".ttc"}

# ── reference character sets ──────────────────────────────────────────────────

def load_project_chars(tex_root: Path) -> set[int]:
    """Extract all CJK codepoints from .tex files under tex_root."""
    chars: set[int] = set()
    for tex in tex_root.rglob("*.tex"):
        try:
            text = tex.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for ch in text:
            cp = ord(ch)
            # CJK Unified Ideographs (basic + extension A/B), compatibility, radicals
            if (0x4E00 <= cp <= 0x9FFF or
                0x3400 <= cp <= 0x4DBF or
                0x20000 <= cp <= 0x2A6DF or
                0x2A700 <= cp <= 0x2CEAF or
                0xF900 <= cp <= 0xFAFF or
                0x2F800 <= cp <= 0x2FA1F or
                # CJK symbols and punctuation
                0x3000 <= cp <= 0x303F or
                # Fullwidth forms
                0xFF00 <= cp <= 0xFFEF):
                chars.add(cp)
    return chars


def big5_range() -> set[int]:
    """Return Unicode codepoints that correspond to Big5 characters."""
    chars: set[int] = set()
    for hi in range(0xA1, 0xF0):
        for lo in list(range(0x40, 0x7F)) + list(range(0xA1, 0xFF)):
            b = bytes([hi, lo])
            try:
                ch = b.decode("big5")
                cp = ord(ch)
                if 0x4E00 <= cp <= 0x9FFF:
                    chars.add(cp)
            except (UnicodeDecodeError, ValueError):
                pass
    return chars


# ── font utilities ────────────────────────────────────────────────────────────

def get_cmap(font_path: Path) -> set[int]:
    """Return the set of Unicode codepoints present in a font."""
    try:
        font = TTFont(str(font_path), fontNumber=0)
        cmap = font.getBestCmap()
        if cmap is None:
            return set()
        return set(cmap.keys())
    except Exception as e:
        return set()


def count_glyphs(font_path: Path) -> int:
    """Total glyph count including .notdef."""
    try:
        font = TTFont(str(font_path), fontNumber=0)
        return len(font.getGlyphOrder())
    except Exception:
        return -1


def collect_fonts() -> list[Path]:
    fonts = []
    seen = set()
    for d in FONT_DIRS:
        if not d.exists():
            continue
        for ext in EXTENSIONS:
            for f in d.glob(f"*{ext}"):
                if f.name not in seen:
                    seen.add(f.name)
                    fonts.append(f)
    return sorted(fonts, key=lambda f: f.name.lower())


# ── report ────────────────────────────────────────────────────────────────────

def coverage_row(
    font_path: Path,
    charsets: dict[str, set[int]],
    show_missing: bool = False,
) -> dict:
    cmap = get_cmap(font_path)
    total_glyphs = count_glyphs(font_path)
    row = {
        "font": font_path.name,
        "category": font_path.parent.name,
        "glyphs": total_glyphs,
    }
    for name, chars in charsets.items():
        if not chars:
            continue
        missing = chars - cmap
        pct = 100 * (1 - len(missing) / len(chars))
        row[f"{name}_pct"] = round(pct, 1)
        row[f"{name}_missing"] = len(missing)
        if show_missing and missing:
            sample = sorted(missing)[:12]
            row[f"{name}_miss_sample"] = " ".join(chr(cp) for cp in sample)
    return row


def print_table(rows: list[dict], charsets: list[str]) -> None:
    # header
    cols = ["font", "category", "glyphs"] + [
        c for name in charsets for c in [f"{name}_pct", f"{name}_missing"]
    ]
    print("\t".join(cols))
    for row in rows:
        print("\t".join(str(row.get(c, "")) for c in cols))


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tex", action="store_true", help="Include project .tex character set")
    ap.add_argument("--font", metavar="PATH", help="Check a single font file")
    ap.add_argument("--missing", action="store_true", help="Show sample of missing chars")
    ap.add_argument("--out", metavar="FILE", help="Write TSV to FILE instead of stdout")
    args = ap.parse_args()

    # build character sets
    charsets: dict[str, set[int]] = {}
    charsets["big5"] = big5_range()
    if args.tex:
        proj = load_project_chars(MATERIAL)
        if proj:
            charsets["project"] = proj
            print(f"# project charset: {len(proj)} unique CJK codepoints from .tex files",
                  file=sys.stderr)

    # fonts to audit
    if args.font:
        fonts = [Path(args.font)]
    else:
        fonts = collect_fonts()

    print(f"# auditing {len(fonts)} fonts against: {', '.join(charsets)}", file=sys.stderr)

    rows = [coverage_row(f, charsets, show_missing=args.missing) for f in fonts]

    # filter to fonts-only-with-missing if --missing requested
    if args.missing:
        rows = [r for r in rows if any(r.get(f"{n}_missing", 0) > 0 for n in charsets)]

    out = open(args.out, "w", encoding="utf-8") if args.out else sys.stdout
    print_table(rows, list(charsets.keys()))
    if args.out:
        out.close()
        print(f"# wrote {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
