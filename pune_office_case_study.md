# Pune Office Case Study: India Commercial Analytics Workbench

## Executive proposition
Build a privacy-safe, auditable India commercial analytics workflow that helps a Pune analytics team move from market signal to client-ready action: identify high-growth therapy opportunities, prioritize regions, model promotion response, and produce traceable recommendations.

This is designed for an analyst/consultant workflow—not a claim about IQVIA's internal systems.

## Why Pune-specific
Public recruitment information describes the Pune/159 Solutions team as working with global/onshore teams on healthcare analytics, promotion-response modelling, patient claims analytics, sales-force strategy, incentive compensation and business intelligence. The role emphasizes large healthcare datasets, SQL/Alteryx/SAS-style workflows, statistical models, PowerPoint and Tableau/Qlik/Sisense communication.

## India evidence from IQVIA
The included `data/iqvia_india_q2_2025_public_metrics.csv` transcribes selected figures from IQVIA's Indian Pharmaceutical Business Quarterly Insights – Q2 2025:

- Q2 2025 market size: INR 61,000 crore
- Growth: 9% versus Q2 2024; 7% versus Q1 2025
- Chronic growth: 10%; acute growth: 7%
- Cardiac growth: 11%; Neuro/CNS growth: 10%
- West zone growth: 11%; the report states Maharashtra and Gujarat reflected double-digit growth
- GLP-1 agonist market growth: 145% in the cited quarter

Source: https://www.iqvia.com/locations/india/library/presentations/indian-pharmaceutical-business-quarterly-insights-q2-2025

## The proposed client value
The workflow helps a brand team answer:

1. Which therapy/region combinations deserve deeper field-force analysis?
2. Which HCP segments respond to which channels?
3. Which promotional actions appear associated with incremental sales?
4. Can the recommendation be reproduced from source data and assumptions?

Potential value is reduced analyst rework, faster scenario analysis, more consistent deliverables, and better prioritization. Revenue impact must be validated with licensed client data and a test/control design.

## Demonstration architecture
- Public IQVIA India market figures: context and prioritization signals
- Synthetic HCP/month-level data: safe demonstration of modelling
- Python/pandas: data preparation and validation
- scikit-learn: illustrative response model
- CSV outputs: transparent HCP ranking
- HTML dashboard: client-ready storytelling
- Model card: limitations, lineage, and governance

## Interview-ready insight
> “For a Pune team serving global life-sciences clients, I localized the workbench to India rather than using only global figures. IQVIA's Q2 2025 India data shows a 9% IPM growth rate, stronger chronic than acute growth, an 11% West-zone growth signal, and very rapid GLP-1 growth. I used those signals to define the prioritization layer, while keeping HCP-level data synthetic because IQVIA's real claims and HCP data are proprietary. The design can be connected to approved licensed data later and includes lineage, validation and model-governance controls.”

## Limitations
The market figures are public, aggregate IQVIA figures. They are not patient-level, HCP-level, or client data. The synthetic model is not causal evidence and cannot be used for real targeting. No claim of IQVIA revenue, savings, or internal employee work is made.
