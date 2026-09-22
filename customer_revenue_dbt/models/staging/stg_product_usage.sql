select
    usage_id,
    customer_id,
    product_id,
    usage_date,
    active_users,
    sessions,
    api_calls,
    storage_gb,
    feature_adoption_score,
    ingestion_timestamp
from {{ source('raw', 'product_usage') }}
