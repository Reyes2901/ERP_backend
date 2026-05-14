# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.clientes import schemas, repositories
from app.shared.exceptions import ConflictError

class ClienteService:
    def __init__(self, db: Session):
        self.repo = repositories.ClienteRepository(db)

    def create_cliente(self, cliente: schemas.ClienteCreate):
        # Validación de email único
        if self.repo.get_by_email(cliente.email):
            raise ConflictError(f"Ya existe un cliente con el email '{cliente.email}'.")
        return self.repo.create(cliente)

    def get_all_clientes(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def get_cliente(self, cliente_id: int):
        return self.repo.get_by_id(cliente_id)

    def update_cliente(self, cliente_id: int, cliente_data: schemas.ClienteUpdate):
        # Si se actualiza el email, validar que no exista en otro cliente
        if cliente_data.email:
            existing = self.repo.get_by_email(cliente_data.email)
            if existing and existing.id != cliente_id:
                raise ConflictError(f"Ya existe un cliente con el email '{cliente_data.email}'.")
        return self.repo.update(cliente_id, cliente_data)

    def delete_cliente(self, cliente_id: int):
        # Aquí podrías agregar lógica para verificar si tiene ventas asociadas antes de eliminar
        return self.repo.delete(cliente_id)