from django.urls import path
from loaders import views

app_name = 'loaders'

urlpatterns = [
    path('failures/', views.FailureListView.as_view(), name='failure-list'),
    path('failures/<int:pk>/$', views.FailureDetailView.as_view(), name='failure-detail'),
]
