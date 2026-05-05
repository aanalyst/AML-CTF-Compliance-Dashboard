"""
AML/CTF Compliance Dashboard Project
Step 1: Exploratory Data Analysis & Data Cleaning
Dataset: AMLNet_August 2025.csv
"""

import pandas as pd
import numpy as np
import datetime


# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────
print("=" * 60)
print("STEP 1: LOADING DATA")
print("=" * 60)

df = pd.read_csv("AMLNet_August 2025.csv")

print(f"Rows:    {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")
print(f"\nColumn names:\n{list(df.columns)}")


# ─────────────────────────────────────────────
# 2. PARSE METADATA COLUMN
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 2: PARSING METADATA COLUMN")
print("=" * 60)

def parse_metadata(meta):
    """
    Parse metadata string using eval().
    We import the datetime MODULE (not the class) so that
    datetime.datetime(...) in the string resolves correctly.
    Scope is restricted to datetime only for safety.
    """
    try:
        if isinstance(meta, str) and meta.strip():
            return eval(meta, {"datetime": datetime}, {})
        return {}
    except Exception:
        return {}

print("Parsing metadata column (this may take several minutes on 1M+ rows)...")
meta_parsed = df["metadata"].apply(parse_metadata)
print("Metadata parsed.")

print("Flattening nested metadata fields...")
meta_df = pd.json_normalize(meta_parsed)
print("Metadata flattened.")

# Rename flattened columns to clean names
meta_df.rename(columns={
    "location.city":                        "city",
    "location.state":                       "state",
    "location.country":                     "country",
    "location.postcode":                    "postcode",
    "device_info.type":                     "device_type",
    "device_info.os":                       "device_os",
    "device_info.ip_address":               "ip_address",
    "merchant_info.merchant_id":            "merchant_id",
    "merchant_info.category":               "merchant_category",
    "merchant_info.risk_level":             "merchant_risk",
    "merchant_info.avg_transaction":        "merchant_avg_transaction",
    "risk_indicators.amount_vs_average":    "amount_vs_average",
    "risk_indicators.customer_risk_score":  "customer_risk_score",
    "risk_indicators.category_risk":        "category_risk",
    "risk_indicators.risk_score":           "risk_score",
    "risk_indicators.unusual_time":         "unusual_time",
    "risk_indicators.unusual_location":     "unusual_location",
}, inplace=True)

# Drop raw metadata column and join flattened columns
df = df.drop(columns=["metadata"])
df = pd.concat([df, meta_df], axis=1)

print(f"New total columns: {df.shape[1]}")
print(f"New columns added:\n{list(meta_df.columns)}")


# ─────────────────────────────────────────────
# 3. DATA QUALITY CHECK
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3: DATA QUALITY CHECK")
print("=" * 60)

print("\nNull counts per column:")
print(df.isnull().sum().to_string())

print("\nChecking for duplicate rows...")
print(f"Duplicate rows: {df.duplicated(subset=['step', 'nameOrig', 'nameDest', 'amount']).sum()}")

print("\nData types:")
print(df.dtypes.to_string())


# ─────────────────────────────────────────────
# 4. EXPLORATORY DATA ANALYSIS
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4: EXPLORATORY DATA ANALYSIS")
print("=" * 60)

total       = len(df)
ml_count    = df["isMoneyLaundering"].sum()
fraud_count = df["isFraud"].sum()

print(f"\n--- Target Variable Distribution ---")
print(f"Total transactions:        {total:,}")
print(f"Money laundering (1):      {ml_count:,}  ({ml_count/total*100:.2f}%)")
print(f"Legitimate (0):            {total - ml_count:,}  ({(total-ml_count)/total*100:.2f}%)")
print(f"Fraud flagged:             {fraud_count:,}  ({fraud_count/total*100:.2f}%)")

print(f"\n--- Laundering Typologies ---")
print(df["laundering_typology"].value_counts().to_string())

print(f"\n--- Transaction Types ---")
print(df["type"].value_counts().to_string())

