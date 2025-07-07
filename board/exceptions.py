
from rest_framework.exceptions import APIException
from rest_framework import status


class BoardDoesNotExist(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = '요청하신 게시글을 찾을 수 없습니다.'
    default_code = 'board_not_found'


class InvalidContentError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '내용이 유효하지 않습니다.'
    default_code = 'invalid_content'
