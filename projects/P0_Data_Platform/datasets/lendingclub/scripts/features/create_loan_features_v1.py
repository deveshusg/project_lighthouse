from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[6]

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

print("Creating feature schema...")

conn.execute("""
create schema if not exists feature
""")

print("Dropping existing table...")

conn.execute("""
drop table if exists feature.loan_features_v1
""")

print("Creating feature.loan_features_v1...")

conn.execute("""
create table feature.loan_features_v1 as

select

    ------------------------------------------------------------
    -- IDENTIFIERS
    ------------------------------------------------------------

    loan_id,

    ------------------------------------------------------------
    -- DATES
    ------------------------------------------------------------

    issue_date,
    issue_date as origination_date,
    earliest_credit_date,

    extract(year from issue_date) as issue_year,
    extract(quarter from issue_date) as issue_quarter,
    extract(month from issue_date) as issue_month_number,

    strftime(issue_date, '%Y-%m') as issue_year_month,

    datediff(
    'month',
    issue_date,
    current_date
                ) as loan_age_months,
    ------------------------------------------------------------
    -- LOAN ATTRIBUTES
    ------------------------------------------------------------

    loan_amnt,
    funded_amnt,
    funded_amnt_inv,

    term,

    case
        when term like '36%' then 36
        when term like '60%' then 60
        else null
    end as term_months,

    int_rate,
    installment,

    grade,
    sub_grade,
    purpose,
    application_type,

    ------------------------------------------------------------
    -- EMPLOYMENT
    ------------------------------------------------------------

    emp_length,

    case
        when emp_length = '< 1 year' then 0
        when emp_length = '1 year' then 1
        when emp_length = '2 years' then 2
        when emp_length = '3 years' then 3
        when emp_length = '4 years' then 4
        when emp_length = '5 years' then 5
        when emp_length = '6 years' then 6
        when emp_length = '7 years' then 7
        when emp_length = '8 years' then 8
        when emp_length = '9 years' then 9
        when emp_length = '10+ years' then 10
        else null
    end as employment_length_numeric,

    ------------------------------------------------------------
    -- INCOME
    ------------------------------------------------------------

    annual_inc,

    verification_status,

    case
        when verification_status = 'Not Verified'
        then 0
        else 1
    end as verified_income_flag,

    ------------------------------------------------------------
    -- HOME
    ------------------------------------------------------------

    home_ownership,

    case
        when home_ownership in ('OWN', 'MORTGAGE')
        then 1
        else 0
    end as homeowner_flag,

    addr_state,
    zip_code,

    ------------------------------------------------------------
    -- CREDIT HISTORY
    ------------------------------------------------------------

    datediff(
        'month',
        earliest_credit_date,
        issue_date
    ) as credit_history_months,

    round(
        datediff(
            'month',
            earliest_credit_date,
            issue_date
        ) / 12.0,
        2
    ) as credit_history_years,

    ------------------------------------------------------------
    -- FICO
    ------------------------------------------------------------

    fico_range_low,
    fico_range_high,

    (
        fico_range_low +
        fico_range_high
    ) / 2.0 as fico_midpoint,

    last_fico_range_low,
    last_fico_range_high,

    (
        last_fico_range_low +
        last_fico_range_high
    ) / 2.0 as last_fico_midpoint,

    (
        (
            last_fico_range_low +
            last_fico_range_high
        ) / 2.0
    )
    -
    (
        (
            fico_range_low +
            fico_range_high
        ) / 2.0
    ) as fico_change,

    ------------------------------------------------------------
    -- DEBT BURDEN
    ------------------------------------------------------------

    dti,

    loan_amnt / nullif(annual_inc,0)
        as loan_to_income_ratio,

    (installment * 12)
        / nullif(annual_inc,0)
        as installment_to_income_ratio,

    revol_bal
        / nullif(annual_inc,0)
        as revolving_balance_to_income,

    total_bal_ex_mort
        / nullif(annual_inc,0)
        as total_balance_to_income,
    ------------------------------------------------------------
    -- REVOLVING CREDIT
    ------------------------------------------------------------

    revol_bal,
    revol_util,

    case
        when revol_util >= 80
        then 1
        else 0
    end as high_utilization_flag,

    case
        when revol_util < 20 then 'LOW'
        when revol_util < 50 then 'MEDIUM'
        when revol_util < 80 then 'HIGH'
        else 'VERY_HIGH'
    end as utilization_band,
    ------------------------------------------------------------
    -- ACCOUNTS
    ------------------------------------------------------------

    open_acc,
    total_acc,
    mort_acc,

    pub_rec,
    pub_rec_bankruptcies,
    tax_liens,

    ------------------------------------------------------------
    -- DELINQUENCY
    ------------------------------------------------------------

    delinq_2yrs,
    acc_now_delinq,

    mths_since_last_delinq,
    mths_since_last_major_derog,

    ------------------------------------------------------------
    -- INQUIRIES
    ------------------------------------------------------------

    inq_last_6mths,
    inq_last_12m,

    case
        when inq_last_6mths >= 2
        then 1
        else 0
    end as recent_inquiry_flag,

    ------------------------------------------------------------
    -- UTILIZATION
    ------------------------------------------------------------

    all_util,
    il_util,
    bc_util,
    percent_bc_gt_75,

    ------------------------------------------------------------
    -- BALANCES
    ------------------------------------------------------------

    tot_cur_bal,
    avg_cur_bal,
    total_bal_ex_mort,
    total_rev_hi_lim,
    tot_hi_cred_lim,

    ------------------------------------------------------------
    -- TRADELINES
    ------------------------------------------------------------

    num_actv_bc_tl,
    num_actv_rev_tl,
    num_bc_sats,
    num_bc_tl,
    num_il_tl,
    num_op_rev_tl,
    num_rev_accts,
    num_sats,

    ------------------------------------------------------------
    -- FLAGS
    ------------------------------------------------------------

    case
        when total_acc <= 5
        then 1
        else 0
    end as thin_file_flag,

    case
        when delinq_2yrs > 0
             or pub_rec > 0
        then 1
        else 0
    end as derogatory_history_flag,

    case
        when pub_rec_bankruptcies > 0
        then 1
        else 0
    end as bankruptcy_flag,

    case
        when mort_acc > 0
        then 1
        else 0
    end as mortgage_flag,

    case
        when application_type <> 'Individual'
        then 1
        else 0
    end as joint_application_flag,

    case
        when dti >= 30
        then 1
        else 0
    end as high_dti_flag,

    ------------------------------------------------------------
    -- TARGET
    ------------------------------------------------------------

    case
        when loan_status in (
            'Charged Off',
            'Default',
            'Late (31-120 days)',
            'Does not meet the credit policy. Status:Charged Off'
        )
        then 1
        else 0
    end as default_flag

from core.loan_master_v2
""")

print(
    conn.execute("""
    select count(*)
    from feature.loan_features_v1
    """).fetchdf()
)

print(
    conn.execute("""
    describe feature.loan_features_v1
    """).fetchdf()
)

conn.close()

print("Complete")