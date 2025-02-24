#!/bin/bash

# Verifica se o Kafka está pronto
echo "Aguardando Kafka em $KAFKA_HOST..."

while ! nc -z kafka 9092; do
    sleep 1
done

echo "Kafka está pronto!"
exec "$@"
