with customers as (

    select *
    from {{ ref('dim_customer') }}

),

subscriptions as (

    select
        customer_id,
        sum(monthly_recurring_revenue) as mrr,
        sum(annual_recurring_revenue) as arr,
        min(renewal_date) as next_renewal_date
    from {{ ref('stg_subscriptions') }}
    where status = 'active'
    group by customer_id

),

health as (

    select
        customer_id,
        score_date,
        health_score,
        adoption_score,
        support_score,
        payment_score,
        renewal_risk,
        churn_risk_probability
    from {{ ref('stg_account_health') }}

)

select
    c.customer_id,
    c.customer_name,
    c.industry,
    c.segment,
    c.region,
    c.country,
    c.annual_contract_value,
    c.account_owner_name,
    s.mrr,
    s.arr,
    s.next_renewal_date,
    h.score_date,
    h.health_score,
    h.adoption_score,
    h.support_score,
    h.payment_score,
    h.renewal_risk,
    h.churn_risk_probability
from customers c
left join subscriptions s
    on c.customer_id = s.customer_id
left join health h
    on c.customer_id = h.customer_id
