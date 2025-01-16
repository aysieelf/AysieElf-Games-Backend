from contextlib import asynccontextmanager

from database.session import init_db
from fastapi import APIRouter, FastAPI
from src.api.v1.routes import api_router
from src.core.config import Settings, settings
from starlette.middleware.cors import CORSMiddleware
import uvicorn


class App:
    def __init__(
        self, settings: Settings = settings, api_router: APIRouter = api_router
    ):
        self.__app = FastAPI(
            title=settings.PROJECT_NAME,
            version="0.1.0",
            docs_url="/docs",
            redoc_url="/redoc",
            openapi_url="/openapi.json",
            lifespan=self.lifespan,
        )
        self.__setup_middlewares(settings=settings)
        self.__setup_routes(settings=settings, router=api_router)

    def __setup_middlewares(self, settings: Settings):
        # TODO: To be concretely defined in production
        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ALLOWED_HOSTS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def __setup_routes(self, router: APIRouter, settings: Settings):
        self.__app.include_router(router, prefix=settings.API_V1_STR)

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        init_db()
        yield

    def __call__(self):
        return self.__app


def create_app() -> FastAPI:
    return App(settings=settings, api_router=api_router)()


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
