import json

from constants import (CONSUME_MAX_POLL, CONSUME_TIMEOUT, KAFKA_GROUP_ID,
                       KAFKA_HOST, KAFKA_PORT, KAFKA_TOPIC)
from kafka import KafkaConsumer
from model import MovieModel


def transform_records(records: list):
    for record in records:
        user_uuid, movie_uuid = record.key.decode().split('+')
        movie_model = MovieModel(user_uuid=user_uuid,
                                 movie_uuid=movie_uuid,
                                 **record.value)
        yield movie_model


def main(kafka_consumer: KafkaConsumer):
    while True:
        msg_poll = kafka_consumer.poll(timeout_ms=CONSUME_TIMEOUT).values()
        for records in msg_poll:
            transformed_records = [record for record in transform_records(records)]
            # TODO: ClickHouse step
            print(transformed_records)


if __name__ == '__main__':
    consumer = KafkaConsumer(KAFKA_TOPIC,
                             group_id=KAFKA_GROUP_ID,
                             bootstrap_servers=[f'{KAFKA_HOST}:{KAFKA_PORT}'],
                             max_poll_records=CONSUME_MAX_POLL,
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    main(consumer)
