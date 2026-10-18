/* KUMIHAN install guides: a localized Copy button on every command block.
   Blocks that already carry their own copy control are left as they are. */
(() => {
  'use strict';
  const LABELS = {
    ja: ['コピー', 'コピーしました', 'コピーできませんでした'],
    en: ['Copy', 'Copied', 'Copy failed'],
    'zh-Hant': ['複製', '已複製', '無法複製'],
    'zh-Hans': ['复制', '已复制', '无法复制'],
    ko: ['복사', '복사했어요', '복사하지 못했어요'],
    th: ['คัดลอก', 'คัดลอกแล้ว', 'คัดลอกไม่ได้'],
    fr: ['Copier', 'Copié', 'Échec de la copie'],
    ar: ['نسخ', 'تم النسخ', 'تعذّر النسخ'],
    es: ['Copiar', 'Copiado', 'No se pudo copiar'],
    pt: ['Copiar', 'Copiado', 'Não foi possível copiar'],
  };
  const lang = document.documentElement.lang || 'en';
  const key = Object.keys(LABELS).find(k => lang === k || lang.startsWith(k + '-')) || 'en';
  const [label, done, failed] = LABELS[key];

  async function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      try { await navigator.clipboard.writeText(text); return true; } catch { /* fall back */ }
    }
    const box = document.createElement('textarea');
    box.value = text; box.setAttribute('readonly', '');
    box.style.cssText = 'position:fixed;left:-9999px;top:0;';
    document.body.appendChild(box); box.select();
    let ok = false;
    try { ok = document.execCommand('copy'); } catch { ok = false; }
    box.remove(); return ok;
  }

  function hasOwnCopy(pre) {
    const ids = [pre.id, ...[...pre.querySelectorAll('[id]')].map(el => el.id)].filter(Boolean);
    return ids.some(id => document.querySelector(`[data-copy="${id}"], [data-copy-target="${id}"]`));
  }

  document.querySelectorAll('main pre').forEach(pre => {
    if (pre.closest('.code-shell') || hasOwnCopy(pre)) return;
    const shell = document.createElement('div');
    shell.className = 'code-shell';
    pre.before(shell); shell.appendChild(pre);
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'copy-code'; button.textContent = label;
    const status = document.createElement('span');
    status.className = 'copy-status-live'; status.setAttribute('role', 'status');
    button.addEventListener('click', async () => {
      const ok = await copyText(pre.textContent.replace(/\n$/, ''));
      button.textContent = ok ? done : failed;
      status.textContent = button.textContent;
      setTimeout(() => { button.textContent = label; status.textContent = ''; }, 2400);
    });
    shell.append(button, status);
  });
})();
