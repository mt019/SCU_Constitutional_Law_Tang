import csv,re,glob,os,collections,sys
from build_quotes import page_for,strip_ix
R='/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/導讀/W11_預習/'
T=list(csv.reader(open('W11_譯名表.tsv'),delimiter='\t'))[1:]
files=sorted(glob.glob(R+'Teile/[1-8]*.tex'))
txts=[(os.path.basename(f)[:2],open(f).read()) for f in files]
def toks(row):
    en=[x.strip().replace('(s)','') for x in re.split(r'\s*/\s*',row[0])]
    zh=[x.strip() for x in re.split(r'／',row[1])]
    return en,zh
res=[]
for row in T:
    en,zh=toks(row)
    occ=[]
    for k,t in txts:
        for e in en:
            if len(e)<3: continue
            for m in re.finditer(re.escape(e.strip('"')),t,re.I):
                occ.append((k,page_for(t,m.end())))
    if not occ:
        for k,t in txts:
            for z in zh:
                for m in re.finditer(re.escape(z),t):
                    occ.append((k,page_for(t,m.end())))
    res.append((row,occ))
def pnum(p):
    m=re.match(r'(Michelman|Post) (\d+)',p)
    return (m.group(1),int(m.group(2))) if m else None
out=[]
for row,occ in res:
    best={}
    for k,p in occ:
        x=pnum(p)
        if not x: continue
        a,n=x
        if a=='Michelman' and not 399<=n<=427: continue
        if a=='Post' and not 429<=n<=443: continue
        best[a]=min(best.get(a,10**6),n)
    out.append((row,best,len(occ)))
import json
json.dump([(r,b,n) for r,b,n in out],open('a3_raw.json','w'),ensure_ascii=False)
for r,b,n in out: print(r[0][:45],'|',r[1],'|',b,n,'|',(r+[''])[3][:30])
