from rest_framework.routers import DefaultRouter
from ..views.board_view import BoardViewSet

board_router = DefaultRouter()
board_router.register(r'', BoardViewSet, basename='board')
