CREATE WAREHOUSE IF NOT EXISTS CUSTOMER_REVENUE_WH
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE;

CREATE DATABASE IF NOT EXISTS CUSTOMER_REVENUE_DB;

CREATE SCHEMA IF NOT EXISTS CUSTOMER_REVENUE_DB.RAW;
CREATE SCHEMA IF NOT EXISTS CUSTOMER_REVENUE_DB.STAGING;
CREATE SCHEMA IF NOT EXISTS CUSTOMER_REVENUE_DB.CORE;
CREATE SCHEMA IF NOT EXISTS CUSTOMER_REVENUE_DB.MARTS;

USE WAREHOUSE CUSTOMER_REVENUE_WH;
USE DATABASE CUSTOMER_REVENUE_DB;
USE SCHEMA RAW;

CREATE TABLE IF NOT EXISTS CUSTOMERS (
    customer_id VARCHAR,
    customer_name VARCHAR,
    industry VARCHAR,
    segment VARCHAR,
    region VARCHAR,
    country VARCHAR,
    employee_count NUMBER,
    annual_contract_value NUMBER(18,2),
    account_owner_id VARCHAR,
    created_at TIMESTAMP_NTZ,
    updated_at TIMESTAMP_NTZ,
    ingestion_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE IF NOT EXISTS ACCOUNT_OWNERS (
    account_owner_id VARCHAR,
    account_owner_name VARCHAR,
    team VARCHAR,
    region VARCHAR,
    email VARCHAR,
    ingestion_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE IF NOT EXISTS PRODUCTS (
    product_id VARCHAR,
    product_name VARCHAR,
    product_category VARCHAR,
    plan_tier VARCHAR,
    monthly_list_price NUMBER(18,2),
    active_flag BOOLEAN,
    ingestion_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE IF NOT EXISTS SUBSCRIPTIONS (
    subscription_id VARCHAR,
    customer_id VARCHAR,
    product_id VARCHAR,
    plan_name VARCHAR,
    start_date DATE,
    end_date DATE,
    renewal_date DATE,
    billing_frequency VARCHAR,
    monthly_recurring_revenue NUMBER(18,2),
    annual_recurring_revenue NUMBER(18,2),
    status VARCHAR,
    updated_at TIMESTAMP_NTZ,
    ingestion_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE IF NOT EXISTS TRANSACTIONS (
    transaction_id VARCHAR,
    customer_id VARCHAR,
    subscription_id VARCHAR,
    transaction_date TIMESTAMP_NTZ,
    transaction_type VARCHAR,
    amount NUMBER(18,2),
    currency VARCHAR,
    payment_status VARCHAR,
    payment_method VARCHAR,
    ingestion_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE IF NOT EXISTS PRODUCT_USAGE (
    usage_id VARCHAR,
    customer_id VARCHAR,
    product_id VARCHAR,
    usage_date DATE,
    active_users NUMBER,
    sessions NUMBER,
    api_calls NUMBER,
    storage_gb NUMBER(18,2),
    feature_adoption_score NUMBER(5,2),
    ingestion_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE IF NOT EXISTS SUPPORT_TICKETS (
    ticket_id VARCHAR,
    customer_id VARCHAR,
    created_at TIMESTAMP_NTZ,
    closed_at TIMESTAMP_NTZ,
    priority VARCHAR,
    status VARCHAR,
    category VARCHAR,
    assigned_team VARCHAR,
    resolution_hours NUMBER(18,2),
    satisfaction_score NUMBER(5,2),
    ingestion_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE IF NOT EXISTS ACCOUNT_HEALTH (
    health_id VARCHAR,
    customer_id VARCHAR,
    score_date DATE,
    health_score NUMBER,
    adoption_score NUMBER,
    support_score NUMBER,
    payment_score NUMBER,
    renewal_risk VARCHAR,
    churn_risk_probability NUMBER(5,4),
    ingestion_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
