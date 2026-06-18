from pathlib import Path

import duckdb
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", None)

# =====================================================
# CONNECT TO DATABASE
# =====================================================

ROOT = Path(__file__).resolve().parents[2]

DB_PATH = (
    ROOT
    / "data"
    / "warehouse"
    / "duckdb"
    / "lendingclub.duckdb"
)

conn = duckdb.connect(str(DB_PATH))

# =====================================================
# CREATE MART SCHEMA
# =====================================================

print("Creating mart schema...")

conn.execute("""
CREATE SCHEMA IF NOT EXISTS mart
""")

# =====================================================
# DROP EXISTING TABLE
# =====================================================

print("Dropping existing table...")

conn.execute("""
DROP TABLE IF EXISTS mart.vintage_performance
""")

# =====================================================
# CREATE MART
# =====================================================

print("Creating mart.vintage_performance ...")

conn.execute("""
CREATE TABLE mart.vintage_performance AS

SELECT

    issue_year_month,

    COUNT(*) AS loan_count,

    SUM(loan_amnt) AS total_loan_amount,

    AVG(loan_amnt) AS avg_loan_amount,

    AVG(fico_midpoint) AS avg_fico,

    AVG(dti) AS avg_dti,

    AVG(int_rate) AS avg_interest_rate,

    AVG(loan_to_income_ratio) AS avg_loan_to_income_ratio,

    AVG(revol_util) AS avg_revolving_utilization_ratio,

    SUM(default_flag) AS default_count,

    ROUND(
        100.0 * AVG(default_flag),
        2
    ) AS default_rate,

    ROUND(
        100.0 * AVG(high_utilization_flag),
        2
    ) AS high_utilization_rate,

    ROUND(
        100.0 * AVG(high_dti_flag),
        2
    ) AS high_dti_rate

FROM feature.loan_features_v1

GROUP BY issue_year_month

ORDER BY issue_year_month
""")

# =====================================================
# VALIDATION
# =====================================================

print()
print("Mart Row Count")

print(
    conn.execute("""
    SELECT
        COUNT(*) AS rows
    FROM mart.vintage_performance
    """).fetchdf()
)

print()
print("Vintage Grain Validation")

print(
    conn.execute("""
    SELECT
        COUNT(*) AS rows,
        COUNT(DISTINCT issue_year_month) AS unique_vintages
    FROM mart.vintage_performance
    """).fetchdf()
)

print()
print("Loan Count Reconciliation")

print(
    conn.execute("""
    SELECT

        (
            SELECT COUNT(*)
            FROM feature.loan_features_v1
        ) AS feature_rows,

        (
            SELECT SUM(loan_count)
            FROM mart.vintage_performance
        ) AS mart_loan_count
    """).fetchdf()
)

print()
print("Table Structure")

print(
    conn.execute("""
    DESCRIBE mart.vintage_performance
    """).fetchdf()
)

print()
print("Default Rate Reconciliation")

print(
    conn.execute("""
    SELECT

        (
            SELECT
                ROUND(
                    AVG(default_flag) * 100,
                    4
                )
            FROM feature.loan_features_v1
        ) AS feature_default_rate,

        (
            SELECT
                ROUND(
                    SUM(default_count) * 100.0
                    / SUM(loan_count),
                    4
                )
            FROM mart.vintage_performance
        ) AS mart_default_rate
    """).fetchdf()
)

print()
print("Earliest Vintages")

print(
    conn.execute("""
    SELECT *
    FROM mart.vintage_performance
    ORDER BY issue_year_month
    LIMIT 20
    """).fetchdf()
)

print()
print("Highest Default Rate Vintages")

print(
    conn.execute("""
    SELECT *
    FROM mart.vintage_performance
    ORDER BY default_rate DESC
    LIMIT 20
    """).fetchdf()
)

print()
print("Complete")