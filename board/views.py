from celery import shared_task
# from .models import Board, Comment # 이제 모델을 직접 불러올 필요 없어!
# from django.shortcuts import get_object_or_404 # 이것도 필요 없어!
import time  # 지연 시간 확인용

from .services import BoardService, CommentService  # 새로 만든 서비스 불러오기!


@shared_task
def create_board_task(title, content):
    print(f"Celery Task: 게시글 생성 Task 시작: {title}")
    try:
        board = BoardService.create_board(title, content)  # 서비스 레이어 호출!
        time.sleep(3)  # 작업 시뮬레이션
        print(f"Celery Task: 게시글 생성 Task 완료: ID {board.id}")
        return {'id': board.id, 'title': board.title, 'content': board.content}
    except Exception as e:
        print(f"Celery Task: 게시글 생성 Task 실패: {e}")
        raise


@shared_task
def update_board_task(board_id, title=None, content=None):
    print(f"Celery Task: 게시글 업데이트 Task 시작: ID {board_id}")
    try:
        BoardService.update_board(board_id, title, content)  # 서비스 레이어 호출!
        time.sleep(1)  # 작업 시뮬레이션
        print(f"Celery Task: 게시글 업데이트 Task 완료: ID {board_id}")
    except Exception as e:
        print(f"Celery Task: 게시글 업데이트 Task 실패: {e}")
        raise


@shared_task
def delete_board_task(board_id):
    print(f"Celery Task: 게시글 삭제 Task 시작: ID {board_id}")
    try:
        BoardService.delete_board(board_id)  # 서비스 레이어 호출!
        time.sleep(1)  # 작업 시뮬레이션
        print(f"Celery Task: 게시글 삭제 Task 완료: ID {board_id}")
    except Exception as e:
        print(f"Celery Task: 게시글 삭제 Task 실패: {e}")
        raise


@shared_task
def create_comment_task(board_id, content):
    print(f"Celery Task: 댓글 생성 Task 시작: Board ID {board_id}")
    try:
        comment = CommentService.create_comment(
            board_id, content)  # 서비스 레이어 호출!
        time.sleep(2)  # 작업 시뮬레이션
        print(f"Celery Task: 댓글 생성 Task 완료: ID {comment.id}")
        return {'id': comment.id, 'content': comment.content, 'board_id': board_id}
    except Exception as e:
        print(f"Celery Task: 댓글 생성 Task 실패: {e}")
        raise


@shared_task
def update_comment_task(comment_id, content):
    print(f"Celery Task: 댓글 업데이트 Task 시작: ID {comment_id}")
    try:
        CommentService.update_comment(comment_id, content)  # 서비스 레이어 호출!
        time.sleep(1)  # 작업 시뮬레이션
        print(f"Celery Task: 댓글 업데이트 Task 완료: ID {comment_id}")
    except Exception as e:
        print(f"Celery Task: 댓글 업데이트 Task 실패: {e}")
        raise


@shared_task
def delete_comment_task(comment_id):
    print(f"Celery Task: 댓글 삭제 Task 시작: ID {comment_id}")
    try:
        CommentService.delete_comment(comment_id)  # 서비스 레이어 호출!
        time.sleep(1)  # 작업 시뮬레이션
        print(f"Celery Task: 댓글 삭제 Task 완료: ID {comment_id}")
    except Exception as e:
        print(f"Celery Task: 댓글 삭제 Task 실패: {e}")
        raise
