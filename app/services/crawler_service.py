import re
from datetime import datetime, timezone
from typing import Any, Optional

from sqlmodel import Session

from app.clients.public_api_client import SWAPIClient
from app.repositories.film_planet_repository import FilmPlanetRepository
from app.repositories.film_repository import FilmRepository
from app.repositories.film_species_repository import FilmSpeciesRepository
from app.repositories.film_starship_repository import FilmStarshipRepository
from app.repositories.film_vehicle_repository import FilmVehicleRepository
from app.repositories.person_film_repository import PersonFilmRepository
from app.repositories.person_repository import PersonRepository
from app.repositories.person_species_repository import PersonSpeciesRepository
from app.repositories.person_starship_repository import PersonStarshipRepository
from app.repositories.person_vehicle_repository import PersonVehicleRepository
from app.repositories.planet_repository import PlanetRepository
from app.repositories.species_repository import SpeciesRepository
from app.repositories.starship_repository import StarshipRepository
from app.repositories.vehicle_repository import VehicleRepository


def _extract_id(url: str) -> int:
    match = re.search(r"/(\d+)/?$", url)
    if not match:
        raise ValueError(f"Cannot extract ID from URL: {url!r}")
    return int(match.group(1))


def _opt_str(value: Any) -> Optional[str]:
    if value is None or value == "":
        return None
    return str(value)


def _parse_dt(value: Any) -> Optional[datetime]:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except (ValueError, AttributeError):
        return None


def _transform_person(raw: dict) -> dict:
    homeworld = raw.get("homeworld")
    return {
        "id": _extract_id(raw["url"]),
        "name": raw["name"],
        "height": _opt_str(raw.get("height")),
        "mass": _opt_str(raw.get("mass")),
        "hair_color": _opt_str(raw.get("hair_color")),
        "skin_color": _opt_str(raw.get("skin_color")),
        "eye_color": _opt_str(raw.get("eye_color")),
        "birth_year": _opt_str(raw.get("birth_year")),
        "gender": _opt_str(raw.get("gender")),
        "homeworld_id": _extract_id(homeworld) if homeworld else None,
        "url": raw.get("url"),
        "created_at": _parse_dt(raw.get("created")),
        "updated_at": _parse_dt(raw.get("edited")),
    }


def _transform_film(raw: dict) -> dict:
    return {
        "id": _extract_id(raw["url"]),
        "title": raw["title"],
        "episode_id": raw.get("episode_id"),
        "opening_crawl": _opt_str(raw.get("opening_crawl")),
        "director": _opt_str(raw.get("director")),
        "producer": _opt_str(raw.get("producer")),
        "release_date": _opt_str(raw.get("release_date")),
        "url": raw.get("url"),
        "created_at": _parse_dt(raw.get("created")),
        "updated_at": _parse_dt(raw.get("edited")),
    }


def _transform_planet(raw: dict) -> dict:
    return {
        "id": _extract_id(raw["url"]),
        "name": raw["name"],
        "rotation_period": _opt_str(raw.get("rotation_period")),
        "orbital_period": _opt_str(raw.get("orbital_period")),
        "diameter": _opt_str(raw.get("diameter")),
        "climate": _opt_str(raw.get("climate")),
        "gravity": _opt_str(raw.get("gravity")),
        "terrain": _opt_str(raw.get("terrain")),
        "surface_water": _opt_str(raw.get("surface_water")),
        "population": _opt_str(raw.get("population")),
        "url": raw.get("url"),
        "created_at": _parse_dt(raw.get("created")),
        "updated_at": _parse_dt(raw.get("edited")),
    }


def _transform_species(raw: dict) -> dict:
    homeworld = raw.get("homeworld")
    return {
        "id": _extract_id(raw["url"]),
        "name": raw["name"],
        "classification": _opt_str(raw.get("classification")),
        "designation": _opt_str(raw.get("designation")),
        "average_height": _opt_str(raw.get("average_height")),
        "skin_colors": _opt_str(raw.get("skin_colors")),
        "hair_colors": _opt_str(raw.get("hair_colors")),
        "eye_colors": _opt_str(raw.get("eye_colors")),
        "average_lifespan": _opt_str(raw.get("average_lifespan")),
        "homeworld_id": _extract_id(homeworld) if homeworld else None,
        "language": _opt_str(raw.get("language")),
        "url": raw.get("url"),
        "created_at": _parse_dt(raw.get("created")),
        "updated_at": _parse_dt(raw.get("edited")),
    }


def _transform_vehicle(raw: dict) -> dict:
    return {
        "id": _extract_id(raw["url"]),
        "name": raw["name"],
        "model": _opt_str(raw.get("model")),
        "manufacturer": _opt_str(raw.get("manufacturer")),
        "cost_in_credits": _opt_str(raw.get("cost_in_credits")),
        "length": _opt_str(raw.get("length")),
        "max_atmosphering_speed": _opt_str(raw.get("max_atmosphering_speed")),
        "crew": _opt_str(raw.get("crew")),
        "passengers": _opt_str(raw.get("passengers")),
        "cargo_capacity": _opt_str(raw.get("cargo_capacity")),
        "consumables": _opt_str(raw.get("consumables")),
        "vehicle_class": _opt_str(raw.get("vehicle_class")),
        "url": raw.get("url"),
        "created_at": _parse_dt(raw.get("created")),
        "updated_at": _parse_dt(raw.get("edited")),
    }


