from typing import Annotated, Any
import uuid
from app.schema.department_schema import DepartmentsPublic
from app.services.department_service import DepartmentService
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from app.core.container import Container

router = APIRouter(prefix="/departments", tags=["departments"])

@router.get(
    "/",
    response_model=DepartmentsPublic,
)
@inject
async def read_departments(ser: DepartmentService = Depends(Provide[Container.department_service]),
                            skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve departments.
    """
    departments = await ser.get_all_departments(skip, limit)
    
    # count = len(users)
    return DepartmentsPublic(data=departments, count=1)

@router.get(
    "/admin",
    response_model=DepartmentsPublic,
)
@inject
async def read_departments_by_admin(ser: DepartmentService = Depends(Provide[Container.department_service]),
                                    userId: uuid.UUID = None,  skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve departments.
    """
    departments = await ser.get_departments_by_admin(userId, skip, limit)
    
    # count = len(users)
    return DepartmentsPublic(data=departments, count=1)