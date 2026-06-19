from pathlib import Path
from datetime import datetime

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

print(DB_PATH)

conn = duckdb.connect(str(DB_PATH))

# =====================================================
# CONFIGURATION
# =====================================================

TABLE_NAME = "feature.loan_features_v1"

CHECK_TIMESTAMP = datetime.now()

# =====================================================
# CLEAR EXISTING RESULTS
# =====================================================

print("Clearing existing quality results...")

conn.execute("""
DELETE FROM audit.data_quality_results
""")

# =====================================================
# QUALITY CHECK DEFINITIONS
# =====================================================

QUALITY_CHECKS = [

    {
        "check_name": "loan_id_uniqueness",
        "query": """
            SELECT COUNT(*)
            FROM (
                SELECT loan_id
                FROM feature.loan_features_v1
                GROUP BY loan_id
                HAVING COUNT(*) > 1
            )
        """,
        "severity": "FAIL"
    },

    {
        "check_name": "loan_amount_positive",
        "query": """
            SELECT COUNT(*)
            FROM feature.loan_features_v1
            WHERE loan_amnt <= 0
               OR loan_amnt IS NULL
        """,
        "severity": "FAIL"
    },

    {
        "check_name": "fico_range_valid",
        "query": """
            SELECT COUNT(*)
            FROM feature.loan_features_v1
            WHERE fico_midpoint < 300
               OR fico_midpoint > 850
               OR fico_midpoint IS NULL
        """,
        "severity": "FAIL"
    },

    {
        "check_name": "dti_negative_values",
        "query": """
            SELECT COUNT(*)
            FROM feature.loan_features_v1
            WHERE dti < 0
        """,
        "severity": "FAIL"
    },

    {
        "check_name": "dti_missing_values",
        "query": """
            SELECT COUNT(*)
            FROM feature.loan_features_v1
            WHERE dti IS NULL
        """,
        "severity": "WARN"
    },

    {
        "check_name": "default_flag_valid",
        "query": """
            SELECT COUNT(*)
            FROM feature.loan_features_v1
            WHERE default_flag NOT IN (0,1)
               OR default_flag IS NULL
        """,
        "severity": "FAIL"
    },

    {
        "check_name": "grade_valid",
        "query": """
            SELECT COUNT(*)
            FROM feature.loan_features_v1
            WHERE grade NOT IN
            ('A','B','C','D','E','F','G')
               OR grade IS NULL
        """,
        "severity": "FAIL"
    },

    {
        "check_name": "issue_date_present",
        "query": """
            SELECT COUNT(*)
            FROM feature.loan_features_v1
            WHERE issue_date IS NULL
        """,
        "severity": "FAIL"
    }

]

# =====================================================
# EXECUTE CHECKS
# =====================================================

print("Running quality checks...")

for check in QUALITY_CHECKS:

    failed_rows = conn.execute(
        check["query"]
    ).fetchone()[0]

    if failed_rows == 0:
        status = "PASS"

    elif check["severity"] == "WARN":
        status = "WARN"

    else:
        status = "FAIL"

    conn.execute(
        """
        INSERT INTO audit.data_quality_results
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            CHECK_TIMESTAMP,
            TABLE_NAME,
            check["check_name"],
            status,
            failed_rows
        ]
    )

# =====================================================
# QUALITY RESULTS
# =====================================================

print()
print("Quality Check Results")

print(
    conn.execute("""
    SELECT *
    FROM audit.data_quality_results
    ORDER BY check_name
    """).fetchdf()
)

# =====================================================
# SUMMARY
# =====================================================

print()
print("Quality Summary")

print(
    conn.execute("""
    SELECT
        status,
        COUNT(*) AS check_count
    FROM audit.data_quality_results
    GROUP BY status
    ORDER BY status
    """).fetchdf()
)

# =====================================================
# FAILURES
# =====================================================

print()
print("Failed Checks")

print(
    conn.execute("""
    SELECT *
    FROM audit.data_quality_results
    WHERE status = 'FAIL'
    ORDER BY failed_rows DESC
    """).fetchdf()
)

# =====================================================
# WARNINGS
# =====================================================

print()
print("Warning Checks")

print(
    conn.execute("""
    SELECT *
    FROM audit.data_quality_results
    WHERE status = 'WARN'
    ORDER BY failed_rows DESC
    """).fetchdf()
)

# =====================================================
# DTI INVESTIGATION
# =====================================================

print()
print("Negative DTI Records")

print(
    conn.execute("""
    SELECT
        loan_id,
        dti,
        annual_inc,
        grade,
        issue_date
    FROM feature.loan_features_v1
    WHERE dti < 0
    """).fetchdf()
)

conn.close()

print()
print("Data Quality Checks Complete")
print("DuckDB connection closed.")