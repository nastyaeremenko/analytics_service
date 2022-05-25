import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import movie_progress
from core import config
from core.logger import LOGGING

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


# @app.on_event('startup')
# async def startup():
#     redis.redis = await redis.RedisCache.connect(f'{config.REDIS_HOST}:{config.REDIS_PORT}')
#     elastic.es = elastic.ElasticSearch(f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}')
#     client.stub = auth_pb2_grpc.AuthStub(client.channel)
#
#
# @app.on_event('shutdown')
# async def shutdown():
#     await redis.redis.close()
#     await elastic.es.close()
#     await client.channel.close()


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
