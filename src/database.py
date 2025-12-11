from typing import Generator
from sqlmodel import SQLModel, Session, create_engine
from config import config

# forces the models to load before making the tables
import models as _  # noqa: F401

if config.database.use_local_database:
    engine = create_engine(
        str(config.database.local_database_url),
    )
else:
    engine = create_engine(
        str(config.database.database_url),
    )

SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
