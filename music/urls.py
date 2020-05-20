from django.urls import path, re_path
from music import views

app_name = 'music'

urlpatterns = [
    re_path(r'^artists-by-letter/(?P<letter>[a-z\*])/$', views.ArtistListByLetterView.as_view(), name='artist-list-by-letter'),
    path('artists/', views.ArtistListView.as_view(), name='artist-list'),
    path('artists/<slug:slug>/', views.ArtistDetailView.as_view(), name='artist-detail'),
    path('artists/<slug:slug>/delete/', views.ArtistDeleteView.as_view(), name='artist-delete'),

    # Admin views
    path('merge-artists/', views.MergeArtistsView.as_view(), name='merge-artists'),
    path('set-artist-name/', views.SetArtistNameView.as_view(), name='set-artist-name'),
]
