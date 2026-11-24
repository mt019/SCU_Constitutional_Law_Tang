import sys,re,html
from html.parser import HTMLParser
def txt(f):
    s=open(f,encoding='utf-8').read()
    s=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S)
    s=re.sub(r'<br\s*/?>|</div>|</tr>|</p>','\n',s)
    s=re.sub(r'<[^>]+>','',s)
    return html.unescape(s)
if __name__=='__main__':
    t=txt(sys.argv[1])
    for a in sys.argv[2:]:
        m=re.search(r'第\s*'+a+r'\s*條\s*\n(.{0,700})',t,re.S)
        print('==',a,re.sub(r'\n\s*\n+','\n',m.group(0)) if m else None)
