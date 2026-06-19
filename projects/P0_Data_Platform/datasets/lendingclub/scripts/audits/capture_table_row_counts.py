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
# TABLES TO AUDIT
# =====================================================

TABLES = [

    ("raw", "lendingclub_raw"),

    ("clean", "lendingclub_clean"),

    ("core", "loan_master"),

    ("feature", "loan_features_v1"),

    ("mart", "portfolio_summary"),

    ("mart", "grade_performance"),

    ("mart", "geographic_performance"),

    ("mart", "vintage_performance"),

    ("mart", "risk_segment_performance")

]

# =====================================================
# CAPTURE ROW COUNTS
# =====================================================

print("Capturing row counts...")

snapshot_timestamp = datetime.now()

for schema_name, table_name in TABLES:

    row_count = conn.execute(
        f"""
        SELECT COUNT(*)
        FROM {schema_name}.{table_name}
        """
    ).fetchone()[0]

    conn.execute(
        """
        INSERT INTO audit.table_row_counts
        VALUES (?, ?, ?, ?)
        """,
        [
            snapshot_timestamp,
            schema_name,
            table_name,
            row_count
        ]
    )

# =====================================================
# VALIDATION
# =====================================================

print()
print("Audit Records Created")

print(
    conn.execute(
        """
        SELECT COUNT(*) AS audit_rows
        FROM audit.table_row_counts
        """
    ).fetchdf()
)

print()
print("Latest Snapshot")

print(
    conn.execute(
        """
        SELECT *
        FROM audit.table_row_counts
        ORDER BY snapshot_timestamp DESC,
                 schema_name,
                 table_name
        """
    ).fetchdf()
)

conn.close()

print()
print("Row Count Audit Capture Complete")
print("DuckDB connection closed.")