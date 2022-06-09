from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.query_params import SortingParams
from api.serializers import Review, ReviewOut, ReviewRatings
from domain.grpc_auth.dependencies import get_user_id
from domain.movie_services.review import ReviewService, get_review_service

router = APIRouter()


@router.post('', status_code=HTTPStatus.CREATED, response_model=ReviewOut)
async def add_review(payload: Review,
                     user_uuid=Depends(get_user_id),
                     service: ReviewService = Depends(get_review_service)):
    response = await service.add_document(payload.dict_with_user_uuid(user_uuid))
    review = await service.get_document_by_id(response.inserted_id)
    return review


@router.get('/{movie_id}', status_code=HTTPStatus.OK, response_model=ReviewRatings)
async def get_review(movie_id: str,
                     sort: SortingParams = Depends(),
                     service: ReviewService = Depends(get_review_service)):
    reviews = await service.get_review_rating(movie_id, sort.__dict__)
    if reviews.__root__:
        return reviews

    return JSONResponse(content=[], status_code=HTTPStatus.NOT_FOUND)


@router.put('/{review_id}', status_code=HTTPStatus.OK, response_model=ReviewOut)
async def update_review(payload: Review,
                        review_id: str,
                        user_uuid=Depends(get_user_id),
                        service: ReviewService = Depends(get_review_service)):
    review = await service.get_document_by_id(review_id)

    if review and review['user_uuid'] == user_uuid:
        updated_payload = payload.dict_with_user_uuid(user_uuid)
        await service.update_document(review_id, updated_payload)
        updated_review = await service.get_document_by_id(review_id)
        return updated_review

    return JSONResponse(content={'message': HTTPStatus.FORBIDDEN.description},
                        status_code=HTTPStatus.FORBIDDEN)


@router.delete('/{review_id}', status_code=HTTPStatus.ACCEPTED)
async def delete_review(review_id: str,
                        user_uuid=Depends(get_user_id),
                        service: ReviewService = Depends(get_review_service)):
    review = await service.get_document_by_id(review_id)

    if review and review['user_uuid'] == user_uuid:
        await service.delete_document(review_id)
        return {'message': f'review was deleted: {review_id}'}

    return JSONResponse(content={'message': HTTPStatus.FORBIDDEN.description},
                        status_code=HTTPStatus.FORBIDDEN)
