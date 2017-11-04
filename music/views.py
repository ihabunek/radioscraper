from django.db.models.aggregates import Count
from django.views.generic import ListView, DetailView

from music.models import ArtistName, Artist


class ArtistListView(ListView):
    model = Artist
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q', None)

        if query:
            return qs.filter(pk__in=self.find_artist_ids(query))

        return qs.none()

    def find_artist_ids(self, query):
        return (ArtistName.objects
            .filter(name__iunaccent__icontains=query)
            .values_list('artist_id', flat=True)
            .distinct())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "q": self.request.GET.get('q'),
        })
        return context


class ArtistDetailView(DetailView):
    model = Artist

    def get_radios(self):
        return (self.object.play_set
            .values_list("radio__slug", "radio__name")
            .annotate(count=Count("*"))
            .order_by('-count'))

    def get_songs(self):
        return (self.object.play_set
            .values_list("title")
            .annotate(count=Count("*"))
            .order_by('-count'))[:10]

    def get_plays(self):
        return (self.object.play_set
            .prefetch_related('radio')
            .order_by('-timestamp'))[:20]

    def get_chart_data(self):
        return (self.object.play_set
            .extra(select={'day': 'date(timestamp)'})
            .order_by('day')
            .values('day')
            .annotate(count=Count("*"))
            .values_list('day', 'count'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "plays": self.get_plays(),
            "radios": self.get_radios(),
            "songs": self.get_songs(),
            "chart_data": self.get_chart_data(),
        })
        return context
