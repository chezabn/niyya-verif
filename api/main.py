import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from api import __name__, __version__
from api.config import Config

logger = logging.Logger(__name__)
cfg: Config = Config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {__name__} with {__version__}")
    yield
    logger.info(f"Stopping {__name__} with {__version__}...")


app = FastAPI(
    title=__name__,
    description=cfg.description,
    version=__version__,
    root_path=cfg.root_path,
    lifespan=lifespan,
)

app.include_router(healthcheck.router)

