from pathlib import Path
import csv
import random
from datetime import date, datetime, timedelta

random.seed(42)

BASE = Path("data/raw")
BASE.mkdir(parents=True, exist_ok=True)

customers = [
    ["C001", "Northstar Retail", "Retail", "Enterprise", "East", "USA", 4200, 420000, "AO001", "2024-01-15 09:00:00", "2026-09-01 12:00:00"],
    ["C002", "BluePeak Finance", "Financial Services", "Enterprise", "East", "USA", 7800, 780000, "AO002", "2024-03-10 10:00:00", "2026-09-05 15:30:00"],
    ["C003", "GreenField Health", "Healthcare", "Mid-Market", "Central", "USA", 1200, 180000, "AO003", "2024-06-22 11:30:00", "2026-08-28 10:15:00"],
    ["C004", "Vertex Logistics", "Logistics", "Enterprise", "West", "USA", 5100, 510000, "AO004", "2024-02-05 08:45:00", "2026-09-10 14:20:00"],
    ["C005", "Summit Energy", "Energy", "Mid-Market", "South", "USA", 950, 145000, "AO005", "2024-09-18 13:00:00", "2026-09-08 09:40:00"],
    ["C006", "Horizon Media", "Media", "SMB", "West", "USA", 280, 72000, "AO004", "2025-01-12 09:20:00", "2026-09-03 11:00:00"],
    ["C007", "Apex Manufacturing", "Manufacturing", "Enterprise", "Central", "USA", 6300, 640000, "AO003", "2024-04-30 15:10:00", "2026-09-12 13:25:00"],
    ["C008", "BrightPath Education", "Education", "Mid-Market", "East", "USA", 1400, 165000, "AO001", "2024-11-03 10:40:00", "2026-09-06 16:10:00"],
]

owners = [
    ["AO001", "Emma Carter", "Enterprise Sales", "East", "emma.carter@example.com"],
    ["AO002", "Liam Brooks", "Strategic Accounts", "East", "liam.brooks@example.com"],
    ["AO003", "Sophia Patel", "Enterprise Sales", "Central", "sophia.patel@example.com"],
    ["AO004", "Noah Kim", "Enterprise Sales", "West", "noah.kim@example.com"],
    ["AO005", "Olivia Reed", "Mid-Market Sales", "South", "olivia.reed@example.com"],
]

products = [
    ["P001", "Analytics Cloud", "Analytics", "Enterprise", 15000, True],
    ["P002", "Data Connect", "Integration", "Professional", 8000, True],
    ["P003", "Identity Secure", "Security", "Enterprise", 12000, True],
    ["P004", "Workflow Pro", "Automation", "Professional", 6000, True],
]

today = date(2026, 9, 18)

subscriptions = [
    ["S001", "C001", "P001", "Enterprise", "2025-10-01", "2026-09-30", "2026-10-01", "monthly", 35000, 420000, "active", "2026-09-01 10:00:00"],
    ["S002", "C002", "P003", "Enterprise", "2025-10-08", "2026-10-07", "2026-10-08", "monthly", 65000, 780000, "active", "2026-09-05 12:00:00"],
    ["S003", "C003", "P002", "Professional", "2026-01-01", "2026-12-31", "2027-01-01", "monthly", 15000, 180000, "active", "2026-08-20 08:00:00"],
    ["S004", "C004", "P001", "Enterprise", "2025-10-25", "2026-10-24", "2026-10-25", "monthly", 42500, 510000, "active", "2026-09-10 09:00:00"],
    ["S005", "C005", "P004", "Professional", "2026-03-01", "2027-02-28", "2027-03-01", "monthly", 12083, 145000, "active", "2026-09-08 09:00:00"],
    ["S006", "C006", "P002", "Professional", "2026-02-01", "2027-01-31", "2027-02-01", "monthly", 6000, 72000, "active", "2026-09-03 10:00:00"],
    ["S007", "C007", "P001", "Enterprise", "2025-11-15", "2026-11-14", "2026-11-15", "monthly", 53333, 640000, "active", "2026-09-12 10:00:00"],
    ["S008", "C008", "P004", "Professional", "2026-04-01", "2027-03-31", "2027-04-01", "monthly", 13750, 165000, "active", "2026-09-06 10:00:00"],
]

transactions = []
tx_id = 1
for sub in subscriptions:
    sub_id, customer_id, _, _, _, _, _, _, mrr, _, _, _ = sub
    for months_ago in range(6):
        tx_date = datetime(2026, 9, 1) - timedelta(days=30 * months_ago)
        status = "paid"
        if customer_id == "C002" and months_ago == 0:
            status = "late"
        if customer_id == "C004" and months_ago == 1:
            status = "failed"

        transactions.append([
            f"T{tx_id:04d}",
            customer_id,
            sub_id,
            tx_date.strftime("%Y-%m-%d %H:%M:%S"),
            "subscription_payment",
            mrr,
            "USD",
            status,
            random.choice(["ACH", "card", "wire"]),
        ])
        tx_id += 1

