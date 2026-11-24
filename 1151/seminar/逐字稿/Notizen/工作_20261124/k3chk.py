exec(open('k3.py').read())
for c,s,_ in speakers: print('SPK',c,s,T[c])
for c in ks: print('BRK',c,breaks[c],T.get(c-1,''), '|', T[c])
