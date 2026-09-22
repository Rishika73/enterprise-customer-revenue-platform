select
    health_id,
    customer_id,
    score_date,
    health_score,
    adoption_score,
    support_score,
    payment_score,
    renewal_risk,
    churn_risk_probability,
    ingestion_timestamp
from {{ source('raw', 'account_health') }}
