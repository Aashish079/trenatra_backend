from datetime import datetime, timezone
from typing import Annotated

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)
from sqlmodel import select

from .database import SessionDependency as DBSession
from .models import Session as UserSession
from .models import User

basic_security = HTTPBasic()


def verify_basic_auth(
    credentials: Annotated[HTTPBasicCredentials, Depends(basic_security)],
    db: DBSession,
) -> User:
    """Verify HTTP Basic credentials and return authenticated user."""
    username = credentials.username
    password = credentials.password

    user = db.exec(select(User).where(User.email == username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    return user


BasicAuthUser = Annotated[User, Depends(verify_basic_auth)]

bearer_security = HTTPBearer()


def verify_bearer_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_security)],
    db: DBSession,
) -> User:
    """Verify Bearer token and return authenticated user."""
    token = credentials.credentials

    user_session = db.exec(
        select(UserSession).where(UserSession.token == token)
    ).first()

    if not user_session or user_session.expires_at.replace(
        tzinfo=timezone.utc
    ) < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )

    return user_session.user


BearerAuthUser = Annotated[User, Depends(verify_bearer_token)]
