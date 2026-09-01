"""Build an auditable synthetic commercial analytics workbench."""
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import json
ROOT=Path(__file__).resolve().parents[1]; data=ROOT/'data'; reports=ROOT/'reports'; reports.mkdir(exist_ok=True)
rng=np.random.default_rng(42)
# Synthetic microdata: explicitly not IQVIA/client data.
regions=['North','South','East','West']; products=['Oncology-A','Oncology-B','Immunology-A','Diabetes-A']; channels=['Field','Email','Webinar']
rows=[]
for hcp in range(1,401):
    region=regions[(hcp-1)%4]; product=products[(hcp-1)%4]; base=rng.uniform(30,180); potential=rng.uniform(.5,1.5)
    for month in range(1,13):
        promo=rng.poisson(2) + (month in [3,6,9,12])*1
        channel=channels[rng.integers(0,3)]
        sales=max(0, base*potential + 18*promo + 7*(channel=='Field') + rng.normal(0,25))
        rows.append([hcp,region,product,month,channel,promo,round(sales,2)])
df=pd.DataFrame(rows,columns=['hcp_id','region','product','month','channel','promo_contacts','sales_units']); df.to_csv(data/'synthetic_hcp_promotion_data.csv',index=False)
# Holdout-free explanatory model (portfolio demonstration only)
X=pd.get_dummies(df[['promo_contacts','channel','product','month']],drop_first=True); y=df.sales_units
m=LinearRegression().fit(X,y); pred=m.predict(X)
model={'r2_in_sample':round(float(r2_score(y,pred)),3),'promo_coefficient_units':round(float(m.coef_[list(X.columns).index('promo_contacts')]),2),'note':'Synthetic demonstration; not causal evidence.'}
json.dump(model,open(reports/'model_metrics.json','w'),indent=2)
# score HCPs for targeting: uplift proxy = predicted change when promo contacts increased by 1
sc=df.groupby(['hcp_id','region','product'],as_index=False).agg(avg_sales=('sales_units','mean'),avg_promo=('promo_contacts','mean'),months=('month','count'))
sc['incremental_uplift_proxy']=model['promo_coefficient_units']
sc['priority_score']=sc['avg_sales']*sc['incremental_uplift_proxy']
sc['priority_rank']=sc['priority_score'].rank(ascending=False,method='first').astype(int)
sc.sort_values('priority_rank').to_csv(reports/'hcp_priority_scores.csv',index=False)
# dashboard-like static HTML, no external dependencies
public=pd.read_csv(data/'iqvia_public_metrics.csv')
html=f'''<!doctype html><meta charset="utf-8"><title>Responsible Commercial Analytics Workbench</title><style>body{{font:16px Arial;max-width:1050px;margin:35px auto;color:#172033}}.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}}.card{{padding:18px;border-radius:12px;background:#eef2ff}}.hero{{background:#111827;color:white;padding:28px;border-radius:16px}}table{{border-collapse:collapse;width:100%;margin-top:18px}}td,th{{border-bottom:1px solid #ddd;padding:9px;text-align:left}}.note{{background:#fff7ed;padding:14px;border-left:4px solid #f97316}}</style><div class="hero"><h1>Responsible Commercial Analytics Workbench</h1><p>Public IQVIA market context + synthetic HCP/promotion microdata</p></div><h2>Executive signal</h2><div class="grid"><div class="card"><b>Oncology 2024</b><br>$252bn</div><div class="card"><b>Oncology 2029</b><br>$441bn</div><div class="card"><b>Implied CAGR</b><br>11.8%</div><div class="card"><b>HCP records</b><br>4,800 synthetic rows</div></div><h2>Decision workflow</h2><ol><li>Validate and document data lineage.</li><li>Estimate the relationship between promotional contacts and sales in synthetic data.</li><li>Rank HCPs by transparent priority score.</li><li>Require human review before any commercial action.</li></ol><h2>Model card</h2><table><tr><th>Metric</th><th>Value</th></tr><tr><td>In-sample R²</td><td>{model['r2_in_sample']}</td></tr><tr><td>Promo coefficient</td><td>{model['promo_coefficient_units']} units/contact proxy</td></tr><tr><td>Privacy</td><td>No patient, employee, client, or IQVIA proprietary data</td></tr><tr><td>Causal claim</td><td>None; coefficient is an illustrative association</td></tr></table><div class="note"><b>Governance:</b> This prototype uses public IQVIA headline metrics for market context and fully synthetic microdata for modelling. Licensed IQVIA data, privacy review, bias testing, holdout validation, and client approval are required before production use.</div><h2>Business case</h2><p>The workflow is designed to reduce analyst time spent on data preparation, prioritization, and explanation while making assumptions and limitations visible. It is a value hypothesis, not a claimed IQVIA result.</p>'''
(reports/'workbench.html').write_text(html)
print('Created synthetic dataset, model card, HCP scores and dashboard:',reports/'workbench.html')
