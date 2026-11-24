import sys,json,re
sys.path.insert(0,'.')
from edits import E
from breaks import S,P
from unc import U
st=json.load(open('state.json'))
ends={int(k):v for k,v in st['ends'].items()}
starts=set(st['starts'])
D='/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/逐字稿/Notizen/W02_0921/'
with open(D+'chunk1.edits.tsv','w',encoding='utf-8') as f:
    f.write('cue\tbefore\tafter\tbasis\n')
    for c,b,a,z in E: f.write(f'{c}\t{b}\t{a}\t{z}\n')
with open(D+'chunk1.breaks.tsv','w',encoding='utf-8') as f:
    f.write('cue\tend\tpara\ttitle\n')
    for k in sorted(set(ends)|starts):
        para='S' if k in S else ('1' if k in starts else '')
        f.write(f"{k}\t{ends.get(k,'')}\t{para}\t{S.get(k,'')}\n")
with open(D+'chunk1.speakers.tsv','w',encoding='utf-8') as f:
    f.write('cue\tspeaker\n')
with open(D+'chunk1.uncertain.tsv','w',encoding='utf-8') as f:
    f.write('cue\t原字\t疑為與理由\n')
    for c,a,b in U: f.write(f'{c}\t{a}\t{b}\n')
