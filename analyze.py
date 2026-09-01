"""Public-data IQVIA commercial analytics portfolio project.
Run: python src/analyze.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "reports"
df = pd.read_csv(ROOT / "data/iqvia_public_metrics.csv")
out.mkdir(exist_ok=True)

# Convert comparable oncology spending points into a transparent growth calculation.
onc = df[df.metric.eq("Oncology spending") | df.metric.eq("Oncology spending forecast")]
start = onc.loc[onc.period.eq("2024"), "value"].iloc[0]
end = onc.loc[onc.period.eq("2029"), "value"].iloc[0]
cagr = (end / start) ** (1 / 5) - 1

summary = pd.DataFrame({"metric": ["Oncology 2024-2029 CAGR", "Oncology absolute increase"],
                        "value": [round(cagr * 100, 1), end - start],
                        "unit": ["percent", "USD_bn"]})
summary.to_csv(out / "derived_metrics.csv", index=False)

plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(["2024", "2029"], [start, end], color=["#4f46e5", "#14b8a6"])
ax.set_title(f"IQVIA public data: oncology spending\nImplied CAGR: {cagr:.1%}")
ax.set_ylabel("USD billions at list prices")
for i, v in enumerate([start, end]): ax.text(i, v + 8, str(v), ha="center", fontweight="bold")
fig.tight_layout(); fig.savefig(out / "oncology_spending.png", dpi=180); plt.close(fig)

# Strategic concentration chart.
areas = pd.DataFrame({"therapy_area": ["Top four areas", "Other areas"], "share": [43, 57]})
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(areas.therapy_area, areas.share, color=["#f97316", "#cbd5e1"])
ax.set_ylim(0, 100); ax.set_ylabel("Share of global pharmaceutical value (%)")
ax.set_title("Market concentration signal from IQVIA public research")
for i, v in enumerate(areas.share): ax.text(i, v + 2, f"{v}%", ha="center", fontweight="bold")
fig.tight_layout(); fig.savefig(out / "therapy_concentration.png", dpi=180); plt.close(fig)

with open(out / "executive_summary.md", "w") as f:
    f.write(f'''# Executive summary\n\n## Evidence\nIQVIA public research indicates oncology spending is projected to rise from ${start}bn in 2024 to ${end}bn in 2029, an implied CAGR of {cagr:.1%}. Four therapy areas—oncology, immunology, diabetes and obesity—represent 43% of global pharmaceutical value in the cited 2025 publication.\n\n## Proposed profitable workflow\nA commercial analytics workbench can prioritize brands, indications, geographies and HCP segments for deeper analysis, while exposing source lineage, quality checks, assumptions and model limitations. This targets the business tension IQVIA itself describes: convert increasingly large healthcare datasets into fast, differentiated, trustworthy insights while protecting privacy and governance.\n\n## Value hypothesis (not a realized IQVIA result)\nIf a client improved commercial prioritization by only 1% of the projected oncology increase, the addressable value signal would be approximately ${((end-start)*0.01):.2f}bn. This is a scenario for discussion—not a claim of savings or revenue. A client would need IQVIA data and an approved test design to validate it.\n\n## Next build\nAdd a synthetic HCP/brand/promotion dataset and an auditable promotion-response model. Keep the IQVIA public figures as market context, not as patient-level or client data.\n''')
print(summary.to_string(index=False))
print(f"Wrote outputs to {out}")
