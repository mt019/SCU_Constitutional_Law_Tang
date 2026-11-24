import csv
D='/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/逐字稿/Notizen/W05_1012/'
K='（Kelsen 綱要第 8 條，Vinx 本 77 頁）'
S='Schmitt 原文（Vinx 本）'
edits=[
(164,'the executed statute','that execute statutes','Kelsen 綱要第 8 條 (b)：decrees that execute statutes and are thus mediate to the constitution（Vinx 本 77 頁）'),
(164,'限接於憲法','間接於憲法','上下文：與「直接於憲法」對舉，綱要 mediate to the constitution'),
(165,'行政法律的事','行政法院的事','上下文：命令牴觸母法屬行政法院審查，Kelsen 77 頁「行政法院或者是其他法院」'),
(166,'only permissible standard for you','only permissible standard for the review','Kelsen 綱要第 8 條 (d)（Vinx 本 77 頁）'),
(166,'無論如果你','無論如何你','上下文：同 cue 前句「無論如何」，音近'),
(167,'cassacion of the legally','cassation of the legally','英文拼法，Kelsen 綱要第 9 條'),
(167,'the cassacion of general wrongs','the cassation of general norms','Kelsen 綱要第 9 條：The cassation of general norms'),
(169,'那個 AXIO','那個 actio','actio popularis，W05_notes.tex 民眾訴訟（Kelsen 64--65 頁）'),
(170,'SEO,就是','Actio,就是','上下文：拉丁字 actio popularis'),
(170,'特別所害','特別損害','上下文，音近；同 171'),
(170,'數字利益','訴之利益','上下文：提起訴訟之要件，音近'),
(171,'什麼所害','什麼損害','上下文，音近；同 170'),
(172,'就是依止權','就是依職權','ex officio 之譯語'),
(172,'可不可以依止權','可不可以依職權','ex officio 之譯語'),
(172,'constitutional abrogate','constitutional advocate','Kelsen 66 頁 advocate of the constitution；W05_notes.tex 用語表'),
(183,'constitutional ad，','constitutional advocate，','同 172；英文截斷'),
(185,'申請大法官解釋','聲請大法官解釋','同音；機關向大法官為聲請（用語）'),
(196,'行政曆法','行政立法','上下文：列舉五院，同音'),
(199,'這個下面的 Karlschmidt','這個下面的 Carl Schmitt','名表'),
(199,'但是 Karlschmidt','但是 Carl Schmitt','名表'),
(199,'記住他的公司','記住他的公式','上下文：形式論證一路往下推，音近'),
(200,'Karschmidt','Carl Schmitt','名表'),
(200,'Hanskelstein','Hans Kelsen','名表'),
(201,'As Guarding of the','As Guardian of the','Schmitt 第一章標題 The judiciary as guardian of the constitution'),
(206,'Cart Schmitt','Carl Schmitt','名表'),
(206,'批評 Huskelsen','批評 Hans Kelsen','名表'),
(206,'看到的 Huskelsen','看到的 Hans Kelsen','名表'),
(207,'Ministerial Limits','Material Limits','Schmitt 第 2 節標題 Material limits of adjudication（Vinx 本 90 頁）'),
(207,'決職限制','實質限制','上下文：Material limits，後句「實體限制」'),
(208,'沒有犯','沒有翻','上下文：本段未譯讀，音近'),
(209,'威馬憲法','威瑪憲法','Weimar 通行譯名'),
(210,'Let it stop in its content','that is doubtful in its content','Schmitt 第 3 節標題（Vinx 本 107 頁）；後句「憲法法在內容方面有疑義」'),
(211,'Hans Coulson','Hans Kelsen','名表'),
(211,'權威性的產事','權威性的闡釋','同音；前句「權威性的界定」'),
(212,'Hunskilsen','Hans Kelsen','名表'),
(213,'Hunskilsen','Hans Kelsen','名表（所指何人另見待核）'),
(214,'做了一些選意','做了一些選譯','上下文：Vinx 譯本為選譯，音近'),
(215,'所產生出來的抑制','所產生出來的意志','同音；同質社群之政治決定'),
(216,'第一個合約','訂一個合約','上下文：社會契約，音近'),
(217,'頁的小柱 71','頁的小註 71','Schmitt 123 頁註 71（W05_notes.tex 681--687 行）'),
(217,'這個小柱 71','這個小註 71','同上'),
(218,'但是小柱 71','但是小註 71','同上'),
(218,'小柱 71 他講了','小註 71 他講了','同上'),
(218,'蠟燭還沒洗面前','蠟燭還沒熄滅前','上下文，音近'),
(218,'Hanskelsen,Hanikman-Stex-Level','Hans Kelsen,Allgemeine Staatslehre','註 71 首引 Allgemeine Staatslehre (Berlin, 1925), p. 324；後句「一般國家法，1925 年的 324 頁」'),
(219,'第 1 個引柱','第 1 個引註','上下文：註 71 所列出處'),
(219,'第 2 個引柱','第 2 個引註','同上'),
(219,'Theism of the Welt, their democracy','Wesen und Wert der Demokratie','註 71 第二引：Wesen und Wert der Demokratie, 2nd edn (Tübingen, 1929)'),
(219,'Tippington','Tübingen','同上'),
(219,'Veism und Entwicklung der Staatsgerichtsparkheit','Wesen und Entwicklung der Staatsgerichtsbarkeit','註 71 第三引；本週 Kelsen 篇原題'),
(221,'裡面的建法','裡面的憲法','上下文：聯邦國家的憲法訴訟，音近'),
(222,'人就叫做 Hanskelsen','人就叫做 Hans Kelsen','名表'),
(222,'assurance,假定','assumes,假定','註 71：The whole report assumes that'),
(223,'statute equals not','statute equals norm','註 71：constitutional statute equals norm'),
(223,'concept of not','concept of norm','註 71：The ambiguous concept of norm'),
(223,'遺花接木','移花接木','成語'),
(224,'帶換成','代換成','同音'),
(224,'things come as norms','things count as norms','註 71：all kinds of things count as norms'),
(227,'a slight of hand','a sleight of hand','註 71：by a sleight of hand'),
(232,'義直的社會','異質的社會','上下文：與同質性對舉，音近'),
(233,'義直性很高','異質性很高','同上'),
(234,'一天大晚上','一天到晚上','上下文，音近'),
(236,'畫不可能為可能','化不可能為可能','成語'),
(249,'一出手內沙拉','一出手那剎那','上下文，音近'),
(250,'洗舞了','習武了','上下文：練拳，同音'),
(251,'人稱哲理','人生哲理','上下文，音近'),
(252,'Rashmitt','Carl Schmitt','名表'),
(252,'現在 79 月','現在 79 頁','Schmitt 第 1 節始於 Vinx 本 79 頁；頁碼非月份'),
(252,'不是憲法所規者','不是憲法守護者','Schmitt 79 頁：not guardians of the constitution in the precise meaning of the term'),
(252,'meaning of the court','meaning of the term','同上'),
(253,'裁判的法律不是','裁判的法院不是','上下文：trial-deciding courts'),
(253,'憲法所規者','憲法守護者','同 252'),
(254,'比你為','比擬為','上下文，音近'),
(255,'者不孝','者無效','上下文：牴觸者無效，音近（語序另見待核）'),
(257,'他這麼宣誓','他這麼宣示','上下文：判決宣示其審查權，同音'),
(259,'《大法官司日第二號》','《大法官釋字第二號》','上下文：大法官解釋編號，音近（號次見待核）'),
(259,'《權力分立新聞》','《權力分立新論》','名表；W05_qa.tex 課堂記錄《權力分立新論》改版'),
(260,'辦品','辦法','上下文'),
(268,'together different','altogether different','Schmitt 80 頁：socially and politically altogether different situation'),
(273,'Angro-Saxon','Anglo-Saxon','Schmitt 80 頁'),
(274,'Cases or consciousness','Cases or controversies','美國憲法第 3 條 cases or controversies；W05_qa.tex'),
(274,'規憲審查','違憲審查','名表用語，音近'),
(275,'Reichesgericht','Reichsgericht','德文拼法'),
(275,'地口法院','帝國法院','Reichsgericht 譯名；257 同'),
(275,'拒絕試用','拒絕適用','上下文：deny application'),
(275,'權威信的解釋','權威性的解釋','同音'),
]
breaks=[
(165,'','1',''),(167,'。','1',''),(168,'','1',''),(169,'0','',''),(172,'','1',''),(173,'。','',''),(174,'','1',''),
(177,'，','',''),(185,'。','',''),(186,'','1',''),(195,'','1',''),(198,'','1',''),
(199,'','S','Schmitt《憲法的守護者》第一章的章節標題'),(201,'','1',''),(203,'','1',''),(204,'。','',''),(205,'','1',''),
(207,'','S','裁判的實質界限（第 2 節，從略）'),(209,'','1',''),
(210,'','S','對內容有疑義之憲法律的權威性確定（第 3 節）'),(212,'','1',''),
(214,'','S','憲法轉化為憲法契約的傾向與註 71 對 Kelsen 的批評（第 4 節 c）'),(215,'。','',''),(216,'','1',''),(217,'。','',''),(218,'。','1',''),(219,'','1',''),
(221,'','1',''),(223,'','1',''),(224,'','1',''),(226,'','1',''),(228,'','1',''),(229,'？','',''),
(234,'','1',''),(236,'','1',''),(237,'','1',''),(241,'','1',''),(242,'','1',''),(245,'','1',''),(248,'','1',''),
(252,'','S','審判法院與附隨的實質審查權（第 1 節，79 至 80 頁）'),(253,'。','1',''),(254,'','1',''),(257,'','1',''),(258,'','1',''),
(261,'','1',''),(268,'','1',''),(271,'。','',''),(272,'','1',''),(275,'','1',''),
]
unc=[
(164,'依照那個法律來訓。','疑為「依照那個法律來審查」，與 165 句首「宣告來審查」可能是同一句的重說；未改'),
(165,'不是官的事','疑為「不是大法官的事」，ASR 漏字；依交辦不補字'),
(166,'會會然會心微笑','疑有重說或聽錯（欣然？）；未改'),
(166,'理論上講人家不要','語意不明，疑聽錯；未改'),
(167,'而不是他的再生','reformation 通常譯「變更」，「再生」疑聽錯；未改'),
(170,'這個拉丁字和一樣','疑為「跟法文一樣」（形容詞後置）；未改'),
(170,'歐名訴訟','疑為「公民訴訟」或「民眾訴訟」（W05_notes.tex 用民眾訴訟）；未改'),
(175,'我跟他們發生幾乎沒有辦法','語意不明，疑聽錯（發生激烈爭執？）；所指應為監察院聲請案的不受理，W05_qa.tex 記黨產條例前案為 unreasonable disagreement'),
(191,'是，','可能是學生作答，也可能是老師自問自答；說話人表未列'),
(196,'考、建造','疑為「考試、監察」；未改'),
(198,'它的方法獨立的','疑為「它的法官獨立的」；未改'),
(199,'很形式的對方，他是形式的對方','疑為「形式的東西／推論」；未改'),
(199,'一直往下推佔','疑為「推展」或「推演」；未改'),
(203,'The General Marks the General of Judicial Review','英文聽錯，原標題為 The general (accessory) so-called material right of judicial review；未改'),
(204,'does not constitute who go to a guardian','原文 does not constitute a guardian of the constitution in Germany；「who go to」疑聽錯，未改'),
(209,'107.93','疑為「107 頁」（第 3 節始於 Vinx 本 107 頁）；數字不改'),
(209,'德國律師憲法','疑為「德國歷史」或「帝國憲法」；未改'),
(213,'那 Hans Kelsen 他顯然是不能同意的','依文義所指應為 Schmitt（不同意此屬司法權），也可能老師口誤；拼法已改，人名待核聽'),
(215,'COSCALS','疑為 Kelsen；未改'),
(215,'從規範和章觀點','疑為「從規範的觀點」或「規範位階觀點」；未改'),
(215,'parishment','疑為 Carl Schmitt；未改'),
(217,'cratch 率的見解','疑為「Carl Schmitt 的見解」；未改'),
(218,'自由的混合','註 71 原文 liberal confusion，疑為「混淆」；未改'),
(219,'welt 形式吧','疑為 Wert（價值）；未改'),
(221,'夥合','疑為「糅合」或「結合」；未改'),
(222,'非愛妥協人','疑為「最愛妥協的人」；未改'),
(224,'規範是什麼王哥','疑為「規範是什麼玩意」；未改'),
(225,'隨著憲法，差異就不重要了','語意不明；未改'),
(227,'遍一遍','疑聽錯（變一變？）；未改'),
(234,'鄭立文','疑為鄭麗文（中國國民黨主席，習近平接見），名表未收；未改'),
(235,'如果沒有換成法律的術語','疑為「如果我們換成」，涉否定詞，不改'),
(236,'分別統治大人','疑為「分別統治兩岸人」；未改'),
(236,'一國還要兩個人','疑為「一國還要兩制」；未改'),
(237,'楊柳的這個叫什麼？沈柏洋','疑為沈伯洋（黑熊學院），名表未收；未改'),
(238,'正立文','疑為鄭麗文，本 cue 兩處；名表未收，未改'),
(239,'書起','疑為蘇起；名表未收，未改'),
(240,'稍微板一下','疑為「延一下」或「往後搬一下」；未改'),
(240,'是正式的','疑聽錯；未改'),
(241,'你的談判是沒有錯吧','語意不明；未改'),
(242,'你們彼老是寧朝','聽不出；未改'),
(248,'兩個大家動手','疑為「兩個大俠」或「兩個高手」；未改'),
(249,'動著一個圓圈圈走','疑為「繞著」；未改'),
(250,'一槍打怪','疑為「一槍打下去」；未改'),
(254,'個案仇善的法院','疑為「個案裁判的法院」；未改'),
(255,'憲法牴觸法律者','語序疑為「法律牴觸憲法者無效」，語序不改'),
(256,'Material Judicial 語言','疑為 Material Judicial Review；未改'),
(256,'有沒有牴觸效應','疑為「牴觸憲法」；未改'),
(257,'1925 年的 11 月 2 月 11 月 4 號','數字重說；判決日為 1925 年 11 月 4 日（W05_notes.tex 525 行），不改'),
(257,'11 月 14 號 1925','判決日為 11 月 4 日，「14」疑聽錯；數字不改'),
(257,'（6510–6531 秒無 cue）','256 與 257 間約 21 秒無字，可能漏轉'),
(258,'法律，將就是憲，他叫做是','語意不明，疑聽錯；未改'),
(259,'釋字第二號','號次待核：老師批判的解釋是否為釋字第 2 號，數字不改'),
(259,'這個興趣就是','疑聽錯；未改'),
(262,'我要強行我們的古早下列的司司','原文 I would like to remind the reader ... of the fact，疑為「我要提醒我們的讀者下列的事實」；未改'),
(274,'安全的行使','疑為「完全的行使」；未改'),
(274,'是如何當然影響','疑聽錯；未改'),
(274,'從 cultured 的談話','疑為 Carl Schmitt；未改'),
]
def w(name,hdr,rows):
    with open(D+name,'w',newline='') as f:
        x=csv.writer(f,delimiter='\t',lineterminator='\n'); x.writerow(hdr); [x.writerow(r) for r in rows]
