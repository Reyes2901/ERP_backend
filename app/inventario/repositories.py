from typing import Optional, List
from sqlalchemy.orm import Session
from app.inventario import models, schemas
from app.shared.exceptions import NotFoundError

class InventarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100, categoria: Optional[str] = None, search: Optional[str] = None):
        query = self.db.query(models.Producto)
        if categoria:
            query = query.filter(models.Producto.categoria == categoria)
        if search:
            query = query.filter(models.Producto.nombre.ilike(f"%{search}%"))
        return query.offset(skip).limit(limit).all()

    def get_by_id(self, producto_id: int):
        producto = self.db.query(models.Producto).filter(models.Producto.id == producto_id).first()
        if not producto:
            raise NotFoundError("Producto", str(producto_id))
        return producto

    def create(self, producto_data: schemas.ProductoCreate):
        db_producto = models.Producto(**producto_data.model_dump())
        self.db.add(db_producto)
        self.db.commit()
        self.db.refresh(db_producto)
        return db_producto

    def update(self, producto_id: int, producto_data: schemas.ProductoUpdate):
        producto = self.get_by_id(producto_id)
        update_data = producto_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(producto, field, value)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def delete(self, producto_id: int):
        producto = self.get_by_id(producto_id)
        self.db.delete(producto)
        self.db.commit()
        return True

    def update_stock(self, producto_id: int, cantidad: int, es_incremento: bool = True, nuevo_precio: float | None =None):
        producto = self.get_by_id(producto_id)
        if es_incremento:
            producto.stock += cantidad
        else:
            if producto.stock < cantidad:
                raise ValueError(f"Stock insuficiente. Actual: {producto.stock}, Requerido: {cantidad}")
            producto.stock -= cantidad
        if nuevo_precio is not None:
            producto.precio = nuevo_precio
        self.db.flush()
        return producto