(() => {
  // Keep source evidence within this browser tab. Never retain full URLs or searches.
  const attributionKey = 'sdpp-attribution-v1';
  const attributionLifetime = 30 * 24 * 60 * 60 * 1000;
  const sourceLabel = value => /^[a-zA-Z0-9_. -]{1,100}$/.test(value || '') ? value : '';
  const clickId = value => /^[a-zA-Z0-9_-]{1,256}$/.test(value || '') ? value : '';
  const sourcePoint = () => {
    const params = new URLSearchParams(location.search);
    let referrerHost = '';
    try { referrerHost = new URL(document.referrer).hostname; } catch { /* Direct or unavailable. */ }
    const ownHosts = ['www.sandiegopalmprotection.com', 'sandiegopalmprotection.com', location.hostname];
    if (ownHosts.includes(referrerHost)) referrerHost = '';
    return {
      at: new Date().toISOString(),
      landing_path: /^[a-zA-Z0-9_./-]{1,200}$/.test(location.pathname) ? location.pathname : '/',
      referrer_host: referrerHost,
      utm_source: sourceLabel(params.get('utm_source')),
      utm_medium: sourceLabel(params.get('utm_medium')),
      utm_campaign: sourceLabel(params.get('utm_campaign')),
      gclid: clickId(params.get('gclid')),
      gbraid: clickId(params.get('gbraid')),
      wbraid: clickId(params.get('wbraid')),
    };
  };
  const currentSource = sourcePoint();
  let attribution = { first: currentSource, last: currentSource };
  try {
    const saved = JSON.parse(sessionStorage.getItem(attributionKey) || 'null');
    const age = Date.now() - Date.parse(saved?.first?.at);
    if (saved?.first && saved?.last && age >= 0 && age < attributionLifetime) {
      attribution = saved;
      if (currentSource.referrer_host || currentSource.utm_source || currentSource.utm_medium ||
          currentSource.utm_campaign || currentSource.gclid || currentSource.gbraid || currentSource.wbraid) {
        attribution.last = currentSource;
      }
    }
  } catch { /* Storage restrictions must never prevent an inquiry. */ }
  try { sessionStorage.setItem(attributionKey, JSON.stringify(attribution)); } catch { /* Optional storage. */ }
  // Account-owned Google Ads tag. Preview and local visits never send ad events.
  const adsDestination = 'AW-18301751378/Wr8pCK6pu4AdENKg-pZE';
  const adsEnabled = ['www.sandiegopalmprotection.com', 'sandiegopalmprotection.com'].includes(location.hostname);
  const adsEvent = function () { window.dataLayer.push(arguments); };
  if (adsEnabled) {
    window.dataLayer = window.dataLayer || [];
    adsEvent('js', new Date());
    adsEvent('config', 'AW-18301751378', { allow_ad_personalization_signals: false });
    const adsScript = document.createElement('script');
    adsScript.async = true;
    adsScript.src = 'https://www.googletagmanager.com/gtag/js?id=AW-18301751378';
    document.head.append(adsScript);
  }
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
  const focusInquiryTarget = () => {
    if (!['#homeowner-inquiry', '#organization-inquiry'].includes(location.hash)) return;
    const target = document.querySelector(location.hash);
    if (!target) return;
    if (target.matches('details')) target.open = true;
    requestAnimationFrame(() => target.focus({ preventScroll: true }));
  };
  focusInquiryTarget();
  window.addEventListener('hashchange', focusInquiryTarget);
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
        let pendingSubmission;
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
            const fields = Object.fromEntries(new FormData(form));
            const signature = JSON.stringify({ ...fields, 'cf-turnstile-response': '' });
            if (!pendingSubmission || pendingSubmission.signature !== signature) {
              pendingSubmission = { signature, id: `${Date.now()}_${crypto.randomUUID().replaceAll('-', '')}` };
            }
            const response = await fetch(form.action, {
              method: 'POST',
              headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                'X-Idempotency-Key': pendingSubmission.id,
              },
              body: JSON.stringify({ ...fields, attribution }),
            });
            const result = await response.json();
            if (!response.ok || !result.ok || !result.verified) throw new Error(result.message || 'Delivery could not be confirmed.');
            setStatus(form, result.message, 'success');
            recordConversion(result.event);
            if (adsEnabled && ['homeowner-inquiry-delivered', 'organization-inquiry-delivered'].includes(result.event)) {
              // No names, email addresses, phone numbers, or inquiry content are sent.
              adsEvent('event', 'conversion', { send_to: adsDestination, transaction_id: result.inquiryId || pendingSubmission.id });
            }
            form.reset();
            pendingSubmission = null;
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

// Progressive enhancement: original photographs remain ordinary links without JS.
(() => {
  const dialog = document.querySelector('.sapw-lightbox');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const fullImage = dialog.querySelector('img');
  let opener;
  document.querySelectorAll('[data-sapw-photo]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      opener = link;
      fullImage.src = link.href;
      fullImage.alt = link.querySelector('img').alt;
      dialog.showModal();
    });
  });
  dialog.querySelector('button').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => { opener?.focus({preventScroll:true}); });
  document.querySelectorAll('.sapw-raw video').forEach(video => {
    video.addEventListener('play', () => {
      document.querySelectorAll('.sapw-raw video').forEach(other => { if (other !== video) other.pause(); });
    });
  });
})();
