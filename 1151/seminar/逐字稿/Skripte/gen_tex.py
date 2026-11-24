#!/usr/bin/env python3
"""一週課堂逐字稿：cue 表＋校訂表＋斷句表＋說話人表＋編註表 → Teile/<週>.tex 與 reviewed.srt。

用法：gen_tex.py <週> [--srt-out <路徑>] [--force]
  <週> 形如 W01_0914，材料在 Notizen/<週>/：
    cues.tsv                 cue、start、end、text（make_cues.py 產出，只讀）
    chunk*.edits.tsv         cue、before、after、basis
    chunk*.breaks.tsv        cue、end、para（1 或 S）、title
    chunk*.speakers.tsv      cue、speaker、split
    編註.tsv                 cue、詞、註、出處、引（bib 鍵，可帶頁碼：key|頁碼）
    meta.tsv                 key、value：title（章名）、date、course、label（hypertarget 前綴，如 w01）
產物：Teile/<週>.tex（已存在而未給 --force 時拒絕覆蓋）、--srt-out 給的 reviewed srt。
每處替換都斷言 before 在該 cue 內恰出現一次；編註的「詞」須在該 cue 內出現。
"""
import csv, re, sys, pathlib, argparse, urllib.parse

ROOT = pathlib.Path(__file__).absolute().parents[1]
CJK = r'[　-〿㐀-鿿＀-￯]'


def read_tsv(p, cols):
    rows = []
    if not p.exists():
        return rows
    for line in p.read_text(encoding='utf-8').splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        parts = line.split('\t')
        if parts[0] == cols[0]:
            continue
        parts += [''] * (len(cols) - len(parts))
        rows.append(dict(zip(cols, parts)))
    return rows


def fullwidth(s):
    s = re.sub(r'[,，]\s*。', '，', s)          # W02 之 srt 句末多為「,。」，視為逗號；句末標點由 breaks 表定
    s = re.sub(r'[,，]\s*([？！])', r'\1', s)
    s = re.sub(rf'(?<={CJK}),\s*|,\s*(?={CJK})', '，', s)
    s = re.sub(rf'(?<={CJK})\?|\?(?={CJK})|(?<={CJK})\?$', '？', s)
    s = re.sub(rf'(?<={CJK})!|!(?={CJK})', '！', s)
    s = re.sub(rf'(?<={CJK}):\s*', '：', s)
    s = re.sub(rf'(?<={CJK});\s*', '；', s)
    return s


TEX_SPECIAL = {'&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_',
               '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}',
               '\\': r'\textbackslash{}'}


def tex(s):
    return ''.join(TEX_SPECIAL.get(ch, ch) for ch in s)


def hms(t):
    t = int(t)
    return f'{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}'


