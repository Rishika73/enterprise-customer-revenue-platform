with transactions as (

    select *
    from {{ ref('fact_transactions') }}

),

subscriptions as (

    select *
    from {{ ref('stg_subscriptions') }}

),

monthly_transactions as (

    select
        date_trunc('month', transaction_date) as revenue_month,
        count(distinct customer_id) as active_customers,
        count(*) as transaction_count,
        sum(amount) as total_revenue,
        sum(
            case
                when payment_status = 'paid' then amount
                else 0
            end
        ) as collected_revenue,
        sum(
            case
                when payment_status <> 'paid' then amount
                else 0
            end
        ) as uncollected_revenue,
        avg(amount) as average_transaction_value
    from transactions
    group by 1

),

monthly_subscription_ids as (

    select distinct
        date_trunc('month', t.transaction_date) as revenue_month,
        t.subscription_id
    from transactions t

),

monthly_subscription_revenue as (

    select
        m.revenue_month,
        sum(s.monthly_recurring_revenue) as mrr,
        sum(s.annual_recurring_revenue) as arr
    from monthly_subscription_ids m
    left join subscriptions s
        on m.subscription_id = s.subscription_id
    group by 1

)

select
    t.revenue_month,
    t.active_customers,
    t.transaction_count,
    t.total_revenue,
    t.collected_revenue,
    t.uncollected_revenue,
    t.average_transaction_value,
    coalesce(s.mrr, 0) as mrr,
    coalesce(s.arr, 0) as arr
from monthly_transactions t
left join monthly_subscription_revenue s
    on t.revenue_month = s.revenue_month
order by t.revenue_month
