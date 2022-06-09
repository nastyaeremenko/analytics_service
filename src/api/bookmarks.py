from http import HTTPStatus
from fastapi import APIRouter, Depends, Query

from api.serializers import Bookmark
from domain.movie_services.bookmark import (get_bookmarks_service, BookmarkService)
from domain.grpc_auth.dependencies import get_user_id

router = APIRouter()


@router.post('', status_code=HTTPStatus.CREATED)
async def add_bookmark(payload: Bookmark,
                       user_uuid=Depends(get_user_id),
                       service: BookmarkService = Depends(get_bookmarks_service)):
    return await service.add_document(payload.dict_with_user_uuid(user_uuid)), HTTPStatus.CREATED


@router.get('', status_code=HTTPStatus.OK)
async def get_bookmarks(
        user_uuid=Depends(get_user_id), service: BookmarkService = Depends(get_bookmarks_service)
):
    return await service.get_bookmarks(user_uuid)


@router.delete('', status_code=HTTPStatus.ACCEPTED)
async def delete_bookmark(bookmark_id: str = Query(..., description='UUID закладки'),
                          user_uuid=Depends(get_user_id),
                          service: BookmarkService = Depends(get_bookmarks_service)):
    if service.get_document(bookmark_id)['user_uuid'] == user_uuid:
        return await service.delete_document(bookmark_id), HTTPStatus.ACCEPTED
    return {'message': HTTPStatus.FORBIDDEN.description}, HTTPStatus.FORBIDDEN
