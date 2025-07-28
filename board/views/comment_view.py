

import logging

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from ..services.comment_service import CommentService
from ..serializers.comment_serializer import CommentSerializer

logger = logging.getLogger('prod')


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # 읽기는 허용, 쓰기는 인증 필요
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        if post_pk:
            return CommentService.get_comments_by_post(post_id=post_pk)
        return Comment.objects.none()

    def list(self, request, post_pk=None):
        logger.info(f"CommentViewSet list: post_pk={post_pk}")
        try:
            comments_queryset = self.get_queryset()
            serializer = self.get_serializer(comments_queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(
                f"CommentViewSet list: Error fetching comments for post {post_pk}: {e}")
            return Response({'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, post_pk=None):
        logger.info(f"CommentViewSet create: post_pk={post_pk}")
        if not request.user.is_authenticated:
            logger.warning(
                f"CommentViewSet create: Unauthorized attempt to create comment for post {post_pk}.")
            return Response({'detail': 'Authentication required to create a comment.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            content = request.data.get('content')
            if not content:
                return Response({'detail': 'Content field is required.'}, status=status.HTTP_400_BAD_REQUEST)

            author_id = request.user.id
            email = request.user.email

            comment = CommentService.create_comment(
                post_id=post_pk,
                author_id=author_id,
                email=email,
                content=content
            )
            serializer = self.get_serializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            logger.error(
                f"CommentViewSet create: Invalid post for comment: {e}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(
                f"CommentViewSet create: Error creating comment for post {post_pk}: {e}")
            return Response({'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentDetailViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['retrieve']:
            return [permissions.AllowAny()]  # 조회는 누구나
        return [permissions.IsAuthenticated()]  # 수정, 삭제는 인증 필요

    def get_object(self):
        try:
            comment_id = self.kwargs.get('pk')
            comment = CommentService.get_comment(comment_id=comment_id)
            self.check_object_permissions(self.request, comment)
            return comment
        except ValueError as e:
            raise status.HTTP_404_NOT_FOUND

    def retrieve(self, request, pk=None):
        logger.info(f"CommentDetailViewSet retrieve: pk={pk}")
        try:
            comment = self.get_object()
            serializer = self.get_serializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(
                f"CommentDetailViewSet retrieve: Error fetching comment {pk}: {e}")
            return Response({'detail': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        logger.info(f"CommentDetailViewSet update: pk={pk}")
        try:
            comment = self.get_object()
            if comment.author_id != request.user.id:
                return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

            content = request.data.get('content')
            if not content:
                return Response({'detail': 'Content field is required.'}, status=status.HTTP_400_BAD_REQUEST)

            updated_comment = CommentService.update_comment(
                comment=comment, content=content)
            serializer = self.get_serializer(updated_comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(
                f"CommentDetailViewSet update: Invalid data for comment {pk}: {e}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(
                f"CommentDetailViewSet update: Error updating comment {pk}: {e}")
            return Response({'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        logger.info(f"CommentDetailViewSet destroy: pk={pk}")
        try:
            comment = self.get_object()
            if comment.author_id != request.user.id:
                return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

            CommentService.delete_comment(comment_id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            logger.error(
                f"CommentDetailViewSet destroy: Comment {pk} not found for deletion: {e}")
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(
                f"CommentDetailViewSet destroy: Error deleting comment {pk}: {e}")
            return Response({'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
