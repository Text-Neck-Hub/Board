from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    BoardViewSet,
    PostViewSet,
    CommentViewSet,
    PostLikeToggleView
)

router = DefaultRouter()
router.register(r'', BoardViewSet, basename='board')

urlpatterns = [
    path('', include(router.urls)),

    path('<str:category_slug>/posts/',
         PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-list-create'),
    path('<str:category_slug>/posts/<int:pk>/',
         PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='post-detail'),

    path('<str:category_slug>/posts/<int:post_id>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list-create'),
    path('<str:category_slug>/posts/<int:post_id>/comments/<int:pk>/',
         CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='comment-detail'),

    path('<str:category_slug>/posts/<int:post_id>/like/',
         PostLikeToggleView.as_view(), name='post-like-toggle'),
]
