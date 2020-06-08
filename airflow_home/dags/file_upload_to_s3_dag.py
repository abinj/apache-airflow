from datetime import timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.timezone import datetime

default_args = {
    'owner': 'abin',
    'start_date': datetime(2019,1,1),
    'retry_delay': timedelta(minutes=5)
}

# Using the context manager allows you not duplicate the dag parameter in each operator
with DAG('S3_dag_test', default_args=default_args, schedule_interval='@once') as dag:
    upload_to_s3_task = PythonOperator(
        task_id = 'upload_file_To_s3',
        python_callable =lambda _ : print("Uploading file to S3")
    )

    # Use arrows to set dependencies between tasks
    upload_to_s3_task
