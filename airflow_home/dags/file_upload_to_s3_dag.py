import boto3

from datetime import timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.timezone import datetime




s3 = boto3.resource('s3')


def upload_file_to_S3(filename, key, bucket_name):
    s3.Bucket(bucket_name).upload_file(filename, key)


default_args = {
    'owner': 'abin',
    'start_date': datetime(2019,1,1),
    'retry_delay': timedelta(minutes=5)
}

# dag = DAG(
#     's3_upload',
#     default_args=default_args,
#     description='File upload to s3 bucket',
#     schedule_interval=timedelta(hours=5),
# )

# Using the context manager allows you not duplicate the dag parameter in each operator
with DAG('S3_dag_test', default_args=default_args, schedule_interval='@once') as dag:
    upload_to_s3_task = PythonOperator(
        task_id = 'upload_file_To_s3',
        python_callable =upload_file_to_S3,
        op_kwargs={
            'filename': '/home/abin/test1.txt',
            'key': 'my_S3_file.csv',
            'bucket_name': 'airflow-storage01'
        },
        dag=dag
    )

    # Use arrows to set dependencies between tasks