from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session

import app.models  # noqa: F401 — registers all models with SQLModel.metadata
from app.config import APP_NAME
from app.db import create_db_and_tables, get_session
from app.models.film import Film
from app.models.person import Person
from app.models.planet import Planet
from app.models.species import Species
from app.models.starship import Starship
from app.models.vehicle import Vehicle
from app.services.entity_service import EntityService


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title=APP_NAME, version="1.0.0", lifespan=lifespan)


# --- People ---


@app.get("/people", response_model=list[Person])
def list_people(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return EntityService(session).list_people(offset=offset, limit=limit)


@app.get("/people/{person_id}", response_model=Person)
def get_person(person_id: int, session: Session = Depends(get_session)):
    person = EntityService(session).get_person(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


# --- Films ---


@app.get("/films", response_model=list[Film])
def list_films(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return EntityService(session).list_films(offset=offset, limit=limit)


@app.get("/films/{film_id}", response_model=Film)
def get_film(film_id: int, session: Session = Depends(get_session)):
    film = EntityService(session).get_film(film_id)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film


# --- Planets ---


@app.get("/planets", response_model=list[Planet])
def list_planets(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return EntityService(session).list_planets(offset=offset, limit=limit)


@app.get("/planets/{planet_id}", response_model=Planet)
def get_planet(planet_id: int, session: Session = Depends(get_session)):
    planet = EntityService(session).get_planet(planet_id)
    if not planet:
        raise HTTPException(status_code=404, detail="Planet not found")
    return planet


# --- Species ---


@app.get("/species", response_model=list[Species])
def list_species(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return EntityService(session).list_species(offset=offset, limit=limit)


@app.get("/species/{species_id}", response_model=Species)
def get_species(species_id: int, session: Session = Depends(get_session)):
    species = EntityService(session).get_species(species_id)
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    return species


# --- Vehicles ---


@app.get("/vehicles", response_model=list[Vehicle])
def list_vehicles(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return EntityService(session).list_vehicles(offset=offset, limit=limit)


@app.get("/vehicles/{vehicle_id}", response_model=Vehicle)
def get_vehicle(vehicle_id: int, session: Session = Depends(get_session)):
    vehicle = EntityService(session).get_vehicle(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


# --- Starships ---


@app.get("/starships", response_model=list[Starship])
def list_starships(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return EntityService(session).list_starships(offset=offset, limit=limit)


@app.get("/starships/{starship_id}", response_model=Starship)
def get_starship(starship_id: int, session: Session = Depends(get_session)):
    starship = EntityService(session).get_starship(starship_id)
    if not starship:
        raise HTTPException(status_code=404, detail="Starship not found")
    return starship
