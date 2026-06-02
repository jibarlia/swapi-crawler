from app.models.film import Film
from app.models.person import Person
from app.models.planet import Planet
from app.models.species import Species
from app.models.starship import Starship
from app.models.vehicle import Vehicle
from app.services.person_service import PersonService

PERSON = Person(id=1, name="Luke Skywalker", homeworld_id=1)


def _make_service(mocker) -> PersonService:
    """Build a PersonService whose repository deps are all mocked (no DB)."""
    mocker.patch("app.services.person_service.PersonRepository")
    mocker.patch("app.services.person_service.PlanetRepository")
    mocker.patch("app.services.person_service.PersonFilmRepository")
    mocker.patch("app.services.person_service.PersonSpeciesRepository")
    mocker.patch("app.services.person_service.PersonVehicleRepository")
    mocker.patch("app.services.person_service.PersonStarshipRepository")
    return PersonService(session=mocker.MagicMock())


class TestGetRelations:
    def test_get_films_queries_join_table_with_correct_args(self, mocker):
        service = _make_service(mocker)
        films = [Film(id=1, title="A New Hope")]
        service._person_film.get_related.return_value = films

        result = service.get_films(1)

        assert result == films
        service._person_film.get_related.assert_called_once_with(
            source_col="person_id",
            source_id=1,
            target_model=Film,
            target_col="film_id",
        )

    def test_get_starships_uses_starship_target(self, mocker):
        service = _make_service(mocker)
        service._person_starship.get_related.return_value = []

        service.get_starships(1)

        service._person_starship.get_related.assert_called_once_with(
            source_col="person_id",
            source_id=1,
            target_model=Starship,
            target_col="starship_id",
        )

    def test_get_vehicles_uses_vehicle_target(self, mocker):
        service = _make_service(mocker)
        service._person_vehicle.get_related.return_value = []

        service.get_vehicles(1)

        service._person_vehicle.get_related.assert_called_once_with(
            source_col="person_id",
            source_id=1,
            target_model=Vehicle,
            target_col="vehicle_id",
        )

    def test_get_species_uses_species_target(self, mocker):
        service = _make_service(mocker)
        service._person_species.get_related.return_value = []

        service.get_species(1)

        service._person_species.get_related.assert_called_once_with(
            source_col="person_id",
            source_id=1,
            target_model=Species,
            target_col="species_id",
        )


class TestGetHomeworld:
    def test_returns_planet_when_homeworld_id_set(self, mocker):
        service = _make_service(mocker)
        planet = Planet(id=1, name="Tatooine")
        service._planets.get_by_id.return_value = planet

        assert service.get_homeworld(PERSON) is planet
        service._planets.get_by_id.assert_called_once_with(1)

    def test_returns_none_when_no_homeworld(self, mocker):
        service = _make_service(mocker)

        assert service.get_homeworld(Person(id=2, name="Droid")) is None
        service._planets.get_by_id.assert_not_called()


class TestGetDetails:
    def test_returns_none_when_person_missing(self, mocker):
        service = _make_service(mocker)
        service._people.get_by_id.return_value = None

        assert service.get_details(999) is None
        service._person_film.get_related.assert_not_called()

    def test_assembles_nested_details(self, mocker):
        service = _make_service(mocker)
        service._people.get_by_id.return_value = PERSON
        service._planets.get_by_id.return_value = Planet(id=1, name="Tatooine")
        service._person_film.get_related.return_value = [Film(id=1, title="A New Hope")]
        service._person_starship.get_related.return_value = [
            Starship(id=2, name="CR90 corvette")
        ]
        service._person_vehicle.get_related.return_value = []
        service._person_species.get_related.return_value = []

        details = service.get_details(1)

        assert details is not None
        assert details.id == 1
        assert details.name == "Luke Skywalker"
        assert details.homeworld.name == "Tatooine"
        assert [f.title for f in details.films] == ["A New Hope"]
        assert [s.name for s in details.starships] == ["CR90 corvette"]
        assert details.vehicles == []
        assert details.species == []
