from typing import Optional

from domain.grpc_auth.protos import auth_pb2_grpc

channel = None

stub: Optional[auth_pb2_grpc.AuthStub] = None


async def get_stub() -> auth_pb2_grpc.AuthStub:
    return stub
