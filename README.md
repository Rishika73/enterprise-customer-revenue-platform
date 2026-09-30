# Enterprise Customer Revenue & Risk Platform

This project is an end-to-end customer revenue and risk analytics platform built using **AWS S3, Snowflake, dbt, Apache Airflow, GitHub Actions, and Tableau**.

I built it to work through the complete data flow instead of creating only a dashboard. The project starts with raw customer data, loads it into Snowflake, transforms and tests it with dbt, handles pipeline orchestration with Airflow, and uses the final analytics data for reporting in Tableau.

The main focus is customer revenue, health score, churn risk, and renewal risk.

## Live Dashboard

The final reporting layer is available as an interactive Tableau dashboard.

**[View the Customer Revenue & Risk Dashboard](https://public.tableau.com/app/profile/rishika.reddy.thumma/viz/CustomerRevenueRiskDashboard/Dashboard1)**

![Customer Revenue & Risk Dashboard](docs/customer-revenue-risk-dashboard.png)

The dashboard currently shows:

| Metric | Value |
| --- | ---: |
| Total ARR | $2.91M |
| Average Health Score | 70.25 |
| High-Risk Customers | 2 |
| Average Churn Risk | 32.13% |

The dashboard includes:

- ARR by Region
- ARR by Customer Segment
- Customers by Renewal Risk
- Churn Risk by Customer
- Health Score by Customer

For the risk charts, I used the same colors across the dashboard:

- Red = High risk
- Orange = Medium risk
- Green = Low risk

For customer health scores, I used a red-to-green scale. Customers with lower health scores appear closer to red, while customers with stronger health scores appear green.

## Project Goal

The goal of this project was to build the full data pipeline behind a customer revenue and risk dashboard.

I wanted the project to answer business questions such as:

- What is the total recurring revenue?
- Which region contributes the most ARR?
- Which customer segment contributes the most revenue?
- Which customers have the highest churn risk?
- Which customers have lower health scores?
- How many customers are currently high risk?
- Which customers may need attention before renewal?
- How can customer changes be tracked over time?

Instead of doing all the analysis directly inside Tableau, I built the data pipeline first and kept the reporting layer separate.

## Architecture

The overall flow of the project is:

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
Snowflake Raw Layer
    |
    v
dbt Staging Models
    |
    v
dbt Core Models
    |
    v
Analytics Marts
    |
    +----------------------+
    |                      |
    v                      v
Tableau              Snowflake Streams
Dashboard                  |
                           v
                      Snowflake Tasks
                           |
                           v
                      Audit / CDC Data
```

Other parts of the project support this pipeline:

```text
Apache Airflow  -> Pipeline orchestration
dbt             -> Transformation and testing
GitHub Actions  -> CI/CD checks
Snowflake       -> Storage, processing and security
Tableau         -> Final reporting and visualization
```

## Technology Stack

| Area | Technology |
| --- | --- |
| Cloud Storage | AWS S3 |
| Data Warehouse | Snowflake |
| Data Ingestion | Snowpipe |
| Data Transformation | dbt |
| Workflow Orchestration | Apache Airflow |
| Change Data Processing | Snowflake Streams & Tasks |
| Data Quality | dbt Tests |
| CI/CD | GitHub Actions |
| Security | Snowflake RBAC / Secure Views |
| Visualization | Tableau |
| Languages | SQL, Python |

## Data Ingestion

The pipeline begins with source customer and revenue data.

The files are stored in **AWS S3** and then loaded into **Snowflake**.

I used Snowpipe for the ingestion process so new data can be loaded into the warehouse without manually rebuilding the complete pipeline every time.

The basic ingestion flow is:

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
Snowflake Raw Tables
```

I keep the raw layer separate from transformed data. This gives me a clean copy of the source data before applying transformations or business rules.

## Snowflake Data Warehouse

Snowflake is the main data warehouse for the project.

I organized the data into different logical layers instead of keeping raw and reporting data together.

```text
RAW
 |
 v
STAGING
 |
 v
CORE
 |
 v
MARTS
```

Each layer has a different purpose.

### Raw Layer

The raw layer contains data loaded from the source.

I avoid putting major business logic here because I want this layer to stay close to the original source data.

### Staging Layer

The staging layer prepares raw data for downstream models.

This includes tasks such as:

- Renaming columns
- Standardizing values
- Converting data types
- Handling basic data cleanup
- Preparing fields for downstream joins

### Core Layer

The core layer contains the main reusable business logic.

This is where customer and revenue data can be combined and prepared for analytics.

The core models support information related to:

- Customers
- Revenue
- ARR
- Customer segments
- Customer health
- Churn risk
- Renewal risk

### Mart Layer

The mart layer contains the final reporting-ready datasets.

These models are designed for analytics and are used by the Tableau dashboard.

Keeping these layers separate makes the pipeline easier to understand and troubleshoot.

## dbt Transformations

I use **dbt** to manage the SQL transformation layer.

Instead of creating one large SQL query, I split the transformation logic into smaller models.

The general dbt flow is:

```text
Sources
   |
   v
Staging Models
   |
   v
Core Models
   |
   v
Analytics Marts
```

This makes individual transformations easier to test, reuse, and update.

It also keeps the SQL logic in the repository, so changes can be tracked through Git.

## Data Quality Testing

I added dbt tests to validate important fields and relationships.

The project uses tests such as:

```text
unique
not_null
accepted_values
relationships
```

For example, these tests can help detect:

- Duplicate customer IDs
- Missing required values
- Unexpected risk categories
- Invalid relationships between models
- Data issues introduced during transformation

Running tests as part of the pipeline gives me a way to catch data problems before the final data reaches the reporting layer.

## Historical Customer Tracking

Customer information can change over time.

For example, a customer's segment, status, or other business attributes may not stay the same forever.

To handle this, I included **Slowly Changing Dimension Type 2 (SCD Type 2)** concepts in the project.

Instead of simply replacing the previous record, historical versions can be retained.

A simplified flow looks like this:

```text
Existing Customer Record
          |
          v
Customer Data Changes
          |
          v
Previous Version Retained
          |
          v
New Version Created
```

This makes it possible to analyze both current and historical customer information.

## Snowflake Streams

I used Snowflake Streams to work with changes made to warehouse tables.

A Stream can track changes such as:

- Inserts
- Updates
- Deletes

This is useful when only changed records need to be processed.

Instead of repeatedly processing an entire table, downstream logic can work with the changes captured by the Stream.

## Snowflake Tasks

Snowflake Tasks are used to automate SQL processing.

I combined Streams and Tasks to create a simple incremental processing flow:

```text
Source Table
     |
     v
Snowflake Stream
     |
     v
Snowflake Task
     |
     v
Audit / Downstream Table
```

The Stream identifies changes and the Task processes those changes.

This was useful for understanding how change data can move through a warehouse without requiring a full reload every time.

## Apache Airflow

I use **Apache Airflow** to organize and orchestrate the pipeline.

The Airflow DAG controls the order in which pipeline steps run.

A simplified workflow is:

```text
Start
  |
  v
Load / Validate Data
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
Reporting Data Ready
```

Using Airflow makes dependencies between different steps clear.

For example, the reporting models should not be treated as ready until the required transformations and tests have completed.

## Security and Access Control

I also included Snowflake security concepts in the project.

The main idea is that not every user should automatically have access to every warehouse object.

I worked with role-based access concepts so permissions can be separated based on what a user or workload needs.

The project also includes secure-view concepts for exposing reporting data without requiring direct access to all of the underlying tables.

The basic approach is:

```text
Raw / Internal Data
        |
        v
Transformation Layer
        |
        v
Controlled Reporting View
        |
        v
Analytics User
```

This keeps the reporting layer separate from the internal warehouse structure.

## CI/CD with GitHub Actions

I use GitHub Actions to add automated checks to the repository.

When project changes are pushed, the workflow can validate the project instead of relying only on manual checks.

The general process is:

```text
Code Change
    |
    v
Git Push / Pull Request
    |
    v
GitHub Actions
    |
    +----> Validate
    |
    +----> Run Checks
    |
    +----> Test dbt Changes
    |
    v
Validated Change
```

This gives the project a repeatable process for checking changes before they become part of the main codebase.

## Tableau Dashboard

The final step of the project is the Tableau reporting layer.

I created the **Customer Revenue & Risk Dashboard** to bring the main customer and revenue metrics together in one place.

**[Open the live Tableau dashboard](https://public.tableau.com/app/profile/rishika.reddy.thumma/viz/CustomerRevenueRiskDashboard/Dashboard1)**

### Total ARR

The current dataset contains:

**$2.91M Total ARR**

This gives a quick view of the annual recurring revenue represented in the dataset.

### Average Health Score

The current average customer health score is:

**70.25**

This gives an overall view of customer health across the dataset.

### High-Risk Customers

There are currently:

**2 High-Risk Customers**

This KPI makes it easy to see how many customers may need closer attention.

### Average Churn Risk

The current average churn risk is:

**32.13%**

This gives a portfolio-level view of churn risk.

## ARR by Region

The ARR by Region chart compares recurring revenue across:

- East
- Central
- West
- South

This makes it easy to see how revenue is distributed geographically.

In the current dataset, the East region contributes the highest ARR.

## ARR by Segment

The dashboard also compares ARR across customer segments:

- Enterprise
- Mid-Market
- SMB

This shows how recurring revenue is distributed across different customer groups.

The current data has a large portion of ARR coming from Enterprise customers.

## Customers by Renewal Risk

Customers are grouped into three renewal-risk categories.

| Renewal Risk | Customers |
| --- | ---: |
| High | 2 |
| Medium | 1 |
| Low | 5 |

I used consistent colors for these categories throughout the dashboard:

```text
High    -> Red
Medium  -> Orange
Low     -> Green
```

This makes the risk level easier to understand without having to read every value individually.

## Churn Risk by Customer

The Churn Risk by Customer chart ranks individual customers based on their churn-risk probability.

Higher-risk customers appear at the top of the chart.

The same risk colors are used here:

```text
High Risk    -> Red
Medium Risk  -> Orange
Low Risk     -> Green
```

This makes it easy to identify the customers with the highest churn probability.

## Health Score by Customer

The Health Score by Customer chart shows the relative health of each customer.

The current health scores are:

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

Instead of using the same color for every bar, I used a red-to-green scale.

Lower scores move toward red, middle scores move through orange/yellow, and higher scores move toward green.

This makes weaker and stronger customer health scores easier to identify visually.

## Repository Structure

The repository is organized by the main parts of the project.

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
│   └── customer-revenue-risk-dashboard.png
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

### `.github/workflows`

Contains GitHub Actions workflow files used for CI/CD checks.

### `airflow`

Contains the Airflow DAG and orchestration-related code.

### `customer_revenue_dbt`

Contains the dbt project, including transformation models and related configuration.

### `data`

Contains data used for development and testing.

### `docs`

Contains supporting project documentation and the Tableau dashboard screenshot.

### `scripts`

Contains supporting scripts used by the project.

### `snowflake`

Contains Snowflake SQL used for warehouse setup, ingestion, Streams, Tasks, security, and related objects.

### `tests`

Contains additional project-level tests.

## Main Metrics

The project focuses on a few customer and revenue metrics.

### ARR

Annual Recurring Revenue is used to understand the recurring revenue represented by each customer and across the overall portfolio.

### Health Score

Health Score provides a simple way to compare the current health of customers.

### Churn Risk Probability

Churn Risk Probability represents the estimated churn risk associated with each customer.

### Renewal Risk

Renewal Risk converts customer risk into easier business categories:

```text
High
Medium
Low
```

These metrics are used together rather than looking at revenue or risk separately.

For example, a customer can have meaningful ARR while also having a high churn probability. Looking at both makes the data more useful for customer and revenue analysis.

## What I Learned

The most useful part of this project was connecting the different pieces into one complete workflow.

Working on the project gave me hands-on experience with:

- Loading data from cloud storage into Snowflake
- Organizing warehouse data into different layers
- Building modular SQL transformations with dbt
- Adding automated data-quality tests
- Working with historical customer data
- Using Streams and Tasks for incremental processing
- Orchestrating pipeline steps with Airflow
- Adding CI/CD checks with GitHub Actions
- Working with Snowflake access-control concepts
- Building a business-facing dashboard in Tableau

It also showed me why it is useful to keep ingestion, transformation, testing, and reporting separate.

If something changes in the source data or business logic, having clear layers makes it much easier to find where the change needs to happen.

## Future Improvements

There are several things I can extend from here.

Some of the next improvements I would like to work on are:

- Automated Tableau data refresh
- Pipeline monitoring and alerting
- More dbt data-quality tests
- Revenue forecasting
- Customer Lifetime Value analysis
- Predictive churn modeling
- Additional customer behavior metrics
- Data observability checks
- More automated infrastructure setup
- Cost and warehouse usage monitoring

## Dashboard Link

The published dashboard can be viewed here:

**[Customer Revenue & Risk Dashboard - Tableau Public](https://public.tableau.com/app/profile/rishika.reddy.thumma/viz/CustomerRevenueRiskDashboard/Dashboard1)**

## Author

**Rishika Reddy Thumma**

MS Computer Science  
Data Engineering | Analytics Engineering | Cloud Data Platforms
