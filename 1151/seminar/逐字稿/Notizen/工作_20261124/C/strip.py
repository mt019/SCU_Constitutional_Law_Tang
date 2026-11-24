import re,sys,html
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
k=sys.argv[2] if len(sys.argv)>2 else ''
n=int(sys.argv[3]) if len(sys.argv)>3 else 1500
i=t.find(k) if k else 0
print(len(t), t[max(0,i-200):i+n])
