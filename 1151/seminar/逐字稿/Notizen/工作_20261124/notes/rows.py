W='1151/seminar/readings/W06/text/waldron_source.tex'
SY='1151/seminar/syllabus.md'
APP='/Users/iw/Documents/NTU/1142/phenom-court-data/data/processed/constitutional-court-app.json'
RF='/Users/iw/Documents/NTU/1142/phenom-court-data/data/processed/constitutionalCourt-reasoning-fulltext.json'
TANG='library/text/湯德宗_權力分立新論卷二/fulltext.txt'
HRA='https://www.legislation.gov.uk/ukpga/1998/42/section/'
CAN='https://laws-lois.justice.gc.ca/eng/Const/FullText.html'
FR='https://www.conseil-constitutionnel.fr/le-bloc-de-constitutionnalite/texte-integral-de-la-constitution-du-4-octobre-1958-en-vigueur'
rows=[
(2,'核心問題','Jeremy Waldron, The Core of the Case Against Judicial Review, 115 Yale Law Journal 1346–1406（2006），課綱第 6 週指定文獻。Waldron 其時任 Columbia University 法學院 University Professor，2006 年 7 月起轉任 New York University 法學院教授。全文除導論與結論外分七部分：第壹部分界定違憲審查，第貳部分設四項假設，第參部分談論證形式，第肆、伍部分分論結果面與程序面的理由，第陸部分討論多數暴政，第柒部分處理非核心情形。',f'{SY} ; 1151/seminar/readings/index.md ; {W}',''),
(77,'tyranny of the majority','英文，多數暴政。本文第陸部分（刊本 1395 頁起）以此為題；該部分註 127 指出此語經 Tocqueville《Democracy in America》推廣，Mill 於 1840 年 10 月刊於 Edinburgh Review 的書評則認為，此語推廣的政治效果會是替保守勢力多添一套反對進步立法的說辭。',W,''),
(78,'Federalist Papers','Alexander Hamilton、James Madison、John Jay 以 Publius 為筆名所寫的 85 篇文章，1787 年 10 月至 1788 年 5 月間主要刊於紐約州兩家報紙，為促成聯邦憲法的批准而作。Madison 執筆的第 10 篇（1787 年 11 月 23 日刊於 New York Packet）把 faction（黨派）界定為一群公民，不論占全體的多數或少數，受共同的激情或利益驅使，與其他公民的權利或社會整體的長遠利益相違，並討論多數結成黨派時民選政府所受的威脅。','https://guides.loc.gov/federalist-papers/full-text ; https://avalon.law.yale.edu/18th_century/fed10.asp',''),
(159,'inappropriate','刊本 1348 頁末句：「This Essay will argue that judicial review of legislation is inappropriate as a mode of final decisionmaking in a free and democratic society.」（本文主張，在自由民主的社會，以法院審查立法作為終局決定的方式並不適當。）',W,''),
(204,'小註十一','刊本 1350 頁註 11 所舉兩部攻擊違憲審查的著作：Larry D. Kramer, The People Themselves: Popular Constitutionalism and Judicial Review（2004）；Mark Tushnet, Taking the Constitution Away from the Courts（1999）。',W,''),
(219,'反多數決的困難','語出 Alexander M. Bickel, The Least Dangerous Branch（1962）第 16 頁起題為 The Counter-Majoritarian Difficulty 的一節，首句為「The root difficulty is that judicial review is a counter-majoritarian force in our system.」（根本的難題在於，違憲審查在我們的體制裡是一股反多數的力量）。該節為課綱第 4 週指定文獻。','1151/seminar/readings/W04/text/bickel_ldb_16-26_1986_fulltext.txt ; '+SY,'bickel2004'),
(223,'脫軌的制度','刊本 1349 頁引 Bickel 之語：「judicial review is a deviant institution in the American democracy」（違憲審查是美國民主之中一項偏離常軌的制度），註 8 註明出處為 The Least Dangerous Branch 第 17 至 18 頁。',W+' ; 1151/seminar/readings/W04/text/bickel_ldb_16-26_1986_fulltext.txt',''),
(250,'臺灣現在是失效','憲法訴訟法第 52 條第 1 項規定：「判決宣告法規範違憲且應失效者，該法規範自判決生效日起失效。但主文另有諭知溯及失效或定期失效者，依其諭知。」第 2 項規定定期失效的期間，法律位階法規範不得逾二年，命令位階法規範不得逾一年。','https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=A0030159&flno=52',''),
(252,'strong judicial review','刊本 1354 頁的定義：在強式違憲審查之下，法院有權在個案中拒絕適用法律，或修正法律的效果（modify the effect of a statute），使其適用合於個人權利；法院並得以法律見解確立某一法律不予適用，經由 stare decisis（遵循先例）與爭點排除，使該法律實際上成為具文。更強的形式則授權法院把法律自法典中整個刪除。',W,''),
(270,'manifestation','刊本 1351 頁：「What I want to do is identify a core argument against judicial review that is independent of both its historical manifestations and questions about its particular effects」，historical manifestations 指違憲審查在各國歷史上呈現的具體樣貌，particular effects 指它作成的個別裁判及其好壞。',W,''),
(303,'血肉','刊本 1351 頁，Waldron 引 Frank Michelman 為 Kramer《The People Themselves》所寫的封底推薦語，稱該書的歷史敘述「puts flesh on the bones of debates over judicial review and popular constitutionalism」；Waldron 自述要「take off some of the flesh and boil down the normative argument to its bare bones」（剔去部分血肉，把規範論證熬到只剩骨架）。',W,''),
(333,'precedent of text and interpretation','刊本 1353 頁原文為「on the contrary, it distracts them with side-issues about precedent, texts, and interpretation」，所列為先例、文本與解釋三項旁枝問題。',W,''),
(365,'weak judicial review','刊本 1355 頁的定義：「courts may scrutinize legislation for its conformity to individual rights but they may not decline to apply it (or moderate its application) simply because rights would otherwise be violated.」（法院得審查立法是否合於個人權利，但不得僅因權利將受侵害而拒絕適用或緩和其適用。）Waldron 以英國、紐西蘭為例，並引 Stephen Gardbaum, The New Commonwealth Model of Constitutionalism, 49 American Journal of Comparative Law 707（2001）。',W,''),
(375,'拒絕適用他認為違法的命令','司法院釋字第 216 號解釋（1987 年 6 月 19 日）：「各機關依其職掌就有關法規為釋示之行政命令，法官於審判案件時，固可予以引用，但仍得依據法律，表示適當之不同見解，並不受其拘束」，並稱釋字第 137 號解釋即本此意旨。中華民國憲法第 80 條規定法官依據法律獨立審判，不受任何干涉。',APP+' ; https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=A0000001&flno=80',''),
(520,'合憲性解釋','法律有數種解釋可能時，採取與憲法相符的解釋，排除牴觸憲法的解釋。司法院釋字第 572 號解釋理由書謂法官聲請解釋時，「如僅對法律是否違憲發生疑義，或系爭法律有合憲解釋之可能者，尚難謂已提出客觀上形成確信法律為違憲之具體理由」。',RF,''),
(628,'509 嘛','司法院釋字第 509 號解釋（2000 年 7 月 7 日）認刑法第 310 條第 1 項及第 2 項誹謗罪符合憲法第 23 條之意旨；就同條第 3 項前段「能證明其為真實者不罰」，解釋文謂「行為人雖不能證明言論內容為真實，但依其所提證據資料，認為行為人有相當理由確信其為真實者，即不能以誹謗罪之刑責相繩」，並據此認該項與憲法保障言論自由之旨趣並無牴觸。',APP,''),
(695,'declaration of incompatibility','英國 Human Rights Act 1998 第 4 條第 2 項規定，法院認定主要立法的條文與公約權利不相容者，得宣告其不相容；第 6 項規定此項宣告「does not affect the validity, continuing operation or enforcement of the provision in respect of which it is given」，對該訴訟的當事人亦無拘束力。依第 5 項，得為宣告的法院包括最高法院、樞密院司法委員會，以及英格蘭與威爾斯的高等法院與上訴法院等。',HRA+'4',''),
(709,'European Convention of Human Rights','正式名稱為 Convention for the Protection of Human Rights and Fundamental Freedoms（保障人權及基本自由公約），1950 年 11 月 4 日由歐洲理事會會員國於羅馬簽署。Human Rights Act 1998 第 1 條所稱 Convention rights，指公約第 2 條至第 12 條、第 14 條，第一議定書第 1 條至第 3 條，及第十三議定書第 1 條所列的權利與基本自由。','https://www.echr.coe.int/documents/d/echr/convention_ENG ; '+HRA+'1',''),
(725,'Human Rights Act','Human Rights Act 1998（1998 c. 42），1998 年 11 月 9 日制定，立法目的為使歐洲人權公約保障的權利與自由在英國法上進一步生效。依 Human Rights Act 1998 (Commencement No. 2) Order 2000，該法尚未施行的條文自 2000 年 10 月 2 日施行。',HRA+'1 ; https://www.legislation.gov.uk/uksi/2000/1851/article/2',''),
(761,'兩公約內國法化','公民與政治權利國際公約及經濟社會文化權利國際公約施行法，2009 年 4 月 22 日制定公布，行政院以同年 10 月 29 日院臺外字第 0980067638 號令定自同年 12 月 10 日施行。第 2 條規定：「兩公約所揭示保障人權之規定，具有國內法律之效力。」','https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0020028 ; https://law.moj.gov.tw/LawClass/LawHistory.aspx?pcode=I0020028',''),
(819,'要四分之三','中華民國憲法增修條文第 12 條規定：「憲法之修改，須經立法院立法委員四分之一之提議，四分之三之出席，及出席委員四分之三之決議，提出憲法修正案，並於公告半年後，經中華民國自由地區選舉人投票複決，有效同意票過選舉人總額之半數，即通過之」。','https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=A0000002&flno=12',''),
(820,'美國要四分之三','美國聯邦憲法第 5 條規定，修正案由國會兩院各三分之二認為必要時提出，或依三分之二州議會的請求召開制憲會議提出；經四分之三州議會或四分之三州的制憲會議批准，即成為憲法的一部分。','https://www.archives.gov/founding-docs/constitution-transcript',''),
(829,'英國最高法院','Supreme Court of the United Kingdom，依 Constitutional Reform Act 2005 第 23 條設立；依 Constitutional Reform Act 2005 (Commencement No. 11) Order 2009，第 23 條至第 44 條自 2009 年 10 月 1 日施行。Human Rights Act 1998 第 4 條第 5 項第 a 款所列得為不相容宣告的法院，同日改為最高法院。','https://www.legislation.gov.uk/ukpga/2005/4/section/23 ; https://www.legislation.gov.uk/uksi/2009/1604/made ; '+HRA+'4',''),
(861,'fast-track legislative procedure','Waldron 所指為 Human Rights Act 1998 第 10 條（本文註 28）：法律條文經依第 4 條宣告不相容，且當事人已表示不上訴、上訴期間已過或上訴已終結者，部長認有不得已的理由（compelling reasons）時，得以命令修正該法律至消除不相容所必要的程度。此種命令稱為 remedial order。',HRA+'10 ; '+W,''),
(876,'逕付二讀','立法院職權行使法第 8 條第 2 項規定，政府機關提出之議案或立法委員提出之法律案，應先送程序委員會，提報院會朗讀標題後，即應交付有關委員會審查；「但有出席委員提議，二十人以上連署或附議，經表決通過，得逕付二讀。」','https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=A0020058&flno=8',''),
(912,'紐西蘭','New Zealand Bill of Rights Act 1990 第 4 條規定，法院不得僅因法律條文與該法所列權利不一致，即認其已被默示廢止、無效，或拒絕適用；第 6 條規定法律可解釋為與該法權利相符者，應優先採取該解釋。刊本 1356 頁兩條均有引錄，Waldron 並指出紐西蘭法院即使自行作出不一致的宣告，該宣告對立法程序亦不生英國法那樣的效果。',W,''),
(948,'加拿大憲法裡面的人權規定','指 Canadian Charter of Rights and Freedoms（加拿大權利與自由憲章），為 Constitution Act, 1982 第一部分。同法第 52 條第 1 項規定，加拿大憲法為加拿大的最高法，任何法律與憲法規定牴觸者，於牴觸的範圍內不生效力。',CAN,''),
(964,'notwithstanding clause','指加拿大權利與自由憲章第 33 條，刊本 1356 頁註 32 錄其第 1、2 項：國會或省議會得於法律中明示宣告，該法律或其條文排除憲章第 2 條或第 7 條至第 15 條的適用而施行。依第 3 項，此項宣告自生效起五年失效，第 4 項許其重新制定。Waldron 在 1356 至 1357 頁稱此條款實際上很少援用，故把加拿大的制度計為強式違憲審查。',CAN+' ; '+W,''),
(1003,'像德國人是兩個都有','德國基本法第 94 條第 1 項第 2 款規定，聯邦憲法法院經聯邦政府、邦政府或聯邦議會議員四分之一聲請，就聯邦法或邦法與基本法是否相符的爭議或疑義為裁判，即抽象規範審查（abstrakte Normenkontrolle）；第 100 條第 1 項規定，法院認為裁判所據的法律違憲者，應停止訴訟程序，聲請聯邦憲法法院裁判，即具體規範審查（konkrete Normenkontrolle）。','https://www.gesetze-im-internet.de/gg/art_94.html ; https://www.gesetze-im-internet.de/gg/art_100.html',''),
(1004,'像法國人只有抽象沒有具體','法國第五共和憲法第 61 條規定，法律於公布前，得由總統、總理、國民議會議長、參議院議長或六十名國民議會議員、六十名參議員提請憲法委員會審查。2008 年修憲增訂第 61-1 條：訴訟繫屬中主張法律條文侵害憲法保障的權利與自由者，經中央行政法院（Conseil d’État）或最高法院（Cour de cassation）移送，憲法委員會得受理之，稱合憲性優先問題（question prioritaire de constitutionnalité）。此程序自 2010 年 3 月 1 日起實施。',FR+' ; https://www.conseil-constitutionnel.fr/decisions/la-qpc','const1958'),
(1005,'像美國人只有具體沒有抽象','美國聯邦憲法第 3 條第 2 項第 1 款規定，司法權及於依憲法、合眾國法律與條約所生的一切案件（Cases），以及該款所列各類爭議（Controversies），聯邦法院的違憲審查在具體案件中為之。','https://www.archives.gov/founding-docs/constitution-transcript',''),
(1045,'the place of individual right','刊本 1357 頁：「A second distinction among types of judicial review pays attention to the place of individual rights in the constitutional system of a society.」在美國，權利審查屬一般憲法審查的一部分，法院基於個人權利宣告法律違憲，與基於其他憲法限制宣告違憲同其精神；1358 頁另舉英國依 Human Rights Act 進行的弱式審查，其所據的權利法案不屬於（結構性的）憲法。',W,''),
(1114,'posteriori review','拉丁文 a posteriori 意為「由後」，ex ante 意為「事前」。刊本 1358 至 1359 頁的第三種區分，一方是美國式的 a posteriori review，在具體訴訟中進行，有時在法律制定很久之後；另一方是 ex ante review，由專設的憲法法院在法案制定的最後階段作抽象評估。Waldron 說明本文集中討論前者。',W,''),
(1126,'老師這個文章裡面有寫','湯德宗〈論違憲審查制度的改進：由「多元多軌」到「一元單軌」的改進方案〉，收於《違憲審查與動態平衡：權力分立新論 卷二》（增訂三版，元照，2005），刊本頁 175 起。該文壹部分以集權式與分權式、抽象與具體、事前與事後、諮詢性與拘束性四組區分比較各國制度；課綱所列教科書為該書增訂五版（2026）。',TANG+' ; '+SY,''),
(1128,'這個叫做憲法委','指法國憲法委員會（Conseil constitutionnel），規定於第五共和憲法第七章。第 56 條規定委員九人，任期九年不得連任，每三年改任三分之一，由總統、國民議會議長、參議院議長各任命三人，卸任總統為當然終身委員。第 24 條規定國會由國民議會與參議院組成。',FR,''),
(1162,'普通法院','刊本 1359 頁的第四種區分：「Judicial review can be carried out by ordinary courts (as in the Massachusetts case we began with) or it can be carried out by a specialized constitutional court.」所稱麻州案件為導論開頭的 Goodridge v. Department of Public Health（2003）。Waldron 說明此區分與後文的論點相關：一般法院的法官受審判紀律牽引，就權利直接說理的能力常被高估。',W,''),
(1171,'集權式的違憲審查','湯德宗〈論違憲審查制度的改進〉壹、一界定：「集權式審查」（centralized review）指一國之內僅有某特定法院（或特定機關）可為違憲審查，原型見於奧地利 1920 年 10 月 1 日頒布的憲法，現存典範為德國聯邦憲法法院；「分權式審查」（decentralized review）指各個法院皆可為違憲審查，原型見於美國憲法。該文註中說明亦有稱「集中審查」者（蘇永欽），其意或為避免「集權」二字在中文的負面意涵，並主張兩詞意涵不同。',TANG,''),
(1396,'三讀程序','立法院職權行使法第 7 條規定：「立法院依憲法第六十三條規定所議決之議案，除法律案、預算案應經三讀會議決外，其餘均經二讀會議決之。」','https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=A0020058&flno=7',''),
(1452,'委任代表','議員依選區選民指示行事者為委任代表。德國基本法第 38 條第 1 項第 2 句規定聯邦議會議員「Vertreter des ganzen Volkes, an Aufträge und Weisungen nicht gebunden und nur ihrem Gewissen unterworfen」（為全體人民的代表，不受委託與指示拘束，只服從自己的良知）。刊本 1361 頁 Waldron 寫議員有時以選區選民的利益與意見為重，有時以 virtual representation（虛擬代表）的方式考量整個社會的利益與意見。','https://www.gesetze-im-internet.de/gg/art_38.html ; '+W,''),
(1479,'負責任的自治','刊本 1361 頁原文為「a culture of democracy, valuing responsible deliberation and political equality」（重視負責任的審議與政治平等的民主文化）；1362 頁接著說明第二項價值 political equality。',W,''),
(1494,'deliberation','英文，指審慎的討論與權衡，政治理論上通譯「審議」。課綱第 9 週 Ferejohn 與 Pasquino 的 Constitutional Courts as Deliberative Institutions、第 12 週 Castro 的 Deliberative Democracy and the Counter-majoritarian Difficulty 均以此詞立題。',SY,''),
(1505,'比例代表','中華民國憲法增修條文第 4 條第 1 項規定，立法委員 113 人，其中自由地區直轄市、縣市 73 人，平地原住民及山地原住民各 3 人，全國不分區及僑居國外國民共 34 人；第 2 項規定全國不分區及僑居國外國民名額依政黨名單投票選舉，由獲得百分之五以上政黨選舉票的政黨依得票比率選出。','https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=A0000002&flno=4',''),
(1567,'大罷免','2025 年 7 月 26 日與 8 月 23 日，第 11 屆立法委員罷免案分兩次投票，計 24 件與 7 件。中央選舉委員會 2025 年 8 月 1 日中選務字第 1143150602 號、8 月 29 日中選務字第 1143150700 號公告的投票結果均為否決。','https://web.cec.gov.tw/api/file/b35ac130-d35d-4a9e-a145-cee7b7c4b8d2.pdf ; https://web.cec.gov.tw/api/file/014afdf7-0209-4598-a1f1-9a2b23ae501c.pdf',''),
(1637,'by abstract reference','刊本 1363 頁 Waldron 假設所討論的法院「do not act on their own motion or by abstract reference, but rather respond to particular claims brought by particular litigants」。abstract reference 的例子如加拿大最高法院法第 53 條：Governor in Council（總督會同內閣）得就憲法的解釋、聯邦或省法律的合憲性等重要法律或事實問題，提交最高法院審理並陳述意見。Waldron 在 1358 至 1359 頁第三種區分已提到憲法法院就法案所作的抽象評估，並說明本文集中討論事後審查。',W+' ; https://laws-lois.justice.gc.ca/eng/acts/s-26/FullText.html',''),
(1690,'唯一的有權的釋憲法院機關','中華民國憲法第 78 條規定：「司法院解釋憲法，並有統一解釋法律及命令之權。」憲法訴訟法第 1 條第 1 項規定，司法院大法官組成憲法法庭，審理法規範憲法審查及裁判憲法審查、機關爭議、總統副總統彈劾、政黨違憲解散、地方自治保障與統一解釋法律及命令等案件。','https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=A0000001&flno=78 ; https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=A0030159&flno=1',''),
]
import sys
out=sys.argv[1]
with open(out,'w',encoding='utf-8') as f:
    f.write('cue\t詞\t註\t出處\t引\n')
    for r in rows: f.write('\t'.join(str(x) for x in r)+'\n')
with open(sys.argv[2],'w',encoding='utf-8') as f:
    for r in rows: f.write(r[2]+'\n\n')
print(len(rows))
