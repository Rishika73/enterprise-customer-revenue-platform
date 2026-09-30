# Enterprise Customer Revenue & Risk Platform

I built this project to create an end-to-end customer revenue analytics pipeline, starting from raw customer data and ending with a dashboard that makes revenue, churn risk, and customer health easier to understand.

The main stack is **Snowflake, dbt, Apache Airflow, AWS S3, GitHub Actions, and Tableau**.

The project covers data ingestion, transformation, testing, orchestration, incremental processing, access control, and visualization.

## Dashboard

I built a Tableau dashboard on top of the final analytics dataset to show the main revenue and customer-risk metrics.

**[View the live Tableau dashboard](https://public.tableau.com/app/profile/rishika.reddy.thumma/viz/CustomerRevenueRiskDashboard/Dashboard1)**

Current dashboard metrics:

| Metric | Value |
| --- | ---: |
| Total ARR | $2.91M |
| Average Health Score | 70.25 |
| High-Risk Customers | 2 |
| Average Churn Risk | 32.13% |

The dashboard includes:

- ARR by region
- ARR by customer segment
- Customers by renewal risk
- Churn risk by customer
- Health score by customer

For the risk charts, I used consistent colors so that high-risk customers are easy to identify. Customer health scores use a red-to-green scale, with lower scores shown in red/orange and stronger scores shown in green.

---

## Why I Built This

I wanted this project to be more than a set of SQL queries or an isolated dashboard.

The idea was to build a small version of the kind of data platform a company could use to answer questions like:

- Where is most of our recurring revenue coming from?
- Which customer segments contribute the most ARR?
- Which customers have the highest churn risk?
- Which customers have low health scores?
- How many customers are currently considered high risk?
- How can customer changes be tracked over time?

That meant building the full flow from ingestion to the reporting layer rather than starting directly in Tableau.

---

## Architecture

```text
Source Data
    |
    v
  AWS S3
    |
    v
 Snowpipe
    |
    v
Snowflake RAW
    |
    v
dbt Staging
    |
    v
 dbt Core
    |
    v
Analytics Marts
    |
    +--------------------+
    |                    |
    v                    v
 Tableau          Streams / Tasks
 Dashboard         CDC & Auditing


Orchestration : Apache Airflow
Testing       : dbt
CI/CD         : GitHub Actions
Security      : Snowflake RBAC / Secure Views
```

---

## Tech Stack

| Area | Technology |
| --- | --- |
| Storage | AWS S3 |
| Data Warehouse | Snowflake |
| Ingestion | Snowpipe |
| Transformation | dbt |
| Orchestration | Apache Airflow |
| Incremental Processing | Snowflake Streams & Tasks |
| Data Quality | dbt tests |
| CI/CD | GitHub Actions |
| Security | Snowflake RBAC, secure views |
| Visualization | Tableau |
| Languages | SQL, Python |

---

## Data Flow

### 1. Ingestion

Raw customer and revenue data is staged in AWS S3 and loaded into Snowflake.

I used Snowpipe to make the ingestion process incremental instead of treating every load as a full refresh.

The raw layer is kept separate from the transformation layer so that source data can be preserved before business logic is applied.

### 2. Transformation with dbt

I organized the dbt models into logical layers.

```text
Raw
 |
 v
Staging
 |
 v
Core
 |
 v
Marts
```

The **staging layer** handles cleanup and standardization.

The **core layer** contains reusable business logic around customers, revenue, churn, health scores, and renewal risk.

The **mart layer** contains the final datasets used for reporting and Tableau.

This keeps the transformation logic modular instead of putting everything into one large SQL query.

### 3. Data Quality

I added dbt tests around important fields and relationships.

The project uses checks such as:

- `unique`
- `not_null`
- `accepted_values`
- `relationships`

These tests help catch duplicate IDs, missing values, unexpected categories, and broken relationships before the data reaches the reporting layer.

### 4. Historical Tracking

For customer attributes that can change over time, I included SCD Type 2-style historical tracking.

Instead of only keeping the latest customer state, this approach preserves previous versions so historical changes can still be analyzed.

### 5. Incremental Processing

I used Snowflake Streams and Tasks for change-data processing.

Streams capture changes to the underlying data, while Tasks can process those changes into downstream or audit tables.

```text
Source Table
     |
     v
   Stream
     |
     v
    Task
     |
     v
Audit / Downstream Table
```

This avoids unnecessarily reprocessing the complete dataset when only a subset of records has changed.

### 6. Orchestration

Apache Airflow is used to coordinate the pipeline.

A simplified workflow looks like:

```text
Load Data
    |
    v
Run dbt Models
    |
    v
Run dbt Tests
    |
    v
Build Analytics Models
    |
    v
Ready for Reporting
```

This gives the different pipeline steps clear dependencies and makes the workflow easier to manage.

---

## Security

I also wanted the project to include some warehouse security rather than treating security as something separate from data engineering.

The Snowflake setup includes role-based access concepts and secure views so that access to analytics data can be controlled based on the user or role.

The goal is to expose only the data needed for a particular use case instead of giving every consumer unrestricted access to the underlying tables.

---

## CI/CD

GitHub Actions is used for automated validation.

The workflow is intended to catch problems with project changes before they are merged into the main branch.

```text
Code Change
    |
    v
GitHub Push / Pull Request
    |
    v
GitHub Actions
    |
    +--> Validate
    +--> Test
    +--> Check dbt changes
    |
    v
Ready to Merge
```

---

## Tableau Dashboard

The final dashboard focuses on a few metrics that would be useful to a customer-success or revenue team.

### ARR by Region

This shows how recurring revenue is distributed across East, Central, West, and South regions.

### ARR by Segment

Customers are grouped into:

- Enterprise
- Mid-Market
- SMB

This makes it easy to see which customer segment contributes most of the recurring revenue.

### Renewal Risk

Customers are classified into three groups:

| Renewal Risk | Customers |
| --- | ---: |
| High | 2 |
| Medium | 1 |
| Low | 5 |

### Churn Risk by Customer

Customers are ranked by churn probability.

I used:

- Red for high risk
- Orange for medium risk
- Green for low risk

This makes the customers that need attention visible immediately.

### Health Score by Customer

The health-score chart uses a red-to-green scale instead of a single bar color.

| Customer | Health Score |
| --- | ---: |
| C007 | 86 |
| C003 | 82 |
| C005 | 79 |
| C008 | 76 |
| C006 | 74 |
| C001 | 62 |
| C004 | 55 |
| C002 | 48 |

Higher scores move toward green and lower scores move toward red.

---

## Repository Structure

```text
enterprise-customer-revenue-platform/
|
├── .github/
│   └── workflows/
│
├── airflow/
│
├── customer_revenue_dbt/
│
├── data/
│
├── docs/
│
├── scripts/
│
├── snowflake/
│
├── tests/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

The repository is separated by responsibility so that Snowflake SQL, dbt transformations, Airflow orchestration, tests, and supporting scripts do not all live in the same place.

---

## What I Learned

The most useful part of this project was connecting the individual tools into one workflow.

Building a dbt model or a Tableau chart by itself is straightforward. The more interesting part was making ingestion, transformations, testing, orchestration, incremental processing, security, CI/CD, and visualization work as parts of the same platform.

It also reinforced why separating raw, staging, core, and reporting layers matters. Changes are much easier to debug when each layer has a clear responsibility.

---

## Possible Next Steps

There are a few things I would like to add next:

- Automated dashboard refreshes
- Pipeline monitoring and alerting
- More extensive dbt tests
- Revenue forecasting
- Customer lifetime value metrics
- A predictive churn model
- Data observability checks
- Infrastructure as Code for more of the environment

---

## Live Dashboard

**[Customer Revenue & Risk Dashboard on Tableau Public](https://public.tableau.com/app/profile/rishika.reddy.thumma/viz/CustomerRevenueRiskDashboard/Dashboard1)**

---

## Author

**Rishika Reddy Thumma**

MS Computer Science  
Data Engineering | Analytics Engineering | Cloud Data Platforms