w('chunk3.edits.tsv',['cue','before','after','basis'],edits)
w('chunk3.breaks.tsv',['cue','end','para','title'],breaks)
w('chunk3.speakers.tsv',['cue','speaker'],[])
w('chunk3.uncertain.tsv',['cue','原字','疑為與理由'],unc)
# validate
cues={int(r['cue']):r['text'] for r in csv.DictReader(open(D+'chunk3.tsv'),delimiter='\t')}
txt=dict(cues); ok=True
for c,b,a,_ in edits:
    n=cues[c].count(b)
    if n!=1: print('COUNT',c,b,n); ok=False
    if abs(len(a)-len(b))>15: print('DIFF>15',c,b)
    txt[c]=txt[c].replace(b,a)
o=sum(map(len,cues.values())); n=sum(map(len,txt.values())); print('len',o,n,round((n-o)/o*100,2),'%')
cs=[b[0] for b in breaks]; print('incr',cs==sorted(set(cs)))
bm={b[0]:b for b in breaks}
for c,e,p,t in breaks:
    assert e in ('','。','？','！','，','0') and p in ('','1','S')
    if p:
        pc=c-1
        if pc in txt:
            pe=bm[pc][1] if pc in bm and bm[pc][1] else txt[pc].strip()[-1]
            if pe not in '。？！': print('BADPREV',c,pe); ok=False
starts=[c for c,e,p,t in breaks if p]; allc=sorted(txt)
paras=[];cur=[]
for c in allc:
    if c in starts and cur: paras.append(cur); cur=[]
    cur.append(c)
paras.append(cur)
L=sorted(((sum(len(txt[c]) for c in p),p[0],p[-1]) for p in paras),reverse=True)
print('paras',len(paras),'top',L[:6]); print('ok',ok)
