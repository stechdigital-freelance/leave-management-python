from contextlib import AbstractAsyncContextManager
from typing import Any, Callable, Dict, Type, TypeVar, List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, asc, desc, func, inspect, select, update, delete
from sqlalchemy.orm import joinedload, aliased, InstrumentedAttribute

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
    
    # ------------------------------------------------------------------
    # Include columns & joins dynamically
    # ------------------------------------------------------------------
    def _include_columns_and_joins(
        self,
        columns: Optional[List[str]] = None,
        joins: Optional[List[dict]] = None,
    ) -> tuple[Select, Dict[str, Any]]:
        base_alias = aliased(self.model)
        model_aliases = {self.model.__name__: base_alias}
        q = select().select_from(base_alias)

        if joins:
            for join in joins:
                join_path = join["path"] if isinstance(join, dict) else join
                onclause = join.get("on") if isinstance(join, dict) else None

                parts = join_path.split(".")
                current_model = self.model
                current_alias = base_alias

                for part in parts:
                    rel = getattr(current_model, part, None)
                    if not rel:
                        break
                    related_model = inspect(rel.property.mapper).class_
                    alias = model_aliases.get(related_model.__name__)
                    if not alias:
                        alias = aliased(related_model)
                        model_aliases[related_model.__name__] = alias

                    q = q.join(alias, getattr(current_alias, part))
                    current_model = related_model
                    current_alias = alias

        if columns:
            select_columns = []
            for col in columns:
                if "." not in col:
                    continue
                model_name, col_name = col.split(".", 1)
                model_alias = model_aliases.get(model_name)
                if model_alias:
                    attr = getattr(model_alias, col_name, None)
                    if attr is not None:
                        select_columns.append(attr)
            q = q.with_only_columns(*select_columns)
        else:
            q = q.with_only_columns([base_alias])

        return q, model_aliases

    # ------------------------------------------------------------------
    # Apply filters
    # ------------------------------------------------------------------
    def _apply_filters(
        self,
        query: Select,
        filter_spec: Optional[List[Dict[str, Any]]],
        model_aliases: Dict[str, Any],
    ) -> Select:
        if not filter_spec:
            return query

        for f in filter_spec:
            field_path = f.get("field")
            op = f.get("op")
            value = f.get("value")

            if not field_path:
                continue

            if "." in field_path:
                model_name, field_name = field_path.split(".", 1)
                model_alias = model_aliases.get(model_name)
            else:
                model_alias = model_aliases[self.model.__name__]
                field_name = field_path

            field: Optional[InstrumentedAttribute] = getattr(model_alias, field_name, None)
            if not field:
                continue

            match op:
                case "=" | "==":
                    expr = field == value
                case "!=":
                    expr = field != value
                case ">":
                    expr = field > value
                case "<":
                    expr = field < value
                case ">=":
                    expr = field >= value
                case "<=":
                    expr = field <= value
                case "in":
                    expr = field.in_(value)
                case "like":
                    expr = field.like(f"%{value}%")
                case "ilike":
                    expr = field.ilike(f"%{value}%")
                case _:
                    continue

            query = query.filter(expr)
        return query

    # ------------------------------------------------------------------
    # Apply order by
    # ------------------------------------------------------------------
    def _apply_ordering(
        self,
        query: Select,
        order_by: Optional[List[str]],
        model_aliases: Dict[str, Any],
    ) -> Select:
        if not order_by:
            return query

        order_clauses = []
        for ob in order_by:
            ob = ob.strip()

            if ob.endswith(" desc"):
                descending = True
                field_path = ob[:-5].strip()
            elif ob.endswith(" asc"):
                descending = False
                field_path = ob[:-4].strip()
            else:
                descending = ob.startswith("-")
                field_path = ob[1:] if descending else ob

            if "." in field_path:
                model_name, field_name = field_path.split(".", 1)
                model_alias = model_aliases.get(model_name)
            else:
                model_alias = model_aliases[self.model.__name__]
                field_name = field_path

            field = getattr(model_alias, field_name, None)
            if field is not None:
                order_clauses.append(desc(field) if descending else asc(field))

        if order_clauses:
            query = query.order_by(*order_clauses)
        return query

    # ------------------------------------------------------------------
    # Pagination helper
    # ------------------------------------------------------------------
    async def _apply_pagination(
        self,
        session: AsyncSession,
        query: Select,
        page: int = 1,
        per_page: int = 20,
    ):
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await session.execute(count_query)
        total = total_result.scalar() or 0
        query = query.limit(per_page).offset((page - 1) * per_page)
        return query, total

    # ------------------------------------------------------------------
    # Main dynamic get_all method
    # ------------------------------------------------------------------
    async def get_all(
        self,
        columns: Optional[List[str]] = None,
        joins: Optional[List[dict]] = None,
        filter_spec: Optional[List[Dict[str, Any]]] = None,
        order_by: Optional[List[str]] = None,
        page: int = 1,
        per_page: int = 20,
    ):
        async with self.session_factory() as session:
            q, model_aliases = self._include_columns_and_joins(columns, joins)
            q = self._apply_filters(q, filter_spec, model_aliases)
            q = self._apply_ordering(q, order_by, model_aliases)
            q, total = await self._apply_pagination(session, q, page, per_page)

            result = await session.execute(q)
            items = [dict(row._mapping) for row in result.all()]

            return {
                "items": items,
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": (total + per_page - 1) // per_page if per_page else 1,
            }

    async def close_scoped_session(self) -> None:
        # In async context, session management is typically handled by the context manager
        # This method might not be needed anymore
        pass