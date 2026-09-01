# Healthcare Commercial Analytics Workbench

An independent portfolio project combining public IQVIA India pharmaceutical market research with synthetic HCP-level promotion data.

## Important disclaimer

This project is not affiliated with IQVIA.

It does not use:

- IQVIA proprietary data
- Patient-level data
- HCP personal data
- Employee data
- Client data
- Confidential company information

Public IQVIA aggregate figures are used only as market context. HCP-level data is synthetic and was created for analytical demonstration.

## Business problem

How can a healthcare analytics team convert market signals and commercial activity data into transparent, actionable, and privacy-safe prioritization recommendations?

## What the project demonstrates

- Healthcare and pharmaceutical commercial analytics
- India pharmaceutical market analysis
- SQL-style data preparation
- Python and pandas data processing
- Statistical modelling
- Promotion-response analysis
- Promotion-by-channel interaction terms
- HCP prioritization
- Time-based train/test validation
- Out-of-sample ranking validation
- Data-quality controls
- Source lineage
- Model documentation
- Power BI-ready data outputs
- Responsible AI and analytics governance

## India market context

Selected public IQVIA India Q2 2025 figures used in the project include:

- Indian Pharmaceutical Market size: ₹61,000 crore
- Year-over-year market growth: 9%
- Sequential market growth: 7%
- Chronic therapy growth: 10%
- Acute therapy growth: 7%
- Cardiac therapy growth: 11%
- Neuro/CNS growth: 10%
- West-zone growth: 11%
- GLP-1 agonist growth: 145%

Source:

https://www.iqvia.com/locations/india/library/presentations/indian-pharmaceutical-business-quarterly-insights-q2-2025

## Modelling approach

The project uses synthetic HCP-month data containing:

- HCP ID
- Region
- Product
- Month
- Promotion channel
- Promotional contacts
- Sales units

The model uses explicit interaction terms:

- Promotion × Field
- Promotion × Email
- Promotion × Webinar
- Promotion × Product

The model is trained on months 1–9 and evaluated on months 10–12.

## Validation

The HCP priority ranking is created using:

- Training-period sales percentile
- Predicted response percentile

The default weighting is:

- 50% sales percentile
- 50% response percentile

The ranking is evaluated using future-period sales in months 10–12.

This is predictive validation on synthetic data. It is not causal evidence of incremental sales or promotional uplift.

## Project files

- `data/` — public market metrics and synthetic HCP data
- `reports/` — dashboards, model metrics, priority scores, and validation outputs
- `src/` — Python analysis scripts

## Future production requirements

A production deployment would require:

- Licensed and approved data
- Privacy and security review
- Data-quality assessment
- Leakage checks
- Fairness and bias review
- Holdout monitoring
- Causal or test/control design
- Client approval
- Human review of recommendations
- Full audit trail

## Author

Vedant Rajesh Tapkir

B.Pharm Candidate | Healthcare and Life-Sciences Data Analytics

Pune, Maharashtra, India
