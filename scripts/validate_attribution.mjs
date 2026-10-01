import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const source = readFileSync(new URL('../site-assets/site.js', import.meta.url), 'utf8');
const storage = new Map();
function visit({ path = '/', query = '', referrer = '', blockedStorage = false } = {}) {
  const context = {
    URL, URLSearchParams, Date,
    location: { hostname: 'preview.example', pathname: path, search: query, hash: '' },
    document: { referrer, querySelector: () => null, querySelectorAll: () => [] },
    window: { addEventListener() {} },
    sessionStorage: {
      getItem(key) { if (blockedStorage) throw new Error('disabled'); return storage.get(key) || null; },
      setItem(key, value) { if (blockedStorage) throw new Error('disabled'); storage.set(key, value); },
    },
  };
  vm.runInNewContext(source, context);
  return JSON.parse(storage.get('sdpp-attribution-v1') || 'null');
}
let record = visit({ path: '/treatment.html', query: '?gclid=ad-click_1&utm_campaign=north_county&email=private@example.com', referrer: 'https://www.google.com/search?q=private-search' });
assert.equal(record.first.gclid, 'ad-click_1');
assert.equal(record.first.referrer_host, 'www.google.com');
assert.equal(record.first.landing_path, '/treatment.html');
assert.doesNotMatch(JSON.stringify(record), /private-search|private@example/);
record = visit({ path: '/inquiry.html', referrer: 'https://preview.example/treatment.html' });
assert.equal(record.last.gclid, 'ad-click_1', 'Internal navigation must preserve acquisition evidence');
record = visit({ path: '/annual.html', referrer: 'https://chatgpt.com/' });
assert.equal(record.first.gclid, 'ad-click_1');
assert.equal(record.last.referrer_host, 'chatgpt.com', 'New external referrals retain both visits');
const expired = JSON.parse(storage.get('sdpp-attribution-v1'));
expired.first.at = '2000-01-01T00:00:00.000Z';
storage.set('sdpp-attribution-v1', JSON.stringify(expired));
record = visit({ query: '?utm_source=person%40example.com&gclid=%3Cscript%3E' });
assert.equal(record.first.gclid, '');
assert.equal(record.first.utm_source, '');
assert.equal(record.first.referrer_host, '');
storage.set('sdpp-attribution-v1', '{broken');
assert.doesNotThrow(() => visit());
assert.doesNotThrow(() => visit({ blockedStorage: true }));
console.log('Attribution checks passed: internal navigation, first/latest visits, expiry, URL minimization, invalid data and blocked storage.');
