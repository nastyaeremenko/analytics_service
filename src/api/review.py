from http import HTTPStatus
from fastapi import APIRouter, Depends, Query

from api.serializers import Review, Sort
from domain.movie_services.review import (get_review_service, ReviewService)
from domain.grpc_auth.dependencies import get_user_id

router = APIRouter()


@router.post('', status_code=HTTPStatus.CREATED)
async def add_review(payload: Review,
                     user_uuid=Depends(get_user_id),
                     service: ReviewService = Depends(get_review_service)):
    return await service.add_document(payload.dict_with_user_uuid(user_uuid)), HTTPStatus.CREATED


@router.get('', status_code=HTTPStatus.OK)
async def get_review(sort: Sort,
                     movie_id: str = Query(..., description='UUID фильма'),
                     service: ReviewService = Depends(get_review_service)):
    return await service.get_review_rating(movie_id, sort.dict())


@router.delete('', status_code=HTTPStatus.ACCEPTED)
async def delete_review(review_id: str = Query(..., description='UUID Отзыва'),
                        user_uuid=Depends(get_user_id),
                        service: ReviewService = Depends(get_review_service)):
    if service.get_document(review_id)['user_uuid'] == user_uuid:
        return await service.delete_document(review_id), HTTPStatus.ACCEPTED
    return {'message': HTTPStatus.FORBIDDEN.description}, HTTPStatus.FORBIDDEN
