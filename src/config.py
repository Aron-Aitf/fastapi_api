from pydantic import BaseModel, AnyUrl
from pydantic_extra_types.semantic_version import SemanticVersion
from tomllib import load


class DatabaseConfig(BaseModel):
    database_url: AnyUrl
    use_local_database: bool
    local_database_url: str


class DocsConfig(BaseModel):
    title: str
    version: SemanticVersion
    description: str


class Config(BaseModel):
    database: DatabaseConfig
    docs: DocsConfig


def strip_whitespace_dict(data):
    if isinstance(data, dict):
        return {key: strip_whitespace_dict(value) for key, value in data.items()}
    elif isinstance(data, str):
        return data.strip()
    else:
        return data


toml_dict = {}

with open("./config.toml", "rb") as file:
    toml_dict = load(file)

toml_dict = strip_whitespace_dict(toml_dict)

config = Config.model_validate(toml_dict)
