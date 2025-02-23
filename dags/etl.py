import os
import pandas as pd
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from dotenv import load_dotenv
import math

# Carregar variáveis de ambiente
load_dotenv()


def abrir_dataframe():
    caminho_base = os.getcwd()
    caminho_arquivo = os.path.join(caminho_base, 'dags', 'citymapper_gtfs')
    base = pd.read_csv(f'{caminho_arquivo}/shapes.txt', sep=',')
    base['shape_id'] = base['shape_id'].astype('string')
    print(base.head())

    return base


def inserir_dados():
    base = abrir_dataframe()
    hook = MsSqlHook(mssql_conn_id='sql_server_conn')

    # Preparar os valores em formato de tuplas para inserção em lote
    valores = [
        (
            linha['shape_id'],
            linha['shape_pt_lat'],
            linha['shape_pt_lon'],
            linha['shape_pt_sequence'],
            linha['shape_dist_traveled']
        )
        for _, linha in base.iterrows()
    ]

    # Inserção em lotes de 1000 registros
    batch_size = 1000
    total_batches = math.ceil(len(valores) / batch_size)
    print(total_batches)

    for i in range(total_batches):
        batch = valores[i * batch_size:(i + 1) * batch_size]
        consulta = """
            INSERT INTO shapes (shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence, shape_dist_traveled)
            VALUES %s
        """ % ",".join(["(%s, %s, %s, %s, %s)"] * len(batch))

        parametros = [item for tupla in batch for item in tupla]
        hook.run(consulta, parameters=parametros)

        print(f"Lote {i + 1}/{total_batches} inserido com sucesso.")
