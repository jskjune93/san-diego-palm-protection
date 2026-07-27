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
  const inquiryForms = [...document.querySelectorAll('[data-inquiry-direct]')];
  if (!inquiryForms.length) return;

  const setStatus = (form, message, state = '') => {
    const status = form.querySelector('[data-form-status]');
    if (!status) return;
    status.textContent = message;
    if (state) status.dataset.state = state;
    else status.removeAttribute('data-state');
  };
  const fallbackMode = form => {
    setStatus(form, 'Direct delivery is temporarily unavailable. Use the email link below; your inquiry is not sent until you send the prepared email.', 'error');
    form.querySelector('button[type="submit"]')?.setAttribute('disabled', '');
  };
  let turnstilePromise;
  const loadTurnstile = () => turnstilePromise ||= new Promise((resolve, reject) => {
    if (window.turnstile) { resolve(window.turnstile); return; }
    const script = document.createElement('script');
    script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';
    script.async = true;
    script.defer = true;
    script.onload = () => resolve(window.turnstile);
    script.onerror = reject;
    document.head.append(script);
  });

  fetch('/api/inquiry', { headers: { Accept: 'application/json' } })
    .then(response => response.ok ? response.json() : Promise.reject())
    .then(async config => {
      if (!config.enabled || !config.turnstileSiteKey) throw new Error('not_configured');
      const turnstile = await loadTurnstile();
      inquiryForms.forEach(form => {
        const container = form.querySelector('[data-turnstile-container]');
        const tokenField = document.createElement('input');
        tokenField.type = 'hidden';
        tokenField.name = 'cf-turnstile-response';
        form.append(tokenField);
        const reset = () => {
          tokenField.value = '';
          if (container.dataset.widgetId) turnstile.reset(container.dataset.widgetId);
        };
        const widgetId = turnstile.render(container, {
          sitekey: config.turnstileSiteKey,
          theme: 'light',
          callback: token => { tokenField.value = token; setStatus(form, 'Security check complete. Your inquiry is ready to submit.'); },
          'expired-callback': reset,
          'error-callback': () => setStatus(form, 'The security check could not load. Please retry or use the email link.', 'error'),
        });
        container.dataset.widgetId = widgetId;

        let started = false;
        form.addEventListener('focusin', () => {
          if (!started) {
            started = true;
            recordConversion(`${form.dataset.inquiryType}-form-started`);
          }
        });
        form.addEventListener('submit', async event => {
          event.preventDefault();
          if (!form.checkValidity()) { form.reportValidity(); return; }
          if (!tokenField.value) {
            setStatus(form, 'Complete the security check before submitting.', 'error');
            return;
          }
          const button = form.querySelector('button[type="submit"]');
          button.disabled = true;
          setStatus(form, 'Submitting securely…');
          try {
            const response = await fetch(form.action, {
              method: 'POST',
              headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                'X-Idempotency-Key': `${Date.now()}_${crypto.randomUUID().replaceAll('-', '')}`,
              },
              body: JSON.stringify(Object.fromEntries(new FormData(form))),
            });
            const result = await response.json();
            if (!response.ok || !result.ok || !result.verified) throw new Error(result.message || 'Delivery could not be confirmed.');
            setStatus(form, result.message, 'success');
            recordConversion(result.event);
            form.reset();
            reset();
          } catch (error) {
            setStatus(form, error.message || 'Delivery could not be confirmed. Please use the email link or call or text SDPP.', 'error');
            reset();
          } finally {
            button.disabled = false;
          }
        });
      });
    })
    .catch(() => inquiryForms.forEach(fallbackMode));
})();
