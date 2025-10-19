from contextlib import AbstractAsyncContextManager
from typing import Any, Callable, List
from app.models import UserPublic
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        super().__init__(session_factory, User)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> Any:
        async with self.session_factory() as session:
            # Get total count - await the scalar result
            count_stmt = select(func.count()).select_from(User)
            count = await session.scalar(count_stmt)

            # Get paginated users - await the scalars result
            stmt = select(User).offset(skip).limit(limit)
            result = await session.scalars(stmt)
            users = result.all()

            # Convert ORM/SQLModel User instances to the public pydantic schema
            users_public: List[UserPublic] = [UserPublic.model_validate(u) for u in users]

            return users_public