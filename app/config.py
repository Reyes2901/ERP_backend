from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = Field("ERP Backend", env="APP_NAME")
    app_env: str = Field("development", env="APP_ENV")
    secret_key: str = Field(..., env="SECRET_KEY")

    # Database
    postgres_user: str = Field("postgres", env="POSTGRES_USER")
    postgres_password: str = Field("postgres", env="POSTGRES_PASSWORD")
    postgres_db: str = Field("erp_db", env="POSTGRES_DB")
    postgres_server: str = Field("localhost", env="POSTGRES_SERVER")
    postgres_port: str = Field("5432", env="POSTGRES_PORT")

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"

    class Config:
        env_file = ".env"

settings = Settings()