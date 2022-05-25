from http import HTTPStatus

import grpc
from fastapi import Depends, HTTPException

from domain.grpc_auth.client import get_stub
from domain.grpc_auth.protos import auth_pb2, auth_pb2_grpc
from domain.http_response import HttpResponse
from helpers import get_auth_token


def invalid_response(error):
    if error.code() == grpc.StatusCode.UNAUTHENTICATED:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=error.details())

    raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail=HttpResponse.grpc_503)


async def get_user_id(token: str = Depends(get_auth_token),
                      stub: auth_pb2_grpc.AuthStub = Depends(get_stub)):
    grpc_token = auth_pb2.Token(token=token)
    try:
        response = await stub.GetUser(grpc_token)
        return response.user_id

    except grpc.RpcError as error:
        invalid_response(error)
