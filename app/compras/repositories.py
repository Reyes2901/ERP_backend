from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.compras import models
from app.shared.exceptions import NotFoundError
from typing import Optional, List

class CompraRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100, proveedor: Optional[str] = None):
        """Obtener todas las compras con filtros opcionales"""
        query = self.db.query(models.Compra)
        
        if proveedor:
            query = query.filter(models.Compra.proveedor.ilike(f"%{proveedor}%"))
        
        return query.order_by(desc(models.Compra.created_at)).offset(skip).limit(limit).all()

    def get_by_id(self, compra_id: int):
        """Obtener compra por ID con sus detalles"""
        compra = self.db.query(models.Compra).filter(models.Compra.id == compra_id).first()
        if not compra:
            raise NotFoundError("Compra", str(compra_id))
        return compra

    def create_compra_con_detalles(self, proveedor: str, total: float, detalles: List[models.DetalleCompra]):
        """
        Crea la compra y sus detalles.
        Este método NO hace commit, asume que el servicio que lo llama manejará la transacción.
        """
        nueva_compra = models.Compra(
            proveedor=proveedor,
            total=total,
        )
        self.db.add(nueva_compra)
        self.db.flush()  # Asigna el ID a nueva_compra sin hacer commit

        for detalle in detalles:
            detalle.compra_id = nueva_compra.id
            self.db.add(detalle)

        self.db.flush()
        return nueva_compra