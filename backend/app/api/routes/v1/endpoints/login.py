from datetime import timedelta
from http.client import HTTPException
from typing import Annotated

from app import crud
from app.core import security
from app.core.config import Settings
from app.core.container import Container
from app.models import Token
from app.services.user_service import UserService
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

router = APIRouter(tags=["login"])

@router.post("/login/access-token")

@inject
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], userService: UserService = Depends(Provide[Container.user_service])
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # SQLAlchemy version: replace session.exec with session.execute().scalars().first()
    # stmt = select(User).where(User.email == form_data.username)
    # user = (await session.execute(stmt)).scalars().first()

    userService: UserService = Container.user_service()

    user = await userService.validate_user_email(form_data.username, form_data.password)

    # access_token_expires = timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_expires = timedelta(minutes=60 * 24 * 8)
    access_token = security.create_access_token(user.id, expires_delta=access_token_expires)

    return Token(access_token=access_token)


