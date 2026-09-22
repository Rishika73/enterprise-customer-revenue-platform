from pathlib import Path
import csv
import sys

BASE = Path("data/raw")


def load_csv(name):
    path = BASE / name
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def assert_unique(rows, key, dataset):
    values = [row[key] for row in rows]

    if len(values) != len(set(values)):
        raise AssertionError(
            f"{dataset}: duplicate values found in {key}"
        )


def assert_not_null(rows, fields, dataset):
    for row_number, row in enumerate(rows, start=2):
        for field in fields:
            if row[field] is None or row[field].strip() == "":
                raise AssertionError(
                    f"{dataset}: null/blank {field} at row {row_number}"
                )


def assert_foreign_key(
    child_rows,
    child_key,
    parent_rows,
    parent_key,
    dataset,
):
    valid_parent_values = {
        row[parent_key]
        for row in parent_rows
    }

    invalid = [
        row[child_key]
        for row in child_rows
        if row[child_key] not in valid_parent_values
    ]

    if invalid:
        raise AssertionError(
            f"{dataset}: invalid {child_key} values: {invalid}"
        )


def main():
    customers = load_csv("customers.csv")
    owners = load_csv("account_owners.csv")
    products = load_csv("products.csv")
    subscriptions = load_csv("subscriptions.csv")
    transactions = load_csv("transactions.csv")
    usage = load_csv("product_usage.csv")
    tickets = load_csv("support_tickets.csv")
    health = load_csv("account_health.csv")

    # Primary-key checks
    assert_unique(customers, "customer_id", "customers")
    assert_unique(owners, "account_owner_id", "account_owners")
    assert_unique(products, "product_id", "products")
    assert_unique(subscriptions, "subscription_id", "subscriptions")
    assert_unique(transactions, "transaction_id", "transactions")
    assert_unique(usage, "usage_id", "product_usage")
    assert_unique(tickets, "ticket_id", "support_tickets")
    assert_unique(health, "health_id", "account_health")

    # Required-column checks
    assert_not_null(
        customers,
        [
            "customer_id",
            "customer_name",
            "segment",
            "annual_contract_value",
        ],
        "customers",
    )

    assert_not_null(
        subscriptions,
        [
            "subscription_id",
            "customer_id",
            "product_id",
            "renewal_date",
            "status",
        ],
        "subscriptions",
    )

    assert_not_null(
        transactions,
        [
            "transaction_id",
            "customer_id",
            "amount",
            "payment_status",
        ],
        "transactions",
    )

    # Foreign-key integrity
    assert_foreign_key(
        customers,
        "account_owner_id",
        owners,
        "account_owner_id",
        "customers",
    )

    assert_foreign_key(
        subscriptions,
        "customer_id",
        customers,
        "customer_id",
        "subscriptions",
    )

    assert_foreign_key(
        subscriptions,
        "product_id",
        products,
        "product_id",
        "subscriptions",
    )

    for dataset_name, rows in [
        ("transactions", transactions),
        ("product_usage", usage),
        ("support_tickets", tickets),
        ("account_health", health),
    ]:
        assert_foreign_key(
            rows,
            "customer_id",
            customers,
            "customer_id",
            dataset_name,
        )

    # Business-rule checks
    for row in customers:
        assert float(row["annual_contract_value"]) >= 0

    for row in subscriptions:
        assert float(row["monthly_recurring_revenue"]) >= 0
        assert float(row["annual_recurring_revenue"]) >= 0

    for row in transactions:
        assert float(row["amount"]) >= 0

    for row in usage:
        assert int(row["active_users"]) >= 0
        assert int(row["sessions"]) >= 0
        assert int(row["api_calls"]) >= 0

        score = float(row["feature_adoption_score"])
        assert 0 <= score <= 100

    for row in health:
        health_score = int(row["health_score"])
        churn_probability = float(
            row["churn_risk_probability"]
        )

        assert 0 <= health_score <= 100
        assert 0 <= churn_probability <= 1

    print("Raw data validation passed.")
    print(f"customers: {len(customers)}")
    print(f"subscriptions: {len(subscriptions)}")
    print(f"transactions: {len(transactions)}")
    print(f"product_usage: {len(usage)}")
    print(f"support_tickets: {len(tickets)}")
    print(f"account_health: {len(health)}")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"VALIDATION FAILED: {exc}")
        sys.exit(1)
