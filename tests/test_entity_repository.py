from datetime import datetime, timezone

from app.repositories.film_repository import FilmRepository
from app.repositories.person_film_repository import PersonFilmRepository
from app.repositories.person_repository import PersonRepository

PERSON_1 = {
    "id": 1,
    "name": "Luke Skywalker",
    "height": "172",
    "mass": "77",
    "hair_color": "blond",
    "skin_color": "fair",
    "eye_color": "blue",
    "birth_year": "19BBY",
    "gender": "male",
    "homeworld_id": None,
    "url": "https://swapi.info/api/people/1",
    "created_at": datetime(2014, 12, 9, 13, 50, 51, tzinfo=timezone.utc),
    "updated_at": datetime(2014, 12, 20, 21, 17, 56, tzinfo=timezone.utc),
}

PERSON_2 = {
    "id": 2,
    "name": "C-3PO",
    "height": "167",
    "mass": "75",
    "hair_color": "n/a",
    "skin_color": "gold",
    "eye_color": "yellow",
    "birth_year": "112BBY",
    "gender": "n/a",
    "homeworld_id": None,
    "url": "https://swapi.info/api/people/2",
    "created_at": datetime(2014, 12, 10, 15, 10, 51, tzinfo=timezone.utc),
    "updated_at": datetime(2014, 12, 20, 21, 17, 56, tzinfo=timezone.utc),
}

FILM_1 = {
    "id": 1,
    "title": "A New Hope",
    "episode_id": 4,
    "opening_crawl": "It is a period of civil war...",
    "director": "George Lucas",
    "producer": "Gary Kurtz, Rick McCallum",
    "release_date": "1977-05-25",
    "url": "https://swapi.info/api/films/1",
    "created_at": datetime(2014, 12, 10, 14, 23, 31, tzinfo=timezone.utc),
    "updated_at": datetime(2014, 12, 20, 19, 49, 45, tzinfo=timezone.utc),
}


class TestPersonRepository:
    def test_upsert_batch_inserts(self, session):
        repo = PersonRepository(session)
        count = repo.upsert_batch([PERSON_1])
        assert count >= 1

    def test_upsert_batch_is_idempotent(self, session):
        repo = PersonRepository(session)
        repo.upsert_batch([PERSON_1])
        count = repo.upsert_batch([PERSON_1])
        assert count >= 1

    def test_upsert_updates_existing(self, session):
        repo = PersonRepository(session)
        repo.upsert_batch([PERSON_1])
        updated = {**PERSON_1, "name": "Luke Skywalker (Updated)"}
        repo.upsert_batch([updated])
        person = repo.get_by_id(1)
        assert person.name == "Luke Skywalker (Updated)"

    def test_get_by_id_returns_record(self, session):
        repo = PersonRepository(session)
        repo.upsert_batch([PERSON_1])
        person = repo.get_by_id(1)
        assert person is not None
        assert person.id == 1
        assert person.name == "Luke Skywalker"

    def test_get_by_id_missing_returns_none(self, session):
        repo = PersonRepository(session)
        assert repo.get_by_id(99999) is None

    def test_get_all_returns_records(self, session):
        repo = PersonRepository(session)
        repo.upsert_batch([PERSON_1, PERSON_2])
        results = repo.get_all(offset=0, limit=10)
        assert len(results) == 2

    def test_get_all_pagination_offset(self, session):
        repo = PersonRepository(session)
        repo.upsert_batch([PERSON_1, PERSON_2])
        page = repo.get_all(offset=1, limit=10)
        assert len(page) == 1
        assert page[0].id == 2

    def test_get_all_pagination_limit(self, session):
        repo = PersonRepository(session)
        repo.upsert_batch([PERSON_1, PERSON_2])
        page = repo.get_all(offset=0, limit=1)
        assert len(page) == 1
        assert page[0].id == 1

    def test_count(self, session):
        repo = PersonRepository(session)
        repo.upsert_batch([PERSON_1, PERSON_2])
        assert repo.count() == 2


class TestFilmRepository:
    def test_upsert_batch_inserts(self, session):
        repo = FilmRepository(session)
        count = repo.upsert_batch([FILM_1])
        assert count >= 1

    def test_get_by_id(self, session):
        repo = FilmRepository(session)
        repo.upsert_batch([FILM_1])
        film = repo.get_by_id(1)
        assert film.title == "A New Hope"
        assert film.episode_id == 4


class TestPersonFilmRepository:
    def test_upsert_batch_inserts_links(self, session):
        PersonRepository(session).upsert_batch([PERSON_1])
        FilmRepository(session).upsert_batch([FILM_1])
        link_repo = PersonFilmRepository(session)
        link_repo.upsert_batch([{"person_id": 1, "film_id": 1}])

    def test_upsert_batch_on_conflict_do_nothing(self, session):
        PersonRepository(session).upsert_batch([PERSON_1])
        FilmRepository(session).upsert_batch([FILM_1])
        link_repo = PersonFilmRepository(session)
        link_repo.upsert_batch([{"person_id": 1, "film_id": 1}])
        link_repo.upsert_batch([{"person_id": 1, "film_id": 1}])
