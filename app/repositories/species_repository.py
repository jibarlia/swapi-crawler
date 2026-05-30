from app.models.species import Species
from app.repositories.base_repository import BaseRepository


class SpeciesRepository(BaseRepository):
    model = Species
