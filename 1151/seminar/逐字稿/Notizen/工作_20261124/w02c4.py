import csv, re, sys
D='/Users/iw/Documents/NTU/SCU_Constitutional_Law_Tang/1151/seminar/逐字稿/Notizen/W02_0921/'
K='核對紀錄 '
P='刊本 '
edits = [
(2058,'that led its popular ratification','that have led to its popular ratification',K+'01:29:39；刊本 534 原文'),
(2068,'不好的優越','不好的譯語',K+'01:30:09；站主 2026-09-22 核定'),
(2076,'你民不服食','你名不副實',K+'01:30:23；成語'),
(2105,'不只回答來是這樣,。','',K+'01:31:16；聽不清，站主 2026-09-22 裁定刪去'),
(2117,'一個人像作家','一個很像作家',K+'01:31:43；medium 重解碼'),
(2122,'講法制式','講法制史',K+'01:31:51'),
(2123,'很有趣的法制式','很有趣的法制史',K+'01:31:52'),
(2124,'不然法制式','不然法制史',K+'01:31:53'),
(2125,'枯造沒有要動','枯燥沒有人要讀',K+'01:31:55；站主 2026-09-22 核定'),
(2126,'建構你的法制','建構你的法制史',K+'01:31:56；站主 2026-09-22 核定'),
(2132,'我們的解讀','有不同的解讀',K+'01:32:05'),
(2133,'光公的是 constitution model','光光是 constitutional moment',K+'01:32:07'),
(2134,'批批的人','批評的人',K+'01:32:09'),
(2139,'他也不隨便罵','他也不隨便罵人',K+'01:32:14'),
(2142,'The is various version of a sophisticated version','The various versions of the Sophisticated View',P+'534 原文；下句「這是複雜觀點」'),
(2152,'art complex indeed','are complex indeed',P+'534 原文'),
(2156,'on their marriage','on their merit',P+'534 原文；下句「就由他們的內容而言」'),
(2162,'conversion had succeeded','one version had succeeded',P+'534 原文 Assuming that one version has succeeded'),
(2170,'資歷與歷','資歷與履歷','音近；上下文解釋 credential'),
(2186,'one might adopt so','one might doubt so',P+'534 原文；下句「這麼懷疑」'),
(2188,'against and affirmative','against an affirmative',P+'534 原文'),
(2205,'language of the class','language of the constitution',P+'535 原文 determined by the language of the constitution'),
(2206,'憲法的文具','憲法的文句','音近；講 language of the constitution'),
(2213,'憲法的文具','憲法的文句','音近；同 2206'),
(2224,'上下棋子','上下其手','成語；講法官解釋的空間'),
(2233,'行事論的套件','形式論的條件','音近；上句 the formalist condition'),
(2235,'scholar judges','scholars, judges',P+'535 原文'),
(2243,'行事論的套件','形式論的條件','同 2233'),
(2245,'scholar judges','scholars, judges',P+'535 原文'),
(2248,'chef justice market theory','Chief Justice Marshall\'s theory',P+'535 原文 Chief Justice Marshall\'s theory of legal meaning'),
(2262,'and determinate','indeterminate',P+'535 原文 makes at least certain constitutional provisions indeterminate；下句「是不確定它的意思」'),
(2269,'interpreted and constituted','interpreted or constructed',P+'535 原文'),
(2274,'憲法文具','憲法文句','同 2206'),
(2278,'建法解釋','憲法解釋','音近；上句 constitutional interpretation'),
(2314,'通奸','通姦','法律用語；通姦罪'),
(2316,'通奸罪','通姦罪','同 2314'),
(2322,'通奸','通姦','同 2314'),
(2326,'特別有利','特別有力',P+'535 原文 This objection is particularly powerful'),
(2327,'特別有利','特別有力','同 2326'),
(2329,'價子','價值',P+'535 原文 find values in sources that lie outside the written constitution'),
(2330,'正立','證立','音近；以價值證立對成文憲法的解釋'),
(2333,'價子','價值','同 2329'),
(2334,'正立','證立','同 2330'),
(2358,'形式上會階高','形式上位階高','音近；上下文「民主的內涵高於普通的立法」'),
(2361,'以協法為準','以憲法為準',P+'537 原文 the constitution ... should morally prevail in case of conflicts'),
(2381,'功能罪事','功能最適','用語；大陸法系「功能最適」'),
(2383,'功能罪事','功能最適','同 2381'),
(2390,'還沒有成為憲法','還沒有成文憲法','上下文；英國無成文憲法'),
(2394,'最高法律','最高法院','上下文；下句「它可以宣告法律確實抵觸 1998 人權法」'),
(2403,'We\'re in a decent','where, in a decent',P+'537 原文'),
(2408,'要不要費死','要不要廢死','音近；死刑存廢為法官決定之例'),
(2420,'正立','證立','音近；上下文 not succeeded to ground the legitimacy'),
(2423,'特定的奏權','特定的授權','音近；specific authorization'),
(2429,'Aergy','I argue',P+'538 原文 In this section, I argue'),
(2437,'to record the concept','to recall the concept',P+'538 原文'),
(2457,'confirm some general','conferring some general',P+'538 原文'),
(2469,'of the sword ground','of this sort ground',P+'539 原文 General principles of this sort ground'),
(2488,'舉證則是','舉證責任','音近；上文推定正當、舉證分配'),
(2499,'grt1','GLT1',P+'539 原文'),
(2501,'abound by','are bound by',P+'539 原文'),
(2553,'the sum democratic category','some democratic pedigree',P+'539 原文 by virtue of some democratic pedigree (SLT4)'),
(2561,'within the end','within the ambit',P+'539 原文'),
(2572,'recognize a good reason for alter for action','recognize as good reasons for action',P+'539 原文'),
(2573,'no legal reasons','nor legal reasons',P+'539 原文'),
(2574,'no legal reasons','nor legal reasons',P+'539 原文'),
(2595,'antecedent law','antecedent norms',P+'544 原文'),
(2597,'in the fourth of the courts','and enforced by the courts',P+'544 原文 as understood and enforced by the courts'),
(2603,'所準具','所準據','音近；司法裁判所依據的法律'),
(2635,'建法解釋','憲法解釋','同 2278'),
(2639,'的建法解釋性論證','的憲法解釋性論證','同 2278'),
(2641,'建法解釋','憲法解釋','同 2278'),
(2642,'建法解釋','憲法解釋','同 2278'),
(2647,'建法解釋','憲法解釋','同 2278'),
(2653,'建法原則','憲法原則','同 2278；2637 作「憲法原則和法則」'),
(2655,'建法解釋','憲法解釋','同 2278'),
(2666,'Criter of Validity','Criteria of Validity',P+'544 原文 criteria of validity'),
(2670,'建法最基本的','憲法最基本的','同 2278'),
(2671,'下值','價值','音近；下句 Values'),
(2727,'猥爭','違憲','音近；依成文憲法宣告違憲'),
(2736,'民主代義補強論','民主代議補強論','用語；Ely 之 representation-reinforcement'),
(2737,'民主代義補強論','民主代議補強論','同 2736'),
(2743,'cissident','antecedent','上下文 antecedent norms；同 2773'),
(2754,'Michael Mann','Michelman',P+'556 Frank Michelman'),
(2755,'Frank Michael Mann','Frank Michelman',P+'556'),
(2765,'Sonsene','Sunstein',P+'556 Cass Sunstein；下句 deliberative democracy'),
(2769,'Ronald Dorkin','Ronald Dworkin',P+'557；下句 Equal citizenship'),
(2773,'enticident norm','antecedent norm',P+'544 起 antecedent norms'),
(2546,'沒關系','沒關係','正字'),
(2837,'關系','關係','正字'),
(2958,'沒關系','沒關係','正字'),
(2867,'Hans Kilsen 跟 Karsch mit','Hans Kelsen 跟 Carl Schmitt','名表；第 4 週起讀 Kelsen 與 Schmitt'),
(2874,'認證讀','認真讀','音近'),
(2890,'文起來','聞起來','上下文「是香的還是臭的」'),
(2900,'這學題','這學期','音近'),
(2910,'上去的學題','上去的學期','音近；同 2900'),
(2919,'請效於','傾向於','音近'),
(2922,'很難賭','很難讀','音近；指定文獻難讀'),
(2923,'大時候','到時候','音近'),
(2924,'大時候','到時候','音近'),
(2925,'大時候','到時候','音近'),
(2965,'選組','群組','音近；加入群組'),
]
unc = [
(2141,'530 試驗','疑為「534 頁」：下句所讀 The various versions... 在刊本 534；數字不依文義改'),
(2154,'and highly controversial（2154、2155 同文）','2155 與 2154 同文，各約 1 秒，疑為重複迴圈；未刪'),
(2167,'overlegization','聽不出；上下文在解釋 superior democratic credentials，未改'),
(2187,'我不可以這麼懷疑','疑為「我可以這麼懷疑」（One might doubt so）；否定詞未改'),
(2226,'籤則','聽不出，疑與「機械說」相關之詞；未改'),
(2230,'不然你只不會有正當性','疑為「不然你就不會有正當性」；否定詞句未改'),
(2234,'2234–2237','與 2244–2247 同文（on various occasions … 有很多情況是可以的），2234–2237 每 cue 約 1 秒，疑為重複迴圈；2238–2241 亦與 2250–2251 相疊；未刪'),
(2285,'計劃的計劃（2285–2289）','重複迴圈，約 9 秒；原應為 Tremblay 535「judicial review of legislation might ultimately reflect the courts\' own perspectives」一句的口譯；未刪'),
(2290,'可以終於提供的法律的觀點','聽不出；疑為「最終反映法院自己的觀點」（刊本 535 might ultimately reflect the courts\' own perspectives）；未改'),
(2292,'尤其是理想和志','疑為「偏好和利益」（preferences and interests）；未改'),
(2306,'體現出來的議詞','聽不出，疑為「意志」或「意思」；未改'),
(2324,'2324、2325','兩 cue 同文「所以是司法成為超級立法者」，疑為重複；未刪'),
(2328,'2328–2331','與 2332–2335 同文，疑為重複迴圈；未刪'),
(2339,'they can open','刊本 535 作 are \'vague\' and \'open\'；講者讀法聽不清，未改'),
(2341,'2341、2342','同文 that their historical language used，疑為重複；未刪'),
(2343,'2343–2349','與 2351–2354 同文（也就可以了／這一點變成是有意義的／第一個反對／第二個反對 537 頁），疑為重複迴圈；未刪'),
(2394,'不是宣告 1998 人權法','依上下文疑為「不能宣告（法律）違反 1998 人權法而無效」；否定詞未改'),
(2396,'退回不回看','聽不出，疑為「退回國會看」；未改'),
(2399,'主論是不對','聽不出；未改'),
(2400,'但是不是民主法來決定的','聽不出，含否定詞；未改'),
(2405,'第一審','疑為 decent（上句 in a decent democratic society）；未改'),
(2470,'when I call it a general legitimacy','刊本 539 作 what I shall call a general legitimacy；講者讀法聽不清，未改'),
(2508,'以合法的方式','刊本 GLT1 為 in a legitimate way，課堂整理作「以正當的方式」；講者可能口說「合法」，未改（2522、2542 同）'),
(2513,'自由主義的一些界限','疑為「一些見解」或「學者」；未改'),
(2515,'魯梭','疑為盧梭（刊本 539 Jean-Jacques Rousseau）；名表無此譯名，未改'),
(2534,'密尼是機關哦','聽不出，疑為「命題是機關」；未改'),
(2536,'存念都有正當性','聽不出；未改'),
(2564,'ceases are not moral permissible','刊本 539 作 are not morally permissible；前字聽不出，未改'),
(2566,'那它們就具有正當性','依上下文（如果不符合的話）疑為「不具有正當性」；否定詞未改'),
(2573,'2573、2574','兩 cue 同文 nor legal reasons that are not legitimate，疑為重複；未刪'),
(2587,'沒有辦法接應講','疑為「沒有辦法接著講」；未改'),
(2588,'5444','疑為「544 頁」（The Constitutional Law Thesis 起於刊本 544）；數字未改'),
(2709,'至少我個人不是寫不出來','依下句「理解太膚淺，做不出來」疑為「講不出來」，句中否定詞未改'),
(2715,'大家誤一頁一下','聽不出；未改'),
(2734,'有供應','疑為 Ely（下文 2752 John Ely，刊本 555）；未改'),
(2742,'那一套預設回法','聽不出，疑為「預設規範」；未改'),
(2758,'他是猶太人','講者對 Frank Michelman 的介紹，事實未核'),
(2781,'會簡直變得正當','疑為「會間接變得正當」；未改'),
(2794,'在座人不考試的局所','聽不出；課堂整理作「近期不應考的同學」；未改'),
(2829,'一直在帶外','疑為「一直在代換」（同一概念換字表述）；未改'),
(2851,'不再一個禮拜','疑為「就再一個禮拜」；否定詞未改'),
(2880,'語方能幫忙','聽不出，疑為受託翻譯的同學姓名；未改'),
(2888,'大家先乒乓簡','聽不出，疑為「品鑑」；未改'),
(2903,'做成一策碼','疑為「做成一冊嘛」；2905 同；未改'),
(2906,'被裝進程','聽不出，疑與裝訂成冊有關；未改'),
(2935,'你不是會做生意的','說話人依內容推為老師；句含否定詞，未改'),
(2956,'正前一臉，還一臉','聽不出；說話人亦不確定'),
(2897,'大家各位先等一下','說話人依內容推為班代（學生），課堂整理記費用由班代預收；2897–2968 間老師與班代交替（2928、2934、2942、2958 起為老師），全依語意推定'),
]
breaks = {}  # cue -> [end, para, title]
def b(c,end='',para='',title=''):
    r=breaks.setdefault(c,['','',''])
    if end: r[0]=end
    if para: r[1]=para
    if title: r[2]=title
