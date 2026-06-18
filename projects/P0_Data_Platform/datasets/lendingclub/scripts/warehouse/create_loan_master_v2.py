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

print("Creating core.loan_master_v2...")

conn.execute("""
create schema if not exists core;
""")

conn.execute("""
create or replace table core.loan_master_v2 as

select

    loan_id,

    strptime(issue_d, '%b-%Y') as issue_date,

    case
        when earliest_cr_line is not null
        then strptime(earliest_cr_line, '%b-%Y')
        else null
    end as earliest_credit_date,

    case
        when last_pymnt_d is not null
        then strptime(last_pymnt_d, '%b-%Y')
        else null
    end as last_payment_date,

    case
        when next_pymnt_d is not null
        then strptime(next_pymnt_d, '%b-%Y')
        else null
    end as next_payment_date,

    case
        when last_credit_pull_d is not null
        then strptime(last_credit_pull_d, '%b-%Y')
        else null
    end as last_credit_pull_date,

    *

    exclude (
        loan_id,
        issue_d,
        earliest_cr_line,
        last_pymnt_d,
        next_pymnt_d,
        last_credit_pull_d
    )

from core.loan_master
""")

rows = conn.execute("""
select count(*)
from core.loan_master_v2
""").fetchone()[0]

print(f"Rows: {rows:,}")

conn.close()

print("Complete")