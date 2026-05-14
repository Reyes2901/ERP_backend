from typing import List
from sqlalchemy.orm import Session
from app.ventas import schemas, repositories
from app.inventario import repositories as inventario_repo
from app.clientes import repositories as clientes_repo
from app.shared.exceptions import InsufficientStockError, NotFoundError
from app.ventas.models import Venta, DetalleVenta

class VentaService:
    def __init__(self, db: Session):
        self.db = db
        self.venta_repo = repositories.VentaRepository(db)
        self.producto_repo = inventario_repo.InventarioRepository(db)
        self.cliente_repo = clientes_repo.ClienteRepository(db)

    def _calcular_y_validar_detalles(self, productos: List[schemas.VentaDetalleCreate]):
        """
        Lógica pura del backend: calcula precios, subtotales y valida stock.
        Retorna una lista de objetos DetalleVenta (sin guardar) y el total.
        """
        detalles_a_crear = []
        total_venta = 0.0

        for item in productos:
            producto = self.producto_repo.get_by_id(item.producto_id)

            # Validación de stock NEGATIVO
            if producto.stock < item.cantidad:
                raise InsufficientStockError(producto.nombre, item.cantidad, producto.stock)

            subtotal = producto.precio * item.cantidad
            total_venta += subtotal

            # Se crea una instancia del modelo ORM pero aún no se guarda.
            detalle = DetalleVenta(
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=producto.precio,
                subtotal=subtotal
            )
            detalles_a_crear.append(detalle)

        return detalles_a_crear, total_venta

    def create_venta(self, venta_data: schemas.VentaCreate):
        # 1. Validar que el cliente exista
        cliente = self.cliente_repo.get_by_id(venta_data.cliente_id)

        # 2. Calcular todo y validar stock
        detalles, total = self._calcular_y_validar_detalles(venta_data.productos)

        # 3. Crear la venta (estado transaccional)
        nueva_venta = self.venta_repo.create_venta_con_detalles(
            cliente_id=venta_data.cliente_id,
            total=total,
            detalles=detalles
        )

        # 4. Actualizar el stock de los productos
        for detalle in detalles:
            self.producto_repo.update_stock(
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad,
                es_incremento=False  # Es un decremento
            )

        self.db.commit()
        self.db.refresh(nueva_venta)
        return nueva_venta