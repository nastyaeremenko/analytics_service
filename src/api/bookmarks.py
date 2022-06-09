from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from api.serializers import Bookmark, BookmarkOut
from domain.grpc_auth.dependencies import get_user_id
from domain.movie_services.bookmark import (BookmarkService,
                                            get_bookmarks_service)

router = APIRouter()


@router.post('', status_code=HTTPStatus.CREATED)
async def add_bookmark(payload: Bookmark,
                       user_uuid=Depends(get_user_id),
                       service: BookmarkService = Depends(get_bookmarks_service)):
    bookmark = await service.add_document(payload.dict_with_user_uuid(user_uuid))
    return {'message': f'bookmark was created: {bookmark.inserted_id}'}


@router.get('', status_code=HTTPStatus.OK, response_model=list[BookmarkOut])
async def get_bookmarks(user_uuid=Depends(get_user_id),
                        service: BookmarkService = Depends(get_bookmarks_service)):
    bookmarks = await service.get_bookmarks(user_uuid)
    return bookmarks


@router.delete('', status_code=HTTPStatus.ACCEPTED)
async def delete_bookmark(bookmark_id: str = Query(..., description='UUID закладки'),
                          user_uuid=Depends(get_user_id),
                          service: BookmarkService = Depends(get_bookmarks_service)):
    bookmark = await service.get_document_by_id(bookmark_id)

    if bookmark and bookmark['user_uuid'] == user_uuid:
        await service.delete_document(bookmark_id)
        return {'message': f'bookmark was deleted: {bookmark_id}'}

    return JSONResponse(content={'message': HTTPStatus.FORBIDDEN.description},
                        status_code=HTTPStatus.FORBIDDEN)
