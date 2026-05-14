from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

# --- Base ---
class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    email: EmailStr
    direccion: Optional[str] = Field(None, max_length=255)

# --- Create ---
class ClienteCreate(ClienteBase):
    pass

# --- Update ---
class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None

# --- Response ---
class ClienteResponse(ClienteBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)