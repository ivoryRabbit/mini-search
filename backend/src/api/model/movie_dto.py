from dataclasses import dataclass
from typing import Optional, Dict, Any

from sqlalchemy import Row


@dataclass
class MovieDTO:
    id: int
    title: str
    genres: str
    year: int
    view: Optional[int] = None
    rating: Optional[float] = None

    def __post_init__(self) -> None:
        self.url = f"https://movielens.org/movies/{self.id}"
        self.genres = ", ".join(self.genres.split("|"))

    @classmethod
    def deserialize(cls, row: Row) -> 'MovieDTO':
        return cls(
            row.id,
            row.title,
            row.genres,
            row.year,
            row.view,
            row.rating,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.id,
            "title": self.title,
            "year": self.year,
            "genres": self.genres,
            "url": self.url,
            "view": self.view,
            "rating": self.rating,
        }
