from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('speaking/', include('speaking.urls')),
    path('user/', include('user.urls')),
    path('', views.home, name='home'),
    path('pricing', views.pricing, name='pricing')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
