from fastapi import HTTPException, status

class BusinessError(Exception):
    """Excepción base para errores de lógica de negocio."""
    def __init__(self, message: str, code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.code = code
        super().__init__(self.message)

class NotFoundError(BusinessError):
    def __init__(self, entity: str, identifier: str):
        super().__init__(message=f"{entity} con identificador '{identifier}' no encontrado.", code=status.HTTP_404_NOT_FOUND)

class ConflictError(BusinessError):
    def __init__(self, message: str):
        super().__init__(message=message, code=status.HTTP_409_CONFLICT)

class InsufficientStockError(BusinessError):
    def __init__(self, product_name: str, requested: int, available: int):
        super().__init__(message=f"Stock insuficiente para '{product_name}'. Solicitado: {requested}, Disponible: {available}.", code=status.HTTP_400_BAD_REQUEST)