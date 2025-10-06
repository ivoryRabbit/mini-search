import os
import logging
from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from sqlalchemy import insert, text

from api.component.database import get_session
from api.entity.movie import Movie

logger = logging.getLogger(__name__)

LOCAL_PREFIX = "/tmp/mini-search/model"
NUM_LISTS = 128
NUM_PROBES = 8


def download_model(app: FastAPI):
    logger.info("Start loading Sentence BERT model...")

    local_path = Path(LOCAL_PREFIX).resolve()
    local_path.mkdir(parents=True, exist_ok=True)

    model = SentenceTransformer(
        model_name_or_path="sentence-transformers/paraphrase-albert-small-v2",
        cache_folder=LOCAL_PREFIX,
    )
    app.state.sentence_bert = model
    logger.info("Finished downloading model...")

    with get_session().begin() as session:
        if session.query(Movie.id).first() is not None:
            logger.info("Dataset is already copied...")
            return

    movie_df = pd.read_csv(os.environ["movies_filename"])

    titles = movie_df["title"].to_list()
    vectors = model.encode(titles, batch_size=128)

    values = [
        dict(
            id=int(row.id),
            title=str(row.title),
            genres=str(row.genres),
            year=int(row.year),
            view=int(row.view),
            rating=float(row.rating),
            embedding=vector,
        )
        for row, vector in zip(movie_df.itertuples(index=False), vectors)
    ]

    with get_session().begin() as session:
        session.execute(insert(Movie), values)
        session.execute(
            text(
                f"""
                    CREATE INDEX ON {Movie.__tablename__}
                    USING ivfflat (embedding vector_cosine_ops) WITH (lists = :lists)
                """
            ).bindparams(lists=NUM_LISTS)
        )
        session.execute(
            text("SET ivfflat.probes = :probes").bindparams(probes=NUM_PROBES)
        )

    logger.info("Finished uploading data...")
