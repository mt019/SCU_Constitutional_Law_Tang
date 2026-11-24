import re, sys, pathlib
W = pathlib.Path('/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/逐字稿/Notizen/W01_0914')
REPO = pathlib.Path('/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang')
PCD = '/Users/iw/Documents/NTU/1142/phenom-court-data/data/processed/'
APP = PCD + 'constitutional-court-app.json'
FT = PCD + 'constitutionalCourt-reasoning-fulltext.json'
SYL = '1151/seminar/syllabus.md'
RIDX = '1151/seminar/readings/index.md'
VINX = 'library/books/Vinx_The_Guardian_of_the_Constitution_Kelsen_and_Schmitt_2015.pdf'
MOJ = 'https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode='
text = {}
for line in (W/'reviewed.tsv').read_text(encoding='utf-8').splitlines()[1:]:
    k,_,_,t = line.split('\t',3); text[int(k)] = t
bib = set(re.findall(r'^@\w+\{([^,]+),', (REPO/'1151/seminar/課程問答/refs.bib').read_text(encoding='utf-8'), re.M))
uncertain = set()
for f in W.glob('chunk*.uncertain.tsv'):
    for l in f.read_text(encoding='utf-8').splitlines()[1:]:
        if l.strip(): uncertain.add(int(l.split('\t')[0]))
R = []
def n(cat, cue, word, note, src, cite=''):
    R.append((cat, cue, word, note, src, cite))
exec(open(sys.argv[1], encoding='utf-8').read())
errs = []
seen = set()
for cat,cue,word,note,src,cite in R:
    w = f'cue {cue}「{word}」'
    if not (1 <= cue <= 1400): errs.append(w+' 超出範圍')
    if word not in text.get(cue,''): errs.append(w+' 詞不在 cue')
    for c in range(1,cue):
        if word in text[c]: print('注意：較早出現', w, '於 cue', c); break
    if cue in uncertain: print('注意：cue 在待核表', w)
    if word in seen: errs.append(w+' 重複')
    seen.add(word)
    if re.search(r'[{}\\%#$&_\t]', note): errs.append(w+' 註文特殊字元')
    if cite and cite.partition('|')[0] not in bib: errs.append(w+' bib 鍵不存在 '+cite)
    for s in [x.strip() for x in src.split(' ; ') if x.strip()]:
        if not s.startswith('http'):
            p = pathlib.Path(s); p = p if p.is_absolute() else REPO/p
            if not p.exists(): errs.append(w+' 檔不存在 '+s)
if errs:
    print('\n'.join(errs)); sys.exit(1)
R.sort(key=lambda r: r[1])
out = ['cue\t詞\t註\t出處\t引'] + [f'{c}\t{w}\t{no}\t{s}\t{ci}' for _,c,w,no,s,ci in R]
pathlib.Path(sys.argv[2]).write_text('\n'.join(out)+'\n', encoding='utf-8')
pathlib.Path(sys.argv[3]).write_text('\n\n'.join(r[3] for r in R)+'\n', encoding='utf-8')
from collections import Counter
print(len(R), Counter(r[0] for r in R))
