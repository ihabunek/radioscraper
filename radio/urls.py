from django.conf.urls import url, include
from django.contrib import admin
from radio.views import IndexView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include('radio.urls', namespace='radio')),
]
