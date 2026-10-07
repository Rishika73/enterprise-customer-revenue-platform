from datetime import datetime
import os
from pathlib import Path

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator


PROJECT_ROOT = Path(
    os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[2])
)

DBT_PROJECT_DIR = Path(
    os.getenv("DBT_PROJECT_DIR", PROJECT_ROOT / "customer_revenue_dbt")
)


with DAG(
    dag_id="customer_revenue_pipeline",
    description="Orchestrates dbt models, tests, and snapshots for the customer revenue platform",
    start_date=datetime(2026, 9, 19),
    schedule=None,
    catchup=False,
    tags=["snowflake", "dbt", "customer-revenue"],
) as dag:

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=f'cd "{DBT_PROJECT_DIR}" && dbt build --exclude resource_type:snapshot',
    )

    dbt_snapshot = BashOperator(
        task_id="dbt_snapshot",
        bash_command=f'cd "{DBT_PROJECT_DIR}" && dbt snapshot --select customer_snapshot',
    )

    dbt_build >> dbt_snapshot
