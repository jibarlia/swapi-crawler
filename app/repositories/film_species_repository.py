from app.models.links import FilmSpecies
from app.repositories.link_repository import BaseLinkRepository


class FilmSpeciesRepository(BaseLinkRepository):
    model = FilmSpecies
    pk_columns = ["film_id", "species_id"]