paras=[2060,2084,2100,2112,2140,2159,2174,2189,2196,2209,2227,2234,2244,2253,2276,2297,2302,2313,2326,2336,2349,2356,2368,2377,2389,2402,2416,2443,2469,2489,2512,2525,2539,2549,2559,2571,2575,2598,2610,2627,2634,2657,2688,2714,2729,2751,2763,2771,2802,2826,2846,2877,2893,2897,2923,2928,2931,2934,2936,2942,2954,2958,2962]
S={2427:'一般正當性的六個命題',2586:'憲法命題的內容與兩個假設',2788:'翻譯作業、停課與後續進度'}
qs=[2202,2380,2412,2605,2651,2840,2853,2876,2911,2965,2967]
for c in qs: b(c,'？')
rows=list(csv.reader(open(D+'chunk4.tsv',encoding='utf-8'),delimiter='\t'))[1:]
text={int(r[0]):r[3] for r in rows}
order=sorted(text)
def ends_sent(c):
    e=breaks.get(c,['','',''])[0]
    if e: return e in '。？！'
    t=text[c].strip()
    return bool(t) and t[-1] in '。？！?!' and not t.endswith(',。')
for c in sorted(paras+list(S)):
    prev=order[order.index(c)-1]
    if not ends_sent(prev): b(prev,'。')
    if c in S: b(c,'','S',S[c])
    else: b(c,'','1')
