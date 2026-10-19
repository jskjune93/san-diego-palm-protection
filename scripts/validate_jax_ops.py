"""Exercise qualification gates, imports, expense deduplication and week boundaries."""
import json, tempfile
from pathlib import Path
from jax_ops import connect, ingest_lead, update, scoreboard

with tempfile.TemporaryDirectory() as temp:
    db=connect(Path(temp)/'test.sqlite')
    lead={'id':'test','campaign_identifier':'JAX_PHC','lead_timestamp':'2026-10-19T12:00:00Z','city':'Jacksonville'}
    assert ingest_lead(db,lead)
    assert not ingest_lead(db,lead)
    assert ingest_lead(db,{**lead,'id':'delivery-test','is_test':True})
    assert scoreboard(db,'2026-10-19','2026-10-26')['campaigns']['JAX_PHC']['new_leads']==1
    try:update(db,'delivery-test',{'status':'qualified'})
    except ValueError:pass
    else:raise AssertionError('Delivery test entered customer pipeline')
    try:update(db,'test',{'status':'won','closed_revenue':100})
    except ValueError:pass
    else:raise AssertionError('Unqualified lead progressed')
    checks={k:True for k in ['decision_maker','real_concern','valuable_palm','serviceable','willing_to_pay']}
    update(db,'test',{'status':'qualified','qualification_checks':checks,'at':'2026-10-20T12:00:00Z'})
    update(db,'test',{'status':'booked','at':'2026-10-21T12:00:00Z'})
    update(db,'test',{'status':'quoted','quoted_value':1000,'at':'2026-10-22T12:00:00Z'})
    update(db,'test',{'status':'won','closed_revenue':900,'fulfillment_cost':200,'transaction_reference':'MOCK','at':'2026-10-23T12:00:00Z'})
    db.execute('INSERT INTO traffic VALUES(?,?,?,?,?,?,?,?,?,?,?)',('t','2026-10-20','JAX_PHC','Jacksonville','Declining palm','','',10,1,1,100))
    db.executemany('INSERT INTO expenses VALUES(?,?,?,?,?,?,?)', [('ad','2026-10-20','JAX_PHC','Google Ads',100,1,'reconcile'),('dev','2026-10-20','JAX_PHC','Landing-page development',50,1,''),('other','2026-10-20','','Software',50,1,'')])
    result=scoreboard(db,'2026-10-19','2026-10-26');m=result['campaigns']['JAX_PHC']
    assert m['total_test_expense']==150 and m['ad_expense_ledger_difference']==0
    assert m['qualified_leads']==1 and m['booked_opportunities']==1 and m['quotes_sent']==1 and m['closed_transactions']==1
    assert m['marketing_customer_acquisition_cost']==150 and m['return_on_ad_spend']==9
    assert m['pipeline_value_current_snapshot']==0 and m['contribution_after_fulfillment_and_test_cost']==550
    assert result['sdpp_marketing']['total_marketing_spend_recorded']==200
    assert result['sdpp_marketing']['jacksonville_marketing_percent']==75
    assert scoreboard(db,'2026-10-26','2026-11-02')['campaigns']['JAX_PHC']['closed_transactions']==0
    assert scoreboard(db,'2026-10-19','2026-11-18')['campaigns']['JAX_PHC']['30_day_signal']['directional_good_signal'] is False
    db.close()
print('JAX_OPS_OK: temporary test data only; no business ledger mutations.')
