from celery import shared_task
from .models import Board, Comment
from django.shortcuts import get_object_or_404


@shared_task
def create_board_task(title, content):
    print(f"게시글 생성 Task 시작: {title}")
    try:
        board = Board.objects.create(title=title, content=content)
        print(f"게시글 생성 Task 완료: ID {board.id}")
        return {'id': board.id, 'title': board.title, 'content': board.content}
    except Exception as e:
        print(f"게시글 생성 Task 실패: {e}")

        raise


@shared_task
def update_board_task(board_id, title=None, content=None):
    print(f"게시글 업데이트 Task 시작: ID {board_id}")
    try:
        board = get_object_or_404(Board, id=board_id)
        if title is not None:
            board.title = title
        if content is not None:
            board.content = content
        board.save()
        print(f"게시글 업데이트 Task 완료: ID {board.id}")
    except Board.DoesNotExist:
        print(f"게시글 업데이트 Task 실패: Board ID {board_id}를 찾을 수 없습니다.")
    except Exception as e:
        print(f"게시글 업데이트 Task 실패: {e}")
        raise


@shared_task
def delete_board_task(board_id):
    print(f"게시글 삭제 Task 시작: ID {board_id}")
    try:
        board = get_object_or_404(Board, id=board_id)
        board.delete()
        print(f"게시글 삭제 Task 완료: ID {board_id}")
    except Board.DoesNotExist:
        print(f"게시글 삭제 Task 실패: Board ID {board_id}를 찾을 수 없습니다.")
    except Exception as e:
        print(f"게시글 삭제 Task 실패: {e}")
        raise


@shared_task
def create_comment_task(board_id, content):
    print(f"댓글 생성 Task 시작: Board ID {board_id}")
    try:
        board = get_object_or_404(Board, id=board_id)
        comment = board.comments.create(content=content)
        print(f"댓글 생성 Task 완료: ID {comment.id}")
        return {'id': comment.id, 'content': comment.content, 'board_id': board_id}
    except Board.DoesNotExist:
        print(f"댓글 생성 Task 실패: Board ID {board_id}를 찾을 수 없습니다.")
    except Exception as e:
        print(f"댓글 생성 Task 실패: {e}")
        raise


@shared_task
def update_comment_task(comment_id, content):
    print(f"댓글 업데이트 Task 시작: ID {comment_id}")
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        comment.content = content
        comment.save()
        print(f"댓글 업데이트 Task 완료: ID {comment.id}")
    except Comment.DoesNotExist:
        print(f"댓글 업데이트 Task 실패: Comment ID {comment_id}를 찾을 수 없습니다.")
    except Exception as e:
        print(f"댓글 업데이트 Task 실패: {e}")
        raise


@shared_task
def delete_comment_task(comment_id):
    print(f"댓글 삭제 Task 시작: ID {comment_id}")
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        print(f"댓글 삭제 Task 완료: ID {comment_id}")
    except Comment.DoesNotExist:
        print(f"댓글 삭제 Task 실패: Comment ID {comment_id}를 찾을 수 없습니다.")
    except Exception as e:
        print(f"댓글 삭제 Task 실패: {e}")
        raise
