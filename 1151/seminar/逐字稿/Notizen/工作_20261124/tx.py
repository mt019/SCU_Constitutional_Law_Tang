import sys,re,html
s=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
s=re.sub(r'(?s)<(script|style).*?</\1>','',s)
s=re.sub(r'<[^>]+>','\n',s); s=html.unescape(s)
s=re.sub(r'\n\s*\n+','\n',s)
open(sys.argv[1]+'.txt','w').write(s)
