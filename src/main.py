import json
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from kafka import KafkaProducer

from api import movie_progress
from core import config
from core.logger import LOGGING
from domain import kafka

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    kafka.producer = KafkaProducer(bootstrap_servers=f'{config.KAFKA_HOST}:{config.KAFKA_PORT}',
                                   value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                   key_serializer=str.encode)


app.include_router(movie_progress.router,
                   prefix='/api/v1/movie/progress',
                   tags=['movie_progress'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
