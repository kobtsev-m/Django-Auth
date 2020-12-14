from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url
from django.conf import settings

from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('', include('common.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns.extend([
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
    ])