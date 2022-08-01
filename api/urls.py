from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('radios/', views.radios, name='radios'),
]
