from django.conf.urls import url
from music import views

app_name = 'music'

urlpatterns = [
    url(r'^artists-by-letter/(?P<letter>[a-z\*])/$', views.ArtistListByLetterView.as_view(), name='artist-list-by-letter'),
    url(r'^artists/$', views.ArtistListView.as_view(), name='artist-list'),
    url(r'^artists/(?P<slug>[\w-]+)/$', views.ArtistDetailView.as_view(), name='artist-detail'),
    url(r'^artists/(?P<slug>[\w-]+)/delete/$', views.ArtistDeleteView.as_view(), name='artist-delete'),

    # Admin views
    url(r'^merge-artists/$', views.MergeArtistsView.as_view(), name='merge-artists'),
    url(r'^set-artist-name/$', views.SetArtistNameView.as_view(), name='set-artist-name'),
]
