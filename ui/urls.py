from django.urls import path
from ui import views

app_name = 'ui'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
