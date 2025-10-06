import logging
from typing import Dict, List

from fastapi import APIRouter, Depends, Query

from api.model.movie_dto import MovieDTO
from api.service.search_service import SearchService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/movies")
def get_movies(
    query: str = Query(),
    size: int = Query(default=10),
    search_service: SearchService = Depends(),
) -> List[MovieDTO]:
    return search_service.get_relevant_movies(query, size)
