import csv,re,sys
D='/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/constitution/逐字稿/Notizen/W01_0914/'
rows=list(csv.DictReader(open(D+'chunk3.tsv'),delimiter='\t'))
text={int(r['cue']):r['text'] for r in rows}; cues=sorted(text)
edits=[l.rstrip('\n').split('\t') for l in open('edits.txt') if l.strip()]
ok=True
new=dict(text)
for c,b,a,_ in edits:
    c=int(c); n=text[c].count(b)
    if n!=1: print('BEFORE COUNT',c,b,n); ok=False
    if abs(len(a)-len(b))>15: print('DIFF>15',c)
    new[c]=new[c].replace(b,a)
o=sum(len(text[c]) for c in cues); m=sum(len(new[c]) for c in cues)
print('chars',o,m,round(100*(m-o)/o,2),'%')
S={3008:'大法官提名的經過',3591:'答題的要求',3775:'中央研究院歐美研究所與社科所法律組的經歷',4004:'實務界的升遷與畢業學校'}
P=[2759,2782,2835,2851,2876,2911,2928,2945,2957,2971,2810,2986,3023,3047,3066,3094,3123,3152,3178,3229,3259,3294,3333,3365,3384,3405,3418,3432,3449,3480,3508,3534,3573,3581,3611,3644,3669,3690,3713,3728,3754,3782,3797,3820,3833,3855,3871,3888,3908,3922,3936,3947,3958,3985,3994,4015,4042,4073,4088,4107,4137]
para={c:'1' for c in P}; para.update({c:'S' for c in S})
# end punctuation heuristics
end={}
Q=re.compile(r'(嗎|對不對|是不是|為什麼|對吧|怎麼辦呢|是誰|是什麼)$')
C=re.compile(r'(呢|的話|因為|所以|但是|而且|然後|結果|如果|那|就是|在|跟|和|把|被|從|對於|關於|比方說|像)$')
for i,c in enumerate(cues):
    t=new[c]; body=t[:-1] if t.endswith('。') else None
    if body is None: continue
    nxt=cues[i+1] if i+1<len(cues) else None
    if Q.search(body) and not re.search(r'(不知道|知不知道)',body): end[c]='？'
    elif C.search(body) and nxt and nxt not in para and len(body)<=12: end[c]='，'
for x in (3450,3455,3918,3977,3335): end.pop(x,None)
def fin(c):
    return end.get(c, new[c][-1])
for c in para:
    i=cues.index(c)
    if i>0 and fin(cues[i-1]) not in '。？！': print('PARA PREV BAD',c); ok=False
# paragraphs
starts=[cues[0]]+[c for c in cues if c in para and c!=cues[0]]
lens=[]
for k,s in enumerate(starts):
    e=starts[k+1] if k+1<len(starts) else cues[-1]+1
    seg=[c for c in cues if s<=c<e]
    lens.append((sum(len(new[c]) for c in seg),seg[0],seg[-1]))
print("short",[x for x in lens if x[0]<80]); lens.sort(reverse=True); print('paras',len(starts),'top3',lens[:3],'min',lens[-3:])
print('ends changed',len(end), {v:list(end.values()).count(v) for v in set(end.values())})
if '--write' in sys.argv and ok:
    w=lambda f,h,rs: open(D+f,'w').write('\t'.join(h)+'\n'+''.join('\t'.join(map(str,r))+'\n' for r in rs))
    w('chunk3.edits.tsv',['cue','before','after','basis'],edits)
    br=sorted(set(end)|set(para))
    w('chunk3.breaks.tsv',['cue','end','para','title'],[[c,end.get(c,''),para.get(c,''),S.get(c,'')] for c in br])
    w('chunk3.speakers.tsv',['cue','speaker'],[l.rstrip('\n').split('\t') for l in open('spk.txt') if l.strip()])
    w('chunk3.uncertain.tsv',['cue','原字','疑為與理由'],[l.rstrip('\n').split('\t') for l in open('unc.txt') if l.strip()])
    print('written')
if '--show' in sys.argv:
    for c,v in sorted(end.items()): print(c,new[c],v)
