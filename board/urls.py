from django.urls import path
from . import views

urlpatterns = [
    path('board-async/', views.board_async_view, name='board_async'),
]