speakers=[(2897,'學生'),(2928,'老師'),(2931,'學生'),(2934,'老師'),(2936,'學生'),(2942,'老師'),(2954,'學生'),(2958,'老師'),(2962,'學生')]
# write
def w(name,header,rs):
    with open(D+name,'w',encoding='utf-8') as f:
        f.write('\t'.join(header)+'\n')
        for r in rs: f.write('\t'.join(str(x) for x in r)+'\n')
w('chunk4.edits.tsv',['cue','before','after','basis'],sorted(edits,key=lambda r:r[0]))
w('chunk4.breaks.tsv',['cue','end','para','title'],[[c]+breaks[c] for c in sorted(breaks)])
w('chunk4.speakers.tsv',['cue','speaker'],speakers)
w('chunk4.uncertain.tsv',['cue','原字','疑為與理由'],sorted(unc,key=lambda r:r[0]))
# validate
ok=True
new=dict(text)
for c,bf,af,_ in edits:
    n=text[c].count(bf)
    if n!=1: print('COUNT',c,bf,n); ok=False
    if abs(len(af)-len(bf))>15: print('DIFF>15',c)
    new[c]=new[c].replace(bf,af)
a=sum(len(v) for v in text.values()); z=sum(len(v) for v in new.values())
print('chars',a,z,f'{(z-a)/a*100:.2f}%')
bc=sorted(breaks)
assert bc==sorted(set(bc))
for c in bc:
    e,p,t=breaks[c]
    assert e in ('','。','？','！','，','0'),c
    assert p in ('','1','S'),c
    if p:
        prev=order[order.index(c)-1]
        if not ends_sent(prev): print('PREV',c); ok=False
# paragraphs
starts=[c for c in order if breaks.get(c,['','',''])[1]]
segs=[]; cur=[order[0]]
for c in order[1:]:
    if c in starts: segs.append(cur); cur=[c]
    else: cur.append(c)
segs.append(cur)
L=sorted(((sum(len(new[x].replace(',。','').rstrip('。')) for x in s),s[0],s[-1]) for s in segs),reverse=True)
print('paras',len(segs),'S',len(S),'top3',L[:3])
print('OK' if ok else 'FAIL')
