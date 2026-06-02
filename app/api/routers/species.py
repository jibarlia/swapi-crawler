from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_entity_service
from app.models.species import Species
from app.services.entity_service import EntityService

router = APIRouter(prefix="/species", tags=["species"])


@router.get("", response_model=list[Species])
def list_species(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: EntityService = Depends(get_entity_service),
):
    return service.list_species(offset=offset, limit=limit)


@router.get("/{species_id}", response_model=Species)
def get_species(species_id: int, service: EntityService = Depends(get_entity_service)):
    species = service.get_species(species_id)
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    return species
