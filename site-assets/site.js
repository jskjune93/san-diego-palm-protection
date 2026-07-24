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
  document.querySelectorAll('[data-conversion]').forEach(link => link.addEventListener('click', () => {
    const detail = { event: 'sdpp_conversion', action: link.dataset.conversion, path: location.pathname };
    window.dispatchEvent(new CustomEvent('sdpp:conversion', { detail }));
    if (Array.isArray(window.dataLayer)) window.dataLayer.push(detail);
  }));
})();
