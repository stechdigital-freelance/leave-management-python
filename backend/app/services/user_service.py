from typing import Any, List
from app.repository.user_repository import UserRepository
from app.services.base_service import BaseService
from app.schema.user_schema import UserPublic
from fastapi import HTTPException
from app import crud

class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    async def get_all_users(self, skip: int = 1, limit: int = 100) -> Any:

         users_data  = await self.user_repository.get_all_users_new(skip, limit)

            # Convert ORM/SQLModel User instances to the public pydantic schema
         users_public: List[UserPublic] = [UserPublic.model_validate(u) for u in users_data["items"]]

         return users_public
        # return await self.user_repository.get_all_users_new(skip, limit)

    async def get_user_by_email(self, email: str) -> Any:

         user  = await self.user_repository.get_user_by_email(email)

            # Convert ORM/SQLModel User instances to the public pydantic schema
        #  user: List[UserPublic] = [UserPublic.model_validate(u) for u in users_data["items"]]

         user_public: UserPublic = UserPublic.model_validate(user)

         return user_public
    
    async def validate_user_email(self, email: str, pwd: str) -> bool:

         user  = await self.user_repository.get_user_by_email(email)

         if not user or not crud.verify_password(pwd, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
         if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

         user_public: UserPublic = UserPublic.model_validate(user)

         return user_public