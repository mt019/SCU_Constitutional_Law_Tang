#!/usr/bin/env python3
r"""由各章產生附錄「各節出處一覽」（Teile/A2_sources.tex）。

自 phenom-court-data docs/tex/scripts/build_sources.py 改寫（2026-11-09）。本預習問答集不以 \qaentry 分則，
改以 \section 為單位，依部（\chapter）分組：

- 本文：第二至第四部各節先列該部所讀之本文，頁次取該節標題 \pg{} 所記之範圍。
- 另引文獻：該節內 \footcite 一族的鍵與頁碼，依首次引用之序，頁碼原樣去重。

每節以 \label{sec:...} 指回正文（緊接 \section 之下一行），缺標籤者報錯，不寫檔。產出檔整份重寫，勿手改。

用法：python3 -I tools/build_sources.py [--check]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "W09_司法至上_預習.tex"
OUT = ROOT / "Teile" / "A2_sources.tex"

CITE = re.compile(r"\\(?:foot)?(?:cite|textcite|parencite)\*?((?:\[[^\]]*\]){0,2})\{([^}]+)\}")
MULTICITE = re.compile(r"\\(?:foot|paren|text)?cites\*?((?:\s*(?:\[[^\]]*\]|\{[^}]*\}))+)")
IX = re.compile(r"\\ix\{[a-z]+\}\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}")
PG = re.compile(r"\\pg\{([^{}]*)\}")
BASE = {"20_AS": "alexander2000", "30_Kramer": "kramer2012", "40_FP": "ferejohn2002"}
BRACED = r"\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}"


def chapters():
    names = re.findall(r"\\input\{Teile/([1-5]\d_[^}]+)\}", MAIN.read_text())
    return [ROOT / "Teile" / f"{n}.tex" for n in names]


def clean(title):
    title = IX.sub("", title)
    return PG.sub("", title).strip()


def cites(part):
    pairs = []
    for m in CITE.finditer(part):
        loc = re.findall(r"\[([^\]]*)\]", m.group(1))
        pairs.append((m.start(), loc[-1].strip() if loc else "", m.group(2)))
    for m in MULTICITE.finditer(part):
        for g in re.finditer(r"((?:\[[^\]]*\])*)\{([^}]*)\}", m.group(1)):
            loc = re.findall(r"\[([^\]]*)\]", g.group(1))
            pairs.append((m.start() + g.start(), loc[-1].strip() if loc else "", g.group(2)))
    found = {}
    for _, loc, keys in sorted(pairs):
        for k in (k.strip() for k in keys.split(",")):
            found.setdefault(k, [])
            if loc and loc not in found[k]:
                found[k].append(loc)
    return found


def render(key, locs):
    return f"\\citeauthor{{{key}}}，\\citetitle{{{key}}}" + ("，" + "；".join(locs) if locs else "")


def main():
    rows, nsec, nsrc = [], 0, 0
    for path in chapters():
        text = IX.sub("", path.read_text())
        ch = re.search(r"^\\chapter" + BRACED, text, re.M)
        rows.append(rf"\multicolumn{{3}}{{@{{}}l}}{{{clean(ch.group(1))}}} \\* \addlinespace[2pt]")
        for part in re.split(r"(?m)^(?=\\section\{)", text)[1:]:
            head = re.match(r"\\section" + BRACED, part)
            label = re.match(r"\\section" + BRACED + r"\s*\n\\label\{(sec:[^}]+)\}", part)
            if not (head and label):
                sys.exit(f"{path.name}：{part.splitlines()[0][:60]} 缺 sec: 標籤")
            pg = PG.search(head.group(1))
            found = cites(part)
            base = BASE.get(path.stem)
            if base and pg:
                rng = re.sub(r"(\d+) 至 (\d+)", r"\1--\2", pg.group(1)).replace(" 頁", "")
                found = {base: [rng] + [l for l in found.pop(base, []) if l != rng], **found}
            srcs = [render(k, v) for k, v in found.items()]
            nsec += 1
            nsrc += len(srcs)
            cell = " \\newline ".join(srcs) if srcs else "---"
            rows.append(f"\\ref{{{label.group(2)}}} & {clean(head.group(1))} & {cell} \\\\")
        rows.append(r"\addlinespace[6pt]")
    if "--check" in sys.argv:
        print(f"{nsec} 節，出處 {nsrc} 筆")
        return
    OUT.write_text(HEADER + "\n".join(rows) + "\n" + FOOTER)
    print(f"A2_sources.tex：{nsec} 節，出處 {nsrc} 筆")


HEADER = r"""% 本檔由 tools/build_sources.py 自各章產生，每次建置整份重寫，不要手改。
\chapter{各節出處一覽}
\label{app:sources}

表~\ref{tab:sources}依各部之序，列出各節所據之出處：第二至第四部各節先列該部所讀之本文及該節所述之刊本頁次，其次為該節另引之文獻，依第一次引用之先後排列，頁碼照該節所引。完整書目見參考文獻。

\begin{small}\setstretch{1.3}
\setlength{\LTpre}{6pt}
\def\LTcaptype{table}
\begin{longtable}{@{}>{\raggedright\arraybackslash}p{10mm}>{\raggedright\arraybackslash}p{62mm}>{\raggedright\arraybackslash}p{\dimexpr\linewidth-72mm-4\tabcolsep\relax}@{}}
\caption{各節之出處}\label{tab:sources}\\
\toprule
節 & 標題 & 出處 \\
\midrule
\endfirsthead
\toprule
節 & 標題 & 出處 \\
\midrule
\endhead
\bottomrule
\endlastfoot
"""

FOOTER = r"""\end{longtable}
\end{small}
"""

if __name__ == "__main__":
    main()
