---
title: Small Caps 測試
summary: 測試 Markdown + HTML 在 MkDocs 的 small caps 呈現效果。
---

# Small Caps 測試

以下為同一句的不同寫法（建議先看第 2、3 行）：

1. 一般文字：Constitutional Interpretation
2. HTML 標籤：<span style="font-variant-caps: small-caps;">Constitutional Interpretation</span>
3. class 寫法：<span class="sc">Constitutional Interpretation</span>
4. 全大寫對照：CONSTITUTIONAL INTERPRETATION
5. 混中英：湯德宗教授之 <span class="sc">Constitutional Interpretation</span> 課程

## 行內範例

- 本週閱讀：<span class="sc">What is "the Constitution"?</span>
- 參照案例：<span class="sc">Obergefell v. Hodges</span>、<span class="sc">Dobbs v. Jackson Women's Health Organization</span>

## 備註

- `small-caps` 對英文效果最佳；中文通常不會有差異。
- 若字型不支援 true small caps，會以縮小大寫替代。
