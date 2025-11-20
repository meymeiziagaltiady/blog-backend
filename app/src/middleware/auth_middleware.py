from fastapi import Request, status
from fnmatch import fnmatch
from fastapi.responses import JSONResponse
from starlette.middleware.base import RequestResponseEndpoint

from app.src.jwt.jwt_handler import get_user_data, get_token
from app.src.schema.response_schema import ApiResponse

ROUTE_PERMISSION = {
    "/users/*": "admin",
    "/content/*": "*",
}


def get_required_role(path: str):
    for pattern, role in ROUTE_PERMISSION.items():
        if fnmatch(path, pattern):
            return role
    return None


async def authorization_middleware(
    request: Request, call_next: RequestResponseEndpoint
):

    path = request.url.path
    required_role = get_required_role(path)

    # public route
    if required_role is None:
        return await call_next(request)

    # get user
    try:
        token = get_token(request)
        user = get_user_data(token)
    except Exception as e:
        return JSONResponse(
            status_code=401,
            content=ApiResponse.error(
                message=str(e), status_code=status.HTTP_401_UNAUTHORIZED
            ).model_dump(),
        )

    # role validation
    if required_role and required_role != "*" and user.role != required_role:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=ApiResponse.error(
                message=f"Forbidden: insufficient role ({required_role} only)",
                status_code=status.HTTP_403_FORBIDDEN,
            ).model_dump(),
        )

    request.state.user = user

    return await call_next(request)
