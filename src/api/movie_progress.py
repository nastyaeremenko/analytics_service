from http import HTTPStatus

from fastapi import APIRouter, Depends
from kafka import KafkaProducer

from api.serializers import MovieProgress
from core.config import KAFKA_TOPIC
from data.kafka import get_kafka_producer
from domain.grpc_auth.dependencies import get_user_id

router = APIRouter()


@router.post('', status_code=HTTPStatus.OK)
async def post_movie_progress(payload: MovieProgress,
                              user_uuid=Depends(get_user_id),
                              kafka_producer: KafkaProducer = Depends(get_kafka_producer)):

    kafka_producer.send(topic=KAFKA_TOPIC,
                        value={'movie_second': payload.movie_second,
                               'movie_length': payload.movie_length,
                               'current_date': payload.current_date.isoformat()},
                        key=f'{user_uuid}+{payload.movie_uuid}')

    return {'message': 'Uploaded successfully'}
