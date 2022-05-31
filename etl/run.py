import json

from clickhouse_driver import Client
from kafka import KafkaConsumer

from constants import (
    CONSUME_MAX_POLL,
    CONSUME_TIMEOUT,
    KAFKA_GROUP_ID,
    KAFKA_HOST,
    KAFKA_PORT,
    KAFKA_TOPIC,
    CH_HOST,
    CH_TABLE_NAME,
)
from intit_db import create_db
from model import MovieModel
from logging import getLogger


def get_consumer():
    return KafkaConsumer(
        KAFKA_TOPIC,
        api_version=(0, 11, 5),
        group_id=KAFKA_GROUP_ID,
        bootstrap_servers=[f'{KAFKA_HOST}:{KAFKA_PORT}'],
        max_poll_records=CONSUME_MAX_POLL,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    )


def connect_to_db():
    create_db()
    return Client(host=CH_HOST)


def transform_records(records: list):
    for record in records:
        user_uuid, movie_uuid = record.key.decode().split('+')
        movie_model = MovieModel(
            user_uuid=user_uuid, movie_uuid=movie_uuid, **record.value
        )
        yield movie_model


def load_data_to_db(client: Client, values: list):
    try:
        client.execute(f'INSERT INTO {CH_TABLE_NAME} VALUES', values)
        return True
    except Exception:
        return False


def main():
    logger = getLogger('main')
    ch_client: Client = connect_to_db()
    kafka_consumer = get_consumer()
    values = []
    msg_poll = kafka_consumer.poll(timeout_ms=CONSUME_TIMEOUT).values()
    for records in msg_poll:
        transformed_records = [record for record in transform_records(records)]
        values.append(transformed_records)
        for _retry in range(3):
            result = load_data_to_db(ch_client, values)
            if result:
                values = []
                break
        else:
            logger.exception('Error to upload data to ClickHouse')


if __name__ == '__main__':
    main()
