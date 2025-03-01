from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import time
import os
from dotenv import load_dotenv
load_dotenv()


class Consumidor:
    def __init__(self):
        self.__topico = 'linhas_onibus'
        self.__bootstrap_servers = 'kafka:9092'
        self.__group_id = 'linhas_sptrans_grupo'
        self.__INFLUXDB_URL = os.environ['INFLUXDB_URL']
        self.__INFLUXDB_TOKEN = os.environ['INFLUXDB_TOKEN']
        self.__INFLUXDB_ORG = os.environ['INFLUXDB_ORG']
        self.__INFLUXDB_BUCKET = os.environ['INFLUXDB_BUCKET']
        self.__cliente = InfluxDBClient(
            url=self.__INFLUXDB_URL,
            token=self.__INFLUXDB_TOKEN,
            org=self.__INFLUXDB_ORG
        )

        for i in range(100):
            try:
                self.__consumidor = KafkaConsumer(
                    self.__topico,
                    bootstrap_servers=self.__bootstrap_servers,
                    group_id=self.__group_id,
                    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                    auto_offset_reset='latest',
                    enable_auto_commit=True
                )
            except KafkaError as e:
                print(f"Tentativa {i + 1}/5 falhou: {e}")
                time.sleep(30)
        else:
            raise RuntimeError(
                "Falha ao conectar ao Kafka consomidor após várias tentativas.")

    def rodar_consumidor(self):
        for mensagem in self.__consumidor:
            for valor in mensagem.value:
                print(valor)


if __name__ == '__main__':
    c = Consumidor()
    c.rodar_consumidor()
