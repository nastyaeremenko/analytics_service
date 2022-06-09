from http import HTTPStatus
from fastapi import APIRouter, Depends, Query

from api.serializers import RateMovie, Sort
from domain.movie_services.movie_rating import get_movie_rating_service, MovieRatingService
from domain.movie_services.review import get_review_service, ReviewService
from domain.grpc_auth.dependencies import get_user_id

router = APIRouter()


@router.post('/movie', status_code=HTTPStatus.CREATED)
async def rate_the_movie(payload: RateMovie,
                         user_uuid=Depends(get_user_id),
                         service: MovieRatingService = Depends(get_movie_rating_service)):
    return await service.add_document(payload.dict_with_user_uuid(user_uuid))


@router.get('/movie', status_code=HTTPStatus.OK)
async def get_movie_rating(movie_id: str,
                           service: MovieRatingService = Depends(get_movie_rating_service)):
    return await service.get_movie_rating(movie_id)


@router.get('/review', status_code=HTTPStatus.OK)
async def get_movie_rating(sort: Sort,
                           movie_id: str = Query(..., description='UUID фильма'),
                           service: ReviewService = Depends(get_review_service)):
    return await service.get_review_rating(movie_id, sort.dict())
