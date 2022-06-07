import uuid
from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends
from kafka import KafkaProducer

from api.serializers import MovieProgress, MovieRating
from core.config import KAFKA_TOPIC
from db.kafka import get_kafka_producer
from domain.grpc_auth.dependencies import get_user_id
from domain.movie_services.movie_rating import (MovieRatingService,
                                                get_movie_rating_service)

router = APIRouter()


@router.post('', status_code=HTTPStatus.OK)
async def post_movie_progress(payload: MovieProgress,
                              user_uuid=Depends(get_user_id),
                              kafka_producer: KafkaProducer = Depends(get_kafka_producer)):
    kafka_producer.send(topic=KAFKA_TOPIC,
                        value={'movie_progress': payload.movie_progress,
                               'movie_length': payload.movie_length,
                               'event_time': datetime.now().isoformat()},
                        key=f'{user_uuid}+{payload.movie_uuid}')

    return {'message': 'Uploaded successfully'}


@router.get('', response_model=MovieRating)
async def get_movie_progress(movie_uuid: uuid.UUID,
                             movie_rating_service: MovieRatingService
                             = Depends(get_movie_rating_service)):
    ratings = await movie_rating_service.get_movie_rating(str(movie_uuid))
    return ratings
