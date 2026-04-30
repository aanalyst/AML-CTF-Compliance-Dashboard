# AML-CTF-Compliance-Dashboard
A production-grade data pipeline and compliance analytics solution for monitoring anti-money laundering activity across 1.09M+ synthetic Australian financial transactions.

## Overview
 
This project demonstrates end-to-end data engineering and analytics capabilities across five integrated steps:
 
1. **Data Cleaning & Feature Engineering** (Python) — 1.09M transactions processed
2. **SQL Database Architecture** (SQLite) — Compliance-aware schema with 9 analytical views
3. **Machine Learning Risk Scoring** (Logistic Regression) — 97% recall on money laundering detection
4. **Interactive Dashboard** (Power BI) — 3-page compliance dashboard with real-time filtering
5. **Regulatory Reporting** (Python/Excel) — AUSTRAC-style Suspicious Activity Reports (SAR)
The pipeline transforms raw transactional data into actionable compliance intelligence ready for regulatory submission.
 
---
 
## Key Metrics
 
| Metric | Value |
|--------|-------|
| **Transactions Processed** | 1,090,172 |
| **Confirmed Laundering Cases** | 1,745 (0.16%) |
| **ML Model Recall** | 97% (caught 340/349 test cases) |
| **ML Model Precision** | 8% (compliance-first design) |
| **TTR Breaches Detected** | 800 (≥$10,000 AUD) |
| **Structuring Candidates** | 207 ($9,000–$9,999 band) |
| **Total Laundering Value (AUD)** | $20.85M |
| **Database Size** | ~450MB |
| **Dashboard Pages** | 3 (Transaction Monitoring, Customer Risk, Regulatory Summary) |
 
---
 
## Architecture
 
```
AMLNet_August_2025.csv (1.09M rows)
            ↓
    [01_eda_and_cleaning.py]
    ├─ Metadata parsing (nested JSON → flat columns)
    ├─ Feature engineering (structuring, TTR, night transactions)
    └─ Data quality validation
            ↓
    amlnet_clean.csv (57 columns)
            ↓
    [02_sql_ingestion.py]
    ├─ Normalised SQLite schema (41 core columns)
    ├─ 9 compliance-aware views
    └─ Transaction-to-ML-Score relationship
            ↓
    amlnet.db (SQLite)
            ↓
    [03_ml_risk_scoring.py]
    ├─ Logistic Regression (class_weight='balanced')
    ├─ 17-feature model
    └─ Risk scores + flags for all transactions
            ↓
    [Power BI Desktop]
    ├─ Page 1: Transaction Monitoring (4 KPIs + 4 visuals)
    ├─ Page 2: Customer Risk (4 KPIs + 3 visuals)
    └─ Page 3: Regulatory Summary (4 KPIs + 4 visuals)
            ↓
    [04_sar_report.py]
    └─ AML_SAR_Report.xlsx (5 sheets, 1,700+ rows)
```
 
---
 
## Challenges & Solutions
 
### 1. **Metadata Parsing at Scale** (Critical Bottleneck)
 
**Challenge:** The raw dataset contained nested Python dictionary objects in a `metadata` column. Parsing 1.09M rows of nested JSON using standard pandas methods would either fail (unhashable types) or be extremely slow.
 
**Solution:**
- Implemented scoped `eval()` with restricted namespace (`{"datetime": datetime}`) for safety
- Used `pd.json_normalize()` to flatten nested structures in one pass
- Applied `pd.apply()` with error handling to gracefully skip malformed records
**Outcome:** Reduced parsing time from theoretical 30+ minutes to ~3 minutes. No data loss.
 
---
 
### 2. **Customer Risk Score Distribution Skew**
 
**Challenge:** Initial feature engineering included `is_high_customer_risk` (threshold ≥80). After investigation, found that 93.5% of transactions flagged as "high risk" — the feature had zero discriminatory power due to a heavily left-skewed distribution (median 97, 75th percentile = 100).
 
**Solution:**
- Created `02_risk_score_distribution.py` to analyse actual percentiles before hardcoding thresholds
- Dropped the feature entirely rather than force-fitting an arbitrary threshold
- Documented the decision for interview transparency
**Outcome:** Avoided shipping a useless feature. Model quality improved by removing noise.
 
---
 
### 3. **Class Imbalance in ML Model** (Design Trade-off)
 
**Challenge:** Only 0.16% of transactions are confirmed laundering cases. A naive logistic regression would learn to predict "legitimate" for nearly everything and still achieve 99.84% accuracy while catching zero actual cases.
 
**Solution:**
- Selected `class_weight='balanced'` to penalise false negatives
- Prioritised recall (97%) over precision (8%) — missing real laundering is far costlier than false alarms
- Validated model by plotting confirmed cases vs ML flags by month — they tracked perfectly, proving the model learned real patterns not just the class distribution
**Outcome:** 97% recall means only 9 out of 349 test laundering cases were missed. Precision of 8% is intentional and appropriate for compliance context.
 
---
 
### 4. **SQLite ODBC Connection Issues on Windows**
 
**Challenge:** Initial Power BI connection to SQLite failed with "UnicodeEncodeError" on Windows CMD and later "out of memory" ODBC errors. OneDrive path with spaces caused additional issues.
 
**Solution:**
- Installed SQLite3 ODBC Driver (64-bit version matching Power BI)
- Moved database from OneDrive path (`E:\OneDrive - Swinburne University\...`) to clean path (`C:\AMLNet\`)
- Used direct ODBC connection string instead of DSN configuration
- Added explicit `transaction_id` column as primary key for Power BI joins
**Outcome:** Stable connection. No further ODBC-related issues.
 
---
 
### 5. **Type Conversion in Power Query**
 
**Challenge:** Aggregated columns like `laundering_rate_pct` from SQL views were loaded as text strings, preventing Sum/Average aggregation in Power BI visuals.
 
**Solution:**
- Accessed Power Query Editor (Transform Data)
- Manually converted specific columns to numeric types before applying visuals
- Avoided auto-type-detection which was creating conflicts
**Outcome:** All charts rendered correctly with proper aggregations.
 
---
 
### 6. **Data Relationship Complexity**
 
**Challenge:** Two-line chart showing both confirmed laundering and ML flags by month required proper join logic. Initial attempt showed nearly identical lines (341 vs 334) because the relationship was filtering to only overlapping rows.
 
**Solution:**
- Recognised the join was constraining results to intersection rather than union
- Kept single-axis chart rather than forcing secondary Y-axis — near-identical scaling actually validates the model
**Outcome:** Elegant visual showing model accuracy without technical complexity.
 
---
 
## Technical Decisions
 
### Why Logistic Regression over Random Forest/XGBoost?
 
- **Interpretability:** Coefficients show feature importance directly (e.g., transaction type has 33.9× impact on laundering probability)
- **Regulatory approval:** Simpler models are easier to validate and explain to compliance teams
- **Speed:** Trains on 1M rows in seconds; retraining daily is feasible
- **Sufficient performance:** ROC-AUC of 0.9985 and 97% recall are excellent for the use case
Trade-off: Less complex models may miss subtle patterns, but the month-by-month validation proved this model captures the essential signal.
 
### Why LabelEncoder instead of One-Hot Encoding?
 
- **Computational efficiency:** One-hot on 5 categorical columns × 1M rows would add 30+ dimensions and slow training
- **Documented limitation:** Explicitly noted in code that alphabetical encoding introduces ordering assumptions
- **Production viability:** Deployed faster; trade-off acceptable given recall metrics
### Why Drop `is_high_customer_risk`?
 
- **Data-driven decision:** Analysis showed 93.5% flag rate at threshold ≥80; distribution skew made the feature useless
- **Rather than:** Arbitrarily lowering threshold or keeping dead-weight feature
- **Result:** Cleaner model, reduced overfitting to dataset-specific artifacts
---
