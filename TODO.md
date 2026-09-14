# TODO

## 這是什麼

東吳大學法律學系湯德宗老師憲法課程的材料與筆記，按學期收。目錄體系見 `README.md`。

## git 歷史的清理與推送現況

2026-09-14 以 `git filter-repo --invert-paths` 剔除 `_Material`、`_Assets`、`_Generated` 三個已不存在的
頂層目錄，合計 3,543 MiB；另刪掉 `refs/codex/turn-diffs/checkpoints/` 底下四個 6 月的 ref，各自釘著一份
16,845 檔的舊版完整樹，filter-repo 跑完之後的 3.2 GB 就是被它們拉著。`.git` 從 3.3 GB 降到 489 MB，
HEAD 的樹雜湊 `280cfb52` 改寫前後相同，commit 由 19 個變成 18 個（有一個改動全在 `_Assets` 底下，
剔除後成為空 commit）。

改寫前的完整鏡像在 `~/Documents/NTU/_backup_SCU_Constitutional_Law_Tang_git_20260914.git`，19 個 commit
與四個 codex ref 都在。推送確認成功之後才可以刪它。

本機 `main` 在 `4afb29c`，遠端停在 `3de80a7`，也就是 2026-09-14 重整之前的結構；該 commit 的 Actions
建置失敗，站台上線的仍是前一次建置成功時產出的那一份。HTTPS 推送在 21.5 MB 與 70 MB 兩種大小上都以
`unexpected disconnect while reading sideband packet` 與 HTTP 408 中斷，換 HTTP/1.1、調
`http.postBuffer`、把 blob 切成 25 MB 一塊串成臨時分支分批預傳，三種都沒過；3 MiB 以下的推送全部
成功，上傳端每秒約 800 KB。剩下的作法是產一把 ed25519 金鑰、用 `gh` 登記到 mt019 帳號，改走 SSH
推那 605 MiB。2026-09-14 站主裁定先不推、倉維持公開。

## 倉內 PDF 與公開範圍

倉裡 HEAD 的 605 MiB 有 485 MiB 是 PDF，共 192 個：`cases/` 271 MiB、`library/books/` 148 MiB、
`1142/seminar/readings/` 126 MiB、`ocw/` 58 MiB。其中教科書掃描本與期刊論文在公開倉裡有授權疑慮，
2026-07-06 那個 commit 已經把官方 ZIP 與彙編 PDF 1.7 GB 遷到 `phenom-court-data`（現為 private），
同樣的處置對這幾類材料適用。站主 2026-09-14 決定維持公開、不移出。

## 1151 指定文獻取件

`1151/seminar/readings/index.md` 登記的 20 篇，17 篇未取。可走的路：學校圖書館電子資源（Oxford
Journals、HeinOnline、Westlaw）、館際合作。取得後放進該週資料夾並回填該表的「本機路徑」與「狀態」。

## 1151 指定書採購

湯德宗《釋憲學思心路》（上、中、下冊）二版（2026）、《違憲審查與動態平衡：權力分立新論 卷二》
增訂五版（2026），本機沒有。

## 站台 site_author 欄位

`notes/mkdocs.yml` 的 `site_author` 寫「湯德宗」。站上的筆記是我寫的，這個欄位應寫誰，待站主決定。
