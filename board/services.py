# your_app_name/services.py
from .models import Board, Comment
from django.shortcuts import get_object_or_404

# 게시글 관련 비즈니스 로직


class BoardService:
    @staticmethod
    def create_board(title, content):
        # 실제 DB 저장 로직
        board = Board.objects.create(title=title, content=content)
        print(f"BoardService: 게시글 생성 완료: ID {board.id}")
        return board

    @staticmethod
    def update_board(board_id, title=None, content=None):
        board = get_object_or_404(Board, id=board_id)
        if title is not None:
            board.title = title
        if content is not None:
            board.content = content
        board.save()
        print(f"BoardService: 게시글 업데이트 완료: ID {board.id}")
        return board

    @staticmethod
    def delete_board(board_id):
        board = get_object_or_404(Board, id=board_id)
        board.delete()
        print(f"BoardService: 게시글 삭제 완료: ID {board_id}")

# 댓글 관련 비즈니스 로직


class CommentService:
    @staticmethod
    def create_comment(board_id, content):
        board = get_object_or_404(Board, id=board_id)
        comment = board.comments.create(content=content)
        print(f"CommentService: 댓글 생성 완료: ID {comment.id}")
        return comment

    @staticmethod
    def update_comment(comment_id, content):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.content = content
        comment.save()
        print(f"CommentService: 댓글 업데이트 완료: ID {comment.id}")
        return comment

    @staticmethod
    def delete_comment(comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        print(f"CommentService: 댓글 삭제 완료: ID {comment_id}")
