# TODO

## 這是什麼

東吳大學「憲法專題研究（四）」課程材料整理（授課教師：湯德宗），含 OCW 講義 PDF 蒐集、Seminar 導讀筆記與 LaTeX 大綱、IIAS 論文集相關素材。體量 7.9G，主要是 PDF／講義檔案，非逐字翻譯或逐條研究產出。

## 目前未提交變更盤點（2026-07-05，共 53 項，`git status --porcelain` 實查）

| 類別 | 數量 | 內容 |
|---|---|---|
| 新增 PDF（`_Material/OCW/.../pdf/`） | 34 | 大法官講堂中華民國憲法及政府課程講義掃描（第 28～39 講），約 34M |
| 新增文件 | 2 | `PDF_README.md`、一份 `.json`（OCW 目錄下） |
| 修改：`.DS_Store` | 2 | `_Generated/`、`_Material/` 各一，系統雜訊 |
| 修改：README/RESUME | 2 | OCW 課程說明文件內容更新 |
| 修改：Seminar LaTeX 產出鏈 | 10 | `Outline.tex` 及其編譯副產物（`.aux/.bbl/.bcf/.blg/.fdb_latexmk/.fls/.log/.out/.pdf/.xdv`）、`references.bib`、一份導讀筆記 `.md`——「政府體制與副署權」主題 |

## 建議收口步驟

1. `.DS_Store`：加入 `.gitignore` 全域排除，不需要每次手動處理。
2. LaTeX 編譯副產物（`.aux/.bbl/.bcf/.blg/.fdb_latexmk/.fls/.log/.out/.xdv`）：加入 `.gitignore`，只保留 `.tex` 原始檔與最終 `.pdf`。
3. 34 個新增 OCW PDF：確認是否為合法課程材料（授課教師提供或公開講堂錄影逐字稿），非侵權疑慮後即可正常 commit；本次盤點未發現檔名含個資或敏感字樣。
4. `Outline.tex` 與 `references.bib` 的內容修改：待該篇導讀筆記作者（本人）確認内容已穩定後 commit，目前未強制要求。
5. IIAS 論文集狀態：本次盤點未在目前變更中發現 IIAS 論文集相關新增/修改，如仍在進行需另立追蹤項。
6. 本次任務**不代為 commit**，上述變更保留在工作樹，由使用者自行決定分批或整批提交。
