(() => {
  const button = document.querySelector('.nav-toggle');
  const nav = document.querySelector('#primary-nav');
  if (button && nav) {
    const close = () => { button.setAttribute('aria-expanded', 'false'); nav.removeAttribute('data-open'); document.body.style.overflow = ''; };
    button.addEventListener('click', () => {
      const open = button.getAttribute('aria-expanded') !== 'true';
      button.setAttribute('aria-expanded', String(open));
      nav.toggleAttribute('data-open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) close(); });
    document.addEventListener('keydown', event => { if (event.key === 'Escape') { close(); button.focus(); } });
    matchMedia('(min-width: 981px)').addEventListener('change', close);
  }
  const recordConversion = action => {
    if (!action) return;
    const detail = { event: 'sdpp_conversion', action, path: location.pathname };
    window.dispatchEvent(new CustomEvent('sdpp:conversion', { detail }));
    if (Array.isArray(window.dataLayer)) window.dataLayer.push(detail);
  };
  document.querySelectorAll('[data-conversion]').forEach(link => link.addEventListener('click', () => {
    recordConversion(link.dataset.conversion);
  }));
  document.querySelectorAll('[data-inquiry-fallback]').forEach(form => form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    const data = new FormData(form);
    const values = [...data.entries()].map(([key, value]) => `${key.replaceAll('_', ' ')}: ${String(value).trim()}`);
    const subject = form.dataset.subject || 'SDPP website inquiry';
    const status = form.querySelector('[data-form-status]');
    if (status) status.textContent = 'Your email application should open with this information. Review it, attach photographs if useful, and press Send. Nothing has been delivered yet.';
    recordConversion(form.dataset.conversion);
    location.href = `mailto:sandiegopalmprotection@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(values.join('\n'))}`;
  }));
})();
