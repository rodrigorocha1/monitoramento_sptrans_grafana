import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from etl import *

# Configuração da DAG
default_args = {
    'start_date': datetime(2024, 2, 22),
    'retries': 1,
}

with DAG(
    dag_id='migracao',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
) as dag:

    carregar_dados = PythonOperator(
        task_id='carregar_dados',
        python_callable=inserir_dados,
    )

    carregar_dados
