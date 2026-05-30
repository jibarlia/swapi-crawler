from app.models.links import PersonFilm
from app.repositories.link_repository import BaseLinkRepository


class PersonFilmRepository(BaseLinkRepository):
    model = PersonFilm
    pk_columns = ["person_id", "film_id"]
