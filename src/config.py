from typing import Any
from pydantic import AnyUrl, PostgresDsn
from pydantic_extra_types.semantic_version import SemanticVersion
from pydantic_settings import BaseSettings
from tomllib import load


class DatabaseConfig(BaseSettings):
    database_url: PostgresDsn = PostgresDsn(
        "postgresql://postgres:postgres@postgres:5432/postgres"
    )
    use_local_database: bool = True
    local_database_url: AnyUrl = AnyUrl("sqlite:///sqlite.db")


class DocsConfig(BaseSettings):
    title: str = "Unnamed API"
    version: SemanticVersion = SemanticVersion(1)
    description: str = ""


class AppConfig(BaseSettings):
    debug: bool = True
    timing_headers: bool = True


class Config(BaseSettings):
    app: AppConfig
    database: DatabaseConfig
    docs: DocsConfig
    logging: dict[str, Any] = {}


with open("./config.toml", "rb") as file:
    toml_dict = load(file)

config = Config.model_validate(toml_dict)
