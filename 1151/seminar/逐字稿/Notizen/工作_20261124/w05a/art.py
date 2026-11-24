import re,sys,html
def arts(fn):
    t=open(fn,encoding='utf-8').read()
    title=re.search(r'<title>(.*?)</title>',t,re.S).group(1).strip()
    out={}
    for m in re.finditer(r'<div class="col-no">\s*<a[^>]*>(.*?)</a>.*?<div class="law-article">(.*?)</div>\s*</div>',t,re.S):
        no=re.sub(r'\s+','',html.unescape(re.sub('<[^>]+>','',m.group(1))))
        body=html.unescape(re.sub(r'<[^>]+>','\n',m.group(2)));body=re.sub(r'\n+','\n',body).strip()
        out[no]=body
    mod=re.search(r'修正日期.*?(\d+ 年 \d+ 月 \d+ 日)',t,re.S)
    return title,out,mod.group(1) if mod else None
fn=sys.argv[1]
title,o,mod=arts(fn); print(title,mod)
for a in sys.argv[2:]: print(a,'|',o.get(a))
