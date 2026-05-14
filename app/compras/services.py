from typing import List, Tuple
from sqlalchemy.orm import Session
from app.compras import schemas, repositories
from app.inventario import repositories as inventario_repo
from app.compras.models import DetalleCompra
from app.shared.exceptions import NotFoundError, BusinessError

class CompraService:
    def __init__(self, db: Session):
        self.db = db
        self.compra_repo = repositories.CompraRepository(db)
        self.producto_repo = inventario_repo.InventarioRepository(db)

    def _calcular_detalles(self, productos: List[schemas.CompraDetalleCreate]) -> Tuple[List[DetalleCompra], float]:
        """
        Lógica pura del backend: calcula subtotales y total de la compra.
        Valida que los productos existan.
        """
        detalles_a_crear = []
        total_compra = 0.0

        for item in productos:
            # Validar que el producto existe
            producto = self.producto_repo.get_by_id(item.producto_id)
            
            # Calcular subtotal
            subtotal = item.precio_unitario * item.cantidad
            total_compra += subtotal

            # Crear detalle (aún no guardado en DB)
            detalle = DetalleCompra(
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario,
                subtotal=subtotal
            )
            detalles_a_crear.append(detalle)

        return detalles_a_crear, total_compra

    def _actualizar_stock_productos(self, detalles: List[DetalleCompra]):
        """
        Actualiza el stock de los productos sumando las cantidades compradas
        """
        for detalle in detalles:
            self.producto_repo.update_stock(
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad,
                es_incremento=True  # IMPORTANTE: Sumar al stock
            )

    def create_compra(self, compra_data: schemas.CompraCreate):
        """
        Registra una nueva compra:
        1. Valida que todos los productos existan
        2. Calcula totales
        3. Crea la compra y sus detalles
        4. ACTUALIZA EL STOCK (suma cantidades)
        """
        # 1. Calcular todos los detalles y el total
        detalles, total = self._calcular_detalles(compra_data.productos)

        # 2. Crear la compra (dentro de una transacción)
        nueva_compra = self.compra_repo.create_compra_con_detalles(
            proveedor=compra_data.proveedor,
            total=total,
            detalles=detalles
        )

        # 3. Actualizar el stock de los productos (SUMAR)
        self._actualizar_stock_productos(detalles)

        # 4. Confirmar la transacción
        self.db.commit()
        self.db.refresh(nueva_compra)
        
        return nueva_compra

    def get_all_compras(self, skip: int = 0, limit: int = 100, proveedor: str = None):
        """Obtener todas las compras"""
        return self.compra_repo.get_all(skip, limit, proveedor)

    def get_compra(self, compra_id: int):
        """Obtener una compra específica"""
        return self.compra_repo.get_by_id(compra_id)