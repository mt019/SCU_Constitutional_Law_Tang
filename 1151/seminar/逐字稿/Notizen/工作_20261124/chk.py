import re,sys,html
f,*keys=sys.argv[1:]
t=open(f,errors='ignore').read()
t=re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',t,flags=re.S)
t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
for k in keys:
    ms=list(re.finditer(k,t))
    print('##',k,len(ms))
    for m in ms[:3]: print('   ',t[max(0,m.start()-200):m.end()+300])
