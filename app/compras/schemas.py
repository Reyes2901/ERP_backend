from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

# --- Item de detalle para la creación ---
class CompraDetalleCreate(BaseModel):
    producto_id: int = Field(..., gt=0)
    cantidad: int = Field(..., gt=0)
    precio_unitario: float = Field(..., gt=0)

# --- Schema para la solicitud de creación ---
class CompraCreate(BaseModel):
    proveedor: str = Field(..., min_length=1, max_length=100)
    productos: List[CompraDetalleCreate] = Field(..., min_length=1)

# --- Schema para el detalle en respuestas ---
class DetalleCompraResponse(BaseModel):
    id: int
    producto_id: int
    producto_nombre: str | None=None 
    cantidad: int
    precio_unitario: float
    subtotal: float
    
    model_config = ConfigDict(from_attributes=True)

# --- Schema para la respuesta ---
class CompraResponse(BaseModel):
    id: int
    proveedor: str
    total: float
    created_at: datetime
    detalles: List[DetalleCompraResponse]
    
    model_config = ConfigDict(from_attributes=True)