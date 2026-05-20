from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.clientes import schemas, services
from app.shared.responses import APIResponse
from app.shared.exceptions import BusinessError

router = APIRouter()

@router.post("/", response_model=APIResponse[schemas.ClienteResponse], status_code=status.HTTP_201_CREATED)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    try:
        service = services.ClienteService(db)
        new_cliente = service.create_cliente(cliente)
        return APIResponse.success_response("Cliente creado exitosamente.", new_cliente)
    except BusinessError as e:
        raise HTTPException(status_code=e.code, detail=APIResponse.error_response(e.message).model_dump())

@router.get("/", response_model=APIResponse[List[schemas.ClienteResponse]])
def list_clientes(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100),nombre: str = Query(None,description="Busqueda por nombre", max_length=50),db: Session = Depends(get_db)):
    service = services.ClienteService(db)
    clientes = service.get_all_clientes(skip, limit,nombre)
    return APIResponse.success_response("Clientes obtenidos correctamente.", clientes)

@router.get("/{cliente_id}", response_model=APIResponse[schemas.ClienteResponse])
def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    try:
        service = services.ClienteService(db)
        cliente = service.get_cliente(cliente_id)
        return APIResponse.success_response("Cliente obtenido correctamente.", cliente)
    except BusinessError as e:
        raise HTTPException(status_code=e.code, detail=APIResponse.error_response(e.message).model_dump())

@router.put("/{cliente_id}", response_model=APIResponse[schemas.ClienteResponse])
def update_cliente(cliente_id: int, cliente_data: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    try:
        service = services.ClienteService(db)
        updated_cliente = service.update_cliente(cliente_id, cliente_data)
        return APIResponse.success_response("Cliente actualizado correctamente.", updated_cliente)
    except BusinessError as e:
        raise HTTPException(status_code=e.code, detail=APIResponse.error_response(e.message).model_dump())

@router.delete("/{cliente_id}", response_model=APIResponse)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    try:
        service = services.ClienteService(db)
        service.delete_cliente(cliente_id)
        return APIResponse.success_response("Cliente eliminado correctamente.")
    except BusinessError as e:
        raise HTTPException(status_code=e.code, detail=APIResponse.error_response(e.message).model_dump())