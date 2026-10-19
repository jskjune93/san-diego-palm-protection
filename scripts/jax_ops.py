"""Private SDPP experiment ledger. Standard-library only; never shipped in dist.

Run --help. All dates use the America/Los_Angeles business reporting day (UTC
timestamps retain offsets). No customer data belongs in Git or public hosting.
"""
import argparse, csv, html, json, sqlite3
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

CAMPAIGNS = ['JAX_PHC', 'JAX_SOURCING']
CATEGORIES = ['Google Ads','Website development','Landing-page development','Call tracking','Software','Travel','Sourcing research','Contractor / partner costs','Freight research','Photography / content','Laboratory / diagnostic costs','Market development','Miscellaneous']
PHC_CHECKS = ['decision_maker','real_concern','valuable_palm','serviceable','willing_to_pay']
SOURCE_CHECKS = ['actual_project','location_provided','requirements_discussed','realistic_budget','identifiable_timeline','plausible_economics','logistics_feasible']
STAGES = ['new','contacted','qualified','booked','quoted','won','lost','unqualified']
TZ = ZoneInfo('America/Los_Angeles')
ENTITY = 'San Diego Palm Protection LLC'
DEFAULT_DB = Path('C:/Users/jskju/Pictures/SDPP/Marketing/Google Ads/SDPP-Jacksonville-Test.sqlite')

def connect(path):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(path);db.row_factory=sqlite3.Row
    db.executescript('''
    CREATE TABLE IF NOT EXISTS leads(id TEXT PRIMARY KEY,campaign TEXT NOT NULL,created TEXT NOT NULL,data TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS milestones(lead_id TEXT NOT NULL,stage TEXT NOT NULL,at TEXT NOT NULL,PRIMARY KEY(lead_id,stage));
    CREATE TABLE IF NOT EXISTS expenses(id TEXT PRIMARY KEY,day TEXT NOT NULL,campaign TEXT,category TEXT NOT NULL,amount REAL NOT NULL,marketing INTEGER NOT NULL,note TEXT);
    CREATE TABLE IF NOT EXISTS traffic(id TEXT PRIMARY KEY,day TEXT NOT NULL,campaign TEXT NOT NULL,location TEXT,theme TEXT,search_term TEXT,asset TEXT,clicks INTEGER NOT NULL,calls INTEGER NOT NULL,forms INTEGER NOT NULL,spend REAL NOT NULL);
    CREATE TABLE IF NOT EXISTS reviews(week TEXT,campaign TEXT,best_location TEXT,best_theme TEXT,best_asset TEXT,worst_waste TEXT,recommendation TEXT,PRIMARY KEY(week,campaign));
    '''); return db

def day(value):
    try: return datetime.fromisoformat(value.replace('Z','+00:00')).astimezone(TZ).date().isoformat() if 'T' in value else date.fromisoformat(value).isoformat()
    except (ValueError,AttributeError): raise ValueError('Use an ISO date or timestamp with timezone.')

def iso(value):
    parsed=datetime.fromisoformat(value.replace('Z','+00:00'))
    if parsed.tzinfo is None: raise ValueError('Timestamp requires a timezone offset.')
    return parsed.astimezone(timezone.utc).isoformat()

def number(value):
    n=float(value or 0)
    if n<0 or not __import__('math').isfinite(n): raise ValueError('Amounts and counts must be nonnegative and finite.')
    return n

def ingest_lead(db, record):
    record=dict(record); lid=record['id']; campaign=record['campaign_identifier']
    if campaign not in CAMPAIGNS: raise ValueError('Unknown campaign.')
    created=iso(record['lead_timestamp'])
    if db.execute('SELECT 1 FROM leads WHERE id=?',(lid,)).fetchone(): return False
    record.update(legal_entity=ENTITY,status='test' if record.get('is_test') is True else 'new',qualified=False,qualification_checks={},quoted_value=0,closed_revenue=0,fulfillment_cost=0,lost_reason='',final_disposition='')
    db.execute('INSERT INTO leads VALUES(?,?,?,?)',(lid,campaign,created,json.dumps(record)))
    return True

