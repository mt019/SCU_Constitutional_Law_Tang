#!/usr/bin/env python3
"""找 whisper 重複解碼：cue 文字（去標點）與前 20 個 cue 之一逐字相同，且連續 3 個以上皆然者，列為刪除。
用法：find_loops.py <週>  → 寫 Notizen/<週>/drop.tsv（cue、理由）；單個、兩個相連的重複不刪（講者常自己重講一次）。"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).absolute().parents[1]
w = sys.argv[1]; nd = ROOT / 'Notizen' / w
rows = [l.split('\t', 3) for l in (nd / 'cues.tsv').read_text(encoding='utf-8').splitlines()[1:]]
t = [(int(r[0]), re.sub(r'[,，。？?！! ]', '', r[3])) for r in rows]
dup = []
for i, (k, s) in enumerate(t):
    if len(s) >= 6:
        for j in range(max(0, i - 20), i):
            if s == t[j][1]:
                dup.append((k, t[j][0])); break
runs, cur = [], []
for k, src in dup:
    if cur and k == cur[-1][0] + 1:
        cur.append((k, src))
    else:
        if len(cur) >= 3: runs.append(cur)
        cur = [(k, src)]
if len(cur) >= 3: runs.append(cur)
out = ['cue\treason'] + [f'{k}\t與 cue {src} 同文（連續 {len(r)} 個重複解碼）' for r in runs for k, src in r]
(nd / 'drop.tsv').write_text('\n'.join(out) + '\n', encoding='utf-8')
print(w, '刪', len(out) - 1, '個 cue；區段', [(r[0][0], r[-1][0]) for r in runs])
