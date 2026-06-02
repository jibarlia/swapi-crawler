from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_entity_service
from app.models.film import Film
from app.services.entity_service import EntityService

router = APIRouter(prefix="/films", tags=["films"])


@router.get("", response_model=list[Film])
def list_films(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: EntityService = Depends(get_entity_service),
):
    return service.list_films(offset=offset, limit=limit)


@router.get("/{film_id}", response_model=Film)
def get_film(film_id: int, service: EntityService = Depends(get_entity_service)):
    film = service.get_film(film_id)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film
