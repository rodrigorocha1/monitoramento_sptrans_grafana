from kafka import KafkaProducer, KafkaAdminClient
from kafka.errors import TopicAlreadyExistsError, KafkaError
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

            except KafkaError:
                sleep(5)
        else:
            raise RuntimeError('Falha ao conectar ao kafka')
