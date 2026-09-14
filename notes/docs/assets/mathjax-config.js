// MathJax 全域設定
window.MathJax = {
  tex: {
    // 行內數學分隔符，例如 $...$ 或 \( ... \)
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    // 區塊數學分隔符，例如 $$...$$ 或 \[ ... \]
    displayMath: [['$$','$$'], ['\\[','\\]']],
    // 允許跳脫，例如 \$ 表示字元而非公式
    processEscapes: true,
    // 啟用 \begin{...} \end{...} 這類環境
    processEnvironments: true
  },
  options: {
    // 告訴 MathJax：這些 HTML 標籤內的內容不要處理
    // （因為 <pre>/<code> 裡通常是程式碼，不應被解釋成數學）
    skipHtmlTags: ['script','noscript','style','textarea','pre','code'],

    // 避免處理特定 class 的區塊，例如：
    // - mermaid：保留給 Mermaid.js 繪圖，不讓 $...$ 被誤判成數學
    // - no-math：自訂 class，可套在不想被解析的區塊
    ignoreHtmlClass: 'mermaid|no-math'
  }
};

// ----------- MkDocs Material SPA 支援 -----------
// MkDocs Material 是單頁應用（SPA），點擊側邊欄或搜尋結果切頁時
// 不會整個刷新頁面，因此 MathJax 不會自動重新跑。
// 以下程式利用 Material 提供的 document$ hook：
// 每次頁面內容換完，就呼叫 MathJax.typesetPromise() 重新渲染數學。

if (typeof document$ !== 'undefined') {
  let t;  // 計時器 ID，用來防止多次觸發
  document$.subscribe(() => {
    clearTimeout(t);  // 清掉前一次排程
    // 設定一個極短的延遲，等 DOM 渲染穩定再執行 MathJax
    t = setTimeout(() => {
      if (window.MathJax?.typesetPromise) {
        MathJax.typesetPromise();
      }
    }, 0);
  });
}