import json
import logging
from dataclasses import asdict
from datetime import datetime
from logging import config

from backoff import backoff
from clickhouse_driver import Client
from constants import (CH_HOST, CH_TABLE_NAME, CONSUME_MAX_POLL,
                       CONSUME_TIMEOUT, KAFKA_GROUP_ID, KAFKA_HOST, KAFKA_PORT,
                       KAFKA_TOPIC)
from intit_db import create_db
from kafka import KafkaConsumer
from logger import LOG_CONFIG
from model import MovieModel

config.dictConfig(LOG_CONFIG)


@backoff(logging=logging)
def connect_to_db():
    create_db()
    return Client(host=CH_HOST)


def transform_records(records: list):
    for record in records:
        user_uuid, movie_uuid = record.key.decode().split('+')
        event_time = record.value.pop('event_time')
        event_time = datetime.fromisoformat(event_time)
        movie_model = MovieModel(
            user_uuid=user_uuid, movie_uuid=movie_uuid,
            event_time=event_time, **record.value
        )
        yield asdict(movie_model)


@backoff(logging=logging)
def load_data_to_db(client: Client, values: list):
    client.execute(f'INSERT INTO analytics.{CH_TABLE_NAME} VALUES', values)


def main(kafka_consumer: KafkaConsumer, ch_client: Client):
    while True:
        msg_poll = kafka_consumer.poll(timeout_ms=CONSUME_TIMEOUT, update_offsets=False)
        for topic_partition, records in msg_poll.items():
            transformed_records = [record for record in transform_records(records)]
            load_data_to_db(ch_client, transformed_records)
            kafka_consumer.seek(topic_partition, records[-1].offset + 1)
            kafka_consumer.commit()


if __name__ == '__main__':
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        api_version=(0, 11, 5),
        group_id=KAFKA_GROUP_ID,
        bootstrap_servers=[f'{KAFKA_HOST}:{KAFKA_PORT}'],
        max_poll_records=CONSUME_MAX_POLL,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        enable_auto_commit=False
    )
    client = connect_to_db()
    main(consumer, client)
