from app.models.person import Person
from app.repositories.base_repository import BaseRepository


class PersonRepository(BaseRepository):
    model = Person
