import csv,sys
sys.path.insert(0,'.')
from edits import E
src='/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/constitution/逐字稿/Notizen/W11_1123/chunk3.tsv'
rows=list(csv.DictReader(open(src),delimiter='\t'))
T={int(r['cue']):r['text'] for r in rows}
new=dict(T)
for c,b,a,_ in E:
    n=T[c].count(b)
    if n!=1: print('COUNT',c,b,n)
    if abs(len(a)-len(b))>15: print('DIFF',c,b)
    new[c]=new[c].replace(b,a)
o=sum(len(v) for v in T.values()); m=sum(len(v) for v in new.values()); print('chars',o,m,(m-o)/o)
for c in sorted(T): print(c,len(new[c]),new[c][-3:])
