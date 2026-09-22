select
    transaction_id,
    customer_id,
    subscription_id,
    transaction_date,
    transaction_type,
    amount,
    currency,
    payment_status,
    payment_method,
    ingestion_timestamp
from {{ source('raw', 'transactions') }}
