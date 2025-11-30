# orchestration/airflow_dag_emo.py
from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.decorators import task

from emo.ingestion import (
    DataLakeLayout,
    emo_daily_attention,
    emo_weekly_synergy,
    emo_monthly_oi_smf,
    emo_yearly_tau,
    ForecastSkillConfig,
)


default_args = {
    "owner": "emo",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="emo_live_observatory",
    default_args=default_args,
    description="EMO v1.0 live ingestion pipelines",
    schedule_interval=None,  # we define schedules per-task below using @task
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["emo", "planetary-cognition"],
) as dag:

    @task(task_id="daily_attention", schedule="@daily")
    def daily_attention_task() -> None:
        layout = DataLakeLayout.from_env()
        emo_daily_attention(layout=layout)

    @task(task_id="weekly_synergy", schedule="@weekly")
    def weekly_synergy_task() -> None:
        layout = DataLakeLayout.from_env()
        emo_weekly_synergy(layout=layout)

    @task(task_id="monthly_oi_smf", schedule="@monthly")
    def monthly_oi_smf_task() -> None:
        layout = DataLakeLayout.from_env()
        emo_monthly_oi_smf(layout=layout)

    @task(task_id="yearly_tau", schedule="@yearly")
    def yearly_tau_task() -> None:
        layout = DataLakeLayout.from_env()
        cfg = ForecastSkillConfig(
            url="https://example.org/ecmwf_headline_scores.csv",
            canonical_name="ecmwf_headline_scores",
        )
        emo_yearly_tau(skill_config=cfg, layout=layout)

    # In Airflow 2.8+ with task-level schedules, tasks can be largely independent.
    # If your Airflow version does not support task-level schedules, you can
    # instead duplicate this DAG into four DAGs, each with its own schedule
    # and a single task.
    daily_attention_task()
    weekly_synergy_task()
    monthly_oi_smf_task()
    yearly_tau_task()
