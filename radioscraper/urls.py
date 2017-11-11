from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include('radio.urls', namespace='radio')),
    url('', include('loaders.urls', namespace='loaders')),
    url('', include('music.urls', namespace='music')),
    url('', include('ui.urls', namespace='ui')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
