from pathlib import Path
import duckdb

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

print("Creating core.loan_master...")

conn.execute("""
create schema if not exists core;
""")

conn.execute("""
create or replace table core.loan_master as

select

    try_cast(id as bigint) as loan_id,

    * exclude(id)

from clean.lendingclub_clean
""")

row_count = conn.execute("""
select count(*)
from core.loan_master
""").fetchone()[0]

print(f"Rows: {row_count:,}")

conn.close()

print("Complete")