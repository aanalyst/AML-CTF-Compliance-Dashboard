# AML/CTF Compliance Dashboard
 
![Dashboard Header](https://github.com/aanalyst/AML-CTF-Compliance-Dashboard/blob/main/Header_Image.png)
 
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
 
![Page 1 - Transaction Monitoring](https://github.com/aanalyst/AML-CTF-Compliance-Dashboard/blob/main/Transaction_Monitoring.png)

**1. High-Risk Categories Are Hiding in Plain Sight** <ul><li>Other (1,508 cases) and Recreation (125) dominate the category chart by volume but Shell Company (89) and Property Investment (18) are the categories that should concern compliance teams most.</li><li>These are classic laundering vehicles. Shell companies provide legal anonymity for fund movement; property investment allows large-scale value transfer through legitimate-looking transactions. Their presence in the data warrants enhanced due diligence regardless of case count.</li><li>Cryptocurrency (5 cases) is the smallest category on the chart but in a real-world context, its emergence as a laundering vehicle is an early warning signal that deserves monitoring as adoption grows.</li></ul> **2. Layering is the Weapon of Choice** <ul><li>The typology chart shows layering (1,370 cases) dwarfs both structuring (321) and integration (54) — it is the dominant method by a wide margin.</li><li>This makes sense operationally since layering is the easiest typology to execute at scale because it only requires access to multiple accounts and repeated transfers. Compliance systems that focus solely on single large transactions will miss the vast majority of laundering activity in this dataset.</li></ul>**3. The ML Model Is Not Just Flagging — It Is Learning** <ul><li>The two-line chart shows confirmed laundering cases and ML-flagged transactions tracking each other almost perfectly across six months — February (341 vs 334), April (197 vs 195), August (58 vs 57).</li><li>The near-identical lines prove the model learned the real seasonal and behavioural patterns driving laundering activity and not just the distribution it was trained on.</li><li>For compliance teams, this means the model can be trusted to flag genuinely suspicious activity in future months, not just replay historical patterns.</li></ul> **4. BSB_Account Dominates Volume but All Three Payment Rails Are Active** <ul><li>BSB_Account (40.05%) leads transaction share, but PayID (29.99%) and CardNumber (29.96%) are nearly equal — meaning no single payment method can be deprioritised from a monitoring perspective.</li><li>The near-even three-way split means laundering activity is not concentrated on one rail. A compliance strategy that monitors only BSB transfers would miss 60% of transaction volume entirely.</li></ul>

### Customer Risk
 
![Page 2 - Customer Risk](https://github.com/aanalyst/AML-CTF-Compliance-Dashboard/blob/main/Customer_Risk.png)
 
**1. The Highest-Risk Transactions Are Also the Highest-Value** <ul><li>The scatter plot shows a dense cluster of low-risk, low-amount transactions on the left. As ML risk score increases toward the right, transaction amounts climb, with the largest outliers (above $4K–$6K) appearing exclusively at higher risk scores.</li><li>This pattern matters for prioritisation. Compliance teams cannot review all 21,938 flagged transactions but the top-right cluster of high-amount, high-risk transactions represents the cases where financial exposure is greatest and investigation effort is best spent.</li></ul> **2. Sydney and Melbourne Require Proportional Not Scrutiny** <ul><li>Sydney (274K) and Melbourne (251K) account for nearly half of all transaction volume. This concentration is expected for Australia's two largest cities.</li><li>The key implication is resource allocation: compliance teams must weight investigation capacity toward these cities not because they are higher risk, but because the sheer volume means more cases will originate there. Treating geographic concentration as a risk signal in itself would lead to misallocated effort.</li></ul> **3. PayID's Laundering Rate Warrants Monitoring as Adoption Grows** <ul><li>The payment method chart shows PayID (0.166) leading CardNumber (0.160) and BSB_Account (0.156) in laundering rate. The differences are narrow today.</li><li>PayID is Australia's fastest-growing real-time payment rail, and AUSTRAC's Tranche 2 reforms significantly expand the types of businesses required to report. As PayID volume scales, even a small rate advantage translates to a materially larger number of cases, making it the payment method most in need of proactive monitoring.</li></ul> **4. A Low Average ML Risk Score Does Not Mean Low Risk** <ul><li>The KPI cards show 10,000 unique customers with an average ML risk score of just 0.026 — consistent with a 0.16% laundering rate across the population.</li><li>A low average score does not indicate a low-risk portfolio; It indicates the model is working as designed, reserving high scores for genuinely suspicious activity.</li></ul>

### Regulatory Summary
 
![](https://github.com/aanalyst/AML-CTF-Compliance-Dashboard/blob/main/Regulatory_Summary.png)
 
**1. TRANSFER Transactions Are the Primary Vehicle for Large-Value Laundering** <ul><li>The TTR breaches chart shows TRANSFER accounting for 598 of 800 breaches — nearly 75% of all transactions that triggered the $10,000 AUD AUSTRAC reporting threshold.</li><li>This is not surprising: bank transfers are the most efficient way to move large amounts between accounts without physical handling. What it tells compliance teams is that TTR monitoring systems must be weighted heavily toward TRANSFER transaction types — DEBIT (84) and PAYMENT (54) are secondary priorities.</li></ul> **2. Structuring Is a National Problem, Not a Local One** <ul><li>The city breakdown shows structuring candidates almost evenly distributed: Sydney (53), Melbourne (52), Perth (27), Brisbane (26), Adelaide (21).</li><li>This even spread across all major cities is a significant finding. If structuring were opportunistic or regionally coordinated, you would expect geographic clustering. The flat distribution instead suggests systematic behaviour — possibly automated or coordinated across accounts — which is a more serious compliance concern than localised activity.</li></ul> **3. Integration Punches Above Its Weight in Total Value** <ul><li>The donut chart shows layering dominating at $15M (74.16%), but integration at $3M (14.58%) is disproportionate given it accounts for the fewest cases of the three typologies.</li><li>This gap between case count and total value is the key insight: integration transactions are individually far larger (SAR report). These are the cases involving Shell Companies and property vehicles where single transactions move millions. For compliance teams, each integration case deserves more investigation time and resources than a layering case even though there are far fewer of them.</li></ul> **4. 800 TTR Deadlines and 207 Investigations Cannot Be Manual** <ul><li>The KPI cards show 800 TTR breaches (each requiring AUSTRAC notification within 10 business days) and 207 structuring candidates requiring investigation — on top of $20.85M in confirmed laundering value to document and report.</li><li>At this scale, manual compliance workflows are not viable. The pipeline built in this project — automated detection, structured views, and pre-formatted SAR reports — is not just a portfolio exercise. It demonstrates the kind of automation layer that financial institutions need to meet AUSTRAC obligations without unsustainable analyst workloads.</li></ul>

# Insights Deep-Dive
 
## Laundering Typologies
 
![Typology Breakdown]()

*Layering Example*
![](https://github.com/aanalyst/AML-CTF-Compliance-Dashboard/blob/main/Layering_Example.png)

 
| |
| --- |
| **Layering vs Integration: Two Different Problems** <br><br> Layering and integration are often discussed together but require completely different detection approaches: <ul><li>**Layering** works through repetition: moving money through multiple accounts in sequence to obscure origin. The data shows clear patterns. Account C986 appearing across three consecutive transfers to C8310 in the dataset is a textbook layering sequence. Detection requires velocity and network analysis across transaction chains, not single-transaction scoring.</li><li>**Integration** works through legitimacy: moving large amounts through apparently legitimate business vehicles. Shell Company and Property Investment categories account for almost all integration cases. Average per-transaction value of $56,290 is nearly 5x higher than layering. Detection requires category and entity-level screening, not pattern frequency analysis.</li><li>**Structuring** works through threshold avoidance — deliberately keeping transactions just below the $10,000 TTR trigger. The 207 candidates in the $9,000–$9,999 band are the observable evidence. Detection requires threshold proximity monitoring combined with account-level repetition checks.</li></ul> A single logistic regression model captures all three but at different confidence levels.

## ML Model Validation
 
![](https://github.com/aanalyst/AML-CTF-Compliance-Dashboard/blob/main/Laundering_cases_month.png)
 
**Why ROC-AUC of 0.9985 Is Not the Story**
 
ROC-AUC can look artificially strong on imbalanced data. The real validation is whether the model tracks actual confirmed cases over time:
 
| Month | Confirmed Cases | ML Flagged | Delta |
| --- | --- | --- | --- |
| February | 341 | 334 | -7 |
| March | 332 | 329 | -3 |
| April | 197 | 195 | -2 |
| May | 276 | 272 | -4 |
| June | 320 | 312 | -8 |
| July | 221 | 217 | -4 |
| August | 58 | 57 | -1 |
 
The model consistently flags slightly fewer transactions than the confirmed count — not randomly over or under. This systematic behaviour shows the model learned the underlying distribution of laundering activity rather than memorising training examples.
 
**The Precision Trade-off**
 
Precision of 8% means 92% of flagged transactions are false positives. In AML this is the correct design:
- Missing a real laundering case risks AUSTRAC enforcement action and fines exceeding $50M.
- Flagging 20,000 legitimate transactions for analyst review costs approximately $100K in labour — a worthwhile trade-off.
- The model is not optimising for analyst convenience; it is optimising for regulatory compliance.
