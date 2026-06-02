from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import agents, auth, executions, health, workflows
from app.api.errors import orqis_error_handler
from app.config import get_settings
from app.core.exceptions import OrqisError
from app.db.arango import close_db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    close_db()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_exception_handler(OrqisError, orqis_error_handler)

    app.include_router(health.router)
    prefix = settings.api_prefix
    app.include_router(auth.router, prefix=prefix)
    app.include_router(agents.router, prefix=prefix)
    app.include_router(workflows.router, prefix=prefix)
    app.include_router(executions.router, prefix=prefix)

    return app


app = create_app()
