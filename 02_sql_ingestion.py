"""
AML/CTF Compliance Dashboard Project
Step 2: SQL Ingestion — SQLite Database
Input:  amlnet_clean.csv
Output: amlnet.db
"""

import pandas as pd
import sqlite3
import time

# ─────────────────────────────────────────────
# 1. LOAD CLEAN DATASET
# ─────────────────────────────────────────────
print("=" * 60)
print("STEP 1: LOADING CLEAN DATASET")
print("=" * 60)

start = time.time()
df = pd.read_csv("amlnet_clean.csv", low_memory=False)
print(f"Rows loaded:    {len(df):,}")
print(f"Columns loaded: {df.shape[1]}")


# ─────────────────────────────────────────────
# 2. DROP USELESS COLUMNS
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 2: DROPPING USELESS COLUMNS")
print("=" * 60)

cols_to_drop = [
    "merchant_info",                       # 100% null
    "sophistication",                      # 99.99% null
    "integration_info.type",               # only populated for 54 integration rows
    "integration_info.legitimacy_score",
    "integration_info.detection_risk",
    "integration_info.location",
    "integration_info.total_amount",
    "integration_info.num_sources",
    "integration_info.average_amount",
    "integration_info.sector",
    "integration_info.platform",
    "structuring.sophistication",          # only populated for 321 structuring rows
    "structuring.threshold_proximity",
    "structuring.pattern_size",
    "layering",                            # only populated for 1,370 layering rows
    "layering_sophistication",
]

df.drop(columns=[c for c in cols_to_drop if c in df.columns], inplace=True)
print(f"Dropped {len(cols_to_drop)} columns.")
print(f"Remaining columns: {df.shape[1]}")


# ─────────────────────────────────────────────
# 4. INGEST INTO SQLITE
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3: INGESTING INTO SQLITE")
print("=" * 60)

db_path = "amlnet.db"
conn = sqlite3.connect(db_path)

print("Writing transactions table (this may take a few minutes on 1M+ rows)...")
df.insert(0, "transaction_id", range(len(df)))
df.to_sql("transactions", conn, if_exists="replace", index=False, chunksize=10000)
print(f"Done. Rows written: {len(df):,}")


# ─────────────────────────────────────────────
# 5. CREATE VIEWS
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4: CREATING VIEWS")
print("=" * 60)

views = {

    "vw_suspicious_transactions": """
        SELECT *
        FROM transactions
        WHERE isMoneyLaundering = 1
    """,

    "vw_high_risk_transactions": """
        SELECT *
        FROM transactions
        WHERE risk_score > 80
    """,

    "vw_ttr_breaches": """
        -- Transactions at or above the AUSTRAC $10,000 TTR threshold
        SELECT *
        FROM transactions
        WHERE exceeds_ttr_threshold = 1
    """,

    "vw_structuring_candidates": """
        -- Transactions in $9,000-$9,999 band — potential structuring activity
        SELECT *
        FROM transactions
        WHERE is_structuring_amount = 1
    """,

    "vw_typology_summary": """
        -- Count and total amount by laundering typology
        SELECT
            laundering_typology,
            COUNT(*)                          AS transaction_count,
            SUM(isMoneyLaundering)            AS laundering_count,
            ROUND(AVG(amount), 2)             AS avg_amount,
            ROUND(SUM(amount), 2)             AS total_amount
        FROM transactions
        GROUP BY laundering_typology
        ORDER BY laundering_count DESC
    """,

    "vw_city_summary": """
        -- Transaction volume and laundering rate by city
        SELECT
            city,
            COUNT(*)                                          AS transaction_count,
            SUM(isMoneyLaundering)                            AS laundering_count,
            ROUND(SUM(amount), 2)                             AS total_amount,
            ROUND(AVG(amount), 2)                             AS avg_amount,
            ROUND(SUM(isMoneyLaundering) * 100.0 / COUNT(*), 4) AS laundering_rate_pct
        FROM transactions
        GROUP BY city
        ORDER BY transaction_count DESC
    """,

    "vw_payment_method_risk": """
        -- Risk profile by payment method
        SELECT
            payment_method,
            COUNT(*)                                          AS transaction_count,
            SUM(isMoneyLaundering)                            AS laundering_count,
            ROUND(AVG(risk_score), 2)                         AS avg_risk_score,
            ROUND(SUM(isMoneyLaundering) * 100.0 / COUNT(*), 4) AS laundering_rate_pct
        FROM transactions
        GROUP BY payment_method
        ORDER BY laundering_rate_pct DESC
    """,

    "vw_hourly_activity": """
        -- Transaction volume and laundering count by hour of day
        SELECT
            hour,
            COUNT(*)               AS transaction_count,
            SUM(isMoneyLaundering) AS laundering_count,
            ROUND(AVG(amount), 2)  AS avg_amount
        FROM transactions
        GROUP BY hour
        ORDER BY hour
    """,

    "vw_category_risk": """
        -- Laundering concentration by transaction category
        SELECT
            category,
            COUNT(*)                                          AS transaction_count,
            SUM(isMoneyLaundering)                            AS laundering_count,
            ROUND(AVG(amount), 2)                             AS avg_amount,
            ROUND(SUM(isMoneyLaundering) * 100.0 / COUNT(*), 4) AS laundering_rate_pct
        FROM transactions
        GROUP BY category
        ORDER BY laundering_count DESC
    """,

}

for view_name, view_sql in views.items():
    conn.execute(f"DROP VIEW IF EXISTS {view_name}")
    conn.execute(f"CREATE VIEW {view_name} AS {view_sql}")
    print(f"  + {view_name}")

conn.commit()


# ─────────────────────────────────────────────
# 6. VERIFICATION
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 5: VERIFICATION")
print("=" * 60)

# Row count
row_count = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
print(f"transactions table row count: {row_count:,}")

# Column count
col_count = conn.execute("PRAGMA table_info(transactions)").fetchall()
print(f"transactions table column count: {len(col_count)}")

# Spot check each view
print("\nView row counts:")
for view_name in views.keys():
    count = conn.execute(f"SELECT COUNT(*) FROM {view_name}").fetchone()[0]
    print(f"  {view_name}: {count:,} rows")

conn.close()

elapsed = round(time.time() - start, 1)
print(f"\nTotal time: {elapsed}s")
print(f"Database saved to: {db_path}")
print("\nStep 2 complete. Ready for ML risk scoring (Step 3).")
