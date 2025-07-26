from celery import shared_task
from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404
import logging

from ..services import PostService
from ..models import Post, Comment


from asgiref.sync import async_to_sync


logger = logging.getLogger('prod')


@shared_task
def process_post_creation(title: str, content: str, author_id: int, board_slug: str, thumbnail=None, attached_files=None):
    logger.info(
        f"게시물 생성 Task 시작: 제목='{title}', 작성자 ID={author_id}, 게시판='{board_slug}'")
    with transaction.atomic():  # 트랜잭션은 여전히 동기 Context에서 관리!
        try:
            # ✨ PostService.create_post가 async 함수이므로, async_to_sync로 감싸서 호출해야 해!
            post = async_to_sync(PostService.create_post)(  # ✨ 여기가 핵심! ✨
                title=title,
                content=content,
                author=author_id,
                board_slug=board_slug,
                thumbnail=thumbnail,
                attached_files=attached_files
            )
            logger.info(f"게시물 생성 Task 완료: ID {post.id}, 제목='{post.title}'")
            return {'post_id': post.id, 'title': post.title}
        except ValueError as e:
            logger.error(f"게시물 생성 Task 실패 (값 오류): {e}")
            raise
        except Exception as e:
            logger.error(f"게시물 생성 Task 실패 (기타 오류): {e}")
            raise
