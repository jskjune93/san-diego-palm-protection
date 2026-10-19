import { configurationReady, verifyTurnstile, rateLimited, json, text, html, validEmail } from './inquiry.mjs';

const fields=['name','email','phone','zip','city','customer_type','species','issue_category','problem','quantity','size','clear_trunk_ft','symptom_duration','fruit_drop','black_flowers','lower_bronzing','spear_affected','crown_collapse','visible_insects','transplanted','freeze_exposure','pruning','irrigation_changes','construction','storm_damage','fertilizer','company','project_location','overall_height','caliper','budget_range','target_budget','timeline','delivery_scope','installation_required','crane_available','crane_required','alternatives','site_access','preferred_contact','notes'];
const campaignIds=new Set(['JAX_PHC','JAX_SOURCING']);
export function validatePhotos(photos){
  if(!Array.isArray(photos)||photos.length>3)throw Error('invalid_photos');
  return photos.map((p,i)=>{
    if(typeof p.content!=='string'||p.content.length>1000000||!/^\/[A-Za-z0-9+/]*={0,2}$/.test(p.content))throw Error('invalid_image');
    const bytes=Buffer.from(p.content,'base64');
    if(bytes.length>750000||bytes.length<4||bytes[0]!==0xff||bytes[1]!==0xd8||bytes.at(-2)!==0xff||bytes.at(-1)!==0xd9)throw Error('invalid_jpeg');
    return {filename:`palm-photo-${i+1}.jpg`,content:bytes.toString('base64')};
  });
}
function cleanAttribution(raw){
  const result={};
  const allowed=['at','landing_page','referrer_host','utm_source','utm_medium','utm_campaign','utm_content','utm_term','campaignid','adgroupid','keyword','matchtype','device','loc_physical_ms','gclid','gbraid','wbraid'];
  for(const touch of ['first','last'])result[touch]=Object.fromEntries(allowed.map(k=>[k,text(raw?.[touch]?.[k],256)]));
  return result;
}
export async function handleJacksonville(request,response,dependencies={}){
  const fetcher=dependencies.fetch||fetch;
  if(request.method==='GET')return json(response,200,{enabled:configurationReady(),turnstileSiteKey:configurationReady()?process.env.TURNSTILE_SITE_KEY:null,uploadsEnabled:configurationReady(),maxPhotos:3,maxPhotoBytes:750000});
  if(request.method!=='POST'){response.setHeader('Allow','GET, POST');return json(response,405,{ok:false});}
  if(!configurationReady())return json(response,503,{ok:false,message:'Secure submission unavailable. Call or email SDPP.'});
  let body;
  try{
    const raw=typeof request.body==='string'?request.body:JSON.stringify(request.body||{});
    if(Buffer.byteLength(raw)>3300000)throw Error();body=typeof request.body==='object'?request.body:JSON.parse(raw);
    if(!body||typeof body!=='object'||Array.isArray(body))throw Error();
  }catch{return json(response,413,{ok:false,message:'Request is too large or could not be read.'});}
  const campaign=body.campaign_identifier, data=Object.fromEntries(fields.map(k=>[k,text(body[k],k==='problem'||k==='notes'||k==='site_access'?3000:200)]));
  const required=['name','email','zip',...(campaign==='JAX_PHC'?['issue_category','problem']:['quantity','clear_trunk_ft','budget_range','timeline'])];
  if(!campaignIds.has(campaign)||text(body.website)||!['on',true].includes(body.contact_consent)||required.some(k=>!data[k])||!validEmail(data.email)||!/^\d{5}$/.test(data.zip)||(data.phone && data.phone.replace(/\D/g,'').length<10)||(campaign==='JAX_SOURCING'&&(!/^\d+$/.test(data.quantity)||+data.quantity<1||+data.quantity>10000)))return json(response,400,{ok:false,message:'Review the required fields. If you add a phone number, include its area code.'});
  // Explicit QA requests still use the same validation, anti-bot and delivery path.
  // The flag only labels/excludes the request from customer-lead measurement.
  const isTest=body.inquiry_kind==='delivery_test';
  const inquiryId=text(request.headers['x-idempotency-key'],128);
  if(!/^[a-zA-Z0-9_-]{16,128}$/.test(inquiryId))return json(response,400,{ok:false});
  const ip=text(request.headers['x-forwarded-for']||request.socket?.remoteAddress||'unknown',128).split(',')[0].trim();
  if(rateLimited('jax:'+ip))return json(response,429,{ok:false});
  if(!await verifyTurnstile(text(body['cf-turnstile-response'],4096),ip,fetcher))return json(response,400,{ok:false,message:'Complete the security check.'});
  let attachments;
  try{attachments=validatePhotos(body.photos||[]);}catch{return json(response,400,{ok:false,message:'Choose up to 3 resized JPEG photos.'});}
  // Stable browser request timestamp keeps the provider payload idempotent on retry.
  // It is source evidence, not a server-certified receipt time.
  if(!/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$/.test(body.lead_timestamp||'')||!Number.isFinite(Date.parse(body.lead_timestamp)))return json(response,400,{ok:false,message:'Refresh and try again.'});
  const lead={schema_version:1,id:inquiryId,legal_entity:'San Diego Palm Protection LLC',campaign_identifier:campaign,lead_timestamp:body.lead_timestamp,first_touch_timestamp:text(body.attribution?.first?.at,40),status:isTest?'test':'new',is_test:isTest,qualified:false,...data,attribution:cleanAttribution(body.attribution),photo_count:attachments.length,contact_consent:true};
  attachments.push({filename:`${campaign}-${inquiryId}.json`,content:Buffer.from(JSON.stringify(lead,null,2)).toString('base64')});
  const rows=[['Request kind',isTest?'TEST ONLY - not a customer lead':'Customer inquiry'],['Campaign / SDPP cost center',campaign],['Reference',inquiryId],...Object.entries(data)];
  try{
    const delivered=await fetcher('https://api.resend.com/emails',{method:'POST',headers:{Authorization:`Bearer ${process.env.RESEND_API_KEY}`,'Content-Type':'application/json','Idempotency-Key':inquiryId},body:JSON.stringify({from:process.env.SDPP_INQUIRY_FROM_EMAIL,to:[process.env.SDPP_INQUIRY_TO_EMAIL],reply_to:data.email,subject:`${isTest?'[TEST ONLY] ':''}${campaign} — Jacksonville inquiry — ${text(data.name,80)}`,text:rows.map(([k,v])=>`${k}: ${v}`).join('\n')+'\n\nNew inquiry, not yet qualified. Attached JSON retains attribution for private import. Photo review is not a confirmed diagnosis. All activity belongs to SDPP.',html:'<h1>'+html(campaign)+' inquiry</h1><table>'+rows.map(([k,v])=>`<tr><th>${html(k)}</th><td>${html(v)}</td></tr>`).join('')+'</table><p>New inquiry, not yet qualified. Import attached JSON into the private Jacksonville reporting tool. All activity belongs to SDPP.</p>',attachments})});
    if(!delivered.ok||!(await delivered.json()).id)throw Error();
  }catch{return json(response,502,{ok:false,message:'Delivery could not be confirmed. Retry or contact SDPP.'});}
  return json(response,200,{ok:true,verified:true,inquiryId,campaign_identifier:campaign,isTest,event:isTest?'jax-test-delivered':'jax-inquiry-delivered'});
}
export default handleJacksonville;
