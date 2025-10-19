from contextlib import AbstractAsyncContextManager
from typing import Any, Callable, Type, TypeVar, List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload

from app.core.config import settings
from app.core.exceptions import DuplicatedError, NotFoundError
from app.model.base_model import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]], model: Type[T]) -> None:
        self.session_factory = session_factory
        self.model = model

    async def read_by_options(self, schema: T, eager: bool = False) -> dict:
        async with self.session_factory() as session:
            schema_as_dict: dict = schema.dict(exclude_none=True)
            ordering: str = schema_as_dict.get("ordering", settings.ORDERING)
            
            # Handle ordering safely
            order_field = ordering[1:] if ordering.startswith("-") else ordering
            if hasattr(self.model, order_field):
                order_query = (
                    getattr(self.model, order_field).desc()
                    if ordering.startswith("-")
                    else getattr(self.model, order_field).asc()
                )
            else:
                # Fallback to ID ordering if specified field doesn't exist
                order_query = self.model.id.asc()
            
            page = schema_as_dict.get("page", settings.PAGE)
            page_size = schema_as_dict.get("page_size", settings.PAGE_SIZE)
            
            # TODO: Implement proper filter options
            # filter_options = dict_to_sqlalchemy_filter_options(self.model, schema.dict(exclude_none=True))
            filter_options = None
            
            # Build query using select
            query = select(self.model)
            
            if eager:
                for eager_relation in getattr(self.model, "eagers", []):
                    query = query.options(joinedload(getattr(self.model, eager_relation)))
            
            if filter_options:
                query = query.where(filter_options)
                
            query = query.order_by(order_query)
            
            # Execute query for results
            if page_size == "all":
                result = await session.execute(query)
                results = result.scalars().all()
            else:
                query = query.limit(page_size).offset((page - 1) * page_size)
                result = await session.execute(query)
                results = result.scalars().all()
            
            # Get total count (without pagination)
            count_query = select(func.count()).select_from(self.model)
            if filter_options:
                count_query = count_query.where(filter_options)
            total_count_result = await session.execute(count_query)
            total_count = total_count_result.scalar_one()
            
            return {
                "founds": results,
                "search_options": {
                    "page": page,
                    "page_size": page_size,
                    "ordering": ordering,
                    "total_count": total_count,
                },
            }

    async def read_by_id(self, id: int, eager: bool = False) -> T:
        async with self.session_factory() as session:
            query = select(self.model).where(self.model.id == id)
            
            if eager:
                for eager_relation in getattr(self.model, "eagers", []):
                    query = query.options(joinedload(getattr(self.model, eager_relation)))
            
            result = await session.execute(query)
            entity = result.scalar_one_or_none()
            
            if not entity:
                raise NotFoundError(detail=f"not found id : {id}")
            return entity

    async def create(self, schema: T) -> T:
        async with self.session_factory() as session:
            query = self.model(**schema.dict())
            try:
                session.add(query)
                await session.commit()
                await session.refresh(query)
            except IntegrityError as e:
                await session.rollback()
                raise DuplicatedError(detail=str(e.orig))
            return query

    async def update(self, id: int, schema: T) -> T:
        async with self.session_factory() as session:
            # Use update statement
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(**schema.dict(exclude_none=True))
            )
            result = await session.execute(stmt)
            
            if result.rowcount == 0:
                raise NotFoundError(detail=f"not found id : {id}")
                
            await session.commit()
            return await self.read_by_id(id)

    async def update_attr(self, id: int, column: str, value: Any) -> T:
        async with self.session_factory() as session:
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values({column: value})
            )
            result = await session.execute(stmt)
            
            if result.rowcount == 0:
                raise NotFoundError(detail=f"not found id : {id}")
                
            await session.commit()
            return await self.read_by_id(id)

    async def whole_update(self, id: int, schema: T) -> T:
        async with self.session_factory() as session:
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(**schema.dict())
            )
            result = await session.execute(stmt)
            
            if result.rowcount == 0:
                raise NotFoundError(detail=f"not found id : {id}")
                
            await session.commit()
            return await self.read_by_id(id)

    async def delete_by_id(self, id: int) -> None:
        async with self.session_factory() as session:
            # First check if entity exists
            query = select(self.model).where(self.model.id == id)
            result = await session.execute(query)
            entity = result.scalar_one_or_none()
            
            if not entity:
                raise NotFoundError(detail=f"not found id : {id}")
            
            # Delete the entity
            stmt = delete(self.model).where(self.model.id == id)
            await session.execute(stmt)
            await session.commit()

    async def close_scoped_session(self) -> None:
        # In async context, session management is typically handled by the context manager
        # This method might not be needed anymore
        pass