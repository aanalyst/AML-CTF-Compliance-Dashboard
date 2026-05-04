# AML/CTF Compliance Dashboard
 
![Dashboard Header](https://github.com/aanalyst/AML-CTF-Compliance-Dashboard/blob/main/Gemini_Generated_Image_psyjqbpsyjqbpsyj.png)
 
| |
| --- |
| **Background** 
Australian financial institutions are required under the *AML/CTF Act 2006* to detect, monitor, and report suspicious financial activity to **AUSTRAC** (Australian Transaction Reports and Analysis Centre). With the **Tranche 2 reforms taking effect July 2026**, compliance obligations have expanded significantly — requiring real-time transaction monitoring, automated risk detection, and structured regulatory reporting. This project builds a production-grade compliance analytics pipeline using **AMLNet v2**, a synthetic dataset of **1,090,172 Australian financial transactions** spanning February to August 2025. The dataset mirrors real-world transaction patterns including money laundering typologies (layering, structuring, integration), Australian payment rails (BPAY, OSKO, NPP, PayID), and AUSTRAC-relevant fields. Reporting as a data analyst embedded in a compliance function, an end-to-end analysis was conducted to identify suspicious patterns, score transaction risk using machine learning, and produce AUSTRAC-ready regulatory reports. The key insights and recommendations focus on the following areas: **North Star Metrics** <br> * **Transaction Monitoring** — Volume, value, typology, and category-level laundering patterns across 1.09M transactions <br> * **Customer Risk** — ML risk scoring, geographic concentration, and payment method risk profiling <br> * **Regulatory Compliance** — TTR breach detection, structuring candidate identification, and SAR report generation |
 
---

# North Star Metrics
 
| Metric | Value | Significance |
|--------|-------|--------------|
| **Transactions Processed** | 1,090,172 | Full AMLNet v2 dataset; 57 columns after feature engineering |
| **Confirmed Laundering Cases** | 1,745 (0.16%) | Severe class imbalance requiring deliberate model design |
| **Total Laundering Value (AUD)** | $20.85M | Aggregated across all 1,745 confirmed cases |
| **ML Model Recall** | 97% | Caught 340 of 349 test laundering cases; only 9 missed |
| **ML Model Precision** | 8% | Compliance-first design; false positives acceptable vs false negatives |
| **TTR Breaches Detected** | 800 | Transactions ≥$10,000 AUD requiring AUSTRAC notification |
| **Structuring Candidates** | 207 | $9,000–$9,999 band; potential deliberate threshold avoidance |
| **Average Laundering Amount** | $11,950 | vs $637 for legitimate transactions — 18.8x higher |
| **Unique Customers** | 10,000 | Average ML risk score: 0.026 |
| **High Risk Transactions** | 6,512 (0.60%) | risk_score > 80; 413 confirmed laundering within this group |
 
---

# Executive Summary
 
### Transaction Monitoring (Feb–Aug 2025)
 
![Page 1 - Transaction Monitoring](https://github.com/aanalyst/AML-CTF-Compliance-Dashboard/blob/main/Screenshot%202026-04-30%20143137.png)

**1. High-Risk Categories Are Hiding in Plain Sight** <ul><li>Other (1,508 cases) and Recreation (125) dominate the category chart by volume but Shell Company (89) and Property Investment (18) are the categories that should concern compliance teams most.</li><li>These are classic laundering vehicles. Shell companies provide legal anonymity for fund movement; property investment allows large-scale value transfer through legitimate-looking transactions. Their presence in the data warrants enhanced due diligence regardless of case count.</li><li>Cryptocurrency (5 cases) is the smallest category on the chart but in a real-world context, its emergence as a laundering vehicle is an early warning signal that deserves monitoring as adoption grows.</li></ul> **2. Layering is the Weapon of Choice** <ul><li>The typology chart shows layering (1,370 cases) dwarfs both structuring (321) and integration (54) — it is the dominant method by a wide margin.</li><li>This makes sense operationally since layering is the easiest typology to execute at scale because it only requires access to multiple accounts and repeated transfers. Compliance systems that focus solely on single large transactions will miss the vast majority of laundering activity in this dataset.</li></ul>**3. The ML Model Is Not Just Flagging — It Is Learning** <ul><li>The two-line chart shows confirmed laundering cases and ML-flagged transactions tracking each other almost perfectly across six months — February (341 vs 334), April (197 vs 195), August (58 vs 57).</li><li>This is the most important validation in the dashboard. A model that only memorised the training data would diverge on unseen months. The near-identical lines prove the model learned the real seasonal and behavioural patterns driving laundering activity and not just the distribution it was trained on.</li><li>For compliance teams, this means the model can be trusted to flag genuinely suspicious activity in future months, not just replay historical patterns.</li></ul> **4. BSB_Account Dominates Volume but All Three Payment Rails Are Active** <ul><li>BSB_Account (40.05%) leads transaction share, but PayID (29.99%) and CardNumber (29.96%) are nearly equal — meaning no single payment method can be deprioritised from a monitoring perspective.</li><li>The near-even three-way split means laundering activity is not concentrated on one rail. A compliance strategy that monitors only BSB transfers would miss 60% of transaction volume entirely.</li></ul>

### Customer Risk
 
![Page 2 - Customer Risk](YOUR_PAGE2_SCREENSHOT_URL_HERE)
 
| | |
| --- | --- |
| **1. The Highest-Risk Transactions Are Also the Highest-Value** <ul><li>The scatter plot shows a dense cluster of low-risk, low-amount transactions on the left — the legitimate baseline. As ML risk score increases toward the right, transaction amounts climb, with the largest outliers (above $4K–$6K) appearing exclusively at higher risk scores.</li><li>This pattern matters for prioritisation. Compliance teams cannot review all 21,938 flagged transactions — but the top-right cluster of high-amount, high-risk transactions represents the cases where financial exposure is greatest and investigation effort is best spent.</li></ul> **2. Sydney and Melbourne Require Proportional — Not Elevated — Scrutiny** <ul><li>Sydney (274K) and Melbourne (251K) account for nearly half of all transaction volume. This concentration is expected for Australia's two largest cities.</li><li>The key implication is resource allocation: compliance teams must weight investigation capacity toward these cities not because they are higher risk, but because the sheer volume means more cases will originate there. Treating geographic concentration as a risk signal in itself would lead to misallocated effort.</li></ul> | **3. PayID's Laundering Rate Warrants Monitoring as Adoption Grows** <ul><li>The payment method chart shows PayID (0.166) leading CardNumber (0.160) and BSB_Account (0.156) in laundering rate. The differences are narrow today.</li><li>But context matters: PayID is Australia's fastest-growing real-time payment rail, and AUSTRAC's Tranche 2 reforms significantly expand the types of businesses required to report. As PayID volume scales, even a small rate advantage translates to a materially larger number of cases — making it the payment method most in need of proactive monitoring.</li></ul> **4. A Low Average ML Risk Score Does Not Mean Low Risk** <ul><li>The KPI cards show 10,000 unique customers with an average ML risk score of just 0.026 — consistent with a 0.16% laundering rate across the population.</li><li>This average is deliberately misleading if read in isolation. The model is calibrated to catch every real case (97% recall), which means most flagged transactions are false positives. A low average score does not indicate a low-risk portfolio — it indicates the model is working as designed, reserving high scores for genuinely suspicious activity.</li></ul> |
 
---