def update(db, lid, changes):
    row=db.execute('SELECT * FROM leads WHERE id=?',(lid,)).fetchone()
    if not row: raise ValueError('Lead not found.')
    record=json.loads(row['data']); old=record['status']; changes=dict(changes)
    if record.get('is_test') is True: raise ValueError('Delivery tests cannot enter the customer pipeline.')
    for protected in ['id','campaign_identifier','legal_entity','lead_timestamp','attribution','first_touch_timestamp','qualified','is_test']:
        if protected in changes: raise ValueError('Immutable field: '+protected)
    at=iso(changes.pop('at',datetime.now(timezone.utc).isoformat()));record.update(changes)
    checks=PHC_CHECKS if row['campaign']=='JAX_PHC' else SOURCE_CHECKS
    record['qualified']=all(record.get('qualification_checks',{}).get(c) is True for c in checks)
    stage=record['status']
    if stage not in STAGES: raise ValueError('Unknown stage.')
    if stage in ['qualified','booked','quoted','won'] and not record['qualified']: raise ValueError('All qualification checks must be explicitly true before progressing.')
    if stage in ['lost','unqualified'] and not record.get('lost_reason'): raise ValueError('Record a lost / unqualified reason.')
    for k in ['quoted_value','closed_revenue','fulfillment_cost']: record[k]=number(record.get(k))
    if stage=='won' and (not record['closed_revenue'] or not record.get('transaction_reference')): raise ValueError('Won requires closed revenue and an invoice/transaction reference.')
    if stage=='quoted' and not record['quoted_value']: raise ValueError('Quoted requires quote value.')
    if stage in ['won','lost','unqualified']: record['final_disposition']=stage
    if record['qualified']: db.execute('INSERT OR IGNORE INTO milestones VALUES(?,?,?)',(lid,'qualified',at))
    if stage!=old: db.execute('INSERT OR IGNORE INTO milestones VALUES(?,?,?)',(lid,stage,at))
    db.execute('UPDATE leads SET data=? WHERE id=?',(json.dumps(record),lid))

