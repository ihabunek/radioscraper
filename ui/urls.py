from django.conf.urls import url
from ui import views

app_name = 'ui'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]
