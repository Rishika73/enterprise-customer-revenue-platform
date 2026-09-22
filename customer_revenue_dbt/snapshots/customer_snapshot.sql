{% snapshot customer_snapshot %}

{{
    config(
        target_schema='CORE',
        unique_key='customer_id',
        strategy='timestamp',
        updated_at='updated_at',
        invalidate_hard_deletes=True
    )
}}

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
    updated_at
from {{ source('raw', 'customers') }}

{% endsnapshot %}
