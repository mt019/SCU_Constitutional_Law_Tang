import sys,re,html
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read(); t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S); t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'[ \t\r]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
open(sys.argv[2],'w').write(t)
