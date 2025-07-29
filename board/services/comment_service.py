import logging
from django.db import transaction
from ..models import Comment, Post

logger = logging.getLogger('prod')


class CommentService:
    @staticmethod
    def create_comment(post_id, author_id, email, content):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise ValueError(f"Post '{post_id}' not found.")

        with transaction.atomic():
            comment = Comment.objects.create(
                post=post,
                author=author_id,
                email=email,
                content=content
            )
            logger.info(
                f"CommentService create: Comment {comment.id} created for Post {post_id}.")
            return comment

    @staticmethod
    def get_comment(comment_id: int) -> Comment:
        try:
            comment = Comment.objects.get(id=comment_id)
            logger.info(
                f"CommentService get_comment: Retrieved comment {comment_id}.")
            return comment
        except Comment.DoesNotExist:
            raise ValueError(f"Comment '{comment_id}' not found.")

    @staticmethod
    def get_comments_by_post(post_id):
        try:
            return list(Comment.objects.filter(post=post_id).order_by('created_at'))
        except Post.DoesNotExist:
            return []

    @staticmethod
    def update_comment(comment_id, content) -> Comment:
        comment = Comment.objects.get(pk=comment_id)
        with transaction.atomic():

            comment.content = content
            comment.save()
            logger.info(
                f"CommentService update: Comment {comment.id} updated with new content.")
            return comment

    @staticmethod
    def delete_comment(comment_id: int):
        with transaction.atomic():
            try:
                comment = Comment.objects.get(pk=comment_id)
                comment.delete()
                logger.info(
                    f"CommentService delete: Comment {comment_id} deleted successfully.")
            except Comment.DoesNotExist:
                raise ValueError(f"Comment '{comment_id}' not found.")