def _transform_starship(raw: dict) -> dict:
    return {
        "id": _extract_id(raw["url"]),
        "name": raw["name"],
        "model": _opt_str(raw.get("model")),
        "manufacturer": _opt_str(raw.get("manufacturer")),
        "cost_in_credits": _opt_str(raw.get("cost_in_credits")),
        "length": _opt_str(raw.get("length")),
        "max_atmosphering_speed": _opt_str(raw.get("max_atmosphering_speed")),
        "crew": _opt_str(raw.get("crew")),
        "passengers": _opt_str(raw.get("passengers")),
        "cargo_capacity": _opt_str(raw.get("cargo_capacity")),
        "consumables": _opt_str(raw.get("consumables")),
        "hyperdrive_rating": _opt_str(raw.get("hyperdrive_rating")),
        "mglt": _opt_str(raw.get("MGLT")),
        "starship_class": _opt_str(raw.get("starship_class")),
        "url": raw.get("url"),
        "created_at": _parse_dt(raw.get("created")),
        "updated_at": _parse_dt(raw.get("edited")),
    }


def _person_film_pairs(raw_people: list[dict]) -> list[dict]:
    return [
        {"person_id": _extract_id(p["url"]), "film_id": _extract_id(url)}
        for p in raw_people
        for url in (p.get("films") or [])
    ]


def _person_species_pairs(raw_people: list[dict]) -> list[dict]:
    return [
        {"person_id": _extract_id(p["url"]), "species_id": _extract_id(url)}
        for p in raw_people
        for url in (p.get("species") or [])
    ]


def _person_vehicle_pairs(raw_people: list[dict]) -> list[dict]:
    return [
        {"person_id": _extract_id(p["url"]), "vehicle_id": _extract_id(url)}
        for p in raw_people
        for url in (p.get("vehicles") or [])
    ]


def _person_starship_pairs(raw_people: list[dict]) -> list[dict]:
    return [
        {"person_id": _extract_id(p["url"]), "starship_id": _extract_id(url)}
        for p in raw_people
        for url in (p.get("starships") or [])
    ]


def _film_planet_pairs(raw_films: list[dict]) -> list[dict]:
    return [
        {"film_id": _extract_id(f["url"]), "planet_id": _extract_id(url)}
        for f in raw_films
        for url in (f.get("planets") or [])
    ]


def _film_vehicle_pairs(raw_films: list[dict]) -> list[dict]:
    return [
        {"film_id": _extract_id(f["url"]), "vehicle_id": _extract_id(url)}
        for f in raw_films
        for url in (f.get("vehicles") or [])
    ]


def _film_starship_pairs(raw_films: list[dict]) -> list[dict]:
    return [
        {"film_id": _extract_id(f["url"]), "starship_id": _extract_id(url)}
        for f in raw_films
        for url in (f.get("starships") or [])
    ]


def _film_species_pairs(raw_films: list[dict]) -> list[dict]:
    return [
        {"film_id": _extract_id(f["url"]), "species_id": _extract_id(url)}
        for f in raw_films
        for url in (f.get("species") or [])
    ]


class CrawlerService:
    def __init__(self, client: SWAPIClient, session: Session):
        self._client = client
        self._people_repo = PersonRepository(session)
        self._film_repo = FilmRepository(session)
        self._planet_repo = PlanetRepository(session)
        self._species_repo = SpeciesRepository(session)
        self._vehicle_repo = VehicleRepository(session)
        self._starship_repo = StarshipRepository(session)
        self._person_film_repo = PersonFilmRepository(session)
        self._person_species_repo = PersonSpeciesRepository(session)
        self._person_vehicle_repo = PersonVehicleRepository(session)
        self._person_starship_repo = PersonStarshipRepository(session)
        self._film_planet_repo = FilmPlanetRepository(session)
        self._film_vehicle_repo = FilmVehicleRepository(session)
        self._film_starship_repo = FilmStarshipRepository(session)
        self._film_species_repo = FilmSpeciesRepository(session)

    def crawl(self) -> dict[str, int]:
        raw_people = self._client.fetch_all_people()
        raw_films = self._client.fetch_all_films()
        raw_planets = self._client.fetch_all_planets()
        raw_species = self._client.fetch_all_species()
        raw_vehicles = self._client.fetch_all_vehicles()
        raw_starships = self._client.fetch_all_starships()

        counts = {
            "planets": self._planet_repo.upsert_batch([_transform_planet(p) for p in raw_planets]),
            "species": self._species_repo.upsert_batch([_transform_species(s) for s in raw_species]),
            "people": self._people_repo.upsert_batch([_transform_person(p) for p in raw_people]),
            "films": self._film_repo.upsert_batch([_transform_film(f) for f in raw_films]),
            "vehicles": self._vehicle_repo.upsert_batch([_transform_vehicle(v) for v in raw_vehicles]),
            "starships": self._starship_repo.upsert_batch([_transform_starship(s) for s in raw_starships]),
        }

        self._person_film_repo.upsert_batch(_person_film_pairs(raw_people))
        self._person_species_repo.upsert_batch(_person_species_pairs(raw_people))
        self._person_vehicle_repo.upsert_batch(_person_vehicle_pairs(raw_people))
        self._person_starship_repo.upsert_batch(_person_starship_pairs(raw_people))
        self._film_planet_repo.upsert_batch(_film_planet_pairs(raw_films))
        self._film_vehicle_repo.upsert_batch(_film_vehicle_pairs(raw_films))
        self._film_starship_repo.upsert_batch(_film_starship_pairs(raw_films))
        self._film_species_repo.upsert_batch(_film_species_pairs(raw_films))

        return counts
