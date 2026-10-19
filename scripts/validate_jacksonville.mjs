import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {handleJacksonville,validatePhotos} from '../api/jacksonville.mjs';

const campaign=JSON.parse(await readFile(new URL('../site-config/jacksonville_campaigns.json',import.meta.url)));
for(const c of campaign.campaigns)for(const group of c.groups){
  for(const h of group.headlines)assert.ok(h.length<=30,`Headline too long (${h.length}): ${h}`);
  for(const d of group.descriptions)assert.ok(d.length<=90,`Description too long (${d.length}): ${d}`);
}
for(const name of ['RESEND_API_KEY','TURNSTILE_SITE_KEY','TURNSTILE_SECRET_KEY','SDPP_INQUIRY_TO_EMAIL','SDPP_INQUIRY_FROM_EMAIL'])process.env[name]='mock-only';
const res=()=>({statusCode:0,status(n){this.statusCode=n;return this;},setHeader(){},json(data){this.data=data;return this;}});
let emails=[];
const fetcher=async(url,opts)=>url.includes('siteverify')?{ok:true,json:async()=>({success:true,hostname:'www.sandiegopalmprotection.com'})}:{ok:true,json:async()=>{emails.push(JSON.parse(opts.body));return {id:'mock-provider-id'};}};
let index=0;
const request=body=>({method:'POST',headers:{'x-idempotency-key':'stable-reference-00001','x-forwarded-for':'mock-ip-'+index++},body});
const base={campaign_identifier:'JAX_PHC',name:'Test',email:'test@example.invalid',phone:'5555550100',zip:'32250',city:'Jacksonville Beach',customer_type:'Homeowner',issue_category:'Unknown decline',problem:'Test request',contact_consent:'on',lead_timestamp:'2026-10-19T12:00:00.000Z',photos:[]};
let r=res();await handleJacksonville(request(base),r,{fetch:fetcher});assert.equal(r.statusCode,200);assert.equal(r.data.verified,true);assert.equal(emails.length,1);
assert.equal(JSON.parse(Buffer.from(emails[0].attachments[0].content,'base64')).campaign_identifier,'JAX_PHC');
assert.equal(r.data.isTest,false);
const firstPayload=emails[0];r=res();await handleJacksonville(request(base),r,{fetch:fetcher});assert.deepEqual(emails[1],firstPayload,'Retry payload must remain identical');
for(const patch of [{email:'invalid'},{email:''},{phone:'123'},{contact_consent:false},{campaign_identifier:'SAN_DIEGO'},{zip:'bad'},{website:'bot'},{photos:[{content:'garbage'}]}]){
  r=res();await handleJacksonville(request({...base,...patch}),r,{fetch:fetcher});assert.equal(r.statusCode,400);assert.ok(!r.data.verified);
}
r=res();await handleJacksonville(request({...base,campaign_identifier:'JAX_SOURCING',quantity:'2',clear_trunk_ft:'10',budget_range:'$15,000–$30,000',timeline:'1–3 months'}),r,{fetch:fetcher});assert.equal(r.statusCode,200);
r=res();await handleJacksonville(request({...base,phone:'',city:'',customer_type:''}),r,{fetch:fetcher});assert.equal(r.statusCode,200,'Email-only short request must be accepted');
r=res();await handleJacksonville(request({...base,inquiry_kind:'delivery_test',photos:[{content:'/9j/2Q=='}]}),r,{fetch:fetcher});assert.equal(r.statusCode,200);assert.equal(r.data.isTest,true);assert.equal(r.data.event,'jax-test-delivered');
const testEmail=emails.at(-1);assert.ok(testEmail.subject.startsWith('[TEST ONLY]'));assert.equal(testEmail.attachments.length,2);
const testReceipt=JSON.parse(Buffer.from(testEmail.attachments.at(-1).content,'base64'));assert.equal(testReceipt.is_test,true);assert.equal(testReceipt.status,'test');assert.equal(testReceipt.photo_count,1);
r=res();await handleJacksonville(request(base),r,{fetch:async(url)=>url.includes('siteverify')?{ok:true,json:async()=>({success:true,hostname:'www.sandiegopalmprotection.com'})}:{ok:false}});assert.equal(r.statusCode,502);assert.ok(!r.data.verified);
r=res();await handleJacksonville(request(base),r,{fetch:async()=>({ok:true,json:async()=>({success:true,hostname:'untrusted.invalid'})})});assert.equal(r.statusCode,400);
r=res();await handleJacksonville(request({...base,notes:'x'.repeat(3400000)}),r,{fetch:fetcher});assert.equal(r.statusCode,413);
assert.throws(()=>validatePhotos(Array(4).fill({content:'/9j/2Q=='})));
delete process.env.RESEND_API_KEY;r=res();await handleJacksonville({method:'GET'},r);assert.equal(r.data.enabled,false);
console.log('JACKSONVILLE_API_AND_AD_COPY_OK: mocked provider only; no email sent.');
