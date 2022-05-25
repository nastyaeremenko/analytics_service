from http import HTTPStatus

from fastapi import APIRouter

from api.serializers import MovieProgress

router = APIRouter()


@router.post('', status_code=HTTPStatus.OK)
async def post_movie_progress(payload: MovieProgress):
    return {'message': 'Uploaded successfully'}
