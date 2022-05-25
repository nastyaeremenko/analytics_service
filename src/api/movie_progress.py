from http import HTTPStatus

from fastapi import APIRouter, Depends
from kafka import KafkaProducer

from api.serializers import MovieProgress
from core.config import KAFKA_TOPIC
from domain.kafka import get_kafka_producer

router = APIRouter()


@router.post('', status_code=HTTPStatus.OK)
async def post_movie_progress(payload: MovieProgress,
                              kafka_producer: KafkaProducer = Depends(get_kafka_producer)):
    kafka_producer.send(topic=KAFKA_TOPIC,
                        value=payload.movie_second,
                        key=f'{payload.user_id}+{payload.movie_id}')
    return {'message': 'Uploaded successfully'}
