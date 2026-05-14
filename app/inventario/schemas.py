from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# --- Base ---
class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    precio: float = Field(..., gt=0, description="Precio debe ser mayor a 0")
    stock: int = Field(..., ge=0, description="Stock no puede ser negativo")
    categoria: Optional[str] = Field(None, max_length=50)

# --- Create ---
class ProductoCreate(ProductoBase):
    pass

# --- Update ---
class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = None
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    categoria: Optional[str] = None

# --- Response ---
class ProductoResponse(ProductoBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)