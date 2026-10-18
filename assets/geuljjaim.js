'use strict';
document.querySelectorAll('[data-copy-target]').forEach((button) => {
  button.addEventListener('click', async () => {
    const text = document.getElementById(button.dataset.copyTarget);
    const status = button.parentElement.querySelector('[role="status"]');
    try {
      await navigator.clipboard.writeText(text.textContent);
      status.textContent = button.dataset.success;
    } catch (_) {
      status.textContent = button.dataset.failure;
    }
  });
});
// Keep a section when it also exists in the translated page; platform paths are static.
document.querySelectorAll('.languages a').forEach((link) => {
  link.addEventListener('click', () => {
    if (location.hash) link.hash = location.hash;
  });
});
