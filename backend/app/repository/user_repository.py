from contextlib import AbstractContextManager
from typing import Any, Callable, List
from app.models import UserPublic
from sqlalchemy import func, select
from sqlalchemy.orm import Session
# from app.model.user_model import User
from app.models import User
from app.repository.base_repository import BaseRepository

# class UserRepository(BaseRepository):
#     def __init__(self, session: Session):
#         super().__init__(session)


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, User)

    def get_all_users(self, skip: int = 0, limit: int = 100) -> Any:
        with self.session_factory() as session:
            # Get total count
            count_stmt = select(func.count()).select_from(User)
            count = session.scalar(count_stmt)

            # Get paginated users
            stmt = select(User).offset(skip).limit(limit)
            users = session.scalars(stmt).all()

            # If service/repo already returns UsersPublic, return it directly
            # if isinstance(users, UsersPublic):
            #   return users
            # Convert ORM/SQLModel User instances to the public pydantic schema
            users_public: List[UserPublic] = [UserPublic.model_validate(u) for u in users]

            return users_public

            # return UsersPublic(data=users, count=count)
