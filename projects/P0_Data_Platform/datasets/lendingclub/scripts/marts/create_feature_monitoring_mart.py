
from pathlib import Path
import duckdb
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

DB_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "warehouse"
    / "duckdb"
    / "lendingclub.duckdb"
)

conn = duckdb.connect(str(DB_PATH))

conn.execute("create schema if not exists mart")
conn.execute("drop table if exists mart.feature_monitoring")

conn.execute('''
create table mart.feature_monitoring as
select
    issue_year,
    count(*) as loan_count,
    avg(fico_midpoint) as avg_fico,
    avg(dti) as avg_dti,
    avg(loan_to_income_ratio) as avg_loan_to_income_ratio,
    avg(revol_util) as avg_revol_util,
    avg(credit_history_years) as avg_credit_history_years,
    round(100.0 * avg(default_flag),2) as default_rate
from feature.loan_features_v1
group by issue_year
order by issue_year
''')

print(conn.execute("select * from mart.feature_monitoring").fetchdf())
