#!/usr/bin/env python3
"""檢查一週的編註表 Notizen/<週>/編註.tsv。

用法：check_notes.py <週> [--srt <reviewed.srt>]
查：cue 存在；詞逐字出現在該 cue 的校訂後文字（預設讀 Notizen/<週>/reviewed.tsv，由 gen_tex.py --cues-out 產生）；
同表同詞不重複；註文不含 { } \\ % # $ & _；出處每一項為網址或本機存在的檔（相對於倉根或絕對路徑）；
註文含西元年份者出處須有網址、本機檔或「引」欄；引欄的 bib 鍵須在 ../課程問答/refs.bib。
退出碼：0 通過，1 有錯。
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).absolute().parents[1]
REPO = ROOT.parents[2]


def main():
    week = sys.argv[1]
    nd = ROOT / 'Notizen' / week
    text = {}
    for line in (nd / 'reviewed.tsv').read_text(encoding='utf-8').splitlines()[1:]:
        k, _, _, t = line.split('\t', 3)
        text[int(k)] = t
    bib = set()
    for bibfile in (ROOT / 'refs.bib', ROOT.parent / '課程問答' / 'refs.bib', ROOT.parent / '導讀' / 'W06_Waldron' / 'refs.bib'):
        if bibfile.exists():
            bib |= set(re.findall(r'^@\w+\{([^,]+),', bibfile.read_text(encoding='utf-8'), re.M))
    errs, seen = [], set()
    rows = [l.split('\t') for l in (nd / '編註.tsv').read_text(encoding='utf-8').splitlines() if l and not l.startswith('#')]
    if rows and rows[0][0] == 'cue':
        rows = rows[1:]
    for i, r in enumerate(rows, 2):
        r += [''] * (5 - len(r))
        cue, word, note, src, cite = r[:5]
        where = f'第 {i} 列 cue {cue}「{word}」'
        if not cue.isdigit() or int(cue) not in text:
            errs.append(f'{where}：cue 不存在'); continue
        if word not in text[int(cue)]:
            errs.append(f'{where}：詞不在該 cue')
        if word in seen:
            errs.append(f'{where}：同表重複')
        seen.add(word)
        if re.search(r'[{}\\%#$&_]', note):
            errs.append(f'{where}：註文含 TeX 特殊字元')
        ok_src = False
        for s in [x.strip() for x in re.split(r' ; |；', src) if x.strip()]:
            if s.startswith('http'):
                ok_src = True
            else:
                p = pathlib.Path(s.split('#')[0].split(':')[0])
                if not p.is_absolute():
                    p = REPO / p
                if p.exists():
                    ok_src = True
                else:
                    errs.append(f'{where}：出處檔不存在 {s}')
        key = cite.partition('|')[0]
        if key and key not in bib:
            errs.append(f'{where}：bib 鍵 {key} 不在 refs.bib')
        if not (ok_src or key):
            errs.append(f'{where}：無出處')
    print(f'{len(rows)} 條；錯誤 {len(errs)}')
    for e in errs:
        print('  ' + e)
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main()
