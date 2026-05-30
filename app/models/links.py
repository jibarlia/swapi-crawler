from sqlmodel import Field, SQLModel


class PersonFilm(SQLModel, table=True):
    __tablename__ = "person_film"

    person_id: int = Field(foreign_key="people.id", primary_key=True)
    film_id: int = Field(foreign_key="films.id", primary_key=True)


class PersonSpecies(SQLModel, table=True):
    __tablename__ = "person_species"

    person_id: int = Field(foreign_key="people.id", primary_key=True)
    species_id: int = Field(foreign_key="species.id", primary_key=True)


class PersonVehicle(SQLModel, table=True):
    __tablename__ = "person_vehicle"

    person_id: int = Field(foreign_key="people.id", primary_key=True)
    vehicle_id: int = Field(foreign_key="vehicles.id", primary_key=True)


class PersonStarship(SQLModel, table=True):
    __tablename__ = "person_starship"

    person_id: int = Field(foreign_key="people.id", primary_key=True)
    starship_id: int = Field(foreign_key="starships.id", primary_key=True)


class FilmPlanet(SQLModel, table=True):
    __tablename__ = "film_planet"

    film_id: int = Field(foreign_key="films.id", primary_key=True)
    planet_id: int = Field(foreign_key="planets.id", primary_key=True)


class FilmVehicle(SQLModel, table=True):
    __tablename__ = "film_vehicle"

    film_id: int = Field(foreign_key="films.id", primary_key=True)
    vehicle_id: int = Field(foreign_key="vehicles.id", primary_key=True)


class FilmStarship(SQLModel, table=True):
    __tablename__ = "film_starship"

    film_id: int = Field(foreign_key="films.id", primary_key=True)
    starship_id: int = Field(foreign_key="starships.id", primary_key=True)


class FilmSpecies(SQLModel, table=True):
    __tablename__ = "film_species"

    film_id: int = Field(foreign_key="films.id", primary_key=True)
    species_id: int = Field(foreign_key="species.id", primary_key=True)
