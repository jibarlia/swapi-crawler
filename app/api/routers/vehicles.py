from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_entity_service
from app.models.vehicle import Vehicle
from app.services.entity_service import EntityService

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("", response_model=list[Vehicle])
def list_vehicles(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: EntityService = Depends(get_entity_service),
):
    return service.list_vehicles(offset=offset, limit=limit)


@router.get("/{vehicle_id}", response_model=Vehicle)
def get_vehicle(vehicle_id: int, service: EntityService = Depends(get_entity_service)):
    vehicle = service.get_vehicle(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle
