import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createHash, webcrypto } from 'node:crypto';
import vm from 'node:vm';

const source = await readFile(new URL('../site-assets/site.js', import.meta.url), 'utf8');
const helper = source.slice(source.indexOf('  async function recordVerifiedInquiryAds('), source.indexOf('  // End enhanced measurement helper.'));
const commands=[]; const timers=[];
const context=vm.createContext({adsEnabled:true, adsDestination:'AW-test/label', adsEvent:(...args)=>commands.push(args), crypto:webcrypto, TextEncoder, setTimeout:callback=>timers.push(callback)});
vm.runInContext(helper,context);
const successful={ok:true,verified:true,event:'homeowner-inquiry-delivered'};
const fields={email:' Test.Person@Gmail.com ',phone:'(262) 492-3135',name:'Private person',concern:'Private message',property_city:'Private city'};
const hash=value=>createHash('sha256').update(value).digest('hex');
await context.recordVerifiedInquiryAds(fields,successful,'inquiry-1',true,false);
let data=commands.find(c=>c[0]==='set' && c[1]==='user_data')[2];
assert.equal(data.sha256_email_address,hash('testperson@gmail.com'));
assert.equal(data.sha256_phone_number,hash('+12624923135'));
assert.deepEqual(Object.keys(data).sort(),['sha256_email_address','sha256_phone_number']);
const event=commands.find(c=>c[0]==='event');
assert.equal(event[2].transaction_id,'inquiry-1');
assert.equal(commands.filter(c=>c[0]==='event').length,1);
event[2].event_callback();
assert.equal(commands.at(-1)[2].ad_user_data,'denied');
assert.equal(commands.at(-2)[2],null);
for(const [allowed,gpc] of [[false,false],[true,true]]){
  commands.length=0;
  await context.recordVerifiedInquiryAds(fields,successful,'basic',allowed,gpc);
  assert.equal(commands.filter(c=>c[0]==='event').length,1);
  assert.ok(!commands.some(c=>c[0]==='set' && c[2]!==null));
  assert.equal(commands[0][2],null,'Clear any previous inquiry data before a basic conversion');
}
for(const result of [{...successful,verified:false},{...successful,ok:false},{...successful,event:'form-started'}]){
  commands.length=0;
  await context.recordVerifiedInquiryAds(fields,result,'failed',true,false);
  assert.equal(commands.length,0);
}
commands.length=0;
await context.recordVerifiedInquiryAds({...fields,phone:'not a phone'},successful,'email-only',true,false);
data=commands.find(c=>c[0]==='set' && c[2]!==null)[2];
assert.deepEqual(Object.keys(data),['sha256_email_address']);
context.crypto={subtle:{digest:async()=>{throw new Error('Hash unavailable')}}};
commands.length=0;
await context.recordVerifiedInquiryAds(fields,successful,'hash-failed',true,false);
assert.equal(commands.filter(c=>c[0]==='event').length,1);
assert.ok(!commands.some(c=>c[0]==='set' && c[2]!==null));
const page=await readFile(new URL('../palm-records-monitoring-verification.html',import.meta.url),'utf8');
assert.equal((page.match(/data-ads-measurement/g)||[]).length,2);
assert.ok(!/type="checkbox"[^>]*data-ads-measurement[^>]*checked/.test(page));
console.log('Ads measurement passed: hashing and normalization; opt-in and GPC boundaries; no private inquiry content; successful delivery only; one conversion; hashing-failure fallback.');
