import re,glob,os,collections,sys
R='/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/導讀/W11_預習/Teile/'
files={os.path.basename(f)[:2]:f for f in sorted(glob.glob(R+'[1-8]*.tex'))}
txt={k:open(v).read() for k,v in files.items()}
log=collections.OrderedDict()
def rep(old,new,only=None,exact=None):
    tot=0
    for k in txt:
        if only and k not in only: continue
        n=txt[k].count(old)
        if n:
            txt[k]=txt[k].replace(old,new); tot+=n
            log.setdefault((old,new),[]).append((k,n))
    if exact is not None and tot!=exact: print('COUNT MISMATCH',old,tot,exact)
    if tot==0: print('NO HIT',old)
# ix first
rep(r'01@\zhlidxcat{民主理論}!純程序標準與程序獨立標準',r'04@\zhlidxcat{正當性}!純粹程序標準與程序獨立之正確標準')
rep('獨立於程序的正確性標準','程序獨立之正確標準')
rep('獨立於程序的正確、正義與民主標準','程序獨立的正確、正義與民主標準')
rep('程序獨立的政治正確性標準','程序獨立之政治正確標準')
rep('程序獨立標準','程序獨立之正確標準')
rep('純程序','純粹程序')
rep('立法之法','造法之法')
rep('基本法','根本法')
rep('民族認同','國族認同')
rep('憲法以上的原則','後設憲法原則')
rep('認知價值','認識價值')
rep('制度性難題','制度難題')
rep('課責觀（福利觀）','問責民主觀（福利民主觀）')
rep('課責觀或福利觀','問責民主觀或福利民主觀')
rep('課責觀','問責民主觀')
rep('民粹觀（populist）','民粹論（populist view）')
rep('民粹觀','民粹論')
rep('國家精神','國族精神')
rep('特殊意志','個別意志')
rep('公共意見','公眾意見')
rep('判斷的負擔','判斷之負擔')
rep('典型的簡單案件','典型的易案')
rep('無可修補的合理分歧','無從化解之合理歧見')
rep('合理分歧','合理歧見')
rep('司法審查','違憲審查',only={'30','60'})
rep('非合意之機關','非合意機關')
rep('以詮釋為名','以解釋為名')
rep('國族共同體','國族社群')
rep('各式意見','各種意見')
for k,v in files.items(): open(v,'w').write(txt[k])
for (o,n),v in log.items(): print(f"{o} -> {n}: {sum(c for _,c in v)} ({', '.join(f'{k}:{c}' for k,c in v)})")
