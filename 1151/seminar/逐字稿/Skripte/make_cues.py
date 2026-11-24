#!/usr/bin/env python3
"""srt → cue 表（cue, start, end, text）並依 cue 切成 N 份，供校訂 agent 分段讀。
用法：make_cues.py <srt> <輸出目錄> [份數=6]
產物：<輸出目錄>/cues.tsv、chunk1.tsv … chunkN.tsv（各份字數約略相等）。"""
import re, sys, pathlib
def ts(s):
    h, m, rest = s.split(':'); sec, ms = rest.split(',')
    return int(h)*3600 + int(m)*60 + int(sec) + int(ms)/1000
def read_srt(p):
    out = []
    for blk in re.split(r'\n\s*\n', pathlib.Path(p).read_text(encoding='utf-8').strip()):
        lines = blk.strip().split('\n')
        if len(lines) < 2: continue
        a, b = [x.strip() for x in lines[1].split('-->')]
        out.append((int(lines[0]), ts(a), ts(b), ' '.join(lines[2:]).strip()))
    return out
if __name__ == '__main__':
    srt, outdir = sys.argv[1], pathlib.Path(sys.argv[2]); n = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    cues = read_srt(srt); outdir.mkdir(parents=True, exist_ok=True)
    assert [c[0] for c in cues] == list(range(1, len(cues)+1)), 'cue 編號不連續'
    row = lambda c: f'{c[0]}\t{c[1]:.3f}\t{c[2]:.3f}\t{c[3]}\n'
    (outdir/'cues.tsv').write_text('cue\tstart\tend\ttext\n' + ''.join(map(row, cues)), encoding='utf-8')
    total = sum(len(c[3]) for c in cues); acc = 0; k = 1; buf = []
    for c in cues:
        buf.append(c); acc += len(c[3])
        if acc >= total*k/n and k < n:
            (outdir/f'chunk{k}.tsv').write_text('cue\tstart\tend\ttext\n' + ''.join(map(row, buf)), encoding='utf-8'); k += 1; buf = []
    (outdir/f'chunk{k}.tsv').write_text('cue\tstart\tend\ttext\n' + ''.join(map(row, buf)), encoding='utf-8')
    print(len(cues), 'cues,', total, 'chars,', k, 'chunks')
