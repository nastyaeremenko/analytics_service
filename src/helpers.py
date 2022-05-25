from http import HTTPStatus
from typing import Optional

from fastapi import Header, HTTPException

from domain.http_response import HttpResponse


def get_auth_token(authorization: Optional[str] = Header(None)) -> str:
    if authorization and 'Bearer' in authorization:
        token = authorization.split(' ')[-1]
        return token
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=HttpResponse.token_404)
