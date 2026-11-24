import sys,re
s=open(sys.argv[1]).read()
for m in list(re.finditer(sys.argv[2],s))[:int(sys.argv[4]) if len(sys.argv)>4 else 2]:
    n=int(sys.argv[3]) if len(sys.argv)>3 else 200
    print('>>',s[max(0,m.start()-n//3):m.end()+n]);print()
