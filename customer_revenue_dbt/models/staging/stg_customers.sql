select
    customer_id,
    customer_name,
    industry,
    segment,
    region,
    country,
    employee_count,
    annual_contract_value,
    account_owner_id,
    created_at,
    updated_at,
    ingestion_timestamp
from {{ source('raw', 'customers') }}
