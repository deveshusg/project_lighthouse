from pathlib import Path

import duckdb


# --------------------------------------------------
# PATHS
# --------------------------------------------------

ROOT = Path(
    r"D:\Project_Lighthouse"
)

DATASET_ROOT = (
    ROOT
    / "projects"
    / "P0_Data_Platform"
    / "datasets"
    / "lendingclub"
)

CSV_PATH = (
    DATASET_ROOT
    / "data"
    / "raw"
    / "accepted_2007_to_2018Q4.csv"
)

DB_PATH = (
    DATASET_ROOT
    / "data"
    / "warehouse"
    / "duckdb"
    / "lendingclub.duckdb"
)

# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

if not CSV_PATH.exists():
    raise FileNotFoundError(
        f"CSV not found:\n{CSV_PATH}"
    )

# --------------------------------------------------
# CONNECT
# --------------------------------------------------

conn = duckdb.connect(
    str(DB_PATH)
)

# --------------------------------------------------
# SCHEMAS
# --------------------------------------------------

conn.execute(
    """
    create schema if not exists raw;
    """
)

# --------------------------------------------------
# LOAD
# --------------------------------------------------

print("Loading LendingClub Raw Dataset...")
print()

conn.execute(
    f"""
    create or replace table raw.lendingclub_raw as

    select *

    from read_csv_auto(
        '{CSV_PATH}',
        sample_size=-1,
        ignore_errors=true
    )
    """
)

# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

row_count = conn.execute(
    """
    select count(*)
    from raw.lendingclub_raw
    """
).fetchone()[0]

column_count = conn.execute(
    """
    select count(*)
    from information_schema.columns
    where table_schema='raw'
      and table_name='lendingclub_raw'
    """
).fetchone()[0]

print(f"Rows    : {row_count:,}")
print(f"Columns : {column_count:,}")

conn.close()

print()
print("Load Complete")