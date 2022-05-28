from dataclasses import dataclass


@dataclass(frozen=True)
class MovieModel:
    user_uuid: str
    movie_uuid: str
    genre_uuid: str
    movie_second: int
    movie_length: int
    current_date: str
