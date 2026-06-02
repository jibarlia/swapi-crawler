from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_entity_service
from app.models.planet import Planet
from app.services.entity_service import EntityService

router = APIRouter(prefix="/planets", tags=["planets"])


@router.get("", response_model=list[Planet])
def list_planets(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: EntityService = Depends(get_entity_service),
):
    return service.list_planets(offset=offset, limit=limit)


@router.get("/{planet_id}", response_model=Planet)
def get_planet(planet_id: int, service: EntityService = Depends(get_entity_service)):
    planet = service.get_planet(planet_id)
    if not planet:
        raise HTTPException(status_code=404, detail="Planet not found")
    return planet
