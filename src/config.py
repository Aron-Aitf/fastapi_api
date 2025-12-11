from pydantic import AnyUrl, PostgresDsn
from pydantic_extra_types.semantic_version import SemanticVersion
from pydantic_settings import BaseSettings
from tomllib import load


class DatabaseConfig(BaseSettings):
    database_url: PostgresDsn
    use_local_database: bool
    local_database_url: AnyUrl


class DocsConfig(BaseSettings):
    title: str
    version: SemanticVersion
    description: str


class AppConfig(BaseSettings):
    debug: bool


class Config(BaseSettings):
    app: AppConfig
    database: DatabaseConfig
    docs: DocsConfig


with open("./config.toml", "rb") as file:
    toml_dict = load(file)

config = Config.model_validate(toml_dict)
