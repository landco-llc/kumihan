(() => {
  const preserveHash = () => document.querySelectorAll('[data-language]').forEach(a => {
    const target = new URL(a.href, location.href);
    target.hash = location.hash;
    a.href = target.href;
  });
  preserveHash();
  window.addEventListener('hashchange', preserveHash);
  document.querySelectorAll('[data-copy]').forEach(button => {
    button.addEventListener('click', async () => {
      const target = document.getElementById(button.dataset.copy);
      try {
        await navigator.clipboard.writeText(target.textContent);
        button.textContent = button.dataset.success;
      } catch {
        button.textContent = button.dataset.failure;
        const range = document.createRange(); range.selectNodeContents(target);
        const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range);
      }
    });
  });
})();
