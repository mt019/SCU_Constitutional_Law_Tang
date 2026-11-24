import re,sys
sys.path.insert(0,'.')
from edits import E
from breaks import S,P,END
src='/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/逐字稿/Notizen/W02_0921/chunk1.tsv'
T={}
for line in open(src,encoding='utf-8').read().splitlines()[1:]:
    p=line.split('\t'); T[int(p[0])]=p[3]
X=dict(T)
for c,b,a,_ in E: X[c]=X[c].replace(b,a)
ends=dict(END)
starts=sorted(set(P)|set(S))
extra=set(int(x) for x in sys.argv[1].split(',')) if len(sys.argv)>1 and sys.argv[1] else set()
for k in T:
    if k in ends: continue
    nxt=k+1
    if T[k].endswith(',。'):
        if nxt in starts or k in extra: ends[k]='。'
        elif re.search(r'[A-Za-z]$',T[k][:-2]) and nxt in T and re.match(r'\s*[A-Za-z]',T[nxt]): ends[k]='0'
        else: ends[k]='，'
    elif nxt in starts and not re.search(r'[。？?！!.]$',T[k]):
        ends[k]='。'
def fin(k):
    t=X[k]; e=ends.get(k)
    if e is None: return t
    t=t.rstrip('，。？！,.?!'); return t if e=='0' else t+e
# 檢查
for s in starts:
    if s==1: continue
    pe=fin(s-1)
    if not re.search(r'[。？?！!.]$',pe): print('NOEND before',s,pe[-15:])
paras=[];cur=None
for k in sorted(T):
    if k in starts: cur=[k,k,0]; paras.append(cur)
    cur[1]=k; cur[2]+=len(fin(k))
for a,b,n in paras: print(a,b,n)
import json; json.dump({'ends':ends,'starts':starts},open('state.json','w'))
if '--show' in sys.argv:
    for a,b,n in paras:
        print(f'[{a}-{b}]',''.join(f'«{k}»'+fin(k) for k in range(a,b+1)))
