from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from api.serializers import MovieRating, RateMovie, RateMovieOut
from domain.grpc_auth.dependencies import get_user_id
from domain.movie_services.movie_rating import (MovieRatingService,
                                                get_movie_rating_service)

router = APIRouter()


@router.post('/movie', status_code=HTTPStatus.CREATED, response_model=RateMovieOut)
async def rate_the_movie(payload: RateMovie,
                         user_uuid=Depends(get_user_id),
                         service: MovieRatingService = Depends(get_movie_rating_service)):
    response = await service.add_document(payload.dict_with_user_uuid(user_uuid))
    movie_rating = await service.get_document_by_id(response.inserted_id)
    return movie_rating


@router.get('/movie', status_code=HTTPStatus.OK, response_model=MovieRating)
async def get_movie_rating(movie_id: str = Query(..., description='UUID фильма'),
                           service: MovieRatingService = Depends(get_movie_rating_service)):
    movie_rating = await service.get_movie_rating(movie_id)
    if movie_rating:
        return movie_rating

    return JSONResponse(content={}, status_code=HTTPStatus.NOT_FOUND)


@router.put('/movie', status_code=HTTPStatus.OK, response_model=RateMovieOut)
async def update_movie_rating(payload: RateMovie,
                              rating_id: str = Query(..., description='UUID Отзыва'),
                              user_uuid=Depends(get_user_id),
                              service: MovieRatingService = Depends(get_movie_rating_service)):
    movie_rating = await service.get_document_by_id(rating_id)

    if movie_rating and movie_rating['user_uuid'] == user_uuid:
        updated_payload = payload.dict_with_user_uuid(user_uuid)
        await service.update_document(rating_id, updated_payload)
        updated_rating = await service.get_document_by_id(rating_id)
        return updated_rating

    return JSONResponse(content={'message': HTTPStatus.FORBIDDEN.description},
                        status_code=HTTPStatus.FORBIDDEN)


@router.delete('/movie', status_code=HTTPStatus.ACCEPTED)
async def delete_movie_rating(rating_id: str = Query(..., description='UUID Отзыва'),
                              user_uuid=Depends(get_user_id),
                              service: MovieRatingService = Depends(get_movie_rating_service)):
    movie_rating = await service.get_document_by_id(rating_id)

    if movie_rating and movie_rating['user_uuid'] == user_uuid:
        await service.delete_document(rating_id)
        return {'message': f'movie rating was deleted: {rating_id}'}

    return JSONResponse(content={'message': HTTPStatus.FORBIDDEN.description},
                        status_code=HTTPStatus.FORBIDDEN)
