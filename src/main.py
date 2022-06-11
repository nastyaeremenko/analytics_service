import json
import logging
import logstash

import grpc
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from kafka import KafkaProducer
from motor.motor_asyncio import AsyncIOMotorClient

from api import bookmarks, movie_progress, rating, review
from core import config
from core.logger import LOGGING
from db import kafka, mongodb
from domain.grpc_auth import client
from domain.grpc_auth.protos import auth_pb2_grpc

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
    client.channel = grpc.aio.insecure_channel(f'{config.GRPC_HOST}:{config.GRPC_PORT}')
    client.stub = auth_pb2_grpc.AuthStub(client.channel)
    mongodb.mongo = AsyncIOMotorClient(host=config.MONGO_HOST, port=config.MONGO_PORT)


@app.on_event('shutdown')
async def shutdown():
    await client.channel.close()
    mongodb.mongo.close()


app.include_router(movie_progress.router,
                   prefix='/api/v1/movie/progress',
                   tags=['movie_progress'])
app.include_router(rating.router,
                   prefix='/api/v1/rating',
                   tags=['rating'])
app.include_router(bookmarks.router,
                   prefix='/api/v1/bookmarks',
                   tags=['bookmarks'])
app.include_router(review.router,
                   prefix='/api/v1/review',
                   tags=['review'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
