from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("outages/<int:pk>", views.OutageDetailView.as_view(), name="outage-detail"),
    path("failures/<int:pk>", views.FailureDetailView.as_view(), name="failure-detail"),
]
