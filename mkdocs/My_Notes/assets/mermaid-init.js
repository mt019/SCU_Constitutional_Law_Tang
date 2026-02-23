/* Initialize Mermaid for MkDocs Material */
window.addEventListener('DOMContentLoaded', () => {
  if (window.mermaid && typeof window.mermaid.initialize === 'function') {
    window.mermaid.initialize({ startOnLoad: true, securityLevel: 'loose', theme: 'default' });
  }
});

