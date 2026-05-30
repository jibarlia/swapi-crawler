from app.models.vehicle import Vehicle
from app.repositories.base_repository import BaseRepository


class VehicleRepository(BaseRepository):
    model = Vehicle