usage = []
usage_id = 1
for customer in customers:
    customer_id = customer[0]
    product_id = subscriptions[int(customer_id[1:]) - 1][2]

    for days_ago in range(0, 84, 7):
        usage_date = today - timedelta(days=days_ago)

        base_users = {
            "C001": 900,
            "C002": 1100,
            "C003": 300,
            "C004": 720,
            "C005": 220,
            "C006": 90,
            "C007": 1000,
            "C008": 340,
        }[customer_id]

        trend = 1.0
        if customer_id in {"C002", "C004"}:
            trend = 0.70 + (days_ago / 84) * 0.30
        elif customer_id == "C001":
            trend = 0.88 + (days_ago / 84) * 0.12

        active_users = max(1, int(base_users * trend + random.randint(-25, 25)))
        sessions = active_users * random.randint(4, 7)
        api_calls = sessions * random.randint(8, 14)
        storage = round(active_users * random.uniform(0.15, 0.28), 2)
        feature_score = round(min(100, max(20, trend * 90 + random.uniform(-5, 5))), 2)

        usage.append([
            f"U{usage_id:05d}",
            customer_id,
            product_id,
            usage_date.isoformat(),
            active_users,
            sessions,
            api_calls,
            storage,
            feature_score,
        ])
        usage_id += 1

tickets = [
    ["INC-1001", "C001", "2026-09-18 10:00:00", "", "high", "open", "API", "Platform Engineering", "", ""],
    ["INC-1002", "C002", "2026-09-18 12:00:00", "", "critical", "open", "Authentication", "Identity Engineering", "", ""],
    ["INC-1003", "C003", "2026-09-15 09:00:00", "2026-09-16 14:00:00", "medium", "closed", "Reporting", "Analytics Engineering", 29, 4.5],
    ["INC-1004", "C001", "2026-09-10 08:00:00", "2026-09-10 13:00:00", "low", "closed", "Configuration", "Customer Engineering", 5, 4.8],
    ["INC-1005", "C004", "2026-09-18 08:00:00", "", "high", "open", "Integration", "Integration Platform", "", ""],
    ["INC-1006", "C002", "2026-09-05 11:00:00", "2026-09-07 15:00:00", "high", "closed", "Authentication", "Identity Engineering", 52, 3.2],
    ["INC-1007", "C004", "2026-08-28 13:00:00", "2026-08-30 11:00:00", "medium", "closed", "Webhook", "Integration Platform", 46, 3.6],
]

health = [
    ["H001", "C001", "2026-09-18", 62, 68, 55, 90, "medium", 0.38],
    ["H002", "C002", "2026-09-18", 48, 42, 35, 70, "high", 0.72],
    ["H003", "C003", "2026-09-18", 82, 88, 80, 95, "low", 0.12],
    ["H004", "C004", "2026-09-18", 55, 50, 45, 65, "high", 0.64],
    ["H005", "C005", "2026-09-18", 79, 81, 76, 92, "low", 0.18],
    ["H006", "C006", "2026-09-18", 74, 78, 72, 88, "low", 0.24],
    ["H007", "C007", "2026-09-18", 86, 90, 84, 96, "low", 0.09],
    ["H008", "C008", "2026-09-18", 76, 79, 74, 90, "low", 0.20],
]

def write_csv(filename, header, rows):
    with (BASE / filename).open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

write_csv(
    "customers.csv",
    ["customer_id", "customer_name", "industry", "segment", "region", "country",
     "employee_count", "annual_contract_value", "account_owner_id", "created_at", "updated_at"],
    customers,
)

write_csv(
    "account_owners.csv",
    ["account_owner_id", "account_owner_name", "team", "region", "email"],
    owners,
)

write_csv(
    "products.csv",
    ["product_id", "product_name", "product_category", "plan_tier", "monthly_list_price", "active_flag"],
    products,
)

write_csv(
    "subscriptions.csv",
    ["subscription_id", "customer_id", "product_id", "plan_name", "start_date", "end_date",
     "renewal_date", "billing_frequency", "monthly_recurring_revenue",
     "annual_recurring_revenue", "status", "updated_at"],
    subscriptions,
)

write_csv(
    "transactions.csv",
    ["transaction_id", "customer_id", "subscription_id", "transaction_date",
     "transaction_type", "amount", "currency", "payment_status", "payment_method"],
    transactions,
)

write_csv(
    "product_usage.csv",
    ["usage_id", "customer_id", "product_id", "usage_date", "active_users",
     "sessions", "api_calls", "storage_gb", "feature_adoption_score"],
    usage,
)

write_csv(
    "support_tickets.csv",
    ["ticket_id", "customer_id", "created_at", "closed_at", "priority",
     "status", "category", "assigned_team", "resolution_hours", "satisfaction_score"],
    tickets,
)

write_csv(
    "account_health.csv",
    ["health_id", "customer_id", "score_date", "health_score", "adoption_score",
     "support_score", "payment_score", "renewal_risk", "churn_risk_probability"],
    health,
)

print("Generated datasets:")
for path in sorted(BASE.glob("*.csv")):
    print(f"- {path}: {sum(1 for _ in path.open()) - 1} rows")
