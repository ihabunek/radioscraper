from django.conf.urls import url
from music import views


urlpatterns = [
    url(r'^artists/$', views.ArtistListView.as_view(), name='artist-list'),
    url(r'^artists-by-letter/(?P<letter>[a-z\*])/$', views.ArtistListByLetterView.as_view(), name='artist-list-by-letter'),
    url(r'^artists/(?P<slug>[\w-]+)/$', views.ArtistDetailView.as_view(), name='artist-detail'),

    url(r'^merge-artists/$', views.MergeArtistsView.as_view(), name='merge-artists'),
]
