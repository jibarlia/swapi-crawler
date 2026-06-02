from fastapi import Depends, HTTPException
from sqlmodel import Session

from app.db import get_session
from app.models.person import Person
from app.services.entity_service import EntityService
from app.services.person_service import PersonService


def get_entity_service(session: Session = Depends(get_session)) -> EntityService:
    return EntityService(session)


def get_person_service(session: Session = Depends(get_session)) -> PersonService:
    return PersonService(session)


def get_existing_person(
    person_id: int,
    service: PersonService = Depends(get_person_service),
) -> Person:
    """Resolve the person or raise 404 — shared by all /people/{id}/... routes."""
    person = service.get_person(person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person
