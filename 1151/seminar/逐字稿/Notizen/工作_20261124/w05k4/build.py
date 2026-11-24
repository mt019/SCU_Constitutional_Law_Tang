import csv,sys,re
D='/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/逐字稿/Notizen/W05_1012/'
rows=list(csv.DictReader(open(D+'chunk4.tsv'),delimiter='\t'))
T={r['cue']:r['text'] for r in rows}
order=[r['cue'] for r in rows]
V='Vinx 英譯 Schmitt'
# (cue, wrong, right, basis)  all occurrences in cue replaced
E=[
('276','上述到這裡','上訴到這裡','上下文：案件上訴到最高法院'),
('277','法的效率','法的效力','上下文：判決之效力；W05_qa.tex Gesetzeskraft'),
('278','Texlicious','Gesetzeskraft','BVerfGG §31 Abs. 2 Gesetzeskraft；355 學生複述；W05_qa.tex'),
('278','這樣的效率','這樣的效力','上下文：Gesetzeskraft 之效力'),
('279','is elicited by the Staatsgerichtshof','is anything but a Staatsgerichtshof',V+' 80 頁'),
('280','constitutional rejuvenation','constitutional adjudication',V+' 80 頁'),
('286','Reichesgericht','Reichsgericht',V+' 82 頁'),
('287','Reichsfinanshof','Reichsfinanzhof',V+' 82 頁'),
('287','Prussisches,Order Itversorgungsgericht','Preußisches Oberverwaltungsgericht',V+' 82 頁'),
('291','下律可能性','下列可能性','上下文'),
('291','the statute of the right','a statute of the Reich',V+' 82 頁'),
('294','拒絕試用','拒絕適用','上下文；W05_notes.tex「拒絕適用」'),
('295','則不效','者無效','憲法第 171 條「法律與憲法牴觸者無效」'),
('296','當中沒看到','當作沒看到','上下文'),
('296','拒絕事由','拒絕適用','上下文；W05_notes.tex「拒絕適用」'),
('300','含色','涵攝','subsumption；W05_notes.tex 用語表「涵攝」'),
('301','含色','涵攝','subsumption；W05_notes.tex 用語表「涵攝」'),
('301','factor situation','factual situation',V+' 83 頁'),
('302','含色','涵攝','subsumption；W05_notes.tex 用語表「涵攝」'),
('302','refuse to reply','refuse to apply',V+' 83 頁'),
('303','含色','涵攝','subsumption；W05_notes.tex 用語表「涵攝」'),
('304','ordinary status','ordinary statute',V+' 83 頁'),
('305','留法權書','六法全書','上下文'),
('306','ordinary status','ordinary statute',V+' 83 頁'),
('307','如此而而','如此而已','上下文'),
('308','ordinary status','ordinary statute',V+' 83 頁'),
('312','by his gericht','by Reichsgericht',V+' 83 頁 decision of the Reichsgericht'),
('313','is the basis in its only justification','is its basis and its only justification',V+' 83 頁'),
('315','函設','涵攝','subsumption；W05_notes.tex 用語表「涵攝」'),
('316','函設','涵攝','subsumption；W05_notes.tex 用語表「涵攝」'),
('316','含設','涵攝','subsumption；W05_notes.tex 用語表「涵攝」'),
('317','Hunskelson','Hans Kelsen','名表'),
('317','徵修','增修','憲法增修條文'),
('318','公統','公投','上下文：公民投票'),
('319','拒絕試用','拒絕適用','上下文'),
('320','抵出憲法','牴觸憲法','上下文'),
('320','Hanskelsen','Hans Kelsen','名表'),
('322','Hanskelsen','Hans Kelsen','名表'),
('322','制定的修協','制定的修憲','上下文'),
('323','Hanskelsen','Hans Kelsen','名表'),
('325','徵修','增修','憲法增修條文'),
('326','徵修','增修','憲法增修條文'),
('326','多數通報','多數通過','上下文：美國憲法第 5 條'),
('326','還有一棟要','還有一定要','上下文'),
('327','徵修','增修','憲法增修條文'),
('328','徵修','增修','憲法增修條文'),
('328','499 號假釋','499 號解釋','釋字第 499 號'),
('329','負多','付託','憲法前言「受全體國民之付託」'),
('331','卓榮太','卓榮泰','名表'),
('331','真修','增修','憲法增修條文'),
('332','徵修','增修','憲法增修條文'),
('332','長之九安','長治久安','上下文'),
('333','全額正當比例代表','全額政黨比例代表','上下文：政黨比例代表制'),
('335','插槍走火','擦槍走火','成語'),
('336','申修','增修','憲法增修條文'),
('336','戰爭跟反對','贊成跟反對','上下文'),
('336','任務寫國大','任務型國大','上下文；337「任務型國大」'),
('337','徵修','增修','憲法增修條文'),
('338','徐姓良','許信良','名表'),
('339','徐姓娘','許信良','名表'),
('339','李子','裡子','成語「贏了裡子，輸了面子」'),
('339','半總統治','半總統制','上下文：政府體制'),
('339','半總治','半總制','上下文：政府體制'),
('339','倒課','倒閣','上下文：倒閣'),
('340','佔純分立','三權分立','上下文：下句「五權分立」對照'),
('340','檢察院','監察院','上下文：三個獨立機關'),
('341','流亡','流氓','上下文'),
('344','刑事','形式','上下文：形式審查'),
('344','投戰爭','投贊成','上下文：Yes 即贊成'),
('344','中學會','中選會','上下文：343「中選會」'),
('345','中學會','中選會','上下文：343「中選會」'),
('345','是立屆','是歷屆','上下文'),
('345','救任','就任','上下文'),
('346','不能共犯','不能公投','上下文：公投案'),
('350','走陸公','走路工','上下文：賄選「走路工」'),
('352','小柱七十一','小柱七十一','__skip'),
('352','Karl Schmitt','Carl Schmitt','名表'),
('352','Hanskels ','Hans Kelsen ','名表'),
('352','方法無不相及','風馬牛不相及','成語'),
('355','Gasescar','Gesetzeskraft','BVerfGG §31 Abs. 2；W05_qa.tex'),
('356','E85','185','釋字第 185 號（大法官解釋拘束全國機關）；ASR 字母誤'),
('357','後法又欲解法','後法優於前法','法諺'),
('358','導族','導讀','上下文'),
]
out=[]
for cue,w,r,b in E:
    if b=='__skip': continue
    t=T[cue]; n=t.count(w)
    assert n>=1,(cue,w)
    if n==1:
        i=t.index(w); a,z=i,i+len(w)
    else:
        a=t.index(w); z=t.rindex(w)+len(w)
    # widen until unique
    while t.count(t[a:z])>1:
        if a>0:a-=1
        if t.count(t[a:z])>1 and z<len(t): z+=1
    bef=t[a:z]; aft=bef.replace(w,r)
    # if another edit later in same cue overlaps, handled by sequential apply check
    out.append((cue,bef,aft,b))
    T[cue]=t  # not applied yet
# check overlaps per cue by sequential apply
T2={r['cue']:r['text'] for r in rows}
for cue,bef,aft,b in out:
    assert T2[cue].count(bef)==1,(cue,bef)
    T2[cue]=T2[cue].replace(bef,aft)
with open(D+'chunk4.edits.tsv','w') as f:
    f.write('cue\tbefore\tafter\tbasis\n')
    for o in out: f.write('\t'.join(o)+'\n')
print(len(out))
for o in out:
    if o[1].count(o[1][:1])>0 and len(o[1])>30: print(o[0],o[1][:60],'...')
