import sys,re,html
s=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
s=re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>',' ',s)
s=re.sub(r'<[^>]+>',' ',s); s=html.unescape(s); s=re.sub(r'\s+',' ',s)
pats=sys.argv[2:]
for p in pats:
  for m in list(re.finditer(p,s))[:4]:
    print('['+p+']',s[max(0,m.start()-200):m.end()+300]); print()
