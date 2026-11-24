import sys,re,html
s=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
s=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S)
s=re.sub(r'<br\s*/?>|</div>|</tr>|</p>|</li>|</h\d>','\n',s)
s=re.sub(r'<[^>]+>','',s)
s=html.unescape(s)
print(re.sub(r'\n\s*\n+','\n',s))
