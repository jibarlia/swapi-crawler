from typing import Optional

from sqlmodel import Session

from app.models.film import Film
from app.models.person import Person
from app.models.planet import Planet
from app.models.species import Species
from app.models.starship import Starship
from app.models.vehicle import Vehicle
from app.repositories.film_repository import FilmRepository
from app.repositories.person_repository import PersonRepository
from app.repositories.planet_repository import PlanetRepository
from app.repositories.species_repository import SpeciesRepository
from app.repositories.starship_repository import StarshipRepository
from app.repositories.vehicle_repository import VehicleRepository


class EntityService:
    def __init__(self, session: Session):
        self._people = PersonRepository(session)
        self._films = FilmRepository(session)
        self._planets = PlanetRepository(session)
        self._species = SpeciesRepository(session)
        self._vehicles = VehicleRepository(session)
        self._starships = StarshipRepository(session)

    def list_people(self, offset: int = 0, limit: int = 20) -> list[Person]:
        return self._people.get_all(offset=offset, limit=limit)

    def get_person(self, person_id: int) -> Optional[Person]:
        return self._people.get_by_id(person_id)

    def list_films(self, offset: int = 0, limit: int = 20) -> list[Film]:
        return self._films.get_all(offset=offset, limit=limit)

    def get_film(self, film_id: int) -> Optional[Film]:
        return self._films.get_by_id(film_id)

    def list_planets(self, offset: int = 0, limit: int = 20) -> list[Planet]:
        return self._planets.get_all(offset=offset, limit=limit)

    def get_planet(self, planet_id: int) -> Optional[Planet]:
        return self._planets.get_by_id(planet_id)

    def list_species(self, offset: int = 0, limit: int = 20) -> list[Species]:
        return self._species.get_all(offset=offset, limit=limit)

    def get_species(self, species_id: int) -> Optional[Species]:
        return self._species.get_by_id(species_id)

    def list_vehicles(self, offset: int = 0, limit: int = 20) -> list[Vehicle]:
        return self._vehicles.get_all(offset=offset, limit=limit)

    def get_vehicle(self, vehicle_id: int) -> Optional[Vehicle]:
        return self._vehicles.get_by_id(vehicle_id)

    def list_starships(self, offset: int = 0, limit: int = 20) -> list[Starship]:
        return self._starships.get_all(offset=offset, limit=limit)

    def get_starship(self, starship_id: int) -> Optional[Starship]:
        return self._starships.get_by_id(starship_id)
