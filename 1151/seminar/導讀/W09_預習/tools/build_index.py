#!/usr/bin/env python3
r"""依 index-terms.tsv 在各章（Teile/[1-5]*.tex）插入索引標記 \ix{索引}{詞條}，並產生互見表。

自 phenom-court-data docs/tex/scripts/build_terms.py 改寫（2026-11-09）。四份索引：
  terms     名詞，兩層：上位概念（依 tsv 的 class 欄先後）、詞
  statutes  法規，三層：法域、法規名稱、條次
  cases     裁判，三層：法域、法院、案名或字號；釋字與憲判字號由正規式自正文抓
  persons   人名，一層，依姓之字母
法域之序同時適用於法規與裁判：依 LAWORDER，其次依 tsv 出現之序。

同一節（\chapter、\section、\subsection 至下一個）內，同一詞只標第一次出現處。不標的位置：註解行、
章節標題行、\caption 行、引註與 \ref、\label、\url 的參數、數學式內。ASCII 比對字串前後不得接英文字母，
免得 Hart 標到 Hartnett。

產出 Teile/90_index_xref.tex（「見」「參見」）。每次先移除舊標記再重插；--strip 只移除。
標記移除後與插入前逐字相同，否則不寫檔。

用法：python3 -I tools/build_index.py [--strip]
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TSV = ROOT / "index-terms.tsv"
FILES = sorted((ROOT / "Teile").glob("[1-5][0-9]_*.tex"))
XREF = ROOT / "Teile" / "90_index_xref.tex"
TAG = re.compile(r"\\ix\{(?:terms|statutes|cases|persons)\}\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}")
LAWORDER = ["中華民國", "美國", "法國", "義大利", "希臘"]
SKIPLINE = re.compile(r"^\\(?:chapter|section|subsection|subsubsection|caption)\b|^%")
RESET = re.compile(r"^\\(?:chapter|section|subsection)\b")
EXCL = re.compile(
    r"\\footcites?(?:\[[^\]]*\]|\{[^}]*\})+"
    r"|\\(?:ref|label|url|pageref|href|texorpdfstring)\{[^}]*\}(?:\{[^}]*\})?"
    r"|\$[^$]*\$"
    r"|\\[A-Za-z]+")


def load():
    with TSV.open() as f:
        rows = list(csv.DictReader((l for l in f if not l.startswith("#")), delimiter="\t"))
    for r in rows:
        for k in ("kind", "class", "display", "sort", "patterns", "see"):
            r[k] = (r.get(k) or "").strip()
    return rows


def esc(s):
    return s.replace('"', '""').replace("!", '"!').replace("@", '"@').replace("|", '"|')


def ordered(seq):
    out = []
    for x in seq:
        if x not in out:
            out.append(x)
    return out


class Keys:
    """排序鍵：名詞類、法域、法規、法院依出現之序編號。"""

    def __init__(self, rows):
        self.classes = ordered(r["class"] for r in rows if r["kind"] == "term")
        doms = ordered(r["class"].split("|")[0] for r in rows if r["kind"] in ("law", "case"))
        doms = ordered(["中華民國"] + doms)
        self.doms = sorted(doms, key=lambda d: (LAWORDER.index(d) if d in LAWORDER else 99, doms.index(d)))
        self.sub = {}
        for r in rows:
            if r["kind"] in ("law", "case"):
                d, s = r["class"].split("|")
                self.sub.setdefault((r["kind"], d), [])
                if s not in self.sub[(r["kind"], d)]:
                    self.sub[(r["kind"], d)].append(s)
        for s in ("司法院大法官", "憲法法庭"):
            self.sub.setdefault(("case", "中華民國"), [])
            if s not in self.sub[("case", "中華民國")]:
                self.sub[("case", "中華民國")].insert(0 if s == "司法院大法官" else 1, s)

    def term(self, cls, disp):
        return f"{self.classes.index(cls) + 1:02d}@\\zhlidxcat{{{esc(cls)}}}!{esc(disp)}"

    def head(self, kind, cls):
        d, s = cls.split("|")
        di = self.doms.index(d) + 1
        si = self.sub[(kind, d)].index(s) + 1
        return f"{di:02d}@{esc(d)}!{si:02d}@{esc(s)}"


def art_key(disp):
    n = int(re.search(r"\d+", disp).group())
    return f"{(100 if '增修' in disp else 0) + n:03d}"


def build_patterns(rows, K):
    pats = []  # (pattern, key, marker)
    for r in rows:
        if r["see"].startswith("see:"):
            continue
        plist = [p for p in (r["patterns"] or r["display"]).split(";") if p]
        k = r["kind"]
        if k == "term":
            marker = rf"\ix{{terms}}{{{K.term(r['class'], r['display'])}}}"
        elif k == "person":
            marker = rf"\ix{{persons}}{{{esc((r['sort'] or r['display']).lower())}@{esc(r['display'])}}}"
        elif k == "law":
            h = K.head("law", r["class"])
            marker = (rf"\ix{{statutes}}{{{h}!{art_key(r['display'])}@{esc(r['display'])}}}"
                      if r["display"] else rf"\ix{{statutes}}{{{h}}}")
        elif k == "case":
            h = K.head("case", r["class"])
            marker = rf"\ix{{cases}}{{{h}!{r['sort']}{esc(r['display'])}@{esc(r['display'])}}}"
        else:
            sys.exit(f"index-terms.tsv：未知的 kind {k}")
        key = (k, r["class"], r["display"])
        for p in plist:
            pats.append((p, key, marker))
    pats.sort(key=lambda t: -len(t[0]))
    return pats


SHIZI = re.compile(r"釋字第 (\d+(?:、\d+)*) 號")
XIANPAN = re.compile(r"(\d{3}) 年憲判字第 (\d+) 號")


def case_marks(line, K):
    out = []
    for m in XIANPAN.finditer(line):
        y, n = int(m.group(1)), int(m.group(2))
        h = K.head("case", "中華民國|憲法法庭")
        out.append((m.end(), ("case", "x", f"{y}-{n}"),
                    rf"\ix{{cases}}{{{h}!{y:03d}{n:03d}@{y} 年憲判字第 {n} 號}}"))
    for m in SHIZI.finditer(line):
        h = K.head("case", "中華民國|司法院大法官")
        for n in m.group(1).split("、"):
            n = int(n)
            out.append((m.end(), ("case", "s", n), rf"\ix{{cases}}{{{h}!{n:04d}@釋字第 {n} 號}}"))
    return out


def finder(p):
    if p.isascii():
        return re.compile(r"(?<![A-Za-z])" + re.escape(p) + r"(?![A-Za-z])")
    return re.compile(re.escape(p))


def tag_file(text, pats, K, seen_all, stats):
    lines = text.split("\n")
    seen = set()
    comp = {p: finder(p) for p, _, _ in pats}
    for i, line in enumerate(lines):
        if RESET.match(line):
            seen = set()
        if SKIPLINE.match(line) or not line.strip():
            continue
        excl = [m.span() for m in EXCL.finditer(line)]

        def bad(a, b):
            return any(x < b and a < y for x, y in excl)

        ins, taken = [], []
        for p, key, marker in pats:
            if key in seen:
                continue
            for m in comp[p].finditer(line):
                k, e = m.span()
                if not bad(k, e) and not any(x < e and k < y for x, y in taken):
                    ins.append((e, marker))
                    taken.append((k, e))
                    seen.add(key)
                    seen_all.add(key)
                    stats[key[0]] = stats.get(key[0], 0) + 1
                    break
        for pos, key, marker in case_marks(line, K):
            if key in seen or bad(pos - 1, pos):
                continue
            ins.append((pos, marker))
            seen.add(key)
            seen_all.add(key)
            stats["case"] = stats.get("case", 0) + 1
        for pos, marker in sorted(ins, key=lambda t: t[0], reverse=True):
            line = line[:pos] + marker + line[pos:]
        lines[i] = line
    return "\n".join(lines)


def main():
    rows = load()
    K = Keys(rows)
    if "--strip" in sys.argv:
        n = 0
        for f in FILES:
            s, k = TAG.subn("", f.read_text())
            f.write_text(s)
            n += k
        XREF.write_text("% 由 tools/build_index.py 產生，勿手改。（標記已移除）\n")
        print(f"移除索引標記 {n} 處")
        return
    pats = build_patterns(rows, K)
    seen_all, stats, out = set(), {}, []
    for f in FILES:
        orig = TAG.sub("", f.read_text())
        new = tag_file(orig, pats, K, seen_all, stats)
        if TAG.sub("", new) != orig:
            sys.exit(f"{f.name}：移除標記後與原文不一致，未寫入")
        out.append((f, new))

    known = {r["display"] for r in rows if r["kind"] == "term" and not r["see"].startswith("see:")}
    xr = ["% 由 tools/build_index.py 自 index-terms.tsv 產生，勿手改。"]
    for r in rows:
        if r["kind"] != "term" or not r["see"]:
            continue
        kind, _, targets = r["see"].partition(":")
        for t in targets.split(";"):
            if t not in known:
                sys.exit(f"index-terms.tsv：{r['display']} 的 {kind} 指向不存在之詞 {t}")
        head = K.term(r["class"], r["display"])
        if kind == "see":
            xr.append(rf"\ix{{terms}}{{{head}|see{{{targets}}}}}")
        elif kind == "seealso" and ("term", r["class"], r["display"]) in seen_all:
            xr.append(rf"\ix{{terms}}{{{head}|seealso{{{targets.replace(';', '、')}}}}}")

    per_class = {c: sum(1 for r in rows if r["kind"] == "term" and r["class"] == c
                        and ("term", c, r["display"]) in seen_all) for c in K.classes}
    thin = [c for c, n in per_class.items() if n < 2]
    if thin:
        sys.exit(f"名詞索引有類少於兩詞：{thin}")
    for f, new in out:
        f.write_text(new)
    XREF.write_text("\n".join(xr) + "\n")

    unmatched = [r["display"] for r in rows if not r["see"].startswith("see:")
                 and (r["kind"], r["class"], r["display"]) not in seen_all]
    print(f"索引標記：名詞 {stats.get('term', 0)} 處（{sum(per_class.values())} 詞，{len(K.classes)} 類）、"
          f"法規 {stats.get('law', 0)} 處、裁判 {stats.get('case', 0)} 處、人名 {stats.get('person', 0)} 處；"
          f"互見 {len(xr) - 1} 項")
    print("名詞各類：" + "；".join(f"{c} {n}" for c, n in per_class.items()))
    if unmatched:
        print("index-terms.tsv 中正文未出現者：" + "、".join(unmatched))


if __name__ == "__main__":
    main()