def srt_ts(t):
    ms = round(t * 1000)
    return f'{ms // 3600000:02d}:{ms % 3600000 // 60000:02d}:{ms % 60000 // 1000:02d},{ms % 1000:03d}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('week')
    ap.add_argument('--srt-out')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--md-out', help='MkDocs 頁：段首時間碼錨點、編註為 footnote')
    a = ap.parse_args()
    nd = ROOT / 'Notizen' / a.week
    cues = read_tsv(nd / 'cues.tsv', ['cue', 'start', 'end', 'text'])
    text = {int(c['cue']): c['text'] for c in cues}
    times = {int(c['cue']): (float(c['start']), float(c['end'])) for c in cues}
    meta = {r['key']: r['value'] for r in read_tsv(nd / 'meta.tsv', ['key', 'value'])}
    label = meta.get('label', a.week.split('_')[0].lower())

    # 〇、刪去的重複解碼（find_loops.py 產生的 drop.tsv）
    drops = {int(r['cue']): r['reason'] for f in ('drop.tsv', 'drop.manual.tsv') for r in read_tsv(nd / f, ['cue', 'reason'])}

    # 一、校訂
    n_edit = 0
    for p in sorted(nd.glob('*.edits.tsv')):
        for r in read_tsv(p, ['cue', 'before', 'after', 'basis']):
            k = int(r['cue'])
            cnt = text[k].count(r['before'])
            assert cnt == 1, f'{p.name} cue {k}：「{r["before"]}」出現 {cnt} 次'
            text[k] = text[k].replace(r['before'], r['after'])
            n_edit += 1
    # 全書人名與用語對照（Notizen/names.tsv：wrong、right、basis），套在各週校訂之後
    for r in read_tsv(ROOT / 'Notizen' / 'names.tsv', ['wrong', 'right', 'basis']):
        for k in text:
            if r['wrong'] in text[k]:
                text[k] = text[k].replace(r['wrong'], r['right']); n_edit += 1
    for k in text:
        text[k] = fullwidth(text[k]).strip()

    # 二、斷句與說話人
    ends, paras, titles = {}, set(), {}
    for p in sorted(nd.glob('*.breaks.tsv')):
        for r in read_tsv(p, ['cue', 'end', 'para', 'title']):
            k = int(r['cue'])
            if r['end']:
                ends[k] = r['end']
            if r['para'] in ('1', 'S'):
                paras.add(k)
            if r['para'] == 'S':
                titles[k] = r['title'].strip()
    speakers = {}
    splits = {}
    for p in sorted(nd.glob('chunk*.speakers.tsv')):
        for r in read_tsv(p, ['cue', 'speaker', 'split']):
            k = int(r['cue'])
            if r['split']:
                splits.setdefault(k, []).append((r['split'], r['speaker']))
            else:
                speakers[k] = r['speaker']
    for k, e in ends.items():
        t = text[k].rstrip('，。？！,.?!')
        text[k] = t if e == '0' else t + e

    # 三、編註
    notes = {}
    for r in read_tsv(nd / '編註.tsv', ['cue', '詞', '註', '出處', '引']):
        notes.setdefault(int(r['cue']), []).append(r)

    def render_cue(k):
        s = text[k]
        marks = []
        for r in notes.get(k, []):
            pos = s.find(r['詞'])
            assert pos >= 0, f'編註 cue {k}：「{r["詞"]}」不在該 cue 內'
            marks.append((pos + len(r['詞']), r))
        out, last = [], 0
        for pos, r in sorted(marks, key=lambda x: x[0]):
            out.append(tex(s[last:pos]))
            body = tex(r['註'])
            if r['引']:
                key, _, post = r['引'].partition('|')
                body += f'\\cite[{post}]{{{key}}}。' if post else f'\\cite{{{key}}}。'
            elif r['出處'].startswith('http'):
                raw = r['出處'].split(' ; ')[0]
                link = urllib.parse.quote(urllib.parse.unquote(raw), safe=':/?&=#+@!$,;~*()')
                link = link.replace('%', '\\%').replace('#', '\\#')
                shown = urllib.parse.unquote(raw)
                if shown.isascii():
                    body += f'\\url{{{link}}}。'
                else:                  # \url 排不了中文：連結保留編碼，顯示解碼後的文字
                    body += f'\\href{{{link}}}{{\\nolinkurl{{{tex(shown)}}}}}。' if False else f'\\href{{{link}}}{{{tex(shown)}}}。'
            out.append(f'\\footnote{{{body}}}')
            last = pos
        out.append(tex(s[last:]))
        body = ''.join(out)
        for frag, spk in splits.get(k, []):
            i = body.find(tex(frag))
            assert i >= 0, f'split cue {k}：「{frag}」不在該 cue 內'
            body = body[:i] + f'\\par\\speaker{{{tex(spk)}}}' + body[i:]
        return body

    md_notes = []

    def render_md(k):
        s = text[k]
        marks = []
        for r in notes.get(k, []):
            marks.append((s.find(r['詞']) + len(r['詞']), r))
        out, last = [], 0
        for pos, r in sorted(marks, key=lambda x: x[0]):
            out.append(s[last:pos])
            body = r['註']
            if r['引']:
                key, _, post = r['引'].partition('|')
                body += f'見 {bibtext.get(key, key)}' + (f'，{post}' if post else '') + '。'
            elif r['出處'].startswith('http'):
                body += f"<{r['出處'].split(' ; ')[0]}>。"
            md_notes.append(body)
            out.append(f'[^{len(md_notes)}]')
            last = pos
        out.append(s[last:])
        body = ''.join(out)
        for frag, spk in splits.get(k, []):
            i = body.find(frag)
            body = body[:i] + f'\n\n**{spk}**：' + body[i:]
        return body

    bibtext = {}
    for r in read_tsv(ROOT / 'Notizen' / 'bibtext.tsv', ['key', 'text']):
        bibtext[r['key']] = r['text']

    lines = [f'% 自 Notizen/{a.week}/ 各表由 Skripte/gen_tex.py 產生；改字改表後重產，不手改本檔。',
             f'\\chapter{{{meta.get("title", a.week)}}}', '']
    if meta.get('intro'):
        lines += [meta['intro'], '']
    front = ['---', f"title: {meta.get('md_title', meta.get('title', a.week))}"]
    for key in ('summary', 'description'):
        if meta.get('md_' + key):
            front.append(f"{key}: {meta['md_' + key]}")
    front.append('---')
    md = front + ['', f"# {meta.get('md_title', meta.get('title', a.week))}", '', meta.get('intro_md', meta.get('intro', '')), '']
    cur = '老師'
    order = sorted(text)
    if order[0] not in titles:
        titles[order[0]] = meta.get('first_section', '開場')
    paras.add(order[0])
    for k in sorted(drops):            # 刪去的 cue 若是段首或節首，移到下一個 cue
        if k in titles and k + 1 not in titles:
            titles[k + 1] = titles.pop(k)
        if k in paras:
            paras.add(k + 1)
    for k in order:
        st, en = times[k]
        if k in drops:
            lines.append(f'% cue {k} {st:.3f} {en:.3f} 刪：{drops[k]}')
            continue
        newspk = speakers.get(k)
        if k in titles:
            lines += ['', f'\\section{{{tex(titles[k])}}}']
            md += ['', f'## {titles[k]}']
        if k in paras or (newspk and newspk != cur):
            lines += ['', f'\\tc{{{hms(st)}}}']
            md += ['', f'<a id="c{k}"></a><span class="tc">{hms(st)}</span> ']
            if newspk:
                cur = newspk
            if cur != '老師' or newspk:
                lines.append(f'\\speaker{{{tex(cur)}}}')
                md[-1] += f'**{cur}**：'
        lines.append(f'% cue {k} {st:.3f} {en:.3f}')
        lines.append(f'\\hypertarget{{{label}:cue:{k}}}{{}}{render_cue(k)}')
        piece = render_md(k)
        if md[-1] and re.match(r'[A-Za-z0-9(]', piece) and re.search(r'[A-Za-z0-9.,;:)]$', md[-1]):
            md[-1] += ' '
        md[-1] += piece
        if splits.get(k):
            cur = splits[k][-1][1]
    (nd / 'reviewed.tsv').write_text('cue\tstart\tend\ttext\n' + ''.join(
        f'{k}\t{times[k][0]:.3f}\t{times[k][1]:.3f}\t{text[k]}\n' for k in order), encoding='utf-8')
    out = ROOT / 'Teile' / f'{a.week}.tex'
    if out.exists() and not a.force:
        sys.exit(f'{out} 已存在；確定重產加 --force')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    if a.md_out:
        md += [''] + [f'[^{i}]: {b}' for i, b in enumerate(md_notes, 1)]
        pathlib.Path(a.md_out).write_text('\n'.join(md) + '\n', encoding='utf-8')
    if a.srt_out:
        blocks = [f'{k}\n{srt_ts(times[k][0])} --> {srt_ts(times[k][1])}\n{text[k]}\n' for k in order if k not in drops]
        pathlib.Path(a.srt_out).write_text('\n'.join(blocks), encoding='utf-8')
    print(f'{out.relative_to(ROOT)}：{len(order)} cue，替換 {n_edit} 處，段 {len(paras)}，節 {len(titles)}，'
          f'說話人標記 {len(speakers) + sum(map(len, splits.values()))}，編註 {sum(map(len, notes.values()))}')


if __name__ == '__main__':
    main()
