import csv,sys
sys.path.insert(0,'.')
from edits import E
src='/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/逐字稿/Notizen/W02_0921/chunk1.tsv'
T={}
for line in open(src,encoding='utf-8').read().splitlines()[1:]:
    p=line.split('\t'); T[int(p[0])]=p[3]
for c,b,a,_ in E:
    n=T.get(c,'').count(b)
    if n!=1: print('BAD',c,b,n, [k for k,v in T.items() if b in v])
