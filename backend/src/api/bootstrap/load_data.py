import os
import logging
import subprocess
import zipfile
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

LOCAL_PREFIX = "/tmp/mini-search/dataset"
FILENAME = "ml-latest-small"
MARKER = "_SUCCESS"


def download_data():
    logger.info("Start loading MovieLens dataset...")

    local_path = Path(LOCAL_PREFIX).resolve()
    local_path.mkdir(parents=True, exist_ok=True)

    os.environ["movies_filename"] = f"{LOCAL_PREFIX}/movies.csv"

    marker_path = str(local_path.joinpath(MARKER))

    if Path(marker_path).is_file() is True:
        logger.info("MovieLens dataset already exists...")
        return

    try:
        download_url = f"https://files.grouplens.org/datasets/movielens/{FILENAME}.zip"
        subprocess.check_call(f"curl -o {LOCAL_PREFIX}/{FILENAME}.zip {download_url}", shell=True)

        file_zip = zipfile.ZipFile(f"{LOCAL_PREFIX}/{FILENAME}.zip")
        file_zip.extractall(local_path)

        ratings = pd.read_csv(
            f"{LOCAL_PREFIX}/{FILENAME}/ratings.csv",
            names=["user_id", "movie_id", "rating", "timestamp"],
            header=0,
            engine="python",
        )

        movie_ratings = (
            ratings
            .groupby("movie_id", as_index=False)
            .agg(view=("user_id", "count"), rating=("rating", "mean"))
        )

        movies = pd.read_csv(
            f"{LOCAL_PREFIX}/{FILENAME}/movies.csv",
            names=["id", "title", "genres"],
            header=0,
            engine="python",
        )

        movies[["title", "year"]] = movies["title"].str.extract(
            r"(?P<title>.*) [(](?P<year>\d{4})[)]$"
        )

        movies = (
            movies
            .dropna()
            .merge(
                movie_ratings,
                how="left",
                left_on="id",
                right_on="movie_id"
            )
            .fillna(value={"view": 0, "rating": 0.0})
        )

        movies.to_csv(os.environ["movies_filename"], index=False)

        subprocess.check_call(f"rm {LOCAL_PREFIX}/{FILENAME}.zip", shell=True)
        subprocess.check_call(f"rm -rf {LOCAL_PREFIX}/{FILENAME}", shell=True)
        subprocess.check_call(f"touch {marker_path}", shell=True)

        logger.info("Finished downloading dataset...")

    except Exception as ex:
        subprocess.check_call(f"rm -rf {LOCAL_PREFIX}", shell=True)

        logger.info("Failed to download dataset...: %s", ex)
