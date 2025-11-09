from dependency_injector import containers, providers

from app.core.config import settings
from app.core.database import Database
from app.repository import *
from app.services import *


class Container(containers.DeclarativeContainer):
    # wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.routes.v1.endpoints.users",
            "app.api.routes.v1.endpoints.departments",
            "app.api.routes.v1.endpoints.login",
            "app.api.deps",
        ]
    )

    # db = providers.Singleton(Database, db_url=settings.SQLALCHEMY_DATABASE_URI)

    # postgres db container connection for testing
    # db = providers.Singleton(Database, db_url='postgresql+psycopg://postgres:postgres@localhost:5433/app')

    # direct db connection for testing
    # db = providers.Singleton(Database, db_url='postgresql+psycopg://postgres:postgres@localhost:5432/app')

    # async db connection for testing for postgres 17
    # db = providers.Singleton(Database, db_url='postgresql+asyncpg://postgres:postgres@localhost:5432/app')

    # async db connection for testing for postgres 18
    db = providers.Singleton(Database, db_url='postgresql+asyncpg://postgres:postgres@localhost:5434/app')

    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)

    user_service = providers.Factory(UserService, user_repository=user_repository)

    department_repository = providers.Factory(DepartmentRepository, session_factory=db.provided.session)

    department_service = providers.Factory(DepartmentService, department_repository=department_repository)

