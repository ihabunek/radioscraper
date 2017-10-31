from django.conf.urls import url
from loaders import views


urlpatterns = [
    url(r'^failures/$', views.FailureListView.as_view(), name='failure-list'),
    url(r'^failures/(?P<pk>[\d]+)/$', views.FailureDetailView.as_view(), name='failure-detail'),
]
