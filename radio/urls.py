from django.urls import path
from radio import views

app_name = 'radio'

urlpatterns = [
    path('stats/', views.StatsView.as_view(), name='stats'),
    path('stats/<slug:slug>/', views.RadioStatsView.as_view(), name='stats'),
    path('stats-redirect/', views.StatsRedirectView.as_view(), name='stats-redirect'),
    path('plays/', views.PlaysView.as_view(), name='plays'),
]
