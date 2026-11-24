#!/usr/bin/env python3
"""把 Notizen/<週>/查核_*.tsv 判「改」的列套進 編註.tsv。用法：apply_audit.py <週> [改動 json]（七欄格式的查核表可省 json）
改動 json：{"列號": {"註": 新註文或省略, "出處": 新出處或省略, "引": 新引或省略}}；列號自表頭下一列算 1。
各「改」列都須出現在 json 裡（未套用者報錯），「未決」列列出不動。"""
import json, sys, pathlib
ROOT = pathlib.Path(__file__).absolute().parents[1]
nd = ROOT / 'Notizen' / sys.argv[1]
ch = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding='utf-8')) if len(sys.argv) > 2 else {}
lines = (nd / '編註.tsv').read_text(encoding='utf-8').splitlines()
head, rows = lines[0], [(l.split('\t') + [''] * 5)[:5] for l in lines[1:]]
want, pend = set(), []
for p in sorted(nd.glob('查核_*.tsv')):
    for l in p.read_text(encoding='utf-8').splitlines():
        c = l.split('\t')
        if len(c) > 1 and c[0].isdigit():
            if c[1].strip().startswith('改'):
                want.add(c[0])
                if len(c) >= 6 and c[0] not in ch:      # 七欄格式：列號 判定 新註 新出處 新引 缺什麼 依據
                    v = {k: c[i].strip() for k, i in (('註', 2), ('出處', 3), ('引', 4)) if c[i].strip()}
                    if v: ch[c[0]] = v
            elif c[1].strip().startswith('未決'): pend.append((c[0], c[2][:60]))
missing = want - set(ch)
assert not missing, f'判改而未給改法的列：{sorted(missing, key=int)}'
for k, v in ch.items():
    r = rows[int(k) - 1]
    for col, i in (('註', 2), ('出處', 3), ('引', 4)):
        if col in v: r[i] = v[col]
(nd / '編註.tsv').write_text('\n'.join([head] + ['\t'.join(r) for r in rows]) + '\n', encoding='utf-8')
print('套用', len(ch), '列；未決', pend)
