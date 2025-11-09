from contextlib import AbstractAsyncContextManager
from typing import Any, Callable
import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.model.department_model import Department
from app.repository.base_repository import BaseRepository


class DepartmentRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        super().__init__(session_factory, Department)

    async def get_all_departments(self, skip: int = 0, limit: int = 100) -> Any:
        async with self.session_factory() as session:
            # Get total count - await the scalar result

            columns = [ "Department.id", "Department.name", "Department.code", "Department.description", "Department.created_at", "Department.updated_at" ]
         
            departments  = await super().get_filter_data(columns, None, None, None, page=skip, per_page=limit)

            return departments
        
    async def get_departments_by_admin(self,  userId: uuid.UUID, skip: int = 0, limit: int = 100) -> Any:
        async with self.session_factory() as session:
            # Get total count - await the scalar result

            # columns = [ "Department.id", "Department.name", "Department.code", "Department.description", 
            #            "DepartmentAdmin.User.first_name", "DepartmentAdmin.User.last_name" ]
            
            # joins = [ ("DepartmentAdmin", "Department.id == DepartmentAdmin.department_id"),
            #             ("User", "DepartmentAdmin.user_id == User.id") ]
            # filters = [ f"DepartmentAdmin.user_id == '{userId}'" ]

            # columns = [ 
            #         "Department.id", 
            #         "Department.name", 
            #         "User.first_name", 
            #         "User.last_name" 
            # ]

            columns = [ "Department.id", "Department.name", "Department.code", "Department.description", 
                        "Department.created_at", "Department.updated_at",
                         "User.first_name", 
                        "User.last_name"  ]
         

            joins = [
                "admins",        # Department.adins relationship
                "admins.user"    # DepartmentAdmin.user relationship
            ]

            # Single filter
            filters = [{"field": "User.user_id", "op": "=", "value": "123"}]

            # Multiple filters
            # filters = [
            #     {"field": "User.user_id", "op": "=", "value": "123"},
            #     {"field": "Department.name", "op": "like", "value": "IT"}]

            departments  = await super().get_filter_data(columns, joins, filters, None, page=skip, per_page=limit)

            return departments