import json,re
d={}
# parse tsv for 註 where text sits in col3 with trailing （改...）
def note(f,n):
    for l in open(f'Notizen/W05_1012/查核_{f}.tsv',encoding='utf-8'):
        c=l.rstrip('\n').split('\t')
        if c[0]==str(n): return c[2]
def strip(s): return re.sub(r'（(改動處|改點|原註|刪去|註文正文)[^（）]*）$','',s).strip()
for f,ns in {1:[1,5,18,19],2:[23,25,26,27,36],3:[53,57],4:[63,70,76,78],5:[81,84,88,91,92],6:[108,110]}.items():
    for n in ns: d[str(n)]={'註':strip(note(f,n))}
d['63']={'註':note(4,63)}
d['1']['出處']='library/books/Vinx_The_Guardian_of_the_Constitution_Kelsen_and_Schmitt_2015.pdf ; 1151/seminar/syllabus.md ; https://www.biographien.ac.at/oebl/oebl_K/Kelsen_Hans_1881_1973.xml'
d['5']['出處']='https://plato.stanford.edu/entries/lawphil-theory/ ; 1151/seminar/readings/W05/sources/DeGruyter-VVDStRL-Heft5-1929-Staatsgerichtsbarkeit.txt ; https://www.biographien.ac.at/oebl/oebl_K/Kelsen_Hans_1881_1973.xml'
d['84']['註']=d['84']['註'].replace('得票率 96.11%，','得票率百分之 96.11，')
d['27']['引']='kelsen1929|38--39, 58--59'
d['70']['出處']='https://udn.com/news/story/122496/9806089 ; https://udn.com/news/story/6656/9806331'
d['76']['引']='kelsen1929|75'
d['94']={'出處':'https://www.bundesfinanzhof.de/de/gericht/geschichte/onlineausstellung-rfh/bfh/epoche-1918-1933/'}
d['112']={'出處':'https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=D0020010 ; https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=D0020053'}
for k,v in d.items():
    for t in v.values():
        assert not re.search(r'[{}\\%#$&_]',v.get('註',''))
        assert '不變' not in t
json.dump(d,open('Notizen/W05_1012/查核_套用.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(d)); print(d['57']['註'][-60:], d['81']['註'], d['84']['註'][-40:])
