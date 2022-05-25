import os
from logging import config as logging_config

from dotenv import load_dotenv

from core.logger import LOGGING

load_dotenv()

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'analytic')

KAFKA_HOST = os.getenv('KAFKA_HOST', 'localhost')
KAFKA_PORT = os.getenv('KAFKA_PORT', '9092')
KAFKA_TOPIC = 'movie_progress'
