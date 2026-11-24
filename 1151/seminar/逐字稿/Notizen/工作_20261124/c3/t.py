import re,html,sys
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
t=re.sub(r'<script.*?</script>|<style.*?</style>|<nav.*?</nav>','',t,flags=re.S)
t=html.unescape(re.sub(r'<[^>]+>','\n',t));t=re.sub(r'\n\s*\n+','\n',t)
print(t)
