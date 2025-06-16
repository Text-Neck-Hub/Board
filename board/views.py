from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Board


@csrf_exempt
def board_list_create_view(request):
    if request.method == 'GET':
        boards = Board.objects.all().values(
            'id', 'title', 'content', 'created_at', 'updated_at')
        return JsonResponse(list(boards), safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        board = Board.objects.create(title=data.get(
            'title'), content=data.get('content'))
        return JsonResponse({'id': board.id, 'title': board.title, 'content': board.content, 'created_at': board.created_at, 'updated_at': board.updated_at})
    return HttpResponseNotAllowed(['GET', 'POST'])


@csrf_exempt
def board_detail_view(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'GET':
        return JsonResponse({'id': board.id, 'title': board.title, 'content': board.content, 'created_at': board.created_at, 'updated_at': board.updated_at})
    elif request.method == 'PUT':
        data = json.loads(request.body)
        board.title = data.get('title', board.title)
        board.content = data.get('content', board.content)
        board.save()
        return JsonResponse({'id': board.id, 'title': board.title, 'content': board.content, 'created_at': board.created_at, 'updated_at': board.updated_at})
    elif request.method == 'DELETE':
        board.delete()
        return JsonResponse({'result': 'deleted'})
    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])
