import re,html,sys
s=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
s=re.sub(r'(?s)<script.*?</script>|<style.*?</style>','',s)
t=html.unescape(re.sub(r'<[^>]+>',' ',s)); t=re.sub(r'\s+',' ',t)
for k in sys.argv[2:]:
    for m in re.finditer(re.escape(k),t):
        print('>>',t[max(0,m.start()-50):m.start()+int(400)]); break
