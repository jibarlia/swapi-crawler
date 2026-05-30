from app.models.links import PersonSpecies
from app.repositories.link_repository import BaseLinkRepository


class PersonSpeciesRepository(BaseLinkRepository):
    model = PersonSpecies
    pk_columns = ["person_id", "species_id"]
