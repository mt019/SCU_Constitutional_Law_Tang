// 鍵盤左右箭頭切換上一頁/下一頁（避免在輸入框觸發）
(function () {
  function isTyping(e) {
    const el = e.target;
    if (!el) return false;
    const tag = el.tagName.toLowerCase();
    return (
      tag === "input" ||
      tag === "textarea" ||
      el.isContentEditable ||
      (tag === "select")
    );
  }

  function gotoRel(rel) {
    // 優先取頁腳按鈕，其次取 <link rel="prev|next">（某些佈局會加在 <head>）
    const footerSel =
      rel === "prev" ? "a.md-footer__link--prev" : "a.md-footer__link--next";
    const a =
      document.querySelector(footerSel) ||
      document.querySelector(`link[rel='${rel}']`);
    if (a) {
      // <link> 沒有 href 屬性在 anchor 上；處理兩種情況
      const href = a.href || a.getAttribute("href");
      if (href) window.location.href = href;
    }
  }

  document.addEventListener("keydown", function (e) {
    if (isTyping(e)) return;          // 正在輸入時不攔截
    if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return; // 保留組合鍵

    if (e.key === "ArrowLeft") {
      e.preventDefault();
      gotoRel("prev");
    } else if (e.key === "ArrowRight") {
      e.preventDefault();
      gotoRel("next");
    }
  });
})();