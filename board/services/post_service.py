import logging
from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import get_object_or_404
from django.db import transaction

from ..models import Post, Board
from ..utils.file_uploader import FileUploader


logger = logging.getLogger('prod')


class PostService:
    @staticmethod
    def get_all_posts(board_slug: str = None):
        logger.info(f"PostService list: board_slug={board_slug}")

        if board_slug:
            try:
                board = Board.objects.get(slug=board_slug)
                posts_queryset = Post.objects.filter(
                    board=board).order_by('-created_at')
            except Board.DoesNotExist:
                logger.error(
                    f"PostService list: Board '{board_slug}' not found.")
                raise Board.DoesNotExist
        else:
            posts_queryset = Post.objects.all().order_by('-created_at')

        logger.info(
            f"PostService list: Total posts fetched: {len(posts_queryset)}.")
        return posts_queryset

    @staticmethod
    def get_post(post_id: int, board_slug: str = None) -> Post:
        logger.info(
            f"PostService retrieve: pk={post_id}, board_slug={board_slug}")
        try:
            if board_slug:
                board = Board.objects.get(slug=board_slug)
                post = get_object_or_404(
                    Post.objects.filter(board=board), pk=post_id)
            else:
                post = get_object_or_404(Post, pk=post_id)
            logger.info(f"PostService retrieve: Post {post_id} found.")
            return post
        except Board.DoesNotExist:
            logger.error(
                f"PostService retrieve: Board '{board_slug}' not found.")
            raise
        except Exception as e:
            logger.error(
                f"PostService retrieve: Error fetching post {post_id}: {e}")
            raise

    @staticmethod
    def create_post(
        title: str,
        content: str,
        author: int,
        email: str,
        board_slug: str,
        thumbnail: UploadedFile = None,
    ) -> Post:
        logger.info(
            f"PostService create: board_slug={board_slug}, has_thumbnail={bool(thumbnail)}")

        try:
            board = Board.objects.get(slug=board_slug)
        except Board.DoesNotExist:
            logger.error(
                f"PostService create: Board '{board_slug}' not found.")
            raise ValueError(f"Board '{board_slug}' not found.")

        with transaction.atomic():
            try:
                post = Post.objects.create(
                    title=title,
                    content=content,
                    email=email,
                    author=author,
                    board=board,
                    thumbnail=thumbnail,
                )
                logger.info(f"PostService create: Post {post.id} created.")
                return post
            except Exception as e:
                logger.error(f"PostService create: Post creation error: {e}")
                raise

    @staticmethod
    def update_post(
        post: Post,
        title: str = None,
        content: str = None,
        thumbnail_file: UploadedFile = None,
    ) -> Post:
        logger.info(f"PostService update: Post {post.id} update initiated.")
        update_fields = []
        if title is not None:
            post.title = title
            update_fields.append('title')
        if content is not None:
            post.content = content
            update_fields.append('content')

        if thumbnail_file is not None:
            if thumbnail_file is False:
                post.thumbnail_url = None
                update_fields.append('thumbnail_url')
            else:
                new_thumbnail_url = FileUploader.upload_file(
                    thumbnail_file, file_type="image")
                post.thumbnail_url = new_thumbnail_url
                update_fields.append('thumbnail_url')

        update_fields.append('updated_at')

        with transaction.atomic():
            post.save(update_fields=update_fields)
        logger.info(f"PostService update: Post {post.id} updated.")
        return post

    @staticmethod
    def delete_post(post: Post):
        post_id = post.id
        with transaction.atomic():
            post.delete()
        logger.info(f"PostService delete: Post {post_id} deleted.")
