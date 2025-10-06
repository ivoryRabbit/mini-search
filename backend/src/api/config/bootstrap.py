import logging

from fastapi import FastAPI

from api.bootstrap import load_data, load_model

logger = logging.getLogger(__name__)


def init_bootstrap(app: FastAPI) -> None:
    load_data.download_data()
    load_model.download_model(app)
