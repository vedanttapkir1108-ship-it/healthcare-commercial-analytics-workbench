"""V2: time-split promotion-response model, interpretable interactions, and out-of-sample ranking validation."""
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
ROOT=Path(__file__).resolve().parents[1]; data=ROOT/'data'; reports=ROOT/'reports'; reports.mkdir(exist_ok=True)
df=pd.read_csv(data/'synthetic_hcp_promotion_data.csv')
# Explicit interactions: continuous promotion count multiplied by one-hot channel/product/region.
df['promo_x_field']=df.promo_contacts*(df.channel=='Field').astype(int)
df['promo_x_email']=df.promo_contacts*(df.channel=='Email').astype(int)
df['promo_x_webinar']=df.promo_contacts*(df.channel=='Webinar').astype(int)
df['promo_x_product']=df.promo_contacts*df['product'].map({'Oncology-A':1.0,'Oncology-B':1.05,'Immunology-A':.95,'Diabetes-A':1.1})
features=['promo_contacts','promo_x_field','promo_x_email','promo_x_webinar','promo_x_product','month','channel','product','region']
num=['promo_contacts','promo_x_field','promo_x_email','promo_x_webinar','promo_x_product','month']; cat=['channel','product','region']
pre=ColumnTransformer([('num','passthrough',num),('cat',OneHotEncoder(handle_unknown='ignore',drop='first'),cat)])
model=Pipeline([('prep',pre),('reg',LinearRegression())])
train=df[df.month<=9].copy(); test=df[df.month>=10].copy(); model.fit(train[features],train.sales_units)
train_pred=model.predict(train[features]); test_pred=model.predict(test[features])
metrics={'train_rows':len(train),'test_rows':len(test),'train_r2':round(float(r2_score(train.sales_units,train_pred)),3),'test_r2':round(float(r2_score(test.sales_units,test_pred)),3),'test_mae':round(float(mean_absolute_error(test.sales_units,test_pred)),2),'note':'Time split: months 1-9 train, months 10-12 test. Synthetic data; association not causation.'}
pd.DataFrame([metrics]).to_json(reports/'v2_model_metrics.json',orient='records',indent=2)
# Rank using training history + model-predicted response proxy; validate against future test sales.
train['pred']=train_pred; test['pred']=test_pred
agg=train.groupby(['hcp_id','region','product'],as_index=False).agg(train_sales=('sales_units','mean'),train_promo=('promo_contacts','mean'),predicted_sales=('pred','mean'))
agg['sales_percentile']=agg.train_sales.rank(pct=True); agg['response_percentile']=agg.predicted_sales.rank(pct=True)
# Business-configurable weights; documented default is 50/50.
agg['priority_score']=0.5*agg.sales_percentile+0.5*agg.response_percentile
agg['priority_band']=pd.qcut(agg.priority_score, q=3, labels=['Monitor','Develop','Prioritize'])
future=test.groupby('hcp_id',as_index=False).agg(test_sales=('sales_units','mean'))
val=agg.merge(future,on='hcp_id',how='left'); val['priority_band']=val.priority_band.astype(str)
validation=val.groupby('priority_band',as_index=False).agg(hcps=('hcp_id','count'),avg_test_sales=('test_sales','mean'),median_test_sales=('test_sales','median'))
validation.to_csv(reports/'v2_priority_validation.csv',index=False); val.sort_values('priority_score',ascending=False).to_csv(reports/'v2_hcp_priority_scores.csv',index=False)
# Power BI-ready star-schema exports.
df[['hcp_id','region','product','month','channel','promo_contacts','sales_units']].to_csv(reports/'fact_hcp_promotion.csv',index=False)
pd.DataFrame({'priority_band':['Monitor','Develop','Prioritize'],'weight_sales_percentile':[.5,.5,.5],'weight_response_percentile':[.5,.5,.5]}).to_csv(reports/'priority_weights.csv',index=False)
with open(reports/'v2_methodology.md','w') as f:
 f.write(f'''# V2 methodology and validation\n\n## Model\nA time-based split trains on months 1–9 and tests on months 10–12. Promotion interactions are explicit continuous terms: promotion count × channel indicator, plus a documented product interaction proxy.\n\n## Metrics\n- Train R²: {metrics["train_r2"]}\n- Test R²: {metrics["test_r2"]}\n- Test MAE: {metrics["test_mae"]} sales units\n\n## Priority design\nPriority score = 50% training sales percentile + 50% predicted-sales percentile. The weights are a transparent business default and should be adjustable after stakeholder discussion.\n\n## Business validation\nThe ranking is evaluated against average sales in months 10–12. See `v2_priority_validation.csv`. This is predictive validation, not causal uplift validation.\n\n## Power BI model\nLoad `fact_hcp_promotion.csv` as the fact table and `v2_hcp_priority_scores.csv` as the HCP scoring table. Join on `hcp_id`; use `priority_band`, `region`, `product`, and `channel` as slicers. Use `priority_weights.csv` as a visible assumptions table.\n\n## Guardrails\nAll HCP-level rows are synthetic. Public IQVIA metrics are aggregate market context only. Production use requires licensed data, privacy review, leakage checks, fairness review, holdout monitoring, and an approved test/control design.\n''')
print(metrics); print(validation.to_string(index=False))
