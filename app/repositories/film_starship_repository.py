from app.models.links import FilmStarship
from app.repositories.link_repository import BaseLinkRepository


class FilmStarshipRepository(BaseLinkRepository):
    model = FilmStarship
    pk_columns = ["film_id", "starship_id"]
