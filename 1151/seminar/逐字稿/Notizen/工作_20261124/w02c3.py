import csv,sys,re
D='/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/逐字稿/Notizen/W02_0921/'
def rd(p):
    rows=[l.split('\t') for l in open(D+p,encoding='utf-8').read().splitlines() if l.strip()]
    return rows[1:]
cues={int(r[0]):r[3] for r in rd('chunk3.tsv')}
orig=dict(cues)
ok=True
for r in rd('chunk3.edits.tsv'):
    k=int(r[0]);b,a=r[1],r[2]
    n=cues[k].count(b)
    if n!=1: print('EDIT FAIL',k,b,n); ok=False; continue
    if abs(len(a)-len(b))>15: print('LEN',k,b,a)
    cues[k]=cues[k].replace(b,a)
o=sum(len(v) for v in orig.values()); e=sum(len(v) for v in cues.values())
print('chars',o,e,round((e-o)/o*100,2),'%')
br={}
prev=None
for r in rd('chunk3.breaks.tsv'):
    r+=['']*(4-len(r)); k=int(r[0])
    assert prev is None or k>prev, ('order',k); prev=k
    assert r[1] in ('','。','？','！','，','0'),(k,r[1])
    assert r[2] in ('','1','S'),(k,r[2])
    br[k]=r
def fin(k):
    t=cues[k]
    if k in br and br[k][1]: return br[k][1]
    t=re.sub(r'[,，]。$','，',t.strip())
    return t[-1]
ks=sorted(cues)
for k in ks:
    if k in br and br[k][2]:
        if k-1 in cues and fin(k-1) not in '。？！?!':
            print('PARA PREV NOT FINAL',k,cues[k-1]); ok=False
# paragraphs
starts=[k for k in ks if k in br and br[k][2]]
segs=[];cur=[ks[0]]
for k in ks[1:]:
    if k in starts: segs.append(cur);cur=[k]
    else: cur.append(k)
segs.append(cur)
L=[(sum(len(re.sub(r'[,，]。$','，',cues[k])) for k in s),s[0],s[-1]) for s in segs]
print('paras',len(segs),'S',sum(1 for k in starts if br[k][2]=='S'))
for l in sorted(L,reverse=True)[:5]: print('long',l)
for l in sorted(L)[:5]: print('short',l)
print('OK' if ok else 'FAIL')
