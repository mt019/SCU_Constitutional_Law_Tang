import sys, re, pathlib
sys.path.insert(0,'/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/逐字稿/Skripte')
from gen_tex import fullwidth, read_tsv
D = pathlib.Path('/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/逐字稿/Notizen/W02_0921')
c = read_tsv(D/'chunk2.tsv',['cue','start','end','text'])
text = {int(r['cue']):r['text'] for r in c}; orig=dict(text)
ok=True
for r in read_tsv(D/'chunk2.edits.tsv',['cue','before','after','basis']):
    k=int(r['cue']); n=text[k].count(r['before'])
    if n!=1: print('BEFORE count',k,r['before'],n); ok=False
    if abs(len(r['after'])-len(r['before']))>15: print('diff>15',k)
    text[k]=text[k].replace(r['before'],r['after'])
a=sum(map(len,orig.values())); b=sum(map(len,text.values()))
print('chars',a,b,f'{(b-a)/a*100:.2f}%')
for k in text: text[k]=fullwidth(text[k]).strip()
br = read_tsv(D/'chunk2.breaks.tsv',['cue','end','para','title'])
ks=[int(r['cue']) for r in br]; print('increasing', ks==sorted(set(ks)))
for r in br:
    assert r['end'] in ('。','？','！','，','0',''), r
    assert r['para'] in ('1','S',''), r
    if r['para']=='S': assert r['title']
for r in br:
    if r['end']:
        k=int(r['cue']); t=text[k].rstrip('，。？！,.?!'); text[k]= t if r['end']=='0' else t+r['end']
paras=[int(r['cue']) for r in br if r['para']]
for k in paras:
    if k-1 in text and text[k-1][-1] not in '。？！': print('para prev bad',k,text[k-1]); ok=False
bad=[k for k in text if text[k].endswith('，。') or ',' in text[k][-2:]]
print('residual ，。 endings', bad[:10], len(bad))
# paragraphs
starts=sorted(set([min(text)]+paras)); segs=[]
order=sorted(text)
for i,s in enumerate(starts):
    e = starts[i+1]-1 if i+1<len(starts) else max(order)
    segs.append((sum(len(text[k]) for k in range(s,e+1)),s,e))
segs.sort(reverse=True); print('paras',len(starts),'top3',segs[:3])
print('sections', sum(1 for r in br if r['para']=='S'))
print('ok' if ok else 'FAIL')
open('rendered.txt','w').write('\n'.join(f'{k}|{text[k]}' for k in order))
