from app.models.links import PersonVehicle
from app.repositories.link_repository import BaseLinkRepository


class PersonVehicleRepository(BaseLinkRepository):
    model = PersonVehicle
    pk_columns = ["person_id", "vehicle_id"]
