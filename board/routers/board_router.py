from rest_framework.routers import DefaultRouter
from ..views.views import BoardViewSet

board_router = DefaultRouter()
board_router.register(r'boards', BoardViewSet, basename='board')
