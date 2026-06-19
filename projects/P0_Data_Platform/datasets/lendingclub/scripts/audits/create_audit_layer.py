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

print(DB_PATH)

conn = duckdb.connect(str(DB_PATH))

# =====================================================
# CREATE AUDIT SCHEMA
# =====================================================

print("Creating audit schema...")

conn.execute("""
CREATE SCHEMA IF NOT EXISTS audit
""")

# =====================================================
# DROP TABLES
# =====================================================

print("Dropping existing audit tables...")

conn.execute("""
DROP TABLE IF EXISTS audit.etl_runs
""")

conn.execute("""
DROP TABLE IF EXISTS audit.table_row_counts
""")

conn.execute("""
DROP TABLE IF EXISTS audit.data_quality_results
""")

conn.execute("""
DROP TABLE IF EXISTS audit.pipeline_execution_log
""")

# =====================================================
# CREATE ETL RUNS TABLE
# =====================================================

print("Creating audit.etl_runs...")

conn.execute("""
CREATE TABLE audit.etl_runs (

    run_id BIGINT,

    run_timestamp TIMESTAMP,

    pipeline_name VARCHAR,

    status VARCHAR,

    rows_processed BIGINT,

    duration_seconds DOUBLE

)
""")

# =====================================================
# CREATE TABLE ROW COUNTS
# =====================================================

print("Creating audit.table_row_counts...")

conn.execute("""
CREATE TABLE audit.table_row_counts (

    snapshot_timestamp TIMESTAMP,

    schema_name VARCHAR,

    table_name VARCHAR,

    row_count BIGINT

)
""")

# =====================================================
# CREATE DATA QUALITY RESULTS
# =====================================================

print("Creating audit.data_quality_results...")

conn.execute("""
CREATE TABLE audit.data_quality_results (

    check_timestamp TIMESTAMP,

    table_name VARCHAR,

    check_name VARCHAR,

    status VARCHAR,

    failed_rows BIGINT

)
""")

# =====================================================
# CREATE PIPELINE EXECUTION LOG
# =====================================================

print("Creating audit.pipeline_execution_log...")

conn.execute("""
CREATE TABLE audit.pipeline_execution_log (

    log_timestamp TIMESTAMP,

    pipeline_name VARCHAR,

    step_name VARCHAR,

    status VARCHAR,

    message VARCHAR

)
""")

# =====================================================
# VALIDATION
# =====================================================

print()
print("Audit Tables Created")

print(
    conn.execute("""
    SELECT
        table_schema,
        table_name
    FROM information_schema.tables
    WHERE table_schema = 'audit'
    ORDER BY table_name
    """).fetchdf()
)

print()
print("ETL Runs Structure")

print(
    conn.execute("""
    DESCRIBE audit.etl_runs
    """).fetchdf()
)

print()
print("Table Row Counts Structure")

print(
    conn.execute("""
    DESCRIBE audit.table_row_counts
    """).fetchdf()
)

print()
print("Data Quality Results Structure")

print(
    conn.execute("""
    DESCRIBE audit.data_quality_results
    """).fetchdf()
)

print()
print("Pipeline Execution Log Structure")

print(
    conn.execute("""
    DESCRIBE audit.pipeline_execution_log
    """).fetchdf()
)

conn.close()

print()
print("Audit Layer Created Successfully")
print("DuckDB connection closed.")