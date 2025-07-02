# your_app_name/exceptions.py (새로운 파일 만들어주는 게 좋아!)
from rest_framework.exceptions import APIException
from rest_framework import status


class BoardDoesNotExist(APIException):  # DRF의 APIException을 상속받으면 좋아!
    status_code = status.HTTP_404_NOT_FOUND  # 404 에러로 보내고 싶을 때
    default_detail = '요청하신 게시글을 찾을 수 없습니다.'
    default_code = 'board_not_found'


class InvalidContentError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST  # 400 에러로 보내고 싶을 때
    default_detail = '내용이 유효하지 않습니다.'
    default_code = 'invalid_content'

# 그리고 views.py나 services.py에서 이렇게 사용할 수 있어!
# from .exceptions import BoardDoesNotExist, InvalidContentError

# def some_function(board_id, content):
#     try:
#         board = Board.objects.get(id=board_id)
#     except Board.DoesNotExist:
#         raise BoardDoesNotExist() # 예외 발생!

#     if len(content) < 5:
#         raise InvalidContentError(detail="내용은 최소 5자 이상이어야 합니다.") # 커스텀 메시지 전달도 가능!
