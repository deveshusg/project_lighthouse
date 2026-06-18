# LendingClub Clean Layer Specification v1

## Source

raw.lendingclub_raw

## Target

clean.lendingclub_clean

## Grain

1 row = 1 loan

## Primary Key

id

## Cleaning Rules

### CLN001

Remove footer records.

Condition:

try_cast(id as bigint) is not null

### CLN002

Remove member_id.

Reason:

100% null.

### CLN003

Remove policy_code.

Reason:

Single value across entire dataset.

### CLN004

Convert date columns.

issue_d
earliest_cr_line
last_pymnt_d
next_pymnt_d
last_credit_pull_d
hardship_start_date
hardship_end_date
payment_plan_start_date
settlement_date
debt_settlement_flag_date

### CLN005

Preserve sparse business columns.

Hardship
Settlement
Joint Applicant

### CLN006

No imputation.

Imputation belongs to feature engineering.

### CLN007

Maintain original loan grain.