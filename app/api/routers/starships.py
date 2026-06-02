from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_entity_service
from app.models.starship import Starship
from app.services.entity_service import EntityService

router = APIRouter(prefix="/starships", tags=["starships"])


@router.get("", response_model=list[Starship])
def list_starships(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: EntityService = Depends(get_entity_service),
):
    return service.list_starships(offset=offset, limit=limit)


@router.get("/{starship_id}", response_model=Starship)
def get_starship(
    starship_id: int, service: EntityService = Depends(get_entity_service)
):
    starship = service.get_starship(starship_id)
    if not starship:
        raise HTTPException(status_code=404, detail="Starship not found")
    return starship
