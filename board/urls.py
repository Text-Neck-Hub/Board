from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BoardViewSet, CommentListCreateView, CommentDetailView


router = DefaultRouter()
router.register(r'boards', BoardViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('boards/<int:board_id>/comments/',
         CommentListCreateView.as_view(), name='comment-list-create'),
    path('boards/<int:board_id>/comments/<int:pk>/',
         CommentDetailView.as_view(), name='comment-detail'),
]
