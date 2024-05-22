from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('events/', include('events.urls')),
    path('tickets/', include('tickets.urls')),
    path('management/', include('management.urls')),
]


# This code from testdriven.io allows Django to serve media files when run on
# the development server. [https://testdriven.io/blog/django-static-files/]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
