# from django.db import transaction
# from .models import Post, Comment, Board, Like, AttachedFile
# from django.core.files.uploadedfile import UploadedFile


# class PostService:
#     @staticmethod
#     def create_post(
#         title: str,
#         content: str,
#         author: int,
#         board_slug: str,
#         thumbnail: UploadedFile = None,
#         attached_files: list[UploadedFile] = None
#     ) -> Post:
#         with transaction.atomic():
#             try:
#                 board = Board.objects.get(slug=board_slug)
#             except Board.DoesNotExist:
#                 raise ValueError("해당하는 게시판을 찾을 수 없습니다.")

#             post = Post.objects.create(
#                 title=title,
#                 content=content,
#                 author=author,
#                 board=board,
#                 thumbnail=thumbnail,
#             )

#             if attached_files:
#                 for file_obj in attached_files:
#                     AttachedFile.objects.create(
#                         post=post,
#                         file=file_obj,
#                         file_name=file_obj.name,
#                         file_size=file_obj.size,
#                         mimetype=file_obj.content_type
#                     )

#             return post

#     @staticmethod
#     def update_post(
#         post: Post,
#         title: str = None,
#         content: str = None,
#         thumbnail: UploadedFile = None,
#         attached_files_to_add: list[UploadedFile] = None,
#         attached_file_ids_to_remove: list[int] = None
#     ) -> Post:
#         with transaction.atomic():
#             if title is not None:
#                 post.title = title
#             if content is not None:
#                 post.content = content

#             if thumbnail is not None:
#                 if thumbnail is False:
#                     post.thumbnail = None
#                 else:
#                     post.thumbnail = thumbnail

#             if attached_files_to_add:
#                 for file_obj in attached_files_to_add:
#                     AttachedFile.objects.create(
#                         post=post,
#                         file=file_obj,
#                         file_name=file_obj.name,
#                         file_size=file_obj.size,
#                         mimetype=file_obj.content_type
#                     )

#             if attached_file_ids_to_remove:
#                 AttachedFile.objects.filter(
#                     post=post, id__in=attached_file_ids_to_remove).delete()

#             post.save()
#             return post

#     @staticmethod
#     def delete_post(post: Post):
#         with transaction.atomic():
#             post_id = post.id
#             post.delete()
#             print(f"게시물 ID {post_id} 삭제 완료.")


# class CommentService:
#     @staticmethod
#     def create_comment(post: Post, author: int, content: str) -> Comment:
#         with transaction.atomic():
#             comment = Comment.objects.create(
#                 post=post,
#                 author=author,
#                 content=content
#             )
#             return comment

#     @staticmethod
#     def update_comment(comment: Comment, content: str) -> Comment:
#         with transaction.atomic():
#             comment.content = content
#             comment.save()
#             return comment

#     @staticmethod
#     def delete_comment(comment: Comment):
#         with transaction.atomic():
#             comment_id = comment.id
#             comment.delete()
#             print(f"댓글 ID {comment_id} 삭제 완료.")


# class LikeService:
#     @staticmethod
#     def toggle_like(post: Post, user_id: int) -> bool:
#         with transaction.atomic():
#             like_instance, created = Like.objects.get_or_create(
#                 post=post, user=user_id)
#             if not created:
#                 like_instance.delete()
#                 return False
#             return True
