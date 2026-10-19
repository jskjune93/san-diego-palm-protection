import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import vm from 'node:vm';

const source=await readFile(new URL('../site-assets/jacksonville.js',import.meta.url),'utf8');
const helper=source.match(/function recordVerifiedAds\(result\) \{[\s\S]*?\n  \}/)?.[0];
assert.ok(helper);
for(const campaign of ['JAX_PHC','JAX_SOURCING']){
  for(const scenario of ['valid','test_page','test_response','failed','unverified','wrong_reference','preview']){
    const window={dataLayer:[]};
    const context={window,campaign,id:'opaque-request-reference',isTest:scenario==='test_page',adsEnabled:scenario!=='preview',adsDestinations:{JAX_PHC:'AW-18301751378/8YZxCKP7yqIdENKg-pZE',JAX_SOURCING:'AW-18301751378/ldaECKb7yqIdENKg-pZE'},result:{ok:scenario!=='failed',verified:scenario!=='unverified',inquiryId:scenario==='wrong_reference'?'other':'opaque-request-reference',isTest:scenario==='test_response'}};
    vm.runInNewContext(helper+';recordVerifiedAds(result)',context);
    assert.equal(window.dataLayer.length,scenario==='valid'?1:0,`${campaign}: ${scenario}`);
    if(scenario==='valid'){
      const payload=window.dataLayer[0][2];
      assert.equal(payload.send_to,context.adsDestinations[campaign]);
      assert.deepEqual(Object.keys(payload).sort(),['currency','send_to','transaction_id','value']);
      assert.equal(payload.value,0);
    }
  }
}
assert.match(source,/function event\(action, extra=\{\}\) \{\s*if \(isTest\) return;/);
console.log('JAX_CONVERSION_BOUNDARY_OK: test, failed, unverified, wrong-reference and preview requests excluded.');
