from typing import Optional

from sqlmodel import Session

from app.api.schemas.person import PersonDetails
from app.models.film import Film
from app.models.person import Person
from app.models.planet import Planet
from app.models.species import Species
from app.models.starship import Starship
from app.models.vehicle import Vehicle
from app.repositories.person_film_repository import PersonFilmRepository
from app.repositories.person_repository import PersonRepository
from app.repositories.person_species_repository import PersonSpeciesRepository
from app.repositories.person_starship_repository import PersonStarshipRepository
from app.repositories.person_vehicle_repository import PersonVehicleRepository
from app.repositories.planet_repository import PlanetRepository


class PersonService:
    """Read-side queries for a person's relationships and composite detail view."""

    def __init__(self, session: Session):
        self._people = PersonRepository(session)
        self._planets = PlanetRepository(session)
        self._person_film = PersonFilmRepository(session)
        self._person_species = PersonSpeciesRepository(session)
        self._person_vehicle = PersonVehicleRepository(session)
        self._person_starship = PersonStarshipRepository(session)

    def get_person(self, person_id: int) -> Optional[Person]:
        return self._people.get_by_id(person_id)

    def get_films(self, person_id: int) -> list[Film]:
        return self._person_film.get_related(
            source_col="person_id",
            source_id=person_id,
            target_model=Film,
            target_col="film_id",
        )

    def get_starships(self, person_id: int) -> list[Starship]:
        return self._person_starship.get_related(
            source_col="person_id",
            source_id=person_id,
            target_model=Starship,
            target_col="starship_id",
        )

    def get_vehicles(self, person_id: int) -> list[Vehicle]:
        return self._person_vehicle.get_related(
            source_col="person_id",
            source_id=person_id,
            target_model=Vehicle,
            target_col="vehicle_id",
        )

    def get_species(self, person_id: int) -> list[Species]:
        return self._person_species.get_related(
            source_col="person_id",
            source_id=person_id,
            target_model=Species,
            target_col="species_id",
        )

    def get_homeworld(self, person: Person) -> Optional[Planet]:
        if person.homeworld_id is None:
            return None
        return self._planets.get_by_id(person.homeworld_id)

    def get_details(self, person_id: int) -> Optional[PersonDetails]:
        person = self._people.get_by_id(person_id)
        if person is None:
            return None
        return PersonDetails(
            **person.model_dump(),
            homeworld=self.get_homeworld(person),
            films=self.get_films(person_id),
            starships=self.get_starships(person_id),
            vehicles=self.get_vehicles(person_id),
            species=self.get_species(person_id),
        )
