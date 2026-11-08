from airflow import DAG
from datetime import datetime,timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
import os


default_args={
    'owner':'Conqueror',
    'retries':2,
    'retry_delay':timedelta(minutes=2)
}

with DAG(
    dag_id="weather_pipeline_airflow",
    description="Orchestrates the weather ETL pipeline using Docker",
    default_args=default_args,
    start_date=datetime(2026,11,4,2),
    schedule_interval=None,
    catchup=False,
    tags=["weather", "etl", "docker"],
) as dag:
    run_weather_etl=DockerOperator(
        task_id="run_weather_etl",
        image="weather-etl:1.0",
        docker_url="unix://var/run/docker.sock",
        api_version="auto",
        auto_remove=True,
        mount_tmp_dir=False,
        network_mode="material_default",
        mounts=[
            Mount(
            source="G:/Data Engineering/weather-data-engineering-pipeline/data",
            target="/app/data",
            type="bind"
            ),
            Mount(
                source="G:/Data Engineering/weather-data-engineering-pipeline/logs",
                target="/app/logs",
                type="bind"
                ),
        ],
        environment={
            "OPENWEATHER_API_KEY": os.getenv("OPENWEATHER_API_KEY"),
            "SQL_USERNAME": os.getenv("SQL_USERNAME"),
            "SQL_PASSWORD": os.getenv("SQL_PASSWORD"),
            "SQL_SERVER": os.getenv("SQL_SERVER"),
            "SQL_PORT": os.getenv("SQL_PORT"),
            "SQL_DATABASE": os.getenv("SQL_DATABASE"),
            },
        working_dir="/app",
        mem_limit="1g",
            

    )