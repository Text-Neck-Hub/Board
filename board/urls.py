from django.urls import path, include
from rest_framework_nested import routers

from .views.post_view import PostViewSet

from .routers.board_router import board_router


posts_router = routers.NestedSimpleRouter(
    board_router, r'', lookup='category')
posts_router.register(r'posts', PostViewSet, basename='post')


urlpatterns = [
    path('', include(board_router.urls)),

    path('', include(posts_router.urls)),
]
