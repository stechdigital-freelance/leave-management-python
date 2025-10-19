from typing import Annotated, Any
# from app.model.user_model import User
# from app.models import UsersPublic
from app.models import UsersPublic
from app.services.user_service import UserService
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from app.core.container import Container

router = APIRouter(prefix="/users", tags=["users"])

@router.get(
    "/",
    response_model=UsersPublic,
)
@inject
async def read_users(ser: UserService = Depends(Provide[Container.user_service]), skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """
    users = await ser.get_all_users(skip, limit)
    
    # count = len(users)
    return UsersPublic(data=users, count=1)