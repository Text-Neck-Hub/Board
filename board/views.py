from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Board, Post, Comment
from .serializers import BoardSerializer, PostSerializer, CommentSerializer


from .tasks import (
    process_post_creation, process_post_update, process_post_deletion,
    process_comment_creation, process_comment_update, process_comment_deletion,
    process_like_toggle
)

from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class BoardViewSet(viewsets.ModelViewSet):
    """
    게시판(카테고리) 리소스에 대한 CRUD API 뷰셋.
    게시판 생성, 수정, 삭제는 관리자만 가능하도록 설정.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            board = get_object_or_404(Board, slug=category_slug)
            return Post.objects.filter(board=board).order_by('-created_at')
        return super().get_queryset()

    def perform_create(self, serializer):
        board_slug = self.kwargs.get('category_slug')
        if not board_slug:
            raise ValidationError({"detail": "게시판 슬러그가 URL에 지정되지 않았습니다."})

        author_id = getattr(self.request.user, 'id', None)
        if not self.request.user.is_authenticated or author_id is None:
            raise ValidationError({"detail": "인증된 사용자만 게시물을 작성할 수 있습니다."})

        thumbnail_file = self.request.FILES.get('thumbnail')
        attached_files_list = self.request.FILES.getlist('attachments')

        task = process_post_creation.delay(
            title=serializer.validated_data['title'],
            content=serializer.validated_data['content'],
            author_id=author_id,
            board_slug=board_slug,
            thumbnail=thumbnail_file,
            attached_files=attached_files_list
        )
        return Response(
            {"message": "게시물 생성을 시작했습니다.", "task_id": task.id},
            status=status.HTTP_202_ACCEPTED
        )

    def perform_update(self, serializer):
        post = self.get_object()
        user_id = getattr(self.request.user, 'id', None)

        if post.author != user_id:
            return Response({"detail": "이 게시물을 수정할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        thumbnail_file = self.request.FILES.get('thumbnail')
        attached_files_to_add = self.request.FILES.getlist(
            'attachments_to_add')
        attached_file_ids_to_remove = serializer.validated_data.get(
            'attachments_to_remove_ids', [])

        thumbnail_delete = serializer.validated_data.get(
            'thumbnail_delete', False)

        thumbnail_to_service = thumbnail_file if thumbnail_file else (
            False if thumbnail_delete else None)

        task = process_post_update.delay(
            post_id=post.pk,
            title=serializer.validated_data.get('title'),
            content=serializer.validated_data.get('content'),
            thumbnail=thumbnail_to_service,
            attached_files_to_add=attached_files_to_add,
            attached_file_ids_to_remove=attached_file_ids_to_remove
        )
        return Response(
            {"message": "게시물 업데이트를 시작했습니다.", "task_id": task.id},
            status=status.HTTP_202_ACCEPTED
        )

    def perform_destroy(self, instance):
        user_id = getattr(self.request.user, 'id', None)

        if instance.author != user_id:
            return Response({"detail": "이 게시물을 삭제할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        task = process_post_deletion.delay(instance.pk)
        return Response(
            {"message": "게시물 삭제를 시작했습니다.", "task_id": task.id},
            status=status.HTTP_202_ACCEPTED
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        post_id = self.kwargs.get('post_id')

        if category_slug and post_id:
            post = get_object_or_404(
                Post, pk=post_id, board__slug=category_slug)
            return Comment.objects.filter(post=post).order_by('created_at')
        return Comment.objects.none()

    def perform_create(self, serializer):
        category_slug = self.kwargs.get('category_slug')
        post_id = self.kwargs.get('post_id')

        post = get_object_or_404(Post, pk=post_id, board__slug=category_slug)

        author_id = getattr(self.request.user, 'id', None)
        if not self.request.user.is_authenticated or author_id is None:
            raise ValidationError({"detail": "인증된 사용자만 댓글을 작성할 수 있습니다."})

        task = process_comment_creation.delay(
            post_id=post.pk,
            author_id=author_id,
            content=serializer.validated_data['content']
        )
        return Response(
            {"message": "댓글 생성을 시작했습니다.", "task_id": task.id},
            status=status.HTTP_202_ACCEPTED
        )

    def perform_update(self, serializer):
        comment = self.get_object()
        user_id = getattr(self.request.user, 'id', None)

        if comment.author != user_id:
            return Response({"detail": "이 댓글을 수정할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        task = process_comment_update.delay(
            comment_id=comment.pk,
            content=serializer.validated_data['content']
        )
        return Response(
            {"message": "댓글 업데이트를 시작했습니다.", "task_id": task.id},
            status=status.HTTP_202_ACCEPTED
        )

    def perform_destroy(self, instance):
        user_id = getattr(self.request.user, 'id', None)

        if instance.author != user_id:
            return Response({"detail": "이 댓글을 삭제할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        task = process_comment_deletion.delay(instance.pk)
        return Response(
            {"message": "댓글 삭제를 시작했습니다.", "task_id": task.id},
            status=status.HTTP_202_ACCEPTED
        )


class PostLikeToggleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, category_slug, post_id):
        board = get_object_or_404(Board, slug=category_slug)
        post = get_object_or_404(Post, pk=post_id, board=board)

        user_id = getattr(self.request.user, 'id', None)
        if not self.request.user.is_authenticated or user_id is None:
            raise ValidationError({"detail": "인증된 사용자만 좋아요를 누를 수 있습니다."})

        task = process_like_toggle.delay(
            post_id=post.pk,
            user_id=user_id,
            category_slug=category_slug
        )
        return Response(
            {"message": "좋아요/취소 요청을 처리 중입니다.", "task_id": task.id},
            status=status.HTTP_202_ACCEPTED
        )
