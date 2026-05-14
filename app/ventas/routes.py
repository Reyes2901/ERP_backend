from fastapi import APIRouter, Depends, HTTPException, status, Query
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.ventas import schemas, services
from app.shared.responses import APIResponse
from app.shared.exceptions import BusinessError

router = APIRouter()

@router.post("/", response_model=APIResponse[schemas.VentaResponse], status_code=status.HTTP_201_CREATED)
def create_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    """
    Registra una nueva venta.
    - Valida stock automáticamente.
    - Calcula precios y total.
    - Descuenta el inventario.
    """
    try:
        service = services.VentaService(db)
        new_venta = service.create_venta(venta)
        return APIResponse.success_response("Venta registrada exitosamente.", new_venta)
    except BusinessError as e:
        raise HTTPException(status_code=e.code, detail=APIResponse.error_response(e.message).model_dump())

@router.get("/", response_model=APIResponse[List[schemas.VentaResponse]])
def list_ventas(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), db: Session = Depends(get_db)):
    service = services.VentaService(db)
    ventas = service.venta_repo.get_all(skip, limit)
    return APIResponse.success_response("Ventas obtenidas correctamente.", ventas)

@router.get("/{venta_id}", response_model=APIResponse[schemas.VentaResponse])
def get_venta(venta_id: int, db: Session = Depends(get_db)):
    try:
        service = services.VentaService(db)
        venta = service.venta_repo.get_by_id(venta_id)
        return APIResponse.success_response("Venta obtenida correctamente.", venta)
    except BusinessError as e:
        raise HTTPException(status_code=e.code, detail=APIResponse.error_response(e.message).model_dump())