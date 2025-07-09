# your_project_name/urls.py (Board 서비스의 최상위 urls.py)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


admin.site.root_path = '/board-admin/'

urlpatterns = [
    
    path('board-admin/', admin.site.urls), 
    path('v2/', include('board.urls')),
    path('prometheus/', include('django_prometheus.urls')), 
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)