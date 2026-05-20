# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.clientes import models, schemas
from app.shared.exceptions import NotFoundError

class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100, nombre: str = None):
        # 1. Iniciamos la consulta base sin filtros
        query = self.db.query(models.Cliente)   
        # 2. SOLO si viene un nombre en la petición, aplicamos el filtro
        if nombre and nombre.strip():
            # ilike maneja el caso de "karla" vs "Karla" e incluye búsquedas parciales
            query = query.filter(models.Cliente.nombre.ilike(f"%{nombre}%"))
        # 3. Aplicamos la paginación y ejecutamos la consulta
        return query.offset(skip).limit(limit).all()        

    def get_by_id(self, cliente_id: int):
        cliente = self.db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
        if not cliente:
            raise NotFoundError("Cliente", str(cliente_id))
        return cliente

    def get_by_email(self, email: str):
        return self.db.query(models.Cliente).filter(models.Cliente.email == email).first()

    def create(self, cliente_data: schemas.ClienteCreate):
        db_cliente = models.Cliente(**cliente_data.model_dump())
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente

    def update(self, cliente_id: int, cliente_data: schemas.ClienteUpdate):
        db_cliente = self.get_by_id(cliente_id)
        update_data = cliente_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cliente, field, value)
        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente

    def delete(self, cliente_id: int):
        db_cliente = self.get_by_id(cliente_id)
        self.db.delete(db_cliente)
        self.db.commit()
        return True