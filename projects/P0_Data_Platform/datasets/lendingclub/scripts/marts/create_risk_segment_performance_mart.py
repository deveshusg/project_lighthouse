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
DROP TABLE IF EXISTS mart.risk_segment_performance
""")

# =====================================================
# CREATE MART
# =====================================================

print("Creating mart.risk_segment_performance ...")

conn.execute("""
CREATE TABLE mart.risk_segment_performance AS

WITH segments AS (

    SELECT
        'GRADE' AS segment_type,
        grade AS segment_value,
        *
    FROM feature.loan_features_v1

    UNION ALL

    SELECT
        'UTILIZATION_BAND' AS segment_type,
        utilization_band AS segment_value,
        *
    FROM feature.loan_features_v1

    UNION ALL

    SELECT
        'HIGH_DTI_FLAG' AS segment_type,
        CAST(high_dti_flag AS VARCHAR) AS segment_value,
        *
    FROM feature.loan_features_v1

    UNION ALL

    SELECT
        'THIN_FILE_FLAG' AS segment_type,
        CAST(thin_file_flag AS VARCHAR) AS segment_value,
        *
    FROM feature.loan_features_v1

    UNION ALL

    SELECT
        'BANKRUPTCY_FLAG' AS segment_type,
        CAST(bankruptcy_flag AS VARCHAR) AS segment_value,
        *
    FROM feature.loan_features_v1

)

SELECT

    segment_type,

    segment_value,

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
    ) AS default_rate

FROM segments

GROUP BY
    segment_type,
    segment_value

ORDER BY
    segment_type,
    default_rate DESC
""")

# =====================================================
# VALIDATION
# =====================================================

print()
print("Mart Row Count")

print(
    conn.execute("""
    SELECT COUNT(*) AS rows
    FROM mart.risk_segment_performance
    """).fetchdf()
)

print()
print("Segment Types")

print(
    conn.execute("""
    SELECT
        segment_type,
        COUNT(*) AS segment_count
    FROM mart.risk_segment_performance
    GROUP BY segment_type
    ORDER BY segment_type
    """).fetchdf()
)

print()
print("Table Structure")

print(
    conn.execute("""
    DESCRIBE mart.risk_segment_performance
    """).fetchdf()
)

print()
print("Highest Risk Segments")

print(
    conn.execute("""
    SELECT *
    FROM mart.risk_segment_performance
    ORDER BY default_rate DESC
    LIMIT 25
    """).fetchdf()
)

print()
print("Grade Performance")

print(
    conn.execute("""
    SELECT *
    FROM mart.risk_segment_performance
    WHERE segment_type = 'GRADE'
    ORDER BY segment_value
    """).fetchdf()
)

print()
print("Complete")