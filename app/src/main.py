from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi

from app.src.exception.global_exception_handler import (
    all_exception_handler,
    http_exception_handler,
)
from app.src.middleware.auth_middleware import authorization_middleware
from app.src.route.ping_route import router as ping_router
from app.src.route.token_route import router as auth_router
from app.src.route.user_route import router as user_router
from app.src.route.content_route import router as content_router

app = FastAPI()


def custom_openapi():
    # custom for security
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Blog Backend API",
        version="1.0.0",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }

    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.middleware("http")(authorization_middleware)

app.include_router(ping_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(content_router)


app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, all_exception_handler)


@app.get("/")
def home():
    return "backend is running..."
