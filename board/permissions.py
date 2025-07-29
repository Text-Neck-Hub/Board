from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = '권한이 없습니다. 해당 게시글의 작성자만 수정하거나 삭제할 수 있습니다.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user.id
