from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    app_name: str = Field("ERP Backend", env="APP_NAME")
    app_env: str = Field("development", env="APP_ENV")
    secret_key: str = Field(..., env="SECRET_KEY")

    # Database (Componentes individuales para local)
    postgres_user: str = Field("postgres", env="POSTGRES_USER")
    postgres_password: str = Field("postgres", env="POSTGRES_PASSWORD")
    postgres_db: str = Field("erp_db", env="POSTGRES_DB")
    postgres_server: str = Field("localhost", env="POSTGRES_SERVER")
    postgres_port: str = Field("5432", env="POSTGRES_PORT")

    # NUEVO: Variable directa completa (Para Producción en AWS Lambda)
    database_url_env: Optional[str] = Field(None, env="DATABASE_URL")

    @property
    def database_url(self) -> str:
        # 1. Si existe "DATABASE_URL" en el entorno (ej. en AWS Lambda), úsala.
        if self.database_url_env:
            return self.database_url_env
            
        # 2. Si no existe (ej. en tu PC local usando el .env), constrúyela.
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"

    class Config:
        env_file = ".env"

settings = Settings()