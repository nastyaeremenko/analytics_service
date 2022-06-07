import uuid
from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends
from kafka import KafkaProducer

from api.query_params import SortingParams
from api.serializers import MovieProgress, ReviewRatings
from core.config import KAFKA_TOPIC
from db.kafka import get_kafka_producer
from domain.grpc_auth.dependencies import get_user_id
from domain.movie_services.review import ReviewService, get_review_service

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


@router.get('', response_model=ReviewRatings)
async def get_movie_progress(movie_uuid: uuid.UUID,
                             sorting: SortingParams = Depends(),
                             review_service: ReviewService = Depends(get_review_service)):
    reviews = await review_service.get_review_rating(str(movie_uuid), sorting.__dict__)
    return reviews
