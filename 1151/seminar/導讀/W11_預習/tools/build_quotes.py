import re,os,collections,glob
from extract_quotes import norm,strip_tex,P1,P2,PG,R
def strip_ix(s):
    while True:
        i=s.find('\\ix{')
        if i<0: return s
        j=i+3
        for _ in range(2):
            if j>=len(s) or s[j]!='{': break
            depth=0
            while j<len(s):
                if s[j]=='{': depth+=1
                elif s[j]=='}':
                    depth-=1
                    if depth==0: j+=1; break
                j+=1
        s=s[:i]+s[j:]
AUTH={'michelman1998':'Michelman','post1998':'Post'}
def page_for(txt,end):
    para_end=txt.find('\n\n',end)
    if para_end<0: para_end=len(txt)
    lim=min(para_end,end+1500)
    nl=txt.find('\n',end)
    g=PG.search(txt,end,lim)
    if not g: return ''
    a=AUTH.get(g.group(2),g.group(2)); p=(g.group(1) or '').replace('\\&','&').replace('\\textdagger','†')
    p=re.sub(r'（[^）]*）','',p).strip()
    return f"{a} {p}" if p else ''
rows=[]
for f in sorted(glob.glob(R+'Teile/[1-8]*.tex')):
    txt=open(f).read(); fn=os.path.basename(f).replace('.tex','')
    for P in (P1,P2):
        for m in P.finditer(txt):
            rows.append((m.group(1),strip_ix(strip_tex(m.group(2))).strip(),page_for(txt,m.end()),fn))
    # table pairs
    pos=0; lastpg=''
    for l in txt.split('\n'):
        if ' & ' in l:
            cells=[c.strip() for c in re.sub(r'\\\\\s*$','',l.strip()).split(' & ')]
            for i in range(len(cells)-1):
                a,b=cells[i],cells[i+1]
                if len(re.findall(r'[A-Za-z]',a))>25 and len(re.findall(r'[一-鿿]',a))<=2 and len(re.findall(r'[一-鿿]',b))>=6:
                    pg=cells[i-1] if i>0 and re.fullmatch(r'\d+',cells[i-1]) else lastpg
                    lastpg=pg
                    rows.append((a,strip_ix(strip_tex(b)).strip(),('Michelman '+pg) if pg else '',fn))
g=collections.OrderedDict()
for en,zh,page,fn in rows:
    en=re.sub(r'\s+',' ',strip_ix(en)).strip()
    k=(norm(en),zh)
    d=g.setdefault(k,{'en':en,'zh':zh,'pages':[],'files':[]})
    if page and page not in d['pages']: d['pages'].append(page)
    if fn not in d['files']: d['files'].append(fn)
c=collections.Counter(k[0] for k in g)
for k,v in c.items():
    if v>1:
        for kk,d in g.items():
            if kk[0]==k: print(repr(kk[1]))
print('groups',len(g),'conflicting',[k for k,v in c.items() if v>1],'nopage',sum(1 for d in g.values() if not d['pages']))
out=['原文\t中譯\t出處頁\t所在檔']
for d in g.values():
    out.append('\t'.join([d['en'],d['zh'],'；'.join(d['pages']),'、'.join(d['files'])]))
os.makedirs(R+'tools',exist_ok=True)
open(R+'tools/quotes.tsv','w').write('\n'.join(out)+'\n')
