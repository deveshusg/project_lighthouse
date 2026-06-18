# Project Lighthouse Constitution v1.0

## Status

Approved

---

# 1. Purpose

Project Lighthouse is a long-term credit risk analytics, data science, and data platform portfolio designed to demonstrate end-to-end capabilities across:

* Data Engineering
* Analytics Engineering
* Credit Risk Analytics
* Statistical Analysis
* Machine Learning
* Risk Modeling
* Portfolio Management
* Business Communication

The project serves two simultaneous objectives:

1. Learning Platform
2. Professional Portfolio

Every design decision must support at least one of these objectives.

---

# 2. Vision

To build a reusable, multi-dataset, enterprise-style analytics platform that demonstrates the complete lifecycle of transforming raw financial data into business insights, analytical assets, and predictive models.

The platform must be:

* Understandable by beginners
* Valuable for learning
* Reproducible from scratch
* Recruiter friendly
* Interview friendly
* Expandable to additional datasets
* Governed through documented standards

---

# 3. Scope

## Current Scope

Implemented Dataset:

* LendingClub

Implemented Project:

* P0_Data_Platform

---

## Future Scope

Planned Projects:

* P1_Underwriting
* P2_Portfolio_Monitoring
* P3_Collections
* P4_Recovery
* P5_IFRS9
* P6_Fraud
* P7_Executive_Risk

These projects are planned but not implemented.

---

# 4. Guiding Principles

## Principle 1

Business understanding precedes modeling.

---

## Principle 2

Metadata precedes feature engineering.

---

## Principle 3

Governance precedes automation.

---

## Principle 4

Reproducibility precedes convenience.

---

## Principle 5

Clarity precedes abstraction.

---

## Principle 6

One task equals one objective.

---

## Principle 7

One notebook equals one objective.

---

## Principle 8

Raw data is immutable.

---

## Principle 9

Every major decision must be documented.

---

## Principle 10

Future datasets must follow approved standards.

---

# 5. Repository Architecture

The approved repository architecture is defined by the Decision Register and Architecture Decision Log.

At a high level:

```text
Project Lighthouse

├── Program Assets
├── Documentation
├── Deliverables
└── Projects

    ├── P0_Data_Platform
    ├── P1_Underwriting
    ├── P2_Portfolio_Monitoring
    ├── P3_Collections
    ├── P4_Recovery
    ├── P5_IFRS9
    ├── P6_Fraud
    └── P7_Executive_Risk
```

---

# 6. Multi-Dataset Strategy

The platform is designed to support multiple datasets.

Current dataset:

* LendingClub

Future datasets:

* Home Credit
* German Credit
* Other public or proprietary datasets

All datasets must reside under:

```text
P0_Data_Platform/datasets
```

Every dataset must follow the approved lifecycle.

---

# 7. Data Lifecycle

Every dataset must follow the same lifecycle:

```text
Raw
 ↓
Clean
 ↓
Core
 ↓
Marts
 ↓
Features
 ↓
Modeling
 ↓
Exports
```

No dataset may bypass lifecycle stages without documented approval.

---

# 8. Storage Architecture

Approved storage architecture:

```text
CSV
 ↓
Parquet
 ↓
DuckDB
```

Technology roles:

| Technology | Role              |
| ---------- | ----------------- |
| CSV        | Raw Source        |
| Parquet    | Canonical Storage |
| DuckDB     | Analytics Engine  |
| Excel      | Export Format     |
| PDF        | Reporting Format  |

---

# 9. Warehouse Architecture

Approved warehouse architecture:

```text
Raw
 ↓
Clean
 ↓
Core Warehouse
 ↓
Data Marts
 ↓
EDA
 ↓
Feature Store
 ↓
Modeling
```

Warehouse modeling standard:

* Star Schema

---

# 10. Data Mart Strategy

Approved marts:

* Underwriting Mart
* Portfolio Mart
* Collections Mart
* Recovery Mart
* Executive Mart

Additional marts require documented justification.

---

# 11. Metadata Framework

Every dataset must maintain:

* Business Process
* Data Dictionary
* KPI Dictionary
* Target Definition
* Leakage Registry
* Feature Catalog
* Lineage Documentation

Metadata is mandatory.

No modeling work may begin before metadata completion.

---

# 12. Notebook Framework

Rules:

* One notebook equals one objective.
* Fully reproducible.
* Version controlled.
* Output artifacts preserved.
* Stored within approved lifecycle folders.

Naming convention:

```text
NB_TXXXX_Name.ipynb
```

Example:

```text
NB_T0060_Univariate_EDA.ipynb
```

---

# 13. Script Framework

Scripts are organized by lifecycle:

```text
acquisition
cleaning
warehouse
marts
features
modeling
utilities
```

Naming convention:

```text
verb_dataset_object.py
```

Example:

```text
build_lendingclub_clean.py
```

---

# 14. Governance Framework

Governance consists of:

* Constitution
* Decision Register
* Architecture Decisions
* Roadmap
* Standards
* Lessons Learned

All major changes require documentation.

---

# 15. Decision Hierarchy

In case of conflict:

```text
Constitution
    ↓
Architecture Decisions
    ↓
Decision Register
    ↓
Standards
    ↓
Roadmap
    ↓
Implementation
```

Higher levels take precedence.

---

# 16. Phase Completion Criteria

A phase is complete only when:

1. All tasks completed.
2. Deliverables produced.
3. Acceptance criteria satisfied.
4. Phase review completed.
5. Lessons learned documented.

---

# 17. Task Governance

Task structure:

* One Task
* One Objective
* One Deliverable

Task IDs follow:

```text
T0000
through
T0349
```

Dependencies are mandatory.

Hard dependencies apply unless explicitly waived.

---

# 18. Learning Philosophy

Project Lighthouse is intended to be:

* A learning repository
* A portfolio repository
* A reference repository

Learning outcomes must be documented alongside technical outputs.

Mistakes, assumptions, trade-offs, and improvements should be captured throughout the project lifecycle.

---

# 19. Amendment Process

Changes to this Constitution require:

1. Documented proposal.
2. Architecture review.
3. Decision Register update.
4. Architecture Decision Log update.
5. Approval record.

---

# 20. Ratification

This Constitution is the governing document of Project Lighthouse.

All future projects, datasets, standards, roadmaps, and implementations must comply with this Constitution unless formally amended.
