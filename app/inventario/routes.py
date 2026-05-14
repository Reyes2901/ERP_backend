from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.inventario import schemas, services
from app.shared.responses import APIResponse
from app.shared.exceptions import BusinessError

router = APIRouter()

@router.post("/", response_model=APIResponse[schemas.ProductoResponse], status_code=status.HTTP_201_CREATED)
def create_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo producto en el inventario.
    """
    try:
        service = services.InventarioService(db)
        new_producto = service.create_producto(producto)
        return APIResponse.success_response("Producto creado exitosamente.", new_producto)
    except BusinessError as e:
        raise HTTPException(status_code=e.code, detail=APIResponse.error_response(e.message).model_dump())

@router.get("/", response_model=APIResponse[List[schemas.ProductoResponse]])
def list_productos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    categoria: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Lista todos los productos con filtros opcionales.
    """
    service = services.InventarioService(db)
    productos = service.get_all_productos(skip, limit, categoria, search)
    return APIResponse.success_response("Productos obtenidos correctamente.", productos)

@router.get("/{producto_id}", response_model=APIResponse[schemas.ProductoResponse])
def get_producto(producto_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un producto específico por su ID.
    """
    try:
        service = services.InventarioService(db)
        producto = service.get_producto(producto_id)
        return APIResponse.success_response("Producto obtenido correctamente.", producto)
    except BusinessError as e:
        raise HTTPException(status_code=e.code, detail=APIResponse.error_response(e.message).model_dump())

@router.put("/{producto_id}", response_model=APIResponse[schemas.ProductoResponse])
def update_producto(
    producto_id: int,
    producto_data: schemas.ProductoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un producto existente.
    """
    try:
        service = services.InventarioService(db)
        updated_producto = service.update_producto(producto_id, producto_data)
        return APIResponse.success_response("Producto actualizado correctamente.", updated_producto)
    except BusinessError as e:
        raise HTTPException(status_code=e.code, detail=APIResponse.error_response(e.message).model_dump())

@router.delete("/{producto_id}", response_model=APIResponse)
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    """
    Elimina un producto del inventario.
    """
    try:
        service = services.InventarioService(db)
        service.delete_producto(producto_id)
        return APIResponse.success_response("Producto eliminado correctamente.")
    except BusinessError as e:
        raise HTTPException(status_code=e.code, detail=APIResponse.error_response(e.message).model_dump())