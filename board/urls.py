from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.board_list_create_view, name='board_list_create'),
    path('board/<int:pk>/', views.board_detail_view, name='board_detail'),

]
