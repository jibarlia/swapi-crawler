from app.models.links import FilmVehicle
from app.repositories.link_repository import BaseLinkRepository


class FilmVehicleRepository(BaseLinkRepository):
    model = FilmVehicle
    pk_columns = ["film_id", "vehicle_id"]
