import os

from dotenv import load_dotenv

load_dotenv()


KAFKA_TOPIC = 'movie_progress'
KAFKA_GROUP_ID = 'movie_group'
KAFKA_HOST = os.getenv('KAFKA_HOST', 'localhost')
KAFKA_PORT = os.getenv('KAFKA_PORT', 9092)
# Kafka consume timeout in ms
CONSUME_TIMEOUT = 60 * 100
CONSUME_MAX_POLL = 10_000

# ClickHouse
CH_HOST = os.getenv('CH_HOST', 'localhost')
CH_TABLE_NAME = os.getenv('CH_TABLE_NAME', 'movie_view')
