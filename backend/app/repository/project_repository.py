from typing import List

from app.model.project_model import Project
from app.repository.base_repository import BaseRepository
from app.schema.project_schema import UpsertPostWithTags
from app.core.exceptions import NotFoundError


class ProjectRepository(BaseRepository):
    def __init__(self):
        super().__init__(Project)

    def create_with_tags(self, schema: UpsertPostWithTags, tags: List):
        """
        Create a post and attach related tags (many-to-many).
        """
        try:
            post = self.model(**schema.dict())
            if tags:
                for tag in tags:
                    post.addTag(tag)
            return post
        except Exception as e:
            raise Exception(f"Error creating post with tags: {e}")

    def update_with_tags(self, id: int, schema: UpsertPostWithTags, tags: List):
        """
        Update a post and reset its related tags.
        """
        post = self.read_by_id(id)
        if not post:
            raise NotFoundError(detail=f"not found id : {id}")

        # Update post fields
        for key, value in schema.dict(exclude_none=True).items():
            setattr(post, key, value)

        # Clear existing tags and reassign
        for tag in list(post.tags):
            post.removeTag(tag)

        if tags:
            for tag in tags:
                post.addTag(tag)

        return post
