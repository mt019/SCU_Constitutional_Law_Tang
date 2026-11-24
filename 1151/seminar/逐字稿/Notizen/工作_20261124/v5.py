import csv
D='/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/逐字稿/Notizen/W01_0914/'
rd=lambda n:list(csv.DictReader(open(D+n),delimiter='\t'))
cue={int(r['cue']):r['text'] for r in rd('chunk5.tsv')}
txt=dict(cue); ok=True
for e in rd('chunk5.edits.tsv'):
    c=int(e['cue']); n=cue[c].count(e['before'])
    if n!=1: print('BAD before',c,e['before'],n); ok=False
    if abs(len(e['after'])-len(e['before']))>15: print('long',c)
    txt[c]=txt[c].replace(e['before'],e['after'])
a=sum(map(len,cue.values())); b=sum(map(len,txt.values()))
print('edits ok' if ok else 'edits FAIL','len',a,b,round(abs(a-b)/a*100,3),'%')
br=rd('chunk5.breaks.tsv'); prev=0; bm={}
for r in br:
    c=int(r['cue']); assert c>prev and c in cue; prev=c
    assert r['end'] in ('。','？','！','，','0',''), r; assert r['para'] in ('1','S',''), r
    bm[c]=r
def endc(c):
    if c in bm and bm[c]['end']: return bm[c]['end']
    return txt[c][-1] if c in txt else '。'
bad=[c for c in bm if bm[c]['para'] and endc(c-1) not in '。？！']
print('para prev-end bad',bad)
starts=[min(cue)]+[c for c in sorted(bm) if bm[c]['para']]
starts=sorted(set(starts)); segs=[]
cs=sorted(cue)
for i,s in enumerate(starts):
    e=(starts[i+1]-1) if i+1<len(starts) else max(cs)
    segs.append((sum(len(txt[c]) for c in range(s,e+1)),s,e))
print('paras',len(starts)-1,'S',sum(1 for c in bm if bm[c]['para']=='S'))
print('longest',sorted(segs,reverse=True)[:3]); print('shortest',sorted(segs)[:3])
sp=rd('chunk5.speakers.tsv'); print('speakers rows',len(sp)); print('uncertain',len(rd('chunk5.uncertain.tsv')),'edits',len(rd('chunk5.edits.tsv')))
