# board/urls.py

from django.urls import path, include

from .views.board_view import BoardViewSet
from .views.post_view import PostViewSet

from .views.comment_view import CommentViewSet, CommentDetailViewSet

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


board_router = DefaultRouter()

board_router.register(r'', BoardViewSet, basename='board')


posts_router = routers.NestedSimpleRouter(
    board_router,
    r'',
    lookup='board'
)
posts_router.register(r'posts', PostViewSet, basename='post')


comments_nested_router = routers.NestedSimpleRouter(
    posts_router,
    r'posts',
    lookup='post'
)
comments_nested_router.register(
    r'comments', CommentViewSet, basename='comment')


comment_detail_router = DefaultRouter()
comment_detail_router.register(
    r'comments', CommentDetailViewSet, basename='comment-detail')


urlpatterns = [

    path('', include(board_router.urls)),
    path('', include(posts_router.urls)),
    path('', include(comments_nested_router.urls)),
    path('', include(comment_detail_router.urls)),
]
