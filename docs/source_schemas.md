# Source Schemas

## customers

- customer_id: string
- customer_name: string
- industry: string
- segment: string
- region: string
- country: string
- employee_count: integer
- annual_contract_value: decimal
- account_owner_id: string
- created_at: timestamp
- updated_at: timestamp

## account_owners

- account_owner_id: string
- account_owner_name: string
- team: string
- region: string
- email: string

## subscriptions

- subscription_id: string
- customer_id: string
- product_id: string
- plan_name: string
- start_date: date
- end_date: date
- renewal_date: date
- billing_frequency: string
- monthly_recurring_revenue: decimal
- annual_recurring_revenue: decimal
- status: string
- updated_at: timestamp

## transactions

- transaction_id: string
- customer_id: string
- subscription_id: string
- transaction_date: timestamp
- transaction_type: string
- amount: decimal
- currency: string
- payment_status: string
- payment_method: string

## products

- product_id: string
- product_name: string
- product_category: string
- plan_tier: string
- monthly_list_price: decimal
- active_flag: boolean

## product_usage

- usage_id: string
- customer_id: string
- product_id: string
- usage_date: date
- active_users: integer
- sessions: integer
- api_calls: integer
- storage_gb: decimal
- feature_adoption_score: decimal

## support_tickets

- ticket_id: string
- customer_id: string
- created_at: timestamp
- closed_at: timestamp
- priority: string
- status: string
- category: string
- assigned_team: string
- resolution_hours: decimal
- satisfaction_score: decimal

## account_health

- health_id: string
- customer_id: string
- score_date: date
- health_score: integer
- adoption_score: integer
- support_score: integer
- payment_score: integer
- renewal_risk: string
- churn_risk_probability: decimal
