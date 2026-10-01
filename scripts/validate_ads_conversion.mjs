import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
const source = readFileSync(new URL('../site-assets/site.js', import.meta.url), 'utf8');

async function scenario({ hostname = 'www.sandiegopalmprotection.com', responseOk = true, verified = true, token = true, retry = false } = {}) {
  const listeners = {};
  const requests = [];
  const status = { dataset: {}, removeAttribute() {} };
  const button = { setAttribute() {} };
  const container = { dataset: {} };
  let tokenField;
  const form = {
    dataset: { inquiryType: 'homeowner' }, action: '/api/inquiry',
    append(field) { tokenField = field; },
    querySelector(selector) { return selector === '[data-turnstile-container]' ? container : selector === '[data-form-status]' ? status : button; },
    addEventListener(name, callback) { listeners[name] = callback; },
    checkValidity: () => true, reset() {},
  };
  const window = {
    dataLayer: [], addEventListener() {}, dispatchEvent() {},
    turnstile: { render(element, config) { if (token) config.callback('test-token'); return 'widget'; }, reset() {} },
  };
  const context = {
    URL, URLSearchParams, Date, console,
    crypto: { randomUUID: () => 'test-uuid-0123456789012345' },
    location: { hostname, pathname: '/inquiry.html', search: '?gclid=testClick', hash: '' },
    sessionStorage: { getItem: () => null, setItem() {} }, window,
    CustomEvent: class { constructor(name, options) { this.detail = options.detail; } },
    document: {
      referrer: 'https://www.google.com/', head: { append() {} }, createElement: () => ({}),
      querySelector: () => null,
      querySelectorAll: selector => selector === '[data-inquiry-direct]' ? [form] : [],
    },
    FormData: class { *[Symbol.iterator]() { yield ['name', 'Private Name']; yield ['email', 'private@example.com']; yield ['cf-turnstile-response', tokenField.value]; } },
    fetch: async (url, options) => {
      if (!options.method) return { ok: true, json: async () => ({ enabled: true, turnstileSiteKey: 'test' }) };
      requests.push(options);
      const ok = retry ? requests.length > 1 : responseOk;
      return { ok, json: async () => ({ ok, verified, inquiryId: options.headers['X-Idempotency-Key'], event: 'homeowner-inquiry-delivered', message: ok ? 'Delivered' : 'Failed' }) };
    },
  };
  vm.runInNewContext(source, context);
  await new Promise(resolve => setImmediate(resolve));
  await listeners.submit({ preventDefault() {} });
  if (retry) { tokenField.value = 'replacement-token'; await listeners.submit({ preventDefault() {} }); }
  return { requests, conversions: window.dataLayer.filter(event => event[0] === 'event' && event[1] === 'conversion'), status };
}
for (const options of [{ responseOk: false }, { verified: false }, { token: false }, { hostname: 'preview.example' }]) {
  const result = await scenario(options);
  assert.equal(result.conversions.length, 0, JSON.stringify(options));
}
const success = await scenario();
assert.equal(success.conversions.length, 1);
assert.equal(success.conversions[0][2].transaction_id, success.requests[0].headers['X-Idempotency-Key']);
assert.doesNotMatch(JSON.stringify(success.conversions), /Private Name|private@example.com|testClick/);
assert.equal(JSON.parse(success.requests[0].body).attribution.first.gclid, 'testClick');
const retried = await scenario({ retry: true });
assert.equal(retried.requests.length, 2);
assert.equal(retried.requests[0].headers['X-Idempotency-Key'], retried.requests[1].headers['X-Idempotency-Key']);
assert.equal(retried.conversions.length, 1);
console.log('Ads conversion checks passed: verified delivery only, no preview events, no customer data, and stable retry/deduplication reference.');
