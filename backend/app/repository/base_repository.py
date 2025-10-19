from contextlib import AbstractContextManager
from typing import Any, Callable, Type, TypeVar, List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.core.config import settings
from app.core.exceptions import DuplicatedError, NotFoundError
from app.model.base_model import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository:
    def __init__(self, session_factory: Session, model: Type[T]) -> None:
        self.session_factory = session_factory
        self.model = model

    def read_by_options(self, schema: T, eager: bool = False) -> dict:
        with self.session_factory() as session:
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
            
            query = session.query(self.model)
            
            if eager:
                for eager_relation in getattr(self.model, "eagers", []):
                    query = query.options(joinedload(getattr(self.model, eager_relation)))
            
            if filter_options:
                filtered_query = query.filter(filter_options)
            else:
                filtered_query = query
                
            query = filtered_query.order_by(order_query)
            
            if page_size == "all":
                results = query.all()
            else:
                results = query.limit(page_size).offset((page - 1) * page_size).all()
            
            total_count = filtered_query.count()
            
            return {
                "founds": results,
                "search_options": {
                    "page": page,
                    "page_size": page_size,
                    "ordering": ordering,
                    "total_count": total_count,
                },
            }

    def read_by_id(self, id: int, eager: bool = False) -> T:
        with self.session_factory() as session:
            query = session.query(self.model)
            if eager:
                for eager_relation in getattr(self.model, "eagers", []):
                    query = query.options(joinedload(getattr(self.model, eager_relation)))
            query = query.filter(self.model.id == id).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {id}")
            return query

    def create(self, schema: T) -> T:
        with self.session_factory() as session:
            query = self.model(**schema.dict())
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
            except IntegrityError as e:
                session.rollback()
                raise DuplicatedError(detail=str(e.orig))
            return query

    def update(self, id: int, schema: T) -> T:
        with self.session_factory() as session:
            result = session.query(self.model).filter(self.model.id == id).update(schema.dict(exclude_none=True))
            if result == 0:
                raise NotFoundError(detail=f"not found id : {id}")
            session.commit()
            return self.read_by_id(id)

    def update_attr(self, id: int, column: str, value: Any) -> T:
        with self.session_factory() as session:
            result = session.query(self.model).filter(self.model.id == id).update({column: value})
            if result == 0:
                raise NotFoundError(detail=f"not found id : {id}")
            session.commit()
            return self.read_by_id(id)

    def whole_update(self, id: int, schema: T) -> T:
        with self.session_factory() as session:
            result = session.query(self.model).filter(self.model.id == id).update(schema.dict())
            if result == 0:
                raise NotFoundError(detail=f"not found id : {id}")
            session.commit()
            return self.read_by_id(id)

    def delete_by_id(self, id: int) -> None:
        with self.session_factory() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {id}")
            session.delete(query)
            session.commit()

    def close_scoped_session(self) -> None:
        with self.session_factory() as session:
            session.close()