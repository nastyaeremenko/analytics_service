from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class MovieModel:
    user_uuid: str
    movie_uuid: str
    movie_progress: int
    movie_length: int
    event_time: datetime
