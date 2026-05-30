from unittest.mock import MagicMock

import pytest

from app.services.crawler_service import (
    CrawlerService,
    _extract_id,
    _film_planet_pairs,
    _opt_str,
    _person_film_pairs,
    _transform_film,
    _transform_person,
    _transform_starship,
)

SAMPLE_PERSON = {
    "name": "Luke Skywalker",
    "height": "172",
    "mass": "77",
    "hair_color": "blond",
    "skin_color": "fair",
    "eye_color": "blue",
    "birth_year": "19BBY",
    "gender": "male",
    "homeworld": "https://swapi.info/api/planets/1",
    "films": ["https://swapi.info/api/films/1", "https://swapi.info/api/films/2"],
    "species": [],
    "vehicles": ["https://swapi.info/api/vehicles/14"],
    "starships": ["https://swapi.info/api/starships/12"],
    "created": "2014-12-09T13:50:51.644000Z",
    "edited": "2014-12-20T21:17:56.891000Z",
    "url": "https://swapi.info/api/people/1",
}

SAMPLE_FILM = {
    "title": "A New Hope",
    "episode_id": 4,
    "opening_crawl": "It is a period of civil war...",
    "director": "George Lucas",
    "producer": "Gary Kurtz, Rick McCallum",
    "release_date": "1977-05-25",
    "characters": ["https://swapi.info/api/people/1"],
    "planets": ["https://swapi.info/api/planets/1", "https://swapi.info/api/planets/2"],
    "starships": ["https://swapi.info/api/starships/2"],
    "vehicles": [],
    "species": ["https://swapi.info/api/species/1"],
    "created": "2014-12-10T14:23:31.880000Z",
    "edited": "2014-12-20T19:49:45.256000Z",
    "url": "https://swapi.info/api/films/1",
}

SAMPLE_STARSHIP = {
    "name": "CR90 corvette",
    "model": "CR90 corvette",
    "manufacturer": "Corellian Engineering Corporation",
    "cost_in_credits": "3500000",
    "length": "150",
    "max_atmosphering_speed": "950",
    "crew": "30-165",
    "passengers": "600",
    "cargo_capacity": "3000000",
    "consumables": "1 year",
    "hyperdrive_rating": "2.0",
    "MGLT": "60",
    "starship_class": "corvette",
    "pilots": [],
    "films": ["https://swapi.info/api/films/1"],
    "created": "2014-12-10T14:20:33.369000Z",
    "edited": "2014-12-20T21:23:49.867000Z",
    "url": "https://swapi.info/api/starships/2",
}


class TestExtractId:
    def test_normal_url(self):
        assert _extract_id("https://swapi.info/api/people/1") == 1

    def test_trailing_slash(self):
        assert _extract_id("https://swapi.info/api/people/83/") == 83

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            _extract_id("https://swapi.info/api/people/")


class TestOptStr:
    def test_none_returns_none(self):
        assert _opt_str(None) is None

    def test_empty_string_returns_none(self):
        assert _opt_str("") is None

    def test_unknown_preserved(self):
        assert _opt_str("unknown") == "unknown"

    def test_na_preserved(self):
        assert _opt_str("n/a") == "n/a"

    def test_normal_value(self):
        assert _opt_str("172") == "172"


class TestTransformPerson:
    def test_happy_path(self):
        result = _transform_person(SAMPLE_PERSON)
        assert result["id"] == 1
        assert result["name"] == "Luke Skywalker"
        assert result["height"] == "172"
        assert result["homeworld_id"] == 1
        assert result["created_at"].year == 2014

    def test_unknown_fields_preserved(self):
        raw = {**SAMPLE_PERSON, "height": "unknown", "mass": "unknown"}
        result = _transform_person(raw)
        assert result["height"] == "unknown"
        assert result["mass"] == "unknown"

    def test_empty_string_becomes_none(self):
        raw = {**SAMPLE_PERSON, "gender": "", "homeworld": None}
        result = _transform_person(raw)
        assert result["gender"] is None
        assert result["homeworld_id"] is None


class TestTransformStarship:
    def test_mglt_mapped_to_snake_case(self):
        result = _transform_starship(SAMPLE_STARSHIP)
        assert result["id"] == 2
        assert result["mglt"] == "60"
        assert "MGLT" not in result

    def test_starship_class(self):
        result = _transform_starship(SAMPLE_STARSHIP)
        assert result["starship_class"] == "corvette"


class TestTransformFilm:
    def test_happy_path(self):
        result = _transform_film(SAMPLE_FILM)
        assert result["id"] == 1
        assert result["title"] == "A New Hope"
        assert result["episode_id"] == 4
        assert result["release_date"] == "1977-05-25"


class TestLinkPairs:
    def test_person_film_pairs(self):
        pairs = _person_film_pairs([SAMPLE_PERSON])
        assert {"person_id": 1, "film_id": 1} in pairs
        assert {"person_id": 1, "film_id": 2} in pairs
        assert len(pairs) == 2

    def test_person_film_pairs_empty_films(self):
        raw = {**SAMPLE_PERSON, "films": []}
        pairs = _person_film_pairs([raw])
        assert pairs == []

    def test_film_planet_pairs(self):
        pairs = _film_planet_pairs([SAMPLE_FILM])
        assert {"film_id": 1, "planet_id": 1} in pairs
        assert {"film_id": 1, "planet_id": 2} in pairs
        assert len(pairs) == 2


class TestCrawlerService:
    def test_crawl_calls_all_fetchers_and_repos(self, mocker):
        mock_client = MagicMock()
        mock_client.fetch_all_people.return_value = [SAMPLE_PERSON]
        mock_client.fetch_all_films.return_value = [SAMPLE_FILM]
        mock_client.fetch_all_planets.return_value = []
        mock_client.fetch_all_species.return_value = []
        mock_client.fetch_all_vehicles.return_value = []
        mock_client.fetch_all_starships.return_value = [SAMPLE_STARSHIP]

        mock_session = MagicMock()

        mocker.patch("app.services.crawler_service.PersonRepository")
        mocker.patch("app.services.crawler_service.FilmRepository")
        mocker.patch("app.services.crawler_service.PlanetRepository")
        mocker.patch("app.services.crawler_service.SpeciesRepository")
        mocker.patch("app.services.crawler_service.VehicleRepository")
        mocker.patch("app.services.crawler_service.StarshipRepository")
        mocker.patch("app.services.crawler_service.PersonFilmRepository")
        mocker.patch("app.services.crawler_service.PersonSpeciesRepository")
        mocker.patch("app.services.crawler_service.PersonVehicleRepository")
        mocker.patch("app.services.crawler_service.PersonStarshipRepository")
        mocker.patch("app.services.crawler_service.FilmPlanetRepository")
        mocker.patch("app.services.crawler_service.FilmVehicleRepository")
        mocker.patch("app.services.crawler_service.FilmStarshipRepository")
        mocker.patch("app.services.crawler_service.FilmSpeciesRepository")

        service = CrawlerService(client=mock_client, session=mock_session)
        service.crawl()

        mock_client.fetch_all_people.assert_called_once()
        mock_client.fetch_all_films.assert_called_once()
        mock_client.fetch_all_planets.assert_called_once()
        mock_client.fetch_all_species.assert_called_once()
        mock_client.fetch_all_vehicles.assert_called_once()
        mock_client.fetch_all_starships.assert_called_once()
