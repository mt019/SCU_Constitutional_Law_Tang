# sources/raw/chan 原始檔索引

取件方式：agent 以 curl 取得（2026-10-05）。PDF 以 `pdftotext -layout` 轉文字層；HTML 去標籤後存 .txt；CBETA 的 JSON 以腳本依行頭 `lb` 切成「行號 TAB 文字」的 .txt（行號以 JSON 內 `lb` 為準）。

| 檔名 | 完整 URL | 抓取時間 | HTTP | 內容 |
|---|---|---|---|---|
| `CBETA-T2008-juan1-2026.json`／`.txt` | https://cbdata.dila.edu.tw/stable/juans?edition=CBETA&work=T2008&juan=1 | 2026-10-05 15:43 | 200 | 大正藏 T2008《六祖大師法寶壇經》（宗寶本）全卷 |
| `CBETA-T2007-juan1-2026.json`／`.txt` | 同上，work=T2007&juan=1 | 15:43 | 200 | 大正藏 T2007 敦煌本《壇經》全卷 |
| `CBETA-T2076-juan{1,3,5,9,12,17,19,24,25}-2026.json`／`.txt` | 同上，work=T2076&juan=N | 15:43 | 200 | 大正藏 T2076《景德傳燈錄》各卷；目錄（慧可至弘忍標題）在卷三卷首 p0216 |
| `NTU佛學-六祖壇經簡介綱要-bj013122281.pdf`／`.txt` | https://buddhism.lib.ntu.edu.tw/FULLTEXT/JR-BJ013/bj013122281.pdf（跳轉至 dlbs.liberal.ntu.edu.tw 同路徑） | 15:45 | 200 | 臺大佛學數位圖書館〈《六祖壇經》簡介（綱要）〉，8 頁。文字層用 CJK 相容字，比對須 NFC 正規化 |
| `內政部宗教資訊網-六祖壇經-cid651.html`／`.txt` | https://religion.moi.gov.tw/Knowledge/Content?ci=2&cid=651 | 15:45 | 200 | 宗教知識〈六祖壇經〉條 |
| `印順-中國禪宗史自序-ChinaChanHistory.pdf`／`.txt` | https://www.buddhistelibrary.org/zh/albums/ChineseDharma/ChinaChanHistory.pdf | 15:45 | 200 | 《中國禪宗史》簡體轉錄全書，112 頁；〈自序〉在 PDF 第 1 至 6 頁，無刊本頁碼 |
| `NTU佛學-敦煌新本六祖壇經簡介-102750.htm`／`.txt` | https://dlbs.liberal.ntu.edu.tw/FULLTEXT/JR-AN/102750.htm | 15:45 | 200 | 《新版 敦煌新本‧六祖壇經》簡介；頁面標「繁體版」「簡體版」的兩段，標示與字形對調 |
| `NTU佛學書目-荷澤大師神會傳-seq264011.html`／`.txt` | https://buddhism.lib.ntu.edu.tw/search/search_detail.jsp?seq=264011（跳轉至 dlbs 主機） | 15:45 | 200 | 臺大佛學數位圖書館書目，《神會和尚遺集》1968 年中央研究院臺北版 |
| `CRTA-Anubis挑戰頁-Mozilla-UA.html` | https://crta.info/wiki/神會和尚遺集_-_DCCB0067 | 15:45 | 200 | 以 Mozilla UA 取得的是 Anubis 工作量證明挑戰頁，無內容，僅留作紀錄 |
| `CRTA-神會和尚遺集-DCCB0067.html`／`.txt` | 同上 | 15:48 | 200 | 改以 curl 預設 UA 取得的條目本文（Chinese Religious Text Authority） |
| `Terebess-shenhui.html`／`.txt` | https://terebess.hu/zen/shenhui.html | 15:45 | 200 | Terebess Zen 文獻頁 |
| `邱敏捷-壇經的作者與版本-nx012133999.pdf`／`.txt` | https://buddhism.lib.ntu.edu.tw/FULLTEXT/JR-NX012/nx012133999.pdf | 15:45 | 200 | 邱敏捷〈《壇經》的作者與版本〉，38 頁 |
| `張程業-錢穆禪宗研究-清華中文學報34-2025.pdf`／`.txt` | https://cl.site.nthu.edu.tw/var/file/401/1401/img/794573116.pdf | 15:45 | 200 | 《清華中文學報》第 34 期（2025 年 12 月）頁 97–147，PDF 52 頁；刊印頁碼在頁尾（PDF 第 15 頁為刊印頁 111） |
| `清華學報-Chiang-Hu-Shih-1994.html`／`.txt` | https://thjcs.site.nthu.edu.tw/p/16-1452-41503.php?Lang=en | 15:45 | 200 | 《清華學報》24 卷 1 期（1994 年 6 月）Tsan-teng Chiang 論文摘要頁 |
| `華藝-錢穆禪宗論衡摘要.html`／`.txt` | https://www.airitilibrary.com/Article/Detail/P20130308005-N202405290005-00001 | 15:45 | 200 | 華藝線上圖書館摘要頁 |
| `Commons-神會和尚遺集NLC416-檔案頁.html`／`.txt` | https://commons.wikimedia.org/wiki/File:NLC416-01jh000678-10441_神會和尚遺集.pdf | 15:48 | 200 | Wikimedia Commons 檔案頁，來源標為中國國家圖書館民國圖書 |
| `國圖NLC416-神會和尚遺集-commons.pdf` | https://upload.wikimedia.org/wikipedia/commons/2/23/NLC416-01jh000678-10441_神會和尚遺集.pdf | 15:48 | 200 | 1930 年版《神會和尚遺集》掃描本，240 頁，無文字層；版權頁在 PDF 第 239 頁 |
