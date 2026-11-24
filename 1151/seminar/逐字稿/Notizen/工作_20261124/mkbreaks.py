import re,sys
D='/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/逐字稿/Notizen/W02_0921/'
cues={int(l.split('\t')[0]):l.split('\t')[3] for l in open(D+'chunk3.tsv',encoding='utf-8').read().splitlines()[1:]}
starts=[int(x) for x in sys.argv[1].split()]
S={1701:'以成文憲法為據的三種說法及其反對'}
extra_end={}
rows={}
for k in starts:
    p=k-1
    t=cues[p].strip()
    if t.endswith((',。','，。')) or t[-1] not in '。？！?!':
        rows.setdefault(p,['',''])[0]='。'
    rows.setdefault(k,['',''])[1]='S' if k in S else '1'
with open(D+'chunk3.breaks.tsv','w',encoding='utf-8') as f:
    f.write('cue\tend\tpara\ttitle\n')
    for k in sorted(rows):
        e,pa=rows[k]
        f.write(f'{k}\t{e}\t{pa}\t{S.get(k,"") if pa=="S" else ""}\n')
