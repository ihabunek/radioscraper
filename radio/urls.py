from django.conf.urls import url
from radio import views

app_name = 'radio'

urlpatterns = [
    url(r'^stats/$', views.StatsView.as_view(), name='stats'),
    url(r'^stats/(?P<radio_slug>[\w-]+)/$', views.RadioStatsView.as_view(), name='stats'),
    url(r'^stats-redirect/$', views.StatsRedirectView.as_view(), name='stats-redirect'),
    url(r'^plays/$', views.PlaysView.as_view(), name='plays'),
]
