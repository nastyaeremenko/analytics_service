import os
from logging import config as logging_config

from dotenv import load_dotenv

from core.logger import LOGGING

load_dotenv()

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'UGC')

KAFKA_HOST = os.getenv('KAFKA_HOST', 'localhost')
KAFKA_PORT = os.getenv('KAFKA_PORT', 9092)
KAFKA_TOPIC = 'movie_progress'

GRPC_HOST = os.getenv('GRPC_HOST', 'localhost')
GRPC_PORT = os.getenv('GRPC_PORT', 50051)

MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = os.getenv('MONGO_PORT', 27017)
MONGO_DB = os.getenv('MONGO_DB', 'ugc')
