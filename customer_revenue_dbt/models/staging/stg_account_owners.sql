select
    account_owner_id,
    account_owner_name,
    region,
    email,
    ingestion_timestamp
from {{ source('raw', 'account_owners') }}
