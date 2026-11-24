import csv,sys
sys.path.insert(0,'.')
from edits import E
from rest import B,S,U
D='/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/constitution/逐字稿/Notizen/W11_1123/'
rows=list(csv.DictReader(open(D+'chunk3.tsv'),delimiter='\t'))
T={int(r['cue']):r['text'] for r in rows}
def w(name,hdr,data):
    with open(D+name,'w',newline='') as f:
        cw=csv.writer(f,delimiter='\t',lineterminator='\n'); cw.writerow(hdr); cw.writerows(data)
w('chunk3.edits.tsv',['cue','before','after','basis'],E)
w('chunk3.breaks.tsv',['cue','end','para','title'],B)
w('chunk3.speakers.tsv',['cue','speaker','split'],S)
w('chunk3.uncertain.tsv',['cue','原字','疑為與理由'],U)
# validate
new=dict(T); ok=True
for c,b,a,_ in E:
    if T[c].count(b)!=1: print('E count',c,b); ok=False
    if abs(len(a)-len(b))>15: print('E diff',c)
    new[c]=new[c].replace(b,a)
o=sum(map(len,T.values())); m=sum(map(len,new.values())); print('字數差',round((m-o)/o*100,2),'%')
cs=[b[0] for b in B]; print('breaks遞增無重',cs==sorted(set(cs)))
bd={b[0]:b for b in B}
for c,e,p,t in B:
    assert e in ('','。','？','！','，','0') and p in ('','1','S')
    if p:
        prev=c-1
        pe=bd[prev][1] if prev in bd and bd[prev][1] else new[prev][-1]
        if pe not in '。？！': print('prev not end',c,pe); ok=False
for c,b,a in U:
    if b not in T[c] and b not in new[c]: print('U not found',c,b)
for c,sp,s in S:
    if s and new[c].count(s)!=1: print('split',c,s,new[c].count(s))
# paragraphs
starts=[c for c,e,p,t in B if p]; cues=sorted(T)
paras=[];cur=[]
for c in cues:
    if c in starts and cur: paras.append(cur); cur=[]
    cur.append(c)
paras.append(cur)
L=sorted(((sum(len(new[c]) for c in p),p[0],p[-1]) for p in paras),reverse=True)
print('段數',len(paras),'最長三段',L[:3]); print('超過400',[x for x in L if x[0]>400])
print('ok',ok,len(E),len(B),len(S),len(U))
