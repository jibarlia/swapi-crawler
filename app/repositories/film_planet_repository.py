from app.models.links import FilmPlanet
from app.repositories.link_repository import BaseLinkRepository


class FilmPlanetRepository(BaseLinkRepository):
    model = FilmPlanet
    pk_columns = ["film_id", "planet_id"]
