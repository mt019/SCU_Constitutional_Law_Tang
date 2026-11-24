import csv,sys
D='/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/逐字稿/Notizen/W05_1012/'
V='Vinx 本 Kelsen 譯文'
edits=[
(1,'廳廳的同學','旁聽的同學','名表用語「旁聽」；上下文為修課人數加旁聽生'),
(3,'在燒腦筋，燒腦筋','在傷腦筋，傷腦筋','成語「傷腦筋」'),
(5,'Hunst-Kilson','Hans Kelsen','名表 Hans Kelsen'),
(6,'Kilson Theory','Kelsen Theory','名表 Hans Kelsen；承 cue 5'),
(6,'規範階層構造則','規範階層構造說','cue 7「階層構造說」'),
(6,'一般區疏力','一般拘束力','上下文：一般規範之一般效力、一般拘束力'),
(7,'這邊的畫講呢','這邊的話講呢','cue 41「我們這邊的話講就是」'),
(9,'有一個 group norm','有一個 Grundnorm','Kelsen 基本規範（Grundnorm）；講者自譯「基本規範」'),
(9,'這個 group norm 不是','這個 Grundnorm 不是','同上'),
(9,'Huskelsen','Hans Kelsen','名表 Hans Kelsen'),
(9,'從 Velfasson','從 Verfassung','德文 Verfassung（憲法），講者隨即說「憲法以下」'),
(10,'這些就是 group note','這些就是 Grundnorm','同 cue 9'),
(10,'遺教就是 group note','遺教就是 Grundnorm','同 cue 9'),
(10,'孫松山先生','孫中山先生','中華民國憲法前言「依據孫中山先生創立中華民國之遺教」'),
(10,'考成三權分立考成這樣','搞成三權分立搞成這樣','上下文'),
(11,'修改若克','修改洛克','孟德斯鳩與洛克（Locke）之權力分立說'),
(11,'學歷分立','權力分立','上下文「三權分立」'),
(11,'Ferros paper','Federalist Papers','講者隨即說「聯邦黨人論」；James Madison'),
(12,'三個權力不明','三個權力部門','上下文：國家權力拆成三塊、三個野心'),
(13,'相互製衡的關係','相互制衡的關係','用語「制衡」'),
(13,'無群分立的困難','五權分立的困難','上下文：中華民國憲法五權、二十種關係'),
(13,'無群分立就有二十種相互製衡','五權分立就有二十種相互制衡','同上'),
(13,'這個憲，二十條憲也畫完','這個線，二十條線也畫完','cue 14「二十條線我畫得出來」'),
(13,'二十條憲也去','二十條線也去','同上'),
(14,'復標題','副標題','上下文：新書發表會不准掛副標題'),
(14,'六種相互智能的關係','六種相互制衡的關係','cue 13 三權分立六種制衡關係'),
(16,'所以武權當中','所以五權當中','上下文'),
(18,'宰藥','摘要','上下文：75 至 78 頁共同報告人的綱要'),
(18,'GoGabHabOchtdue','Mitberichterstatter','講者釋為「共同報告人」；W05_notes 附錄「Leitsätze des Mitberichterstatters」'),
(18,'共同報告人的 Gaima','共同報告人的綱要','W05_notes 附錄譯名「共同報告人的綱要」'),
(18,'Weizen und Enricho,Beschtesgerichtsbarkeit','Wesen und Entwicklung der Staatsgerichtsbarkeit','Kelsen 原題，Vinx 本 22 頁篇首注'),
(19,'以及其發財','以及其發展','原題 Entwicklung；cue 20「Nature and Development」'),
(19,'Statsgerichtsbarkeit','Staatsgerichtsbarkeit','德文原題'),
(20,'這是第一邊','這是第一篇','cue 22「第二篇文章」'),
(20,'Huskelsen','Hans Kelsen','名表 Hans Kelsen'),
(21,'審查課題','審查客體','W05_notes IV.2「審查的客體」；cue 29 同'),
(22,'好相啊','好像啊','上下文'),
(22,'可見我們劉德的學者','可見我們留德的學者','上下文：臺灣制度學習德國'),
(22,'那劉德的學者','那留德的學者','同上'),
(22,'七十九月','七十九頁','Schmitt 篇自 79 頁起（W05_notes）'),
(22,'《The Hüter der Verfassung》','《Der Hüter der Verfassung》','Schmitt 書名 Der Hüter der Verfassung'),
(23,'《The Hüter der Verfassung》','《Der Hüter der Verfassung》','同上'),
(25,'四季辯論','世紀辯論','上下文：Kelsen 與 Schmitt 之爭'),
(26,'the constant of constitution','the concept of constitution',V+' 27 頁節名 II The concept of constitution；講者譯「憲法的概念」'),
(27,'the Guarantees of liability','the Guarantees of legality',V+' 35 頁節名 III The guarantees of legality；講者譯「合法性的守護」'),
(28,'the constitution report','the constitutional court',V+' 44 頁節名 1 The constitutional court；講者譯「設立一個憲法法院」'),
(29,'exercise by the Constitutional Court','exercised by the Constitutional Court',V+' 48 頁節名'),
(29,'審查標定，或者叫審查課題','審查標的，或者叫審查客體','大法官用語「審查標的」「審查客體」'),
(29,'Generalvino','general norm','cue 6 講者「一般規範」；講者隨即譯「一般性規範」'),
(30,'Decrease','Decrees',V+' 48 頁 (b) decrees；講者譯「命令」'),
(30,'直接預計憲法','直接依據憲法','cue 35「依據憲法直接行使職權」'),
(31,'那個錶裡面','那個表裡面','上下文：講義附表'),
(32,'法律未接任法規範','法律位階法規範','憲法訴訟法第 55 條「法律位階法規範」；W05_qa 第 267 行'),
(34,'有司法院為之','由司法院為之','中華民國憲法第 173 條「憲法之解釋，由司法院為之」'),
(35,'Karskelson','Hans Kelsen','名表 Hans Kelsen'),
(35,'Karsham','Carl Schmitt','名表 Carl Schmitt；講者並稱二人'),
(36,'Karsham','Carl Schmitt','同上'),
(36,'行使之權所做的決定','行使職權所做的決定','cue 35「依據憲法直接行使職權」'),
(37,'照字面執意','照字面直譯','上下文'),
(39,'致死無效','自始無效','上下文：向將來失效與自始無效'),
(40,'有德國人的話說','用德國人的話說','上下文；cue 31「用我們憲法上的話說」'),
(42,'75 下的 guide line','75 頁的 guidelines',V+' 75 頁 Guidelines of the co-rapporteur'),
(43,'a link of the system','a limb of the system',V+' 22 頁「It is a limb of the system」'),
(46,'Consequently inks the function of state','Consequently, the functions of state',V+' 22 頁'),
(47,'Hunskelsen','Hans Kelsen','名表 Hans Kelsen'),
(51,'Peticeo principi','petitio principii',V+' 22 頁'),
(52,'backed question','begging the question','petitio principii 之英語通稱；講者釋「以問答問」'),
(56,'not to coordinate the function of state','not two co-ordinate functions of the state',V+' 23 頁'),
(59,'to the bottom view of the level','to the bottom via the level',V+' 23 頁'),
(61,'24 月的第一大段','24 頁的第一大段','上下文：引 24 頁第一段'),
(62,'in which status is common to existence','in which statutes come into existence',V+' 24 頁'),
(62,'if a sin in relation to the custody','if seen in relation to the constitution',V+' 24 頁'),
(70,'conformity of the degree','conformity of the decree',V+' 25 頁「conformity of a decree」'),
(78,'在講一遍','再講一遍','上下文'),
(78,'確保法律的核心性，而法律的核心性','確保法律的合憲性，而法律的合憲性','cue 75「法律合憲性的確保」'),
(78,'就是法律的核心性，剛才講的','就是法律的合法性，剛才講的','同句「剛才講的 legality」；cue 77 legality 即 conformity'),
(79,'into the story, the legal nature and the function of the state','into the thoroughly legal nature of the functions of the state',V+' 25 頁'),
(80,'或者在私有法律','或者在適用法律','cue 54「又是創造法律，又是在適用法律」'),
(81,'從軍主立憲','從君主立憲','上下文；W05_notes（一）3 君主立憲'),
(82,'談到軍主立憲','談到君主立憲','同上'),
(82,'by which the status came about','by which the statute came about',V+' 27 頁'),
(83,'程序的核限性','程序的合憲性',V+' 27 頁 constitutionality of the process'),
(83,'立法是核限的，程序上是核限的','立法是合憲的，程序上是合憲的','同上'),
(83,'就是附所','就是副署','ministerial countersignature；W05_notes 部長副署'),
(84,'就是要講附屬','就是要講副署','同上'),
]
breaks=[  # cue,end,para,title
(1,'','S','講義分發與臺大新書發表會'),
(2,'。','',''),
(3,'','1',''),
(4,'。','',''),
(5,'','S','法規範階層構造與權力分立的制衡關係'),
(7,'。','',''),
(8,'','1',''),
(10,'','1',''),
(11,'','1',''),
(12,'。','',''),
(13,'','1',''),
(14,'。','',''),
(15,'','1',''),
(17,'','S','Kelsen 與 Schmitt 兩篇的篇目與結構'),
(18,'。','',''),
(19,'','1',''),
(21,'','1',''),
(23,'','1',''),
(24,'','1',''),
(26,'','1',''),
(27,'。','',''),
(28,'','1',''),
(30,'','1',''),
(31,'','1',''),
(33,'','1',''),
(35,'','1',''),
(37,'','1',''),
(38,'','1',''),
(40,'','1',''),
(41,'','1',''),
(42,'。','',''),
(43,'','S','合法性的問題：立法與執行的相對區分'),
(44,'？','',''),
(45,'','1',''),
(46,'','1',''),
(47,'','1',''),
(48,'','1',''),
(50,'。','1',''),
(51,'','1',''),
(53,'','1',''),
(56,'','1',''),
(59,'','1',''),
(60,'。','',''),
(61,'','1',''),
(62,'。','',''),
(63,'','1',''),
(65,'','1',''),
(68,'','1',''),
(73,'','1',''),
(76,'','1',''),
(79,'','1',''),
(82,'。','1',''),
(83,'','1',''),
]
unc=[
(1,'學科人數八人','疑為「修課人數」或「選課人數」；未改'),
(1,'我是按照這個分量力的','疑為「按照這個份量印的」（講義印量）；未改'),
(1,'以前在憲法對話，對話憲法這個書','書名聽不清，名表無此書；未改'),
(2,'請不吝點贊 訂閱 轉發 打賞支持明鏡與點點欄目','Whisper 幻覺字串，時段 35.8 至 80.4 秒的實際講話未辨出，須回錄音核聽'),
(3,'那兩位一帆多次跟你。我們那個從我來問問','聽不出所指，疑為點名兩位同學；未改'),
(3,'去幫我私照一下，鼓動蜂巢一下','疑為「捧場一下」「鼓動風潮一下」（臺大新書發表會）；未改'),
(4,'別的地方新蘇聯講會就可以','疑為「新書發表會」或「新書演講會」；未改'),
(6,'或者 Ball Theory','疑為「Pure Theory」（純粹法學）；未改'),
(6,'General,No.Line,No','講義三角形表之三層，疑為 general norm、individual norm 等；聽不出，未改'),
(7,'是指定法延伸出來的','疑為「實定法」或「制定法」；未改'),
(7,'去執行法律的議制','疑為「意旨」；未改'),
(11,'沒有，他已經沒有任何一張紙了。那班長再去，誰還欣賞','回答 cue 10「你還有嗎？」，句首「沒有」或為學生或助教所說；「誰還欣賞」聽不出；說話人未改'),
(13,'他們戲學規要我講的權力分立主論','疑為「系學會」與「權力分立新論」（名表書名《權力分立新論》）；未改'),
(13,'這是一場作談論','疑為「座談會」；未改'),
(14,'從我們的新書發表會跟建築會，臺大說不可以，那比較偉大','「建築會」疑為「簽書會」；「那比較偉大」聽不出；未改'),
(15,'只要我，','與 cue 16「我沒有監察權存在」相接，疑為「只要我有監察權存在」；否定詞，未改'),
(16,'都要剉了一代','疑為「剉咧等」（臺語）；未改'),
(17,'它等於是會者','疑為「綱要」「摘要」；未改'),
(17,'有人替我們做古記','疑為「做筆記」；未改'),
(17,'那個 Hotbookdue','疑為 Berichterstatter（報告人），講者隨即說「通常我們講報告人」；德文發音拿不準，未改'),
(20,'就是他的學界、他的審判權','「學界」疑為「權限」或「管轄」；未改'),
(20,'這個國家法院可以關上','疑為「可以管什麼」；未改'),
(23,'憲法的守護者太偽翻了，這是翁先生的用語','「偽翻」疑為「硬翻」；「翁先生」名表無，疑指翁岳生或另有其人，須核聽'),
(25,'憲法審查非比憲法審查','疑為「憲法守護非必憲法審查」；未改'),
(25,'合法性格','疑為「合法性的問題」（the problem of legality）；未改'),
(26,'它是在阻止這個概念','聽不出；未改'),
(28,'有條大堆','疑為「有一大堆」；未改'),
(28,'我們現在還搞清楚是怎麼回事','疑漏「沒」；否定詞，未改'),
(33,'有，那法官來審查、決定','憲法第 171 條第 2 項由司法院解釋，疑為「那大法官來審查」；未改'),
(34,'我現在只是假概念','疑為「講概念」或「假設」；未改'),
(38,'我不知道現在又不開合議了','疑為「有沒有開合議」；否定詞，未改'),
(39,'申請大法官啟示','疑為「聲請大法官解釋」；未改'),
(45,'或者是經濟的法律','對應 created law is executed，疑為「既定的法律」；未改'),
(51,'至少馬老師告訴我','名表無此人；未改'),
(52,'那個 COR,關係 P','疑為講者重念 petitio principii；聽不出，未改'),
(52,'什麼叫做綠的合法性','疑為「法律的合法性」（legality of law，Vinx 22 頁）；未改'),
(60,'管得到他的指示立法程序','疑為「只是立法程序」；未改'),
(64,'但是不會產生法規命令','疑為「就不會產生」；未改'),
(64,'上下一番的劃分','疑為「上下位階的劃分」；未改'),
(73,'第四號','疑為「第四行」；數字，未改'),
(77,'三道事情','疑為「三件事情」；數字，未改'),
(79,'可以跟它一起','疑為「跟它一致」；未改'),
]
def w(name,header,rows):
    with open(D+name,'w',newline='') as f:
        wr=csv.writer(f,delimiter='\t',lineterminator='\n'); wr.writerow(header)
        for r in rows: wr.writerow(r)
