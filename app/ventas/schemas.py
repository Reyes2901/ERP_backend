from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

# --- Item de detalle para la creación ---
class VentaDetalleCreate(BaseModel):
    producto_id: int = Field(..., gt=0)
    cantidad: int = Field(..., gt=0)

# --- Schema para la solicitud de creación ---
class VentaCreate(BaseModel):
    cliente_id: int = Field(..., gt=0)
    productos: List[VentaDetalleCreate] = Field(..., min_length=1)

# --- Schema para el detalle en respuestas ---
class DetalleVentaResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float
    
    model_config = ConfigDict(from_attributes=True)

# --- Schema para la respuesta ---
class VentaResponse(BaseModel):
    id: int
    cliente_id: int
    total: float
    created_at: datetime
    detalles: List[DetalleVentaResponse]
    
    model_config = ConfigDict(from_attributes=True)