import duckdb

from pathlib import Path

ROOT = Path(r"D:\project_lighthouse")

DB_PATH = (
    ROOT
    / "projects"
    / "P0_Data_Platform"
    / "datasets"
    / "lendingclub"
    / "data"
    / "warehouse"
    / "duckdb"
    / "lendingclub.duckdb"
)

conn = duckdb.connect(str(DB_PATH))

print("Creating clean.lendingclub_clean ...")

conn.execute(
    """
    create schema if not exists clean;
    """
)

conn.execute(
    """
    create or replace table clean.lendingclub_clean as

    select
        *

    exclude (
        member_id,
        policy_code
    )

    from raw.lendingclub_raw

    where try_cast(id as bigint) is not null
    """
)

results = conn.execute(
    """
    select count(*) as rows
    from clean.lendingclub_clean
    """
).fetchdf()

print(results)

conn.close()

print("Complete")