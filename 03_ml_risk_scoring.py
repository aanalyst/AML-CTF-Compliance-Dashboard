"""
AML/CTF Compliance Dashboard Project
Step 3: ML Risk Scoring — Logistic Regression
Input:  amlnet.db (transactions table)
Output: amlnet.db (ml_risk_scores table added)
"""

import sqlite3
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    precision_recall_curve,
    average_precision_score,
)
import time

start = time.time()

# ─────────────────────────────────────────────
# 1. LOAD DATA FROM SQLITE
# ─────────────────────────────────────────────
print("=" * 60)
print("STEP 1: LOADING DATA FROM SQLITE")
print("=" * 60)

conn = sqlite3.connect("amlnet.db")

df = pd.read_sql("SELECT * FROM transactions", conn)
print(f"Rows loaded:    {len(df):,}")
print(f"Columns loaded: {df.shape[1]}")


# ─────────────────────────────────────────────
# 2. FEATURE SELECTION
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 2: FEATURE SELECTION")
print("=" * 60)

FEATURES = [
    # Core transactional
    "amount",
    "hour",
    "day_of_week",
    "balance_delta",
    # Categorical (will be encoded)
    "type",
    "payment_method",
    "category",
    "device_type",
    "device_os",
    # Engineered flags
    "is_structuring_amount",
    "exceeds_ttr_threshold",
    "is_night_transaction",
    "is_weekend",
    "category_risk_encoded",
    # Risk fields
    "risk_score",
    "amount_vs_average",
    "customer_risk_score",
]

TARGET = "isMoneyLaundering"

print(f"Features selected: {len(FEATURES)}")
for f in FEATURES:
    print(f"  - {f}")


# ─────────────────────────────────────────────
# 3. PREPROCESSING
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3: PREPROCESSING")
print("=" * 60)

X = df[FEATURES].copy()
y = df[TARGET].copy()

# Encode categorical columns with LabelEncoder
categorical_cols = ["type", "payment_method", "category", "device_type", "device_os"]
encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    encoders[col] = le
    print(f"  Encoded: {col} ({le.classes_.tolist()})")

# Cast boolean columns to int (SQLite may load them as object)
bool_cols = ["is_structuring_amount", "exceeds_ttr_threshold",
             "is_night_transaction", "is_weekend"]
for col in bool_cols:
    X[col] = X[col].astype(int)

# Handle any remaining nulls
null_counts = X.isnull().sum()
if null_counts.any():
    print(f"\nNulls found — filling with column medians:")
    for col in null_counts[null_counts > 0].index:
        median = X[col].median()
        X[col].fillna(median, inplace=True)
        print(f"  {col}: filled with {median:.2f}")
else:
    print("\nNo nulls found in feature set.")

# Train/test split — stratified to preserve class ratio
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTrain set: {len(X_train):,} rows")
print(f"Test set:  {len(X_test):,} rows")
print(f"Laundering in train: {y_train.sum():,} ({y_train.mean()*100:.2f}%)")
print(f"Laundering in test:  {y_test.sum():,} ({y_test.mean()*100:.2f}%)")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)


# ─────────────────────────────────────────────
# 4. TRAIN MODEL
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4: TRAINING LOGISTIC REGRESSION")
print("=" * 60)

model = LogisticRegression(
    class_weight="balanced",
    max_iter=1000,
    random_state=42,
    solver="lbfgs",
)

print("Training model...")
model.fit(X_train_scaled, y_train)
print("Training complete.")


# ─────────────────────────────────────────────
# 5. EVALUATE MODEL
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 5: MODEL EVALUATION")
print("=" * 60)

y_pred       = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

print("\n--- Classification Report ---")
print(classification_report(y_test, y_pred, target_names=["Legitimate", "Laundering"]))

print("--- Confusion Matrix ---")
cm = confusion_matrix(y_test, y_pred)
print(f"  True Negatives:  {cm[0][0]:,}")
print(f"  False Positives: {cm[0][1]:,}")
print(f"  False Negatives: {cm[1][0]:,}")
print(f"  True Positives:  {cm[1][1]:,}")

roc_auc = roc_auc_score(y_test, y_pred_proba)
avg_precision = average_precision_score(y_test, y_pred_proba)
print(f"\nROC-AUC Score:             {roc_auc:.4f}")
print(f"Average Precision Score:   {avg_precision:.4f}")

print("\n--- Feature Coefficients (influence on laundering prediction) ---")
coef_df = pd.DataFrame({
    "feature":     FEATURES,
    "coefficient": model.coef_[0]
}).sort_values("coefficient", ascending=False)
print(coef_df.to_string(index=False))


# ─────────────────────────────────────────────
# 6. SCORE FULL DATASET
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 6: SCORING FULL DATASET")
print("=" * 60)

X_all = df[FEATURES].copy()
for col in categorical_cols:
    X_all[col] = encoders[col].transform(X_all[col].astype(str))
for col in bool_cols:
    X_all[col] = X_all[col].astype(int)
for col in null_counts[null_counts > 0].index:
    X_all[col].fillna(X_all[col].median(), inplace=True)

X_all_scaled = scaler.transform(X_all)
ml_scores    = model.predict_proba(X_all_scaled)[:, 1]

print(f"Scores generated for {len(ml_scores):,} transactions.")
print(f"Score range: {ml_scores.min():.4f} — {ml_scores.max():.4f}")
print(f"Mean score:  {ml_scores.mean():.4f}")


# ─────────────────────────────────────────────
# 7. WRITE SCORES BACK TO SQLITE
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 7: WRITING SCORES TO SQLITE")
print("=" * 60)

scores_df = pd.DataFrame({
    "transaction_id":    df.index,          # synthetic PK — row position in original dataset
    "nameOrig":          df["nameOrig"],
    "nameDest":          df["nameDest"],
    "amount":            df["amount"],
    "timestamp":         df["timestamp"],
    "isMoneyLaundering": df["isMoneyLaundering"],
    "laundering_typology": df["laundering_typology"],
    "ml_risk_score":     np.round(ml_scores, 6),
    "ml_flag":           (ml_scores >= 0.5).astype(int),
})

scores_df.to_sql("ml_risk_scores", conn, if_exists="replace", index=False)
print(f"ml_risk_scores table written: {len(scores_df):,} rows")
print(f"ML flagged transactions: {scores_df['ml_flag'].sum():,}")

# Create a view joining scores back to transactions via transaction_id
conn.execute("DROP VIEW IF EXISTS vw_ml_flagged")
conn.execute("""
    CREATE VIEW vw_ml_flagged AS
    SELECT
        t.*,
        s.ml_risk_score,
        s.ml_flag
    FROM transactions t
    JOIN ml_risk_scores s ON t.rowid = s.transaction_id + 1
    WHERE s.ml_flag = 1
""")
conn.commit()
print("vw_ml_flagged view created.")

conn.close()

elapsed = round(time.time() - start, 1)
print(f"\nTotal time: {elapsed}s")
print("\nStep 3 complete. Ready for Power BI dashboard (Step 4).")
