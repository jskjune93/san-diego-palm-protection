(() => {
  const form = document.querySelector('[data-jax-form]');
  if (!form) return;
  const campaign = form.dataset.campaign;
  const adsDestinations = {
    JAX_PHC: 'AW-18301751378/8YZxCKP7yqIdENKg-pZE',
    JAX_SOURCING: 'AW-18301751378/ldaECKb7yqIdENKg-pZE',
  };
  const adsEnabled = ['www.sandiegopalmprotection.com', 'sandiegopalmprotection.com'].includes(location.hostname);
  function recordVerifiedAds(result) {
    if (isTest || result.isTest || !adsEnabled || !result.ok || !result.verified || result.inquiryId !== id || !adsDestinations[campaign]) return;
    window.dataLayer = window.dataLayer || [];
    const gtag = function () { window.dataLayer.push(arguments); };
    gtag('event', 'conversion', { send_to: adsDestinations[campaign], transaction_id: id, value: 0, currency: 'USD' });
  }
  const status = form.querySelector('[data-jax-status]');
  const submit = form.querySelector('button[type=submit]');
  const retrySecurity = document.createElement('button');
  retrySecurity.type = 'button';
  retrySecurity.className = 'button';
  retrySecurity.textContent = 'Retry security check';
  retrySecurity.hidden = true;
  status.after(retrySecurity);
  const id = crypto.randomUUID();
  let token = '', photos = [], busy = false, processingPhotos = false, started = false, widget, leadTimestamp;
  function securityUnavailable() {
    token = ''; submit.disabled = true; retrySecurity.hidden = false;
    status.textContent = 'Security check timed out or is unavailable. Retry the check below; your details and photos stay here. You can also call or email SDPP.';
  }
  retrySecurity.addEventListener('click', () => {
    if (busy || widget === undefined || !window.turnstile) return;
    token = ''; submit.disabled = true; retrySecurity.hidden = true;
    status.textContent = 'Retrying the security check. Your details and photos are still here.';
    window.turnstile.reset(widget);
  });
  const params = new URLSearchParams(location.search);
  const isTest = params.get('sdpp_test') === 'delivery';
  if (isTest) {
    form.elements.inquiry_kind.value = 'delivery_test';
    const notice = form.querySelector('[data-jax-test]');
    notice.hidden = false;
    notice.textContent = 'TEST ONLY: this request checks SDPP inbox and photo delivery. It will not count as a customer lead or an advertising conversion.';
  }
  const keys = ['utm_source','utm_medium','utm_campaign','utm_content','utm_term','campaignid','adgroupid','keyword','matchtype','device','loc_physical_ms','gclid','gbraid','wbraid'];
  const point = Object.fromEntries(keys.map(k => [k,(params.get(k) || '').slice(0,256)]));
  point.at = new Date().toISOString(); point.landing_page = location.pathname;
  try { point.referrer_host = document.referrer ? new URL(document.referrer).hostname : ''; } catch {}
  let attribution = {first:point,last:point};
  try {
    const saved = JSON.parse(sessionStorage.getItem('sdpp-jax-touch-'+campaign) || 'null');
    if (saved?.first && Date.now()-Date.parse(saved.first.at)<30*86400000) attribution.first=saved.first;
    sessionStorage.setItem('sdpp-jax-touch-'+campaign,JSON.stringify(attribution));
  } catch {}
  function event(action, extra={}) {
    if (isTest) return;
    // Only fixed labels and opaque references reach analytics, never form values/photos.
    const detail={event:'sdpp_jax',action,campaign_identifier:campaign,landing_page:location.pathname,...extra};
    window.dataLayer=window.dataLayer||[]; window.dataLayer.push(detail);
    window.dispatchEvent(new CustomEvent('sdpp:jax',{detail}));
  }
  event('landing_page_visit');
  document.querySelectorAll('[data-jax-call],body[data-jax-campaign] a[href^="tel:"]').forEach(a=>a.addEventListener('click',()=>event('phone_click')));
  form.addEventListener('input',()=>{if(!started){started=true;event('form_start');}});
  function conditional() {
    const issue=form.elements.issue_category?.value;
    form.querySelectorAll('[data-issue]').forEach(el=>{
      el.hidden=!!issue && !el.dataset.issue.split('|').includes(issue);
      el.querySelectorAll('input,select,textarea').forEach(c=>c.disabled=el.hidden);
    });
  }
  form.elements.issue_category?.addEventListener('change',conditional); conditional();
  const objectURLs=[];
  form.elements.photos.addEventListener('change',async()=>{
    photos=[]; processingPhotos=true; submit.disabled=true;
    objectURLs.splice(0).forEach(u=>URL.revokeObjectURL(u));
    const preview=form.querySelector('[data-photo-preview]'); preview.replaceChildren();
    const files=[...form.elements.photos.files];
    if(files.length>3){status.textContent='Choose up to 3 photos.';form.elements.photos.value='';processingPhotos=false;submit.disabled=!token;return;}
    try {
      for(const [index,file] of files.entries()){
        if(file.size>25*1024*1024) throw Error('One photo is too large. Choose an image under 25 MB.');
        const bitmap=await createImageBitmap(file);
        const scale=Math.min(1,1600/Math.max(bitmap.width,bitmap.height));
        const canvas=document.createElement('canvas');canvas.width=Math.round(bitmap.width*scale);canvas.height=Math.round(bitmap.height*scale);
        canvas.getContext('2d').drawImage(bitmap,0,0,canvas.width,canvas.height);bitmap.close();
        const blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/jpeg',.78));
        if(!blob || blob.size>750000) throw Error('Photo could not be resized small enough. Choose a smaller image.');
        const content=await new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(r.result.split(',')[1]);r.onerror=reject;r.readAsDataURL(blob);});
        photos.push({filename:`${campaign.toLowerCase()}-photo-${index+1}.jpg`,content});
        const figure=document.createElement('figure'),img=document.createElement('img'),caption=document.createElement('figcaption');
        const url=URL.createObjectURL(blob);objectURLs.push(url);img.src=url;img.alt='Selected photo '+(index+1);caption.textContent='Photo '+(index+1)+' ready';figure.append(img,caption);preview.append(figure);
      }
      status.textContent=files.length?'Photos ready. Complete your request and security check.':'Complete your request and security check.';
      if(photos.length) event('photo_selected',{photo_count:photos.length});
    } catch { photos=[];preview.replaceChildren();form.elements.photos.value='';status.textContent='This image could not be prepared. Choose a smaller JPEG/PNG, or email SDPP with the originals.'; }
    processingPhotos=false;submit.disabled=!token;
  });
  async function initialize(){
    try{
      const response=await fetch('/api/jacksonville',{cache:'no-store'});if(!response.ok)throw Error();const config=await response.json();
      if(!config.enabled || !config.turnstileSiteKey)throw Error();
      await new Promise((resolve,reject)=>{const s=document.createElement('script');s.src='https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';s.onload=resolve;s.onerror=reject;document.head.append(s);});
      widget=window.turnstile.render(form.querySelector('[data-jax-challenge]'),{sitekey:config.turnstileSiteKey,callback:value=>{token=value;submit.disabled=processingPhotos;retrySecurity.hidden=true;},'expired-callback':securityUnavailable,'timeout-callback':securityUnavailable,'error-callback':securityUnavailable});
      status.textContent='Complete your request and security check.';
    }catch{status.textContent='Secure submission is unavailable here. Call or email SDPP using the links below; attach photos in your email app.';}
  }
  form.addEventListener('submit',async e=>{
    e.preventDefault();if(busy||processingPhotos||!token||!form.reportValidity())return;
    busy=true;leadTimestamp=leadTimestamp||new Date().toISOString();submit.disabled=true;status.textContent='Sending your request…';
    const values=Object.fromEntries(new FormData(form));delete values.photos;
    try{
      const response=await fetch('/api/jacksonville',{method:'POST',headers:{'Content-Type':'application/json','X-Idempotency-Key':id},body:JSON.stringify({...values,campaign_identifier:campaign,lead_timestamp:leadTimestamp,attribution,photos,'cf-turnstile-response':token})});
      const result=await response.json();
      if(!response.ok||!result.ok||!result.verified||result.inquiryId!==id)throw Error();
      if (!result.isTest) {
        event('form_submission',{inquiry_id:id});if(photos.length)event('photo_upload',{inquiry_id:id,photo_count:photos.length});
      }
      recordVerifiedAds(result);
      status.textContent=(result.isTest?'TEST delivered to SDPP; excluded from customer-lead and conversion counts. Reference: ':'Your request was delivered to SDPP. Reference: ')+id+(result.isTest?'':'. John will review the details and confirm the next step. A booking or quote has not yet been confirmed.');
      form.querySelectorAll('input,select,textarea,button').forEach(c=>c.disabled=true);
    }catch{status.textContent='Delivery could not be confirmed. Please retry or call/email SDPP. Keep reference '+id+' if you contact us.';token='';window.turnstile?.reset(widget);submit.disabled=true;}
    busy=false;
  });
  initialize();
})();
