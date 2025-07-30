import logging

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from ..services.like_service import LikeService
from ..serializers.like_serializer import LikeSerializer

logger = logging.getLogger('prod')


class LikeViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer

    def create(self, request, post_pk=None):
        user_id = request.user.id

        try:
            like = LikeService.add_like(user_id=user_id, post_id=post_pk)
            serializer = self.get_serializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as ve:
            logger.warning(f"좋아요 추가 유효성 오류: {ve}")
            return Response({'detail': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("좋아요 추가 실패")
            return Response({'detail': '서버 오류로 좋아요를 추가할 수 없습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, post_pk=None):
        user_id = request.user.id

        try:
            LikeService.remove_like(user_id=user_id, post_id=post_pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as ve:
            logger.warning(f"좋아요 취소 유효성 오류: {ve}")
            return Response({'detail': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("좋아요 취소 실패")
            return Response({'detail': '서버 오류로 좋아요를 취소할 수 없습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
