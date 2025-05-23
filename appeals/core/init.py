from contextlib import asynccontextmanager
from fastapi import FastAPI

from appeals.config.config import Config
from appeals.core.routers import init_app
from appeals.db.db import init, close


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init()
    yield
    await close()


app = FastAPI(lifespan=lifespan)
init_app(app)


def run_server():
    import uvicorn
    uvicorn.run(
        "appeals.core.init:app",
        host=Config.api_host,
        port=Config.api_port,
        log_level="info"
    )


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
