with customer_360 as (

    select *
    from {{ ref('mart_customer_360') }}

),

usage as (

    select
        customer_id,
        avg(active_users) as avg_active_users,
        avg(sessions) as avg_sessions,
        avg(api_calls) as avg_api_calls,
        avg(feature_adoption_score) as avg_feature_adoption_score
    from {{ ref('fact_product_usage') }}
    group by customer_id

),

support as (

    select
        customer_id,
        count(*) as total_tickets,
        sum(
            case
                when status <> 'closed' then 1
                else 0
            end
        ) as open_tickets,
        avg(resolution_hours) as avg_resolution_hours,
        avg(satisfaction_score) as avg_satisfaction_score
    from {{ ref('fact_support_events') }}
    group by customer_id

)

select
    c.customer_id,
    c.customer_name,
    c.segment,
    c.region,
    c.annual_contract_value,
    c.mrr,
    c.arr,
    c.next_renewal_date,
    c.health_score,
    c.adoption_score,
    c.support_score,
    c.payment_score,
    c.renewal_risk,
    c.churn_risk_probability,
    u.avg_active_users,
    u.avg_sessions,
    u.avg_api_calls,
    u.avg_feature_adoption_score,
    coalesce(s.total_tickets, 0) as total_tickets,
    coalesce(s.open_tickets, 0) as open_tickets,
    s.avg_resolution_hours,
    s.avg_satisfaction_score
from customer_360 c
left join usage u
    on c.customer_id = u.customer_id
left join support s
    on c.customer_id = s.customer_id
