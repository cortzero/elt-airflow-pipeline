from datetime import datetime
from dotenv import load_dotenv
from airflow import DAG
from docker.types import Mount
from airflow.operators.python_operator import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
import subprocess
import os

load_dotenv()
dbt_transformations_folder_path = os.getenv("DBT_TRANSFORMATIONS_FOLDER_PATH")
dbt_user_folder_path = os.getenv("DBT_USER_FOLDER_PATH")

default_args = {
  'owner': 'airflow',
  'depends_on_past': False,
  'email_on_failure': False,
  'email_on_retry': False
}

def run_elt_script():
  script_path = "/opt/airflow/elt/elt_script.py"
  result = subprocess.run(["python", script_path], capture_output=True, text=True)
  if result.returncode != 0:
    raise Exception(f"Script failed with error: {result.stderr}")
  else:
    print(result.stdout)

dag = DAG(
  dag_id="elt_and_dbt",
  default_args=default_args,
  description="An ELT workflow with dbt",
  start_date=datetime(2025, 4, 15),
  schedule="30 * * * *",
  catchup=False
)

task_1 = PythonOperator(
  task_id="run_elt_script",
  python_callable=run_elt_script,
  dag=dag
)

task_2 = DockerOperator(
  task_id="dbt_run",
  image="ghcr.io/dbt-labs/dbt-postgres:1.4.7",
  command=[
      "run",
      "--profiles-dir",
      "/root",
      "--project-dir",
      "/dbt",
      "--full-refresh"
  ],
  auto_remove='success',
  docker_url="unix://var/run/docker.sock",
  network_mode="bridge",
  mounts=[
      Mount(source=dbt_transformations_folder_path, target="/dbt", type="bind"),
      Mount(source=dbt_user_folder_path, target="/root", type="bind"),
  ],
  dag=dag
)

task_1 >> task_2
