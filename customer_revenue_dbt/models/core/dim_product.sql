select
    product_id,
    product_name,
    product_category,
    plan_tier,
    monthly_list_price,
    active_flag,
    ingestion_timestamp
from {{ ref('stg_products') }}
