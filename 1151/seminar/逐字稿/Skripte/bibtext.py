#!/usr/bin/env python3
"""自 bib 檔產生 Notizen/bibtext.tsv（key、text），供 gen_tex.py --md-out 在站上頁的 footnote 印出書目。
用法：bibtext.py <bib>…  寫到 Notizen/bibtext.tsv。格式從簡：作者，〈篇名〉或《書名》，刊名 卷期，頁碼（年）；英文用斜體書名。"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).absolute().parents[1]
def entries(t):
    for m in re.finditer(r'@(\w+)\{([^,]+),(.*?)\n\}', t, re.S):
        f = dict((k.lower(), re.sub(r'[{}]', '', v).strip()) for k, v in re.findall(r'(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}', m.group(3)))
        yield m.group(1).lower(), m.group(2).strip(), f
out, seen = ['key\ttext'], set()
for b in sys.argv[1:]:
    for typ, key, f in entries(pathlib.Path(b).read_text(encoding='utf-8')):
        if key in seen: continue
        seen.add(key)
        zh = f.get('langid') == 'chinese'
        au = f.get('author') or f.get('editor', '')
        au = '、'.join(au.split(' and ')) if zh else '; '.join(au.split(' and '))
        ti = f.get('title', '')
        yr = f.get('year') or f.get('date', '')[:4]
        if typ in ('jurisdiction', 'legislation'):
            s = ti + (f'（{f["date"]}）' if f.get('date') else '')
        elif zh:
            ti = f'〈{ti}〉' if typ in ('article', 'incollection') else f'《{ti}》'
            jt = f.get('journaltitle', '')
            s = '，'.join(x for x in [au, ti, (f'《{jt}》' if jt else '') + (f'第 {f["number"]} 期' if f.get('number') else ''), (f'頁 {f["pages"]}' if f.get('pages') else ''), yr] if x)
        else:
            ti = f'“{ti}”' if typ in ('article', 'incollection') else f'*{ti}*'
            jt = f.get('journaltitle', '')
            s = ', '.join(x for x in [au, ti, ' '.join(y for y in [f.get('volume', ''), jt] if y), f.get('pages', ''), f'({yr})' if yr else ''] if x)
        out.append(f'{key}\t{s.replace(chr(9), " ").replace("--", "–")}')
(ROOT / 'Notizen' / 'bibtext.tsv').write_text('\n'.join(out) + '\n', encoding='utf-8')
print(len(out) - 1, 'entries')
