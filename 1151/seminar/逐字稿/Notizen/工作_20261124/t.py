import sys,re,html
s=open(sys.argv[1],encoding='utf-8').read()
s=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S)
s=re.sub(r'</(div|tr|li|p)>','\n',s)
s=re.sub(r'<[^>]+>','',s); s=html.unescape(s)
s=re.sub(r'[ \t　]+',' ',s); s=re.sub(r'\n\s*\n+','\n',s)
open(sys.argv[1]+'.txt','w').write(s)