w('chunk1.edits.tsv',['cue','before','after','basis'],edits)
w('chunk1.breaks.tsv',['cue','end','para','title'],breaks)
w('chunk1.speakers.tsv',['cue','speaker'],[])
w('chunk1.uncertain.tsv',['cue','原字','疑為與理由'],unc)
# checks
cues={int(r['cue']):r['text'] for r in csv.DictReader(open(D+'chunk1.tsv'),delimiter='\t') if r['cue']!='cue'}
ok=True
new=dict(cues)
for c,b,a,_ in edits:
    n=cues[c].count(b)
    if n!=1: print('COUNT',c,b,n); ok=False
    if abs(len(a)-len(b))>15: print('LEN>15',c,b)
    new[c]=new[c].replace(b,a)
o=sum(map(len,cues.values())); nn=sum(map(len,new.values())); print('chars',o,nn,f'{(nn-o)/o*100:.2f}%')
prev=0
bd={}
for c,e,p,t in breaks:
    assert c>prev; prev=c
    assert e in ('','。','？','！','，','0'); assert p in ('','1','S')
    if p=='S': assert t
    bd[c]=(e,p)
for c,(e,p) in bd.items():
    if p and c>1:
        pe=bd.get(c-1,('',''))[0]
        last=pe if pe else new[c-1][-1]
        if last not in '。？！': print('BADPREV',c,last); ok=False
paras=[];cur=[];curs=None
for c in sorted(new):
    e,p=bd.get(c,('',''))
    if p and cur: paras.append((curs,c-1,sum(len(new[x]) for x in cur))); cur=[]
    if not cur: curs=c
    cur.append(c)
paras.append((curs,max(new),sum(len(new[x]) for x in cur)))
print('paras',len(paras),'sections',sum(1 for b in breaks if b[2]=='S'))
print(sorted(paras,key=lambda x:-x[2])[:3], 'min',min(paras,key=lambda x:x[2]))
print('OK' if ok else 'FAIL', 'edits',len(edits),'unc',len(unc))
