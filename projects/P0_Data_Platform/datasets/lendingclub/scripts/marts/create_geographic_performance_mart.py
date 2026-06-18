from pathlib import Path

import duckdb
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", None)

DB_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "warehouse"
    / "duckdb"
    / "lendingclub.duckdb"
)

conn = duckdb.connect(str(DB_PATH))

print("Creating mart schema...")

conn.execute("""
create schema if not exists mart
""")

print("Dropping existing table...")

conn.execute("""
drop table if exists mart.geographic_performance
""")

print("Creating mart.geographic_performance ...")

conn.execute("""
create table mart.geographic_performance as

select

    addr_state,

    count(*) as loan_count,

    sum(loan_amnt) as total_loan_amount,

    avg(loan_amnt) as avg_loan_amount,

    avg(int_rate) as avg_interest_rate,

    avg(fico_midpoint) as avg_fico,

    avg(dti) as avg_dti,

    avg(credit_history_years) as avg_credit_history_years,

    avg(loan_to_income_ratio) as avg_loan_to_income_ratio,

    avg(revol_util) as avg_revolving_utilization,

    sum(default_flag) as default_count,

    round(
        100.0 * avg(default_flag),
        2
    ) as default_rate,

    sum(high_utilization_flag) as high_utilization_count,

    round(
        100.0 * avg(high_utilization_flag),
        2
    ) as high_utilization_rate

from feature.loan_features_v1

where addr_state is not null

group by addr_state

order by loan_count desc
""")

print()

print("Mart Row Count")
print(
    conn.execute("""
    select count(*) as rows
    from mart.geographic_performance
    """).fetchdf()
)

print()

print("Sample Records")
print(
    conn.execute("""
    select *
    from mart.geographic_performance
    order by loan_count desc
    limit 20
    """).fetchdf()
)

print("Complete")
