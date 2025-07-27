from django.http import JsonResponse
import logging

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action

from ..services.post_service import PostService
from ..tasks.post_task import FileTask

logger = logging.getLogger('prod')


class PostViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    async def create(self, request):
        try:
            data = request.data
            title = data.get('title')
            content = data.get('content')

            author_email = self.request.user.email
            board_slug = data.get('board_slug')

            thumbnail_data = data.get('thumbnail')
            attached_files_data = data.get('attached_files')

            post = PostService.create_post(
                title=title,
                content=content,
                author_email=author_email,
                board_slug=board_slug,
                thumbnail_data=thumbnail_data
            )

            file_task_id = None
            if attached_files_data:
                file_task_result = FileTask.delay(
                    post_id=post.id,
                    attached_files=attached_files_data
                )
                file_task_id = file_task_result.id

            logger.info(
                f"게시물 '{post.title}' (ID: {post.id}) 본문 및 썸네일 생성 완료. 첨부 파일 처리는 Celery 태스크({file_task_id if file_task_id else '없음'})에 위임. 작성자: {author_email}")
            return JsonResponse({
                'status': 'success',
                'message': '게시물이 성공적으로 작성되었습니다. 첨부 파일은 백그라운드에서 처리됩니다.',
                'post_id': post.id,
                'file_task_id': file_task_id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception(
                f"게시물 생성 요청 처리 중 예외 발생: {e}. 요청 데이터: {request.data}")
            return JsonResponse({
                'status': 'error',
                'message': f'게시물 생성 중 오류가 발생했습니다: {e}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def force_delete(self, request, pk=None):
        logger.info(f"관리자 요청: 게시물 {pk} 강제 삭제 시도 by {self.request.user.email}")
        return JsonResponse({'message': f'게시물 {pk} 강제 삭제 요청 완료'}, status=status.HTTP_200_OK)
