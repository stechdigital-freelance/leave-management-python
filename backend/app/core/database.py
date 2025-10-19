from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session, async_sessionmaker 
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class BaseModel:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=True)
        self._session_factory = async_scoped_session(
            async_sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
                class_=AsyncSession,  # Explicitly specify AsyncSession
            ),
            scopefunc=lambda: None,  # You might want to set a proper scopefunc
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
            await session.commit()  # Explicit commit for async
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
            await self._session_factory.remove()  # Clean up scoped session



# from contextlib import AbstractContextManager, contextmanager
# from typing import Any, Generator

# from sqlalchemy import create_engine, orm

# from sqlalchemy.ext.declarative import as_declarative, declared_attr
# from sqlalchemy.orm import Session


# @as_declarative()
# class BaseModel:
#     id: Any
#     __name__: str

#     # Generate __tablename__ automatically
#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()


# class Database:
#     def __init__(self, db_url: str) -> None:
#         self._engine = create_engine(db_url, echo=True)
#         self._session_factory = orm.scoped_session(
#             orm.sessionmaker(
#                 autocommit=False,
#                 autoflush=False,
#                 bind=self._engine,
#             ),
#         )

#     def create_database(self) -> None:
#         BaseModel.metadata.create_all(self._engine)

#     @contextmanager
#     def session(self) -> Generator[Any, Any, AbstractContextManager[Session]]:
#         session: Session = self._session_factory()
#         try:
#             yield session
#         except Exception:
#             session.rollback()
#             raise
#         finally:
#             session.close()
