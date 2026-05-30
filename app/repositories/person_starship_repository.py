from app.models.links import PersonStarship
from app.repositories.link_repository import BaseLinkRepository


class PersonStarshipRepository(BaseLinkRepository):
    model = PersonStarship
    pk_columns = ["person_id", "starship_id"]
