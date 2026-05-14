from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.compras import schemas, services
from app.shared.responses import APIResponse
from app.shared.exceptions import BusinessError

router = APIRouter()

@router.post("/", response_model=APIResponse[schemas.CompraResponse], status_code=status.HTTP_201_CREATED)
def create_compra(
    compra: schemas.CompraCreate, 
    db: Session = Depends(get_db)
):
    """
    Registra una nueva compra.
    
    - **proveedor**: Nombre del proveedor
    - **productos**: Lista de productos con cantidad y precio unitario
    
    El backend:
    - Calcula automáticamente subtotales y total
    - Actualiza el stock de los productos (SUMA las cantidades)
    - Valida que todos los productos existan
    """
    try:
        service = services.CompraService(db)
        new_compra = service.create_compra(compra)
        
        # Enriquecer la respuesta con nombres de productos
        response_data = schemas.CompraResponse.model_validate(new_compra)
        
        # Agregar nombres de productos a los detalles
        for idx, detalle in enumerate(response_data.detalles):
            producto = service.producto_repo.get_by_id(detalle.producto_id)
            response_data.detalles[idx].producto_nombre = producto.nombre
        
        return APIResponse.success_response("Compra registrada exitosamente.", response_data)
    except BusinessError as e:
        raise HTTPException(status_code=e.code, detail=APIResponse.error_response(e.message).model_dump())

@router.get("/", response_model=APIResponse[List[schemas.CompraResponse]])
def list_compras(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=100, description="Límite de registros"),
    proveedor: Optional[str] = Query(None, description="Filtrar por proveedor"),
    db: Session = Depends(get_db)
):
    """
    Obtiene una lista paginada de todas las compras.
    Puede filtrar por proveedor.
    """
    service = services.CompraService(db)
    compras = service.get_all_compras(skip, limit, proveedor)
    
    # Enriquecer la respuesta
    response_data = []
    for compra in compras:
        compra_dict = schemas.CompraResponse.model_validate(compra)
        for idx, detalle in enumerate(compra_dict.detalles):
            producto = service.producto_repo.get_by_id(detalle.producto_id)
            compra_dict.detalles[idx].producto_nombre = producto.nombre
        response_data.append(compra_dict)
    
    return APIResponse.success_response("Compras obtenidas correctamente.", response_data)

@router.get("/{compra_id}", response_model=APIResponse[schemas.CompraResponse])
def get_compra(compra_id: int, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de una compra específica por su ID.
    """
    try:
        service = services.CompraService(db)
        compra = service.get_compra(compra_id)
        
        response_data = schemas.CompraResponse.model_validate(compra)
        for idx, detalle in enumerate(response_data.detalles):
            producto = service.producto_repo.get_by_id(detalle.producto_id)
            response_data.detalles[idx].producto_nombre = producto.nombre
            
        return APIResponse.success_response("Compra obtenida correctamente.", response_data)
    except BusinessError as e:
        raise HTTPException(status_code=e.code, detail=APIResponse.error_response(e.message).model_dump())