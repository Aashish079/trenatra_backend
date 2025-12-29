from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from .settings import get_settings

settings = get_settings()
engine = create_engine(settings.database_url, echo=True)


def get_db_session():
    """Dependency that provides a database session."""
    with Session(engine) as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_db_session)]
