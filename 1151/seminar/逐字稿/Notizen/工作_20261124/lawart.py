import sys,re,html,subprocess
pc,fl=sys.argv[1],sys.argv[2]
t=subprocess.run(['curl','-sL','-A','Mozilla/5.0',f'https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode={pc}&flno={fl}'],capture_output=True,text=True).stdout
m=re.search(r'<title>(.*?)</title>',t,re.S); print(html.unescape(m.group(1).strip()) if m else '')
m=re.search(r'<div class="law-article">(.*?)</div></div>',t,re.S)
if m:
  for x in re.findall(r'<div class="line-[^"]*">(.*?)</div>',m.group(1)+'</div>',re.S): print(html.unescape(re.sub('<[^>]+>','',x)).strip())
