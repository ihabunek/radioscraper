from django.conf.urls import url
from radio import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^most-played/$', views.MostPlayedView.as_view(), name='most-played'),
    url(r'^most-played/(?P<radio_slug>\w+)/$', views.MostPlayedView.as_view(), name='most-played'),
    url(r'^plays/$', views.PlaysView.as_view(), name='plays'),
    url(r'^plays/(?P<radio_slug>\w+)/$', views.PlaysView.as_view(), name='plays'),
]
