import re,html,sys
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
for a in sys.argv[2:]:
    if a=='前言':
        i=t.find('中華民國國民大會受全體國民之付託'); print(t[i:i+150]); continue
    i=t.find(a+' ')
    print(t[i:i+int(700)]); print('---')
