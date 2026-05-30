from app.models.planet import Planet
from app.repositories.base_repository import BaseRepository


class PlanetRepository(BaseRepository):
    model = Planet
