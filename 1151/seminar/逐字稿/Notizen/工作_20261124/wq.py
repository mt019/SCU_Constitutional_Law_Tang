import re,sys
t=open(sys.argv[1],encoding='utf-8').read()
for pat in sys.argv[2:]:
    for m in re.finditer(pat,t,re.I):
        pre=t[:m.start()]
        pages=re.findall(r'⟦(\d+)⟧|\\pagemark\{(\d+)\}',pre)
        pg=[a or b for a,b in pages][-1] if pages else '?'
        s=max(0,m.start()-350); e=min(len(t),m.end()+450)
        print(f'== [{pat}] p{pg}\n'+t[s:e].replace('\n',' ')+'\n')
