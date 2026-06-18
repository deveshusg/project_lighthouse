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
drop table if exists mart.portfolio_summary
""")

print("Creating mart.portfolio_summary ...")

conn.execute("""
create table mart.portfolio_summary as

select

    cast(issue_year_month || '-01' as date) as issue_month,

    grade,

    addr_state,

    purpose,

    count(*) as loan_count,

    sum(loan_amnt) as total_loan_amount,

    avg(loan_amnt) as avg_loan_amount,

    avg(int_rate) as avg_interest_rate,

    avg(fico_midpoint) as avg_fico,

    avg(dti) as avg_dti,

    avg(loan_to_income_ratio)
        as avg_loan_to_income_ratio,

    avg(revol_util)
        as avg_revolving_utilization_ratio,

    sum(default_flag) as default_count,
    
    sum(default_flag * loan_amnt)
    as defaulted_loan_amount,

    round(
        100.0 * avg(default_flag),
        2
    ) as default_rate,

    sum(high_utilization_flag)
        as high_utilization_count,

    round(
        100.0 * avg(high_utilization_flag),
        2
    ) as high_utilization_rate

from feature.loan_features_v1

group by

    cast(issue_year_month || '-01' as date),
    grade,
    addr_state,
    purpose
""")

print()

print("Mart Row Count")

print(
    conn.execute("""
    select
        count(*) as rows
    from mart.portfolio_summary
    """).fetchdf()
)

print()

print("Mart Grain Validation")

print(
    conn.execute("""
    select

        count(*) as rows,

        count(
            distinct concat(
                cast(issue_month as varchar),
                '|',
                grade,
                '|',
                addr_state,
                '|',
                purpose
            )
        ) as unique_rows

    from mart.portfolio_summary
    """).fetchdf()
)

print()

print("Loan Count Reconciliation")

print(
    conn.execute("""
    select

        (
            select count(*)
            from feature.loan_features_v1
        ) as feature_rows,

        (
            select sum(loan_count)
            from mart.portfolio_summary
        ) as mart_loan_count
    """).fetchdf()
)

print()

print("Table Structure")

print(
    conn.execute("""
    describe mart.portfolio_summary
    """).fetchdf()
)

print()

print("Sample Records")

print(
    conn.execute("""
    select *
    from mart.portfolio_summary
    order by issue_month desc
    limit 20
    """).fetchdf()
)

print()

print("Complete")