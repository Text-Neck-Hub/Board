from django.shortcuts import render
from django.http import JsonResponse
from .tasks import example_task

def board_async_view(request):
    # 예시: 비동기 작업 큐에 추가
    result = example_task.delay(1, 2)
    return JsonResponse({'task_id': result.id, 'status': 'queued'})
