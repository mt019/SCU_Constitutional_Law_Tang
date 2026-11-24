import csv
D = '/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/逐字稿/Notizen/W06_1019/'
rd = lambda n: list(csv.reader(open(D + n), delimiter='\t', quoting=csv.QUOTE_NONE))
rows = rd('chunk1.tsv')[1:]
T = {int(r[0]): r[3] for r in rows}
orig = {k: v for k, v in T.items()}
ok = True
E = rd('chunk1.edits.tsv')[1:]
for c, b, a, basis in E:
    c = int(c)
    n = T[c].count(b)
    if n != 1: print('EDIT not unique/missing', c, b, n); ok = False
    if abs(len(a) - len(b)) > 15: print('big diff', c)
for c, b, a, basis in E:
    T[int(c)] = T[int(c)].replace(b, a, 1)
lo, ln = sum(map(len, orig.values())), sum(map(len, T.values()))
print('edits', len(E), 'len', lo, ln, f'{(ln-lo)/lo*100:.2f}%')
B = rd('chunk1.breaks.tsv')[1:]
cs = [int(r[0]) for r in B]
print('breaks increasing', cs == sorted(set(cs)))
endm = {}
for r in B:
    c, e, p = int(r[0]), r[1], r[2]
    if e not in ('。', '？', '！', '，', '0', ''): print('bad end', c); ok = False
    if p not in ('1', 'S', ''): print('bad para', c); ok = False
    if e: endm[c] = e
def tail(c):
    t = T[c].rstrip()
    if c in endm:
        return endm[c] if endm[c] != '0' else ''
    return t[-1:]
starts = [int(r[0]) for r in B if r[2]]
for s in starts:
    if s > 1 and tail(s - 1) not in '。？！':
        print('para without sentence end before', s, repr(T[s-1][-3:])); ok = False
# paragraphs
cues = sorted(T)
paras = []; cur = []
for c in cues:
    if c in starts and cur: paras.append(cur); cur = []
    cur.append(c)
paras.append(cur)
L = [(sum(len(T[c]) for c in p), p[0], p[-1]) for p in paras]
L.sort(reverse=True)
print('paras', len(paras), 'sections', sum(1 for r in B if r[2] == 'S'))
print('longest3', L[:3]); print('shortest3', sorted(L)[:5])
SP = rd('chunk1.speakers.tsv')[1:]
print('speakers rows', len(SP), 'increasing', [int(r[0]) for r in SP] == sorted(set(int(r[0]) for r in SP)))
print('uncertain', len(rd('chunk1.uncertain.tsv')) - 1)
print('OK' if ok else 'FAIL')
for n,a,b in sorted(L, key=lambda x:x[1]):
    if n<80: print('short',n,a,b, ''.join(T[c] for c in range(a,b+1))[:60])
