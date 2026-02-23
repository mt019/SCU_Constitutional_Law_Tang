(function () {
  // 取得右側 TOC 的可滾動容器
  function getTocScroller() {
    const side = document.querySelector(".md-sidebar--secondary");
    if (!side) return null;
    return (
      side.querySelector(".md-sidebar__scrollwrap") ||
      side.querySelector(".md-sidebar__inner") ||
      side
    );
  }

  // 取得當前 active 的 TOC 鏈接
  function getActiveLink(scroller) {
    if (!scroller) return null;
    return (
      scroller.querySelector(".md-nav__link--active") ||
      (function () {
        const li = scroller.querySelector(".md-nav__item--active > a.md-nav__link");
        return li || null;
      })()
    );
  }

  // 若 active 超出可視範圍，將其捲至中間
  function ensureActiveVisible() {
    const scroller = getTocScroller();
    const active = getActiveLink(scroller);
    if (!scroller || !active) return;

    const a = active.getBoundingClientRect();
    const c = scroller.getBoundingClientRect();
    const pad = 12; // 上下緩衝

    const outAbove = a.top < c.top + pad;
    const outBelow = a.bottom > c.bottom - pad;

    if (outAbove || outBelow) {
      const delta = (a.top - c.top) - (c.height / 2 - a.height / 2);
      scroller.scrollTo({ top: scroller.scrollTop + delta, behavior: "smooth" });
    }
  }

  // 用 rAF 節流，避免頻繁觸發
  let scheduled = false;
  function schedule() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => {
      scheduled = false;
      ensureActiveVisible();
    });
  }

  // 綁定：頁面滾動時檢查（Material 以 IntersectionObserver 改 active）
  window.addEventListener("scroll", schedule, { passive: true });

  // 綁定：右側 TOC 結構或 active class 變化時檢查
  function bindObserver() {
    const scroller = getTocScroller();
    if (!scroller) return;
    const nav = scroller.querySelector(".md-nav--secondary") || scroller;
    const mo = new MutationObserver(schedule);
    mo.observe(nav, { subtree: true, attributes: true, attributeFilter: ["class"] });
  }

  // 初次與延遲嘗試（應對 SPA 導航與延遲掛載）
  document.addEventListener("DOMContentLoaded", () => {
    schedule();
    bindObserver();
    // 再保險：首秒多次嘗試
    let tries = 6;
    const id = setInterval(() => {
      schedule();
      bindObserver();
      if (--tries <= 0) clearInterval(id);
    }, 200);
  });

  // Material 的即時導航事件（若啟用 navigation.instant 時更穩）
  document.addEventListener("navigation", schedule);
})();

// 在頂部導覽加入「一鍵學術連結」
(function () {
  const links = [
    { label: "DWDS", url: "https://www.dwds.de/", emoji: "📘" },
    { label: "德語助手", url: "https://www.godic.net/", emoji: "📙" },
    // { label: "裁判書查詢", url: "https://judgment.judicial.gov.tw/FJUD/default.aspx", emoji: "⚖️" }
  ];

  function addQuickLinks() {
    const headerInner = document.querySelector('.md-header .md-header__inner');
    if (!headerInner) return;
    if (headerInner.querySelector('.qa-links')) return; // 已加入

    const wrap = document.createElement('div');
    wrap.className = 'qa-links';

    links.forEach(l => {
      const a = document.createElement('a');
      a.href = l.url;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      const em = document.createElement('span');
      em.className = 'qa-emoji';
      em.textContent = l.emoji || '🔗';
      const txt = document.createElement('span');
      txt.textContent = l.label;
      a.appendChild(em);
      a.appendChild(txt);
      wrap.appendChild(a);
    });

    // 嘗試找搜尋框，將連結放在其「前面」
    const searchEl =
      headerInner.querySelector('[data-md-component="search"]') ||
      headerInner.querySelector('.md-search') ||
      null;

    if (searchEl && searchEl.parentNode === headerInner) {
      headerInner.insertBefore(wrap, searchEl);
    } else if (searchEl) {
      // 若 search 不在 headerInner 之下，則插入到其祖先前
      headerInner.insertBefore(wrap, headerInner.firstChild);
    } else {
      // 後備：找不到 search 時，仍加到右側
      headerInner.appendChild(wrap);
    }
  }

  document.addEventListener('DOMContentLoaded', addQuickLinks);
  // MkDocs Material SPA 導航事件
  document.addEventListener('navigation', addQuickLinks);
})();
