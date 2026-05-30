from app.models.starship import Starship
from app.repositories.base_repository import BaseRepository


class StarshipRepository(BaseRepository):
    model = Starship
