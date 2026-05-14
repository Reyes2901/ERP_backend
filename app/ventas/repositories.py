from sqlalchemy.orm import Session
from app.ventas import models
from app.shared.exceptions import NotFoundError

class VentaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.Venta).offset(skip).limit(limit).all()

    def get_by_id(self, venta_id: int):
        venta = self.db.query(models.Venta).filter(models.Venta.id == venta_id).first()
        if not venta:
            raise NotFoundError("Venta", str(venta_id))
        return venta

    def create_venta_con_detalles(self, cliente_id: int, total: float, detalles: list):
        """
        Crea la venta y sus detalles. Se espera que los detalles sean instancias de DetalleVenta.
        Este método NO hace commit, asume que el servicio que lo llama manejará la transacción.
        """
        nueva_venta = models.Venta(
            cliente_id=cliente_id,
            total=total,
        )
        self.db.add(nueva_venta)
        self.db.flush()  # Asigna el ID a nueva_venta sin hacer commit

        for detalle in detalles:
            detalle.venta_id = nueva_venta.id
            self.db.add(detalle)

        self.db.flush()
        return nueva_venta