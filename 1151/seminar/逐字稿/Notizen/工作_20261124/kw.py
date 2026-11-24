import re,html,sys
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read(); t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S); t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
n=int(sys.argv[2]) if len(sys.argv)>2 and sys.argv[2].isdigit() else 200
ks=sys.argv[3:] if len(sys.argv)>3 else []
if not ks: print(t[:n]); sys.exit()
for k in ks:
  for m in list(re.finditer(re.escape(k),t))[:3]: print('['+k+']',t[max(0,m.start()-n):m.start()+n]); print()
