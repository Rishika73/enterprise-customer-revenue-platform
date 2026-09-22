select
    ticket_id,
    customer_id,
    created_at,
    closed_at,
    priority,
    status,
    category,
    assigned_team,
    resolution_hours,
    satisfaction_score,
    ingestion_timestamp
from {{ ref('stg_support_tickets') }}
