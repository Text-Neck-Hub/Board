from ..models import Post, Board, AttachedFile
from django.core.files.uploadedfile import UploadedFile
from asgiref.sync import sync_to_async


class PostService:
    @staticmethod
    async def create_post(
        title: str,
        content: str,
        author: int,
        board_slug: str,
        thumbnail: UploadedFile = None,
        attached_files: list[UploadedFile] = None
    ) -> Post:

        try:
            board = await sync_to_async(Board.objects.get)(slug=board_slug)
        except Board.DoesNotExist:
            raise ValueError("해당하는 게시판을 찾을 수 없습니다.")

        post = await sync_to_async(Post.objects.create)(
            title=title,
            content=content,
            author=author,
            board=board,
            thumbnail=thumbnail,
        )

        if attached_files:
            for file_obj in attached_files:
                await sync_to_async(AttachedFile.objects.create)(
                    post=post,
                    file=file_obj,
                    file_name=file_obj.name,
                    file_size=file_obj.size,
                    mimetype=file_obj.content_type
                )
        return post

    @staticmethod
    async def update_post(
        post: Post,
        title: str = None,
        content: str = None,
        thumbnail: UploadedFile = None,
        attached_files_to_add: list[UploadedFile] = None,
        attached_file_ids_to_remove: list[int] = None
    ) -> Post:

        if title is not None:
            post.title = title
        if content is not None:
            post.content = content

        if thumbnail is not None:
            if thumbnail is False:
                post.thumbnail = None
            else:
                post.thumbnail = thumbnail

        if attached_files_to_add:
            for file_obj in attached_files_to_add:
                await sync_to_async(AttachedFile.objects.create)(
                    post=post,
                    file=file_obj,
                    file_name=file_obj.name,
                    file_size=file_obj.size,
                    mimetype=file_obj.content_type
                )

        if attached_file_ids_to_remove:
            await sync_to_async(
                lambda: AttachedFile.objects.filter(
                    post=post, id__in=attached_file_ids_to_remove).delete()
            )()

        await sync_to_async(post.save)()
        return post

    @staticmethod
    async def delete_post(post: Post):
        post_id = post.id
        await sync_to_async(post.delete)()
        print(f"게시물 ID {post_id} 삭제 완료.")
