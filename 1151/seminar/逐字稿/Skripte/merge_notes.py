#!/usr/bin/env python3
"""合併 Notizen/<週>/編註_*.tsv 成 編註.tsv：依 cue 排序，同詞留首見。用法：merge_notes.py <週>"""
import sys, pathlib
ROOT = pathlib.Path(__file__).absolute().parents[1]
nd = ROOT / 'Notizen' / sys.argv[1]
rows, seen, dropped = [], set(), []
for p in sorted(nd.glob('編註_*.tsv')):
    for l in p.read_text(encoding='utf-8').splitlines():
        if not l.strip() or l.startswith('#') or l.startswith('cue\t'):
            continue
        r = (l.split('\t') + [''] * 5)[:5]
        rows.append((int(r[0]), p.stem, r))
rows.sort(key=lambda x: x[0])
out = ['cue\t詞\t註\t出處\t引']
for k, src, r in rows:
    if r[1] in seen:
        dropped.append(f'{src} cue {k} {r[1]}'); continue
    seen.add(r[1]); out.append('\t'.join(r))
(nd / '編註.tsv').write_text('\n'.join(out) + '\n', encoding='utf-8')
print(len(out) - 1, '條；去重', len(dropped), dropped)
