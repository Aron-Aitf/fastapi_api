from pydantic import BaseModel, AnyUrl, PostgresDsn
from pydantic_extra_types.semantic_version import SemanticVersion
from tomllib import load


class DatabaseConfig(BaseModel):
    database_url: PostgresDsn
    use_local_database: bool
    local_database_url: AnyUrl


class DocsConfig(BaseModel):
    title: str
    version: SemanticVersion
    description: str


class AppConfig(BaseModel):
    debug: bool


class Config(BaseModel):
    app: AppConfig
    database: DatabaseConfig
    docs: DocsConfig


with open("./config.toml", "rb") as file:
    toml_dict = load(file)

config = Config.model_validate(toml_dict)
