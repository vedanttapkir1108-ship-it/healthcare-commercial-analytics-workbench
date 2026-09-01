# V2 methodology and validation

## Model
A time-based split trains on months 1–9 and tests on months 10–12. Promotion interactions are explicit continuous terms: promotion count × channel indicator, plus a documented product interaction proxy.

## Metrics
- Train R²: 0.166
- Test R²: 0.185
- Test MAE: 50.01 sales units

## Priority design
Priority score = 50% training sales percentile + 50% predicted-sales percentile. The weights are a transparent business default and should be adjustable after stakeholder discussion.

## Business validation
The ranking is evaluated against average sales in months 10–12. See `v2_priority_validation.csv`. This is predictive validation, not causal uplift validation.

## Power BI model
Load `fact_hcp_promotion.csv` as the fact table and `v2_hcp_priority_scores.csv` as the HCP scoring table. Join on `hcp_id`; use `priority_band`, `region`, `product`, and `channel` as slicers. Use `priority_weights.csv` as a visible assumptions table.

## Guardrails
All HCP-level rows are synthetic. Public IQVIA metrics are aggregate market context only. Production use requires licensed data, privacy review, leakage checks, fairness review, holdout monitoring, and an approved test/control design.
