from django.urls import path, include
from rest_framework_nested import routers


from .views.views import (
    BoardViewSet,
    PostViewSet,

)


from .routers.board_router import board_router


posts_router = routers.NestedSimpleRouter(
    board_router, r'boards', lookup='category')
posts_router.register(r'posts', PostViewSet, basename='post')


urlpatterns = [
    path('', include(board_router.urls)),

    path('', include(posts_router.urls)),


]
