import re,html,sys
f=sys.argv[1]
t=open(f+'.html',encoding='utf8',errors='ignore').read()
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
t=html.unescape(re.sub(r'<[^>]+>','\n',t)); t=re.sub(r'\n\s*\n+','\n',t)
open(f+'.txt','w').write(t)
m=re.search(r'解釋公布院令\s*(中華民國[^\n]*)',t); print(f,len(t),m.group(1) if m else None)
