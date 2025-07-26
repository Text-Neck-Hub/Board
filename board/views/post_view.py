from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import logging
import json


from ..tasks import process_post_creation

logger = logging.getLogger('prod')


@require_http_methods(["POST"])
async def create_post_view(request):
    try:

        data = json.loads(request.body)
        title = data.get('title')
        content = data.get('content')
        author_id = data.get('author_id')
        board_slug = data.get('board_slug')

        thumbnail_url = None

        attached_file_urls = None

        task = process_post_creation.delay(
            title=title,
            content=content,
            author_id=author_id,
            board_slug=board_slug,
            thumbnail_url=thumbnail_url,
            attached_file_urls=attached_file_urls
        )

        logger.info(f"게시물 생성 요청 수신 및 Celery 태스크({task.id})에 위임.")
        return JsonResponse({
            'status': 'success',
            'message': '게시물 생성이 백그라운드에서 처리됩니다.',
            'task_id': task.id
        }, status=202)

    except json.JSONDecodeError:
        logger.error("잘못된 JSON 형식 요청 수신.")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
    except Exception as e:
        logger.exception(f"게시물 생성 요청 처리 중 예외 발생: {e}")
        return JsonResponse({'status': 'error', 'message': 'Server error processing your request'}, status=500)
