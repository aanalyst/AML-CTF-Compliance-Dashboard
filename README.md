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
