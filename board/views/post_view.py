import logging

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.files.uploadedfile import UploadedFile

from ..services.post_service import PostService
from ..serializers.post_serializer import PostSerializer
from ..models import Board


logger = logging.getLogger('prod')


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, board_slug=None):
        logger.info(f"PostViewSet list: board_slug={board_slug}")
        try:
            posts_queryset = PostService.get_all_posts(board_slug=board_slug)

            serializer = self.get_serializer(posts_queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            logger.error(f"PostViewSet list: Board '{board_slug}' not found.")
            return Response({'detail': f"Board '{board_slug}' not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(f"PostViewSet list: Error fetching posts: {e}")
            return Response({'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None, board_slug=None):
        logger.info(f"PostViewSet retrieve: pk={pk}, board_slug={board_slug}")
        try:
            post = PostService.get_post(post_id=pk, board_slug=board_slug)
            serializer = self.get_serializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            logger.error(
                f"PostViewSet retrieve: Board '{board_slug}' not found.")
            return Response({'detail': f"Board '{board_slug}' not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(
                f"PostViewSet retrieve: Error fetching post {pk}: {e}")
            return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, board_slug=None):
        logger.info(f"PostViewSet create: board_slug={board_slug}")
        try:
            data = request.data
            title = data.get('title')
            content = data.get('content')
            author = request.user.id
            email = request.user.email
            thumbnail = request.FILES.get('thumbnail')

            post = PostService.create_post(
                title=title,
                content=content,
                author=author,
                email=email,
                board_slug=board_slug,
                thumbnail=thumbnail
            )
            serializer = self.get_serializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            logger.error(f"PostViewSet create: Invalid data/board: {e}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"PostViewSet create: Error creating post: {e}")
            return Response({'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None, board_slug=None):
        logger.info(f"PostViewSet update: pk={pk}, board_slug={board_slug}")
        try:
            post = PostService.get_post(post_id=pk, board_slug=board_slug)
            title = request.data.get('title')
            content = request.data.get('content')
            thumbnail: UploadedFile = request.FILES.get('thumbnail')
            updated_post = PostService.update_post(
                post=post,
                title=title,
                content=content,
                thumbnail=thumbnail
            )
            serializer = self.get_serializer(updated_post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(
                f"PostViewSet update: Error updating post {pk}: {e}")
            return Response({'detail': 'Error updating post'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None, board_slug=None):
        logger.info(f"PostViewSet destroy: pk={pk}, board_slug={board_slug}")
        try:
            post = PostService.get_post(post_id=pk, board_slug=board_slug)
            PostService.delete_post(post)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.exception(
                f"PostViewSet destroy: Error deleting post {pk}: {e}")
            return Response({'detail': 'Error deleting post'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def force_delete(self, request, pk=None, board_slug=None):
        logger.info(
            f"PostViewSet force_delete: Post {pk} on board {board_slug} by {self.request.user.id}")
        try:
            post = PostService.get_post(post_id=pk, board_slug=board_slug)
            PostService.delete_post(post)
            return Response({'message': f'Post {pk} force deleted successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(
                f"PostViewSet force_delete: Error deleting post {pk}: {e}")
            return Response({'detail': 'Error force deleting post'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
