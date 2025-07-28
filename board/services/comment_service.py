

import logging
from django.db import transaction
from ..models import Comment, Post

logger = logging.getLogger('prod')


class CommentService:
    @staticmethod
    def create_comment(post_id: int, author_id: int, email: str, content: str) -> Comment:
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            logger.error(f"CommentService create: Post '{post_id}' not found.")
            raise ValueError(f"Post '{post_id}' not found.")

        with transaction.atomic():
            comment = Comment.objects.create(
                post=post,
                author_id=author_id,
                email=email,
                content=content
            )
            logger.info(
                f"CommentService create: Comment {comment.id} created for Post {post_id}.")
            return comment

    @staticmethod
    def get_comments_by_post(post_id: int) -> list[Comment]:
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            logger.error(
                f"CommentService get_by_post: Post '{post_id}' not found.")
            return []

        return list(Comment.objects.filter(post=post))

    @staticmethod
    def get_comment(comment_id: int) -> Comment:
        try:
            comment = Comment.objects.get(id=comment_id)
            return comment
        except Comment.DoesNotExist:
            logger.error(
                f"CommentService get_comment: Comment '{comment_id}' not found.")
            raise ValueError(f"Comment '{comment_id}' not found.")

    @staticmethod
    def update_comment(comment: Comment, content: str) -> Comment:
        with transaction.atomic():
            comment.content = content
            comment.save()
            logger.info(
                f"CommentService update: Comment {comment.id} updated.")
            return comment

    @staticmethod
    def delete_comment(comment_id: int):
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            logger.info(
                f"CommentService delete: Comment {comment_id} deleted.")
        except Comment.DoesNotExist:
            logger.error(
                f"CommentService delete: Comment '{comment_id}' not found for deletion.")
            raise ValueError(f"Comment '{comment_id}' not found.")
