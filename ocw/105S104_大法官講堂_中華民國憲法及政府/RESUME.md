# OCW PDF 下載完成紀錄

原暫停時間：2026-06-15  
續抓完成時間：2026-06-27

## 目前狀態

- 課程：NTU OCW `105S104`，大法官講堂：中華民國憲法及政府
- 教師：湯德宗
- 資源頁：<https://ocw.aca.ntu.edu.tw/courses/105S104/resources>
- 目標：下載「講義」PDF，不下載影片。
- PDF 位置：`pdf/`
- 已成功下載正式 PDF：61 份
- 狀態：完成，無失敗項目。
- 完整索引：`pdf_manifest.json`
- 人讀索引：`PDF_README.md`

## 重要注意

`markdown/` 與舊 `manifest.json` 是先前錯誤以連續 item id 推測產生的替代資料，部分內容會出現「找不到網頁」或對錯講次。後續分析應使用 `pdf/` 內的 PDF 與 `pdf_manifest.json`。

OCW 原站對命令列直接下載會觸發 Cloudflare 403。可行做法是：

1. 用本機 Chrome 開啟資源頁並通過 Cloudflare。
2. 透過 Chrome DevTools Protocol 在瀏覽器上下文中讀取 `a[download]` 且 `download` 含「講義」的 61 個連結。
3. 以 `fetch(..., { credentials: "include" })` 下載 `application/pdf` bytes。
4. 下載完更新 `pdf_manifest.json` 與 `PDF_README.md`。

## 已知正確 PDF 連結規則

不要用連續 id 推測。必須從資源頁 DOM 抓實際連結。

第 9 講「違憲審查制度」的兩份 PDF 是：

- `course_item_files/5760`
- `course_item_files/5761`
