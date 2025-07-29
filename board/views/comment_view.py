import logging

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from ..services.comment_service import CommentService
from ..serializers.comment_serializer import CommentSerializer

logger = logging.getLogger('prod')


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, post_pk=None, board_slug=None):
        try:
            comments = CommentService.get_comments_by_post(
                post_id=post_pk)
            serializer = self.get_serializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("댓글 목록 조회 실패ㅠㅠ")
            return Response({'detail': '서버 오류가 발생했어요.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, post_pk=None, board_slug=None):
        content = request.data.get('content')
        if not content:
            return Response({'detail': '댓글 내용을 입력해주세요!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            comment = CommentService.create_comment(
                post_id=post_pk,
                author_id=request.user.id,
                email=request.user.email,
                content=content
            )
            serializer = self.get_serializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as ve:
            logger.warning(f"유효성 오류 발생: {ve}")
            return Response({'detail': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("댓글 생성 실패ㅠㅠ")
            return Response({'detail': '서버 오류가 발생했어요.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, post_pk=None, board_slug=None, commnet_pk=None):
        try:
            comment = CommentService.get_comment_by_id(comment_id=commnet_pk)
            serializer = self.get_serializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            logger.warning(f"댓글을 찾을 수 없어요. 댓글 ID: {commnet_pk}")
            return Response({'detail': '해당 댓글을 찾을 수 없어요!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("댓글 상세 조회 실패ㅠㅠ")
            return Response({'detail': '서버 오류가 발생했어요.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, post_pk=None, pk=None, board_slug=None):
        content = request.data.get('content')
        if not content:
            return Response({'detail': '수정할 댓글 내용을 입력해주세요!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            comment = CommentService.update_comment(
                comment_id=pk,
                content=content
            )
            serializer = self.get_serializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            logger.warning(f"댓글을 찾을 수 없어서 수정할 수 없어요. 댓글 ID: {commnet_pk}")
            return Response({'detail': '수정할 댓글을 찾을 수 없어요!'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as ve:
            logger.warning(f"댓글 수정 유효성 또는 권한 오류: {ve}")
            return Response({'detail': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("댓글 수정 실패ㅠㅠ")
            return Response({'detail': '서버 오류가 발생했어요.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, post_pk=None, pk=None, board_slug=None):
        try:
            CommentService.delete_comment(
                comment_id=pk,

            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            logger.warning(f"댓글을 찾을 수 없어서 삭제할 수 없어요. 댓글 ID: {pk}")
            return Response({'detail': '삭제할 댓글을 찾을 수 없어요!'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as ve:
            logger.warning(f"댓글 삭제 권한 오류: {ve}")
            return Response({'detail': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("댓글 삭제 실패ㅠㅠ")
            return Response({'detail': '서버 오류가 발생했어요.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
