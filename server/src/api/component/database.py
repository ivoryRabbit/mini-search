import os
import logging
from typing import Optional

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker

from api.config.database import DatabaseConfig
from api.entity.base import Base

logger = logging.getLogger(__name__)

_engine: Optional[Engine] = None
_session = sessionmaker(expire_on_commit=False)


def init_connection() -> None:
    logger.info("Initiate database connection pool...")

    database_config = DatabaseConfig(
        host="pgvector-dev",
        port=5432,
        database="postgres",
        user=os.environ.get("POSTGRES_USER", "postgres"),
        password=os.environ.get("POSTGRES_PASSWORD", "postgres"),
        schema=os.environ.get("POSTGRES_SCHEMA", "dev"),
    )

    global _engine
    _engine = create_engine(
        url=database_config.url,
        connect_args={"options": f"-csearch_path={database_config.schema}"},
        echo=True,
    )
    _session.configure(bind=_engine)
    Base.metadata.create_all(_engine)

    logger.info("Finished acquiring pgvector connection...")


def close_connection() -> None:
    global _engine
    if _engine is not None:
        _engine.dispose()


def get_connection() -> Engine:
    global _engine
    assert _engine is not None
    return _engine


def get_session() -> sessionmaker:
    return _session
