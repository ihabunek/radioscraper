from django.conf.urls import url
from radio import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^stats/$', views.StatsView.as_view(), name='stats'),
    url(r'^stats/(?P<radio_slug>\w+)/$', views.StatsView.as_view(), name='stats'),
    url(r'^plays/$', views.PlaysView.as_view(), name='plays'),
    url(r'^plays/(?P<radio_slug>\w+)/$', views.PlaysView.as_view(), name='plays'),
]
