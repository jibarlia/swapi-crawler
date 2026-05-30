from app.models.film import Film
from app.repositories.base_repository import BaseRepository


class FilmRepository(BaseRepository):
    model = Film