def import_csv(db, kind, path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            campaign=r.get('campaign','')
            if campaign and campaign not in CAMPAIGNS: raise ValueError('Campaign must be blank (other SDPP) or a JAX identifier.')
            d=day(r['day'])
            if kind=='expenses':
                if r['category'] not in CATEGORIES: raise ValueError('Unknown expense category.')
                if r['marketing'] not in ['0','1']:raise ValueError('marketing must be 0 or 1.')
                db.execute('INSERT INTO expenses VALUES(?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET day=excluded.day,campaign=excluded.campaign,category=excluded.category,amount=excluded.amount,marketing=excluded.marketing,note=excluded.note',(r['id'],d,campaign,r['category'],number(r['amount']),int(r['marketing']),r.get('note','')))
            else:
                if not campaign: raise ValueError('Traffic requires a JAX campaign.')
                counts=[number(r[k]) for k in ['clicks','calls','forms']]
                if any(n!=int(n) for n in counts):raise ValueError('Counts must be whole numbers.')
                db.execute('INSERT INTO traffic VALUES(?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET day=excluded.day,campaign=excluded.campaign,location=excluded.location,theme=excluded.theme,search_term=excluded.search_term,asset=excluded.asset,clicks=excluded.clicks,calls=excluded.calls,forms=excluded.forms,spend=excluded.spend',(r['id'],d,campaign,r.get('location',''),r.get('theme',''),r.get('search_term',''),r.get('asset',''),*map(int,counts),number(r['spend'])))

def ratio(a,b): return round(a/b,2) if b else None

def scoreboard(db, start, end):
    rows=[dict(r) for r in db.execute('SELECT * FROM leads') if json.loads(r['data']).get('is_test') is not True]; traffic=[dict(r) for r in db.execute('SELECT * FROM traffic WHERE day>=? AND day<?',(start,end))];expenses=[dict(r) for r in db.execute('SELECT * FROM expenses WHERE day>=? AND day<?',(start,end))]
    milestones=[dict(r) for r in db.execute('SELECT * FROM milestones')]
    output={'start_inclusive':start,'end_exclusive':end,'reporting_timezone':str(TZ),'legal_entity':ENTITY,'campaigns':{}}
    for camp in CAMPAIGNS+['Combined Jacksonville']:
        selected=lambda c:c in CAMPAIGNS if camp=='Combined Jacksonville' else c==camp
        ls=[r for r in rows if selected(r['campaign'])]; ids={r['id'] for r in ls};cohort=[r for r in ls if start<=day(r['created'])<end]
        ts=[r for r in traffic if selected(r['campaign'])]; es=[r for r in expenses if selected(r['campaign'])]
        count=lambda stage:len({m['lead_id'] for m in milestones if m['lead_id'] in ids and m['stage']==stage and start<=day(m['at'])<end})
        spend=sum(r['spend'] for r in ts); nonad=sum(r['amount'] for r in es if r['category']!='Google Ads'); adledger=sum(r['amount'] for r in es if r['category']=='Google Ads')
        marketing_nonad=sum(r['amount'] for r in es if r['category']!='Google Ads' and r['marketing'])
        won={m['lead_id'] for m in milestones if m['lead_id'] in ids and m['stage']=='won' and start<=day(m['at'])<end}
        revenue=sum(json.loads(r['data']).get('closed_revenue',0) for r in ls if r['id'] in won)
        fulfillment=sum(json.loads(r['data']).get('fulfillment_cost',0) for r in ls if r['id'] in won)
        qualified=count('qualified');booked=count('booked');closed=count('won')
        pipeline=sum(json.loads(r['data']).get('quoted_value',0) for r in ls if json.loads(r['data'])['status']=='quoted')
        report={'ad_spend':round(spend,2),'non_ad_test_expense':round(nonad,2),'total_test_expense':round(spend+nonad,2),'ad_expense_ledger_difference':round(adledger-spend,2),'clicks':sum(r['clicks'] for r in ts),'calls':sum(r['calls'] for r in ts),'forms':sum(r['forms'] for r in ts),'new_leads':len(cohort),'qualified_leads':qualified,'booked_opportunities':booked,'quotes_sent':count('quoted'),'closed_transactions':closed,'closed_revenue':revenue,'ad_cost_per_qualified_lead':ratio(spend,qualified),'fully_loaded_cost_per_qualified_lead':ratio(spend+nonad,qualified),'ad_cost_per_booked_opportunity':ratio(spend,booked),'marketing_customer_acquisition_cost':ratio(spend+marketing_nonad,closed),'return_on_ad_spend':ratio(revenue,spend),'pipeline_value_current_snapshot':pipeline,'closed_fulfillment_cost':fulfillment,'contribution_after_fulfillment_and_test_cost':round(revenue-fulfillment-spend-nonad,2),'cohort_qualified_to_date':sum(json.loads(r['data'])['qualified'] for r in cohort),'cohort_won_to_date':sum(json.loads(r['data'])['status']=='won' for r in cohort)}
        review=db.execute('SELECT * FROM reviews WHERE week=? AND campaign=?',(start,camp)).fetchone()
        for key in ['best_location','best_theme','best_asset','worst_waste','recommendation']:report[key]=review[key] if review else 'Review needed — no conclusion recorded'
        if end == (date.fromisoformat(start)+timedelta(days=30)).isoformat():
            records=[json.loads(r['data']) for r in cohort]
            q=sum(r['qualified'] for r in records)
            if camp=='JAX_PHC':
                appointments=sum(any(m['lead_id']==r['id'] and m['stage']=='booked' for m in milestones) for r in records)
                viable=sum(r['status']=='won' or (r.get('viable_opportunity') is True and bool(r.get('viability_evidence'))) for r in records)
                recurring=any(r.get('recurring_interest') is True and r.get('recurring_evidence') for r in records)
                specialist=any(r.get('values_specialist') is True and r.get('specialist_evidence') for r in records)
                report['30_day_signal']={'qualified_leads_at_least_5':q>=5,'booked_opportunities_at_least_3':appointments>=3,'paying_or_evidenced_viable_at_least_2':viable>=2,'recurring_demand_evidence':bool(recurring),'specialist_value_evidence':bool(specialist),'directional_good_signal':q>=5 and appointments>=3 and viable>=2 and bool(recurring) and bool(specialist)}
            elif camp=='JAX_SOURCING':
                serious=sum(r['qualified'] and r.get('quote_requested') is True and bool(r.get('quote_request_evidence')) for r in records)
                report['30_day_signal']={'qualified_inquiries_at_least_3':q>=3,'serious_quote_requests_at_least_1':serious>=1,'species_size_budget_installation_learning':[{'species':r.get('species'),'clear_trunk_ft':r.get('clear_trunk_ft'),'budget':r.get('budget_range'),'installation':r.get('delivery_scope')} for r in records if r['qualified']],'directional_good_signal':q>=3 and serious>=1}
        output['campaigns'][camp]=report
    jax=output['campaigns']['Combined Jacksonville'];other=sum(r['amount'] for r in expenses if not r['campaign'] and r['marketing']); jax_marketing=sum(r['spend'] for r in traffic)+sum(r['amount'] for r in expenses if r['campaign'] in CAMPAIGNS and r['category']!='Google Ads' and r['marketing'])
    output['sdpp_marketing']={'total_marketing_spend_recorded':round(other+jax_marketing,2),'jacksonville_marketing_spend':round(jax_marketing,2),'jacksonville_all_test_expense':jax['total_test_expense'],'jacksonville_marketing_percent':ratio(100*jax_marketing,other+jax_marketing),'coverage':'Recorded/imported expenses only; reconcile to the SDPP accounting ledger. JAX ad ledger rows are reconciliation evidence, not added again.'}
    output['definitions']={'flow':'Qualified, booked, quotes and won count first recorded milestone dates in this interval. Older-lead outcomes may appear; these ratios are period efficiency, not cohort attribution.','cohort':'New leads acquired in the interval plus their current qualification/won state.','pipeline':'Current open quoted value across all dates, unweighted; not historical end-of-week pipeline.','calls':'Actual tracked calls from imported call reports, not phone clicks. Deduplicate providers by lead/reference.','forms':'Provider-confirmed forms imported once; include them in the traffic import, not analytics form starts.','costs':'Fulfillment cost must exclude costs already recorded as test expense, preventing double-counting. Null ratios mean denominator is zero; no inferred results.'}
    return output

def render_report(data, path):
    esc=lambda v:html.escape(str(v if v is not None else '—'))
    cards=''
    for name,metrics in data['campaigns'].items():cards+=f'<section><h2>{esc(name)}</h2><table>'+''.join(f'<tr><th>{esc(k.replace("_"," "))}</th><td>{esc(v)}</td></tr>' for k,v in metrics.items())+'</table></section>'
    body=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>SDPP Jacksonville scoreboard</title><style>body{{font:16px/1.5 system-ui;background:#fffdf8;color:#16221d;margin:32px auto;padding:0 20px;max-width:1150px}}h1,h2{{color:#073d2b}}main{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px}}table{{border-collapse:collapse;width:100%}}th,td{{padding:7px;text-align:left;border-bottom:1px solid #ddd;overflow-wrap:anywhere}}th{{font-weight:500}}section{{min-width:0}}.note{{background:#f4efe3;padding:16px}}</style><h1>Jacksonville market test</h1><p>{esc(ENTITY)} · Private operating report · {esc(data["start_inclusive"])} through {esc(data["end_exclusive"])} (exclusive)</p><p class="note">Empty figures are zero recorded activity, not proof of no demand. No campaign has been launched by this report.</p><main>{cards}</main><h2>SDPP marketing</h2><pre style="white-space:pre-wrap">{esc(json.dumps(data["sdpp_marketing"],indent=2))}</pre><h2>Reading these figures</h2>'+''.join(f'<p><b>{esc(k)}:</b> {esc(v)}</p>' for k,v in data['definitions'].items())+'</html>'
    Path(path).write_text(body,encoding='utf-8')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--db',type=Path,default=DEFAULT_DB);s=p.add_subparsers(dest='command',required=True)
    s.add_parser('init')
    q=s.add_parser('import-lead');q.add_argument('file',type=Path)
    for name in ['expenses','traffic']:
        q=s.add_parser('import-'+name);q.add_argument('file',type=Path)
    q=s.add_parser('update');q.add_argument('id');q.add_argument('file',type=Path,help='JSON changes including status, qualification_checks, at, values and evidence references')
    q=s.add_parser('find');q.add_argument('--campaign',choices=CAMPAIGNS);q.add_argument('--query',default='',help='Search private lead JSON: species, ZIP, budget, height, timeline or type')
    q=s.add_parser('review');q.add_argument('file',type=Path)
    q=s.add_parser('report');q.add_argument('--start',required=True);q.add_argument('--days',type=int,default=7);q.add_argument('--output',type=Path,required=True)
    args=p.parse_args();db=connect(args.db)
    with db:
        if args.command=='import-lead':print('Imported' if ingest_lead(db,json.loads(args.file.read_text(encoding='utf-8-sig'))) else 'Already imported — unchanged')
        elif args.command.startswith('import-'):import_csv(db,args.command[7:],args.file)
        elif args.command=='update':update(db,args.id,json.loads(args.file.read_text(encoding='utf-8-sig')))
        elif args.command=='find':
            for row in db.execute('SELECT * FROM leads WHERE (? IS NULL OR campaign=?) AND lower(data) LIKE ?', (args.campaign,args.campaign,'%'+args.query.lower()+'%')): print(row['data'])
        elif args.command=='review':
            r=json.loads(args.file.read_text(encoding='utf-8-sig'));db.execute('INSERT OR REPLACE INTO reviews VALUES(?,?,?,?,?,?,?)',tuple(r[k] for k in ['week','campaign','best_location','best_theme','best_asset','worst_waste','recommendation']))
        elif args.command=='report':
            if args.days<1 or args.days>366:raise ValueError('Days must be 1–366.')
            start=date.fromisoformat(args.start);data=scoreboard(db,start.isoformat(),(start+timedelta(days=args.days)).isoformat());args.output.parent.mkdir(parents=True,exist_ok=True);args.output.with_suffix('.json').write_text(json.dumps(data,indent=2),encoding='utf-8');render_report(data,args.output)
    db.close()

if __name__=='__main__': main()
