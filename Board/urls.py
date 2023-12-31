from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('appointments/', include(('appointment.urls', 'appointments'), namespace='appointments')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include("backend.profiles.urls")),
    path('callboard/', include('backend.callboard.urls')),
    path('accounts/', include('allauth.urls')),


]

# подключили медиа
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    # path('api-auth/', include('rest_framework.urls')),
    # path('profile/', include("backend.profiles.urls")),
    # path('', include("backend.callboard.urls")),