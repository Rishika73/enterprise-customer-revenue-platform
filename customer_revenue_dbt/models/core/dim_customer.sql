select
    c.customer_id,
    c.customer_name,
    c.industry,
    c.segment,
    c.region,
    c.country,
    c.employee_count,
    c.annual_contract_value,
    c.account_owner_id,
    ao.account_owner_name,
    ao.email as account_owner_email,
    c.created_at,
    c.updated_at,
    c.ingestion_timestamp
from {{ ref('stg_customers') }} c
left join {{ ref('stg_account_owners') }} ao
    on c.account_owner_id = ao.account_owner_id