print(f"\n--- Transaction Categories ---")
print(df["category"].value_counts().to_string())

print(f"\n--- Amount Statistics (AUD) ---")
print(df["amount"].describe().apply(lambda x: f"${x:,.2f}").to_string())

print(f"\n--- Average Amount by Money Laundering Label ---")
print(df.groupby("isMoneyLaundering")["amount"].describe()[["mean", "min", "max"]].to_string())

print(f"\n--- Top 10 Cities by Transaction Volume ---")
print(df["city"].value_counts().head(10).to_string())

print(f"\n--- State Distribution ---")
print(df["state"].value_counts().to_string())

print(f"\n--- Device Type Distribution ---")
print(df["device_type"].value_counts().to_string())

print(f"\n--- Payment Method Distribution ---")
print(df["payment_method"].value_counts().to_string())

print(f"\n--- Transactions by Hour of Day ---")
print(df["hour"].value_counts().sort_index().to_string())

print(f"\n--- High Risk Transactions (risk_score > 80) ---")
high_risk = df[df["risk_score"] > 80]
print(f"Count:                             {len(high_risk):,} ({len(high_risk)/total*100:.2f}% of all transactions)")
print(f"Money laundering within high risk: {high_risk['isMoneyLaundering'].sum():,}")

print(f"\n--- Unusual Time / Location Flags ---")
print(f"Unusual time transactions:     {df['unusual_time'].sum():,}")
print(f"Unusual location transactions: {df['unusual_location'].sum():,}")


# ─────────────────────────────────────────────
# 5. FEATURE ENGINEERING
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 5: FEATURE ENGINEERING")
print("=" * 60)

# Balance delta — how much the account balance moved
df["balance_delta"] = df["oldbalanceOrg"] - df["newbalanceOrig"]

# Structuring flag — just below $10,000 AUD AUSTRAC reporting threshold
df["is_structuring_amount"] = df["amount"].apply(lambda x: 1 if 9000 <= x < 10000 else 0)

# TTR threshold — at or above $10,000 AUD (Threshold Transaction Report trigger)
df["exceeds_ttr_threshold"] = df["amount"].apply(lambda x: 1 if x >= 10000 else 0)

# Night transaction flag — 11pm to 5am
df["is_night_transaction"] = df["hour"].apply(lambda x: 1 if x >= 23 or x <= 5 else 0)

# Weekend flag
df["is_weekend"] = df["day_of_week"].apply(lambda x: 1 if x >= 6 else 0)

# Encode category_risk as numeric for ML model
risk_map = {"low": 1, "medium": 2, "high": 3}
df["category_risk_encoded"] = df["category_risk"].map(risk_map).fillna(0).astype(int)

# NOTE: is_high_customer_risk was removed — customer_risk_score is heavily
# right-skewed in AMLNet v2 (median 97, 75th percentile = 100), making any
# threshold-based flag near-useless (93.5% of rows flagged at >= 80).

print("Engineered features added:")
new_features = [
    "balance_delta", "is_structuring_amount", "exceeds_ttr_threshold",
    "is_night_transaction", "is_weekend", "category_risk_encoded"
]
for f in new_features:
    print(f"  + {f}")

print(f"\nStructuring candidates ($9k-$10k): {df['is_structuring_amount'].sum():,}")
print(f"TTR threshold breaches (>=$10k):   {df['exceeds_ttr_threshold'].sum():,}")
print(f"Night transactions:                {df['is_night_transaction'].sum():,}")


# ─────────────────────────────────────────────
# 6. EXPORT CLEAN DATASET
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 6: EXPORTING CLEAN DATASET")
print("=" * 60)

output_path = "amlnet_clean.csv"
df.to_csv(output_path, index=False)

print(f"Clean dataset saved to: {output_path}")
print(f"Final shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"Columns in clean dataset:\n{list(df.columns)}")
print("\n Step 1 complete. Ready for SQL ingestion (Step 2).")