select
    subscription_id,
    customer_id,
    product_id,
    plan_name,
    start_date,
    end_date,
    renewal_date,
    billing_frequency,
    monthly_recurring_revenue,
    annual_recurring_revenue,
    status,
    updated_at,
    ingestion_timestamp
from {{ source('raw', 'subscriptions') }}
