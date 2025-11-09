from typing import Any, List
import uuid
from app.repository.department_repository import DepartmentRepository
from app.schema.department_schema import DepartmentRead
from app.services.base_service import BaseService
from app.schema.user_schema import UserPublic


class DepartmentService(BaseService):
    def __init__(self, department_repository: DepartmentRepository):
        self.department_repository = department_repository
        super().__init__(department_repository)

    async def get_all_departments(self, skip: int = 1, limit: int = 100) -> Any:

         departments_data  = await self.department_repository.get_all_departments(skip, limit)

            # Convert ORM/SQLModel User instances to the public pydantic schema
         departments_public: List[DepartmentRead] = [DepartmentRead.model_validate(u) for u in departments_data["items"]]

         return departments_public
        # return await self.user_repository.get_all_users_new(skip, limit)

    async def get_departments_by_admin(self, userId: uuid.UUID, skip: int = 1, limit: int = 100) -> Any:

         departments_data  = await self.department_repository.get_departments_by_admin(userId, skip, limit)

            # Convert ORM/SQLModel User instances to the public pydantic schema
         departments_public: List[DepartmentRead] = [DepartmentRead.model_validate(u) for u in departments_data["items"]]

         return departments_public
        # return await self.user_repository.get_all_users_new(skip, limit)