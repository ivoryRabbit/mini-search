import logging
from typing import List

from sqlalchemy import select

from api.component.database import get_session
from api.entity.movie import Movie
from api.model.movie_dto import MovieDTO

logger = logging.getLogger(__name__)


class MovieRepository:
    def __init__(self) -> None:
        self._session = get_session()

    def search_by_vector(self, query_vector: List[float], size: int) -> List[MovieDTO]:
        with self._session.begin() as session:
            rows = session.scalars(
                select(Movie)
                .order_by(Movie.embedding.cosine_distance(query_vector))
                .limit(size)
            ).all()

        if rows is None:
            return list()

        return [MovieDTO.deserialize(row) for row in rows]
