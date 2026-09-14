# WORKLOG

- 2026-09-14：倉庫改成跨學期結構，收 1151 學期材料。
  - 目錄：`library/`（五本指定書與一篇指定論文、文字層一本一夾）、`cases/`（釋字 31 件、憲判 4 件、法規）、
    `ocw/`（大法官講堂講義 114 份）、`1142/`、`1151/`、`notes/`（原 `mkdocs/`）、`latex/`、`scripts/`。
    `_Material/`、`_Assets/`、`_Generated/` 三個頂層目錄不再存在。
  - 指定書改名為「作者_書名_版_年」，新增 Gerhardt、Griffin、Rowe 編 *Constitutional Theory* 第三版（1151 指定書）。
    五個 `_parsed*` 目錄併成 `library/text/{alexander,barber_fleming,beatty,gaf}/`。
  - 卷內文書歸入 `cases/`：111 年憲判字第 6 號 43 件（本機唯一一份）、釋字第 738 號 20 件與其文字層 21 件、
    第 769 號。原在 `_Material/Seminar/06_導讀認領_我的題目/台灣/` 底下。
  - 字型：27 個字型檔、`categories/` 70 檔與 `compare/` 移至 `~/Documents/NTU/1142/font-lab/packs/scu-constitutional/`
    （該倉已 gitignore `packs/`），本倉留 `latex/fonts/` 的 manifest 與腳本。腳本讀 `SCU_FONT_PACK`。
    安裝前綴由 `TranslationFonts` 改為 `SCUQuoteCards`，與 `uninstall_user_fonts.sh` 所刪的前綴一致。
  - 刪除：`_Generated/font_compare/` 46 項（含 29 個字型檔）、0 位元組的 `-l.txt`、只含 symlink 的
    `_Material/Laws` 與 `_Material/Undergrad`、空的 `_Material/研究資料`、`_Material/Seminar/README.md`、
    全倉 `.DS_Store`、LaTeX 編譯副產物。`稿/` 目錄刪 6 檔：
    `W02_Introduction_Perry_Alexander_FULL_CLEAN.md.pre_format.bak`、`…FULL_CLEAN.md.punct.bak`、
    `…FULL_RAW.md.bak`、`…RAW.md.bak`、`W02_Introduction_Perry_Alexander_RAW.md`（與短版內容相同）、
    `W02_Introduction_Perry_Alexander_FULL_RAW.md`（已被清稿取代）。保留的三檔改放他處：
    `W01_0223.md` 是 W01 課堂逐字稿，改名 `W01_0223_逐字稿.md` 留在研討會筆記；
    `…FULL_CLEAN.md` 與 `…Perry_Alexander.md` 是 Alexander 導論的清稿與節錄，移入 `library/text/alexander/`。
  - 113 年憲判字第 9 號的兩個 `pages.json` 原為指向自身路徑的斷鏈 symlink，以 `scripts/extract_pdf_text.py`
    自判決 PDF（332 頁）與摘要 PDF（81 頁）重產。全倉斷鏈 symlink 歸零。
  - 釋字第 632 號 `_parsed/` 三個檔名長 315 至 319 位元組，超過 Linux 單一檔名 255 位元組上限，
    GitHub Actions 自 2026-07-06 起每次 checkout 都失敗；改名為 `6_632抄本_六份意見書合訂_*`。
  - `requirements.txt` 與 `mkdocs.yml` 移除 `mkdocs-sitemap-plugin`——該套件 PyPI 上不存在（404），
    mkdocs-material 本身即產生 sitemap.xml。`notes/Dockerfile` 補齊 rss、jupyter 與社群卡片的相依套件。
  - 站台：`mkdocs/My_Notes/` 改為 `notes/docs/`，站內按 `<學期>/<課>/` 分。`site_name`、`site_url`、
    `repo_url` 改用新倉名。新寫站首頁、1151 研討會頁與臺大旁聽頁的 `index.md`。
  - 本機路徑：倉內寫死 `1142_SCU_CONSTITUTIONAL_LAW` 的 26 個檔改為倉內相對路徑（21 個 OCR json、5 篇筆記）。
- 2026-07-11：中研院法研所出版品快照（`_Material/研究資料/中研院法律學研究所/`，533MB）與抓取腳本 `scripts/fetch_iias_publications.py` 遷出至專門資料倉 `~/Documents/NTU/1142/iias-publications-data`（GitHub: mt019/iias-publications-data，private）。本倉僅移除工作樹檔案，git 歷史內舊 blob 未清（重寫歷史需另行授權）。
- 2026-07-05：套用工作區治理制度，建立 `TODO.md` 盤點目前 53 項未提交變更（34 新增 OCW PDF、2 份 `.DS_Store`、2 份 README/RESUME 修改、13 項 Seminar LaTeX 編譯鏈修改）；變更本身未 commit，留待使用者決定收口方式。倉庫體量 7.9G，未執行任何刪除或內容修改。
