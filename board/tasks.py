# from celery import shared_task
# from django.db import transaction, IntegrityError
# from django.shortcuts import get_object_or_404
# import logging

# from .services import PostService, CommentService, LikeService
# from .models import Post, Comment


# logger = logging.getLogger('prod')


# @shared_task
# def process_post_creation(title: str, content: str, author_id: int, board_slug: str, thumbnail=None, attached_files=None):
#     logger.info(
#         f"게시물 생성 Task 시작: 제목='{title}', 작성자 ID={author_id}, 게시판='{board_slug}'")
#     with transaction.atomic():
#         try:
#             post = PostService.create_post(
#                 title=title,
#                 content=content,
#                 author=author_id,
#                 board_slug=board_slug,
#                 thumbnail=thumbnail,
#                 attached_files=attached_files
#             )
#             logger.info(f"게시물 생성 Task 완료: ID {post.id}, 제목='{post.title}'")
#             return {'post_id': post.id, 'title': post.title}
#         except ValueError as e:
#             logger.error(f"게시물 생성 Task 실패 (값 오류): {e}")
#             raise
#         except Exception as e:
#             logger.error(f"게시물 생성 Task 실패 (기타 오류): {e}")
#             raise


# # @shared_task
# # def process_post_update(post_id: int, title: str = None, content: str = None, thumbnail=None, attached_files_to_add=None, attached_file_ids_to_remove=None):
# #     logger.info(f"게시물 업데이트 Task 시작: ID {post_id}")
# #     with transaction.atomic():
# #         try:
# #             post = get_object_or_404(Post, pk=post_id)
# #             updated_post = PostService.update_post(
# #                 post=post,
# #                 title=title,
# #                 content=content,
# #                 thumbnail=thumbnail,
# #                 attached_files_to_add=attached_files_to_add,
# #                 attached_file_ids_to_remove=attached_file_ids_to_remove
# #             )
# #             logger.info(f"게시물 업데이트 Task 완료: ID {updated_post.id}")
# #             return {'post_id': updated_post.id, 'title': updated_post.title}
# #         except Post.DoesNotExist:
# #             logger.error(f"게시물 업데이트 Task 실패: Post ID {post_id}를 찾을 수 없습니다.")
# #             raise
# #         except Exception as e:
# #             logger.error(f"게시물 업데이트 Task 실패: {e}")
# #             raise


# # @shared_task
# # def process_post_deletion(post_id: int):
# #     logger.info(f"게시물 삭제 Task 시작: ID {post_id}")
# #     with transaction.atomic():
# #         try:
# #             post = get_object_or_404(Post, pk=post_id)
# #             PostService.delete_post(post)
# #             logger.info(f"게시물 삭제 Task 완료: ID {post_id}")
# #             return {'status': 'deleted', 'post_id': post_id}
# #         except Post.DoesNotExist:
# #             logger.error(f"게시물 삭제 Task 실패: Post ID {post_id}를 찾을 수 없습니다.")
# #             raise
# #         except Exception as e:
# #             logger.error(f"게시물 삭제 Task 실패: {e}")
# #             raise


# # @shared_task
# # def process_comment_creation(post_id: int, author_id: int, content: str):
# #     logger.info(f"댓글 생성 Task 시작: 게시물 ID {post_id}, 작성자 ID {author_id}")
# #     with transaction.atomic():
# #         try:
# #             post = get_object_or_404(Post, pk=post_id)
# #             comment = CommentService.create_comment(
# #                 post=post,
# #                 author=author_id,
# #                 content=content
# #             )
# #             logger.info(f"댓글 생성 Task 완료: ID {comment.id}")
# #             return {'comment_id': comment.id, 'content': comment.content, 'post_id': post_id}
# #         except Post.DoesNotExist:
# #             logger.error(f"댓글 생성 Task 실패: Post ID {post_id}를 찾을 수 없습니다.")
# #             raise
# #         except Exception as e:
# #             logger.error(f"댓글 생성 Task 실패: {e}")
# #             raise


# # @shared_task
# # def process_comment_update(comment_id: int, content: str):
# #     logger.info(f"댓글 업데이트 Task 시작: ID {comment_id}")
# #     with transaction.atomic():
# #         try:
# #             comment = get_object_or_404(Comment, pk=comment_id)
# #             updated_comment = CommentService.update_comment(
# #                 comment=comment,
# #                 content=content
# #             )
# #             logger.info(f"댓글 업데이트 Task 완료: ID {updated_comment.id}")
# #             return {'comment_id': updated_comment.id, 'content': updated_comment.content}
# #         except Comment.DoesNotExist:
# #             logger.error(
# #                 f"댓글 업데이트 Task 실패: Comment ID {comment_id}를 찾을 수 없습니다.")
# #             raise
# #         except Exception as e:
# #             logger.error(f"댓글 업데이트 Task 실패: {e}")
# #             raise


# # @shared_task
# # def process_like_toggle(post_id: int, user_id: int, category_slug: str):
# #     logger.info(
# #         f"좋아요 토글 Task 시작: 게시물 ID {post_id}, 사용자 ID {user_id}, 게시판 슬러그 {category_slug}")
# #     with transaction.atomic():
# #         try:
# #             post = get_object_or_404(
# #                 Post, pk=post_id, board__slug=category_slug)

# #             added = LikeService.toggle_like(post=post, user_id=user_id)

# #             if added:
# #                 logger.info(f"좋아요 추가 완료: 게시물 ID {post_id}, 사용자 ID {user_id}")
# #                 return {"status": "added", "post_id": post_id, "user_id": user_id}
# #             else:
# #                 logger.info(f"좋아요 취소 완료: 게시물 ID {post_id}, 사용자 ID {user_id}")
# #                 return {"status": "removed", "post_id": post_id, "user_id": user_id}
# #         except IntegrityError:
# #             logger.warning(
# #                 f"좋아요 토글 Task 경고: 이미 처리된 요청 (게시물 ID {post_id}, 사용자 ID {user_id})"
# #             )
# #             return {"status": "already_processed", "post_id": post_id, "user_id": user_id}
# #         except Post.DoesNotExist:
# #             logger.error(
# #                 f"좋아요 토글 Task 실패: 게시물 ID {post_id} 또는 게시판 슬러그 {category_slug}를 찾을 수 없습니다.")
# #             raise
# #         except Exception as e:
# #             logger.error(f"좋아요 토글 Task 실패 (기타 오류): {e}")
# #             raise
