from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    app_description: str
    app_version: str
    postgres_hostname: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: str
    db_connection_string: str
    initialize_database_schema: bool
    populate_database:bool

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
