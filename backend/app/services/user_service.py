from typing import Any, List
from app.repository.user_repository import UserRepository
from app.services.base_service import BaseService
from app.schema.user_schema import UserPublic


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