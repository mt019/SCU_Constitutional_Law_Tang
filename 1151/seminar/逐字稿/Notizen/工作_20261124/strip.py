import sys,re,html
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
t=re.sub(r'(?s)<(script|style).*?</\1>','',t)
t=re.sub(r'<br\s*/?>|</div>|</p>|</tr>','\n',t)
t=html.unescape(re.sub(r'<[^>]+>','',t))
t=re.sub(r'\n\s*\n+','\n',t)
print(t)
