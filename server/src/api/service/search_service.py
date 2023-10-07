from typing import List

from fastapi import Request, Depends

from api.model.movie_dto import MovieDTO
from api.repository.movie_repository import MovieRepository


class SearchService:
    def __init__(
        self,
        request: Request,
        movie_repository: MovieRepository = Depends()
    ):
        self.sentence_bert = request.app.state.sentence_bert
        self.movie_repository = movie_repository

    def get_relevant_movies(self, query: str, size: int) -> List[MovieDTO]:
        query_vector = (
            self.sentence_bert
                .encode(query)
                .flatten()
                .tolist()
        )
        return self.movie_repository.search_by_vector(query_vector, size)
