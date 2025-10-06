import gc
import yaml
import logging.config

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config.router import router
from api.config import bootstrap
from api.component import database

with open("resource/logging.yaml") as f:
    logging_config = yaml.load(f, Loader=yaml.FullLoader)
    logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="mini-search",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
async def app_startup() -> None:
    logger.info("App startup")

    # Bootstrap
    gc.freeze()
    database.init_connection()
    bootstrap.init_bootstrap(app)


@app.on_event("shutdown")
async def app_shutdown() -> None:
    logger.info("App shutdown")

    database.close_connection()


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8080,
        access_log=False,
        reload=True,
    )
