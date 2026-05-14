from typing import Optional, List
from sqlalchemy.orm import Session
from app.inventario import schemas, repositories
from app.shared.exceptions import ConflictError, NotFoundError

class InventarioService:
    def __init__(self, db: Session):
        self.repo = repositories.InventarioRepository(db)

    def create_producto(self, producto: schemas.ProductoCreate):
        # Validar precio
        if producto.precio <= 0:
            raise ConflictError("El precio debe ser mayor a 0")
        # Validar stock
        if producto.stock < 0:
            raise ConflictError("El stock no puede ser negativo")
        return self.repo.create(producto)

    def get_all_productos(self, skip: int = 0, limit: int = 100, categoria: Optional[str] = None, search: Optional[str] = None):
        return self.repo.get_all(skip, limit, categoria, search)

    def get_producto(self, producto_id: int):
        return self.repo.get_by_id(producto_id)

    def update_producto(self, producto_id: int, producto_data: schemas.ProductoUpdate):
        # Validar que el producto existe
        existing = self.repo.get_by_id(producto_id)
        
        # Validar precio si viene en la actualización
        if producto_data.precio is not None and producto_data.precio <= 0:
            raise ConflictError("El precio debe ser mayor a 0")
        
        # Validar stock si viene en la actualización
        if producto_data.stock is not None and producto_data.stock < 0:
            raise ConflictError("El stock no puede ser negativo")
        
        return self.repo.update(producto_id, producto_data)

    def delete_producto(self, producto_id: int):
        # Validar que el producto existe
        self.repo.get_by_id(producto_id)
        return self.repo.delete(producto_id)