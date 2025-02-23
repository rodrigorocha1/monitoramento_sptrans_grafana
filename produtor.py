from typing import Dict
from kafka import KafkaProducer, KafkaAdminClient
from kafka.errors import TopicAlreadyExistsError, KafkaError
from kafka.admin import NewTopic
from src.api_sptrans import APISPTRANS
import json
from time import sleep


class Produtor:

    def __init__(self):
        for i in range(11):
            try:

                self.__URL_KAFKA = 'kafka:9092'
                self.__produtor = KafkaProducer(
                    bootstrap_servers=self.__URL_KAFKA,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    key_serializer=lambda k: k.encode('utf-8')
                )

                self.__admin_cliente = KafkaAdminClient(
                    bootstrap_servers=self.__URL_KAFKA
                )
                self.__req_api_sptrans = APISPTRANS()

            except KafkaError:
                sleep(5)
        else:
            raise RuntimeError('Falha ao conectar ao kafka')

    def __criar_topico(self, topico: str, numero_particoes: int):
        try:
            novo_topico = NewTopic(
                name=topico,
                num_partitions=numero_particoes,
                replication_factor=1
            )
            self.__admin_cliente.create_topics([novo_topico])
        except TopicAlreadyExistsError:
            print('Tópico já criado')

    def __enviar_dados(self, topico: str, codigo_linha: str, dados: Dict, particao: int):
        self.__produtor.send(
            topic=topico,
            value=dados,
            key=codigo_linha,
            partition=particao
        )
        self.__produtor.flush()

    def rodar_produtor(self):
        self.__criar_topico(topico='linhas_onibus', numero_particoes=1)
        while True:
            dados_linha = self.__req_api_sptrans.buscar_linhas()
            for dado in dados_linha:
                self.__enviar_dados(
                    topico='linhas_onibus',
                    dado=dado,
                    codigo_linha='1',
                    particao=1
                )
            sleep(5)
