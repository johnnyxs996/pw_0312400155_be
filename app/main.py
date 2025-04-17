import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from app.api import api_router
from app.api.common.errors import GenericException
from app.core.config import settings
from app.db import create_db_and_tables

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup DataBase on app startup
    create_db_and_tables()
    yield


app = FastAPI(
    title="Financial Management API",
    description="API for managing a financial system",
    lifespan=lifespan
)
add_pagination(app)


@app.exception_handler(GenericException)
async def unicorn_generic_exception_handler(request: Request, exc: GenericException):
    return JSONResponse(
        status_code=exc.status_code,
        content=dict(
            message=exc.message,
            type=exc.type)
    )


app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        settings.APP,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
