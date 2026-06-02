from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import (
    get_entity_service,
    get_existing_person,
    get_person_service,
)
from app.api.schemas.person import PersonDetails
from app.models.film import Film
from app.models.person import Person
from app.models.species import Species
from app.models.starship import Starship
from app.models.vehicle import Vehicle
from app.services.entity_service import EntityService
from app.services.person_service import PersonService

router = APIRouter(prefix="/people", tags=["people"])


@router.get("", response_model=list[Person])
def list_people(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: EntityService = Depends(get_entity_service),
):
    return service.list_people(offset=offset, limit=limit)


@router.get("/{person_id}", response_model=Person)
def get_person(person_id: int, service: EntityService = Depends(get_entity_service)):
    person = service.get_person(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@router.get("/{person_id}/films", response_model=list[Film])
def get_person_films(
    person: Person = Depends(get_existing_person),
    service: PersonService = Depends(get_person_service),
):
    return service.get_films(person.id)


@router.get("/{person_id}/starships", response_model=list[Starship])
def get_person_starships(
    person: Person = Depends(get_existing_person),
    service: PersonService = Depends(get_person_service),
):
    return service.get_starships(person.id)


@router.get("/{person_id}/vehicles", response_model=list[Vehicle])
def get_person_vehicles(
    person: Person = Depends(get_existing_person),
    service: PersonService = Depends(get_person_service),
):
    return service.get_vehicles(person.id)


@router.get("/{person_id}/species", response_model=list[Species])
def get_person_species(
    person: Person = Depends(get_existing_person),
    service: PersonService = Depends(get_person_service),
):
    return service.get_species(person.id)


@router.get("/{person_id}/details", response_model=PersonDetails)
def get_person_details(
    person: Person = Depends(get_existing_person),
    service: PersonService = Depends(get_person_service),
):
    return service.get_details(person.id)
