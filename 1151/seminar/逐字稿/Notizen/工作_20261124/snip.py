import sys,re
s=open(sys.argv[1],errors='ignore').read()
for pat in sys.argv[2:]:
    for m in list(re.finditer(pat,s))[:3]:
        print('['+pat+']', s[max(0,m.start()-220):m.end()+260]); print()
