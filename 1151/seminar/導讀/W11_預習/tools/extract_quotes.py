import re,glob,sys,os,collections
R='/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/導讀/W11_預習/'
def strip_tex(s):
    s=re.sub(r'\\ix\{[^{}]*\}\{[^{}]*\}','',s)
    s=re.sub(r'\\footcite(\[[^\]]*\])*\{[^{}]*\}','',s)
    s=re.sub(r'\\textquotesingle\s*','\'',s)
    return s
def norm(e):
    e=e.lower().replace('’',"'").replace('‘',"'")
    e=re.sub(r'\\[a-z]+\s*','',e)
    return re.sub(r'[^a-z0-9]+','',e)
P1=re.compile(r'「([^「」〔〕]+)」〔((?:[^〔〕]|\\ix\{[^{}]*\}\{[^{}]*\})+)〕')
P2=re.compile(r'(?<![A-Za-z])((?:[A-Za-z][A-Za-z0-9\-\'’,.]*\s+){0,12}[A-Za-z][A-Za-z0-9\-\'’]*)〔((?:[^〔〕]|\\ix\{[^{}]*\}\{[^{}]*\})+)〕')
PG=re.compile(r'\\footcite(?:\[([^\]]*)\])?\{([^{}]*)\}')
def run():
    rows=[]
    for f in sorted(glob.glob(R+'Teile/*.tex')):
        txt=open(f).read()
        for kind,P in (('q',P1),('e',P2)):
            for m in P.finditer(txt):
                en=m.group(1); zh=strip_tex(m.group(2)).strip()
                g=PG.search(txt,m.end(),m.end()+400)
                nl=txt.find('\n',m.end())
                page=''
                if g and (nl==-1 or g.start()<nl):
                    page=(g.group(1) or '')+'@'+g.group(2)
                rows.append((kind,en,zh,page,os.path.basename(f),m.start()))
    return rows
if __name__=='__main__':
    rows=run()
    d=collections.defaultdict(list)
    for r in rows: d[norm(r[1])].append(r)
    for k,v in sorted(d.items(), key=lambda kv:kv[1][0][1].lower()):
        zhs=collections.Counter(r[2] for r in v)
        if len(zhs)>1 or '-all' in sys.argv:
            print('##',v[0][1][:120])
            for z,c in zhs.items(): print('   ',c,z[:150],[r[4][:2] for r in v if r[2]==z])
    print(len(rows),len(d),sum(1 for v in d.values() if len({r[2] for r in v})>1))

def table_pairs():
    out=[]
    for f in sorted(glob.glob(R+'Teile/*.tex')):
        for ln,l in enumerate(open(f).read().split('\n'),1):
            if ' & ' not in l: continue
            cells=[c.strip() for c in re.sub(r'\\\\\s*$','',l.strip()).split(' & ')]
            for i in range(len(cells)-1):
                a,b=cells[i],cells[i+1]
                lat=len(re.findall(r'[A-Za-z]',a)); cjk=len(re.findall(r'[一-鿿]',b)); cja=len(re.findall(r'[一-鿿]',a))
                if lat>25 and cja<=2 and cjk>=6:
                    out.append(('t',a,strip_tex(b),'',os.path.basename(f),ln))
    return out
