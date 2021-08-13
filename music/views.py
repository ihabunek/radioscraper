import re

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models.aggregates import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View, ListView, DetailView, TemplateView, DeleteView

from music.models import ArtistName, Artist
from music.utils import merge_artists
from radioscraper.mixins import UserIsStaffMixin


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


class ArtistListByLetterView(ListView):
    template_name = 'music/artist_letter.html'
    model = Artist

    def dispatch(self, request, *args, **kwargs):
        self.letter = kwargs.get('letter')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()

        if re.match("^[a-z]$", self.letter):
            return qs.filter(name__iunaccent__istartswith=self.letter)

        if self.letter == '*':
            from string import ascii_lowercase
            for c in ascii_lowercase:
                qs = qs.exclude(name__iunaccent__istartswith=c)
            return qs

        raise ValueError("Invalid letter, expected a-z or *")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "letter": self.letter
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


class ArtistDeleteView(UserIsStaffMixin, DeleteView):
    model = Artist
    template_name = 'music/artist_delete.html'

    def get_success_url(self):
        return reverse('music:artist-list')


class MergeArtistsView(UserIsStaffMixin, TemplateView):
    template_name = 'music/artist_merge.html'
    http_method_names = ['post']

    def get_artists(self):
        artist_ids = self.request.POST.getlist('artist')
        if not artist_ids:
            raise ValidationError("No artists to merge given")
        return Artist.objects.filter(pk__in=artist_ids)

    def get_target_artist(self):
        artist_id = self.request.POST.get('target_artist')
        if not artist_id:
            raise ValidationError("Target artist not given")
        return Artist.objects.get(pk=artist_id)

    def get_target_name(self):
        artist_id = self.request.POST.get('target_name')
        if not artist_id:
            raise ValidationError("Target name not given")
        return ArtistName.objects.get(pk=artist_id)

    def merge(self, request):
        target_artist = self.get_target_artist()
        target_name = self.get_target_name()
        artists = self.get_artists().exclude(pk=target_artist.pk)

        merge_artists(artists, target_artist, target_name)
        messages.info(request, "Artists merged")

        url = reverse("music:artist-detail", args=[target_artist.slug])
        return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "artists": self.get_artists(),
        })
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('action') == 'Merge':
            try:
                return self.merge(request)
            except ValidationError as e:
                messages.error(request, e.message)

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class SetArtistNameView(UserIsStaffMixin, View):
    """
    Sets the default artist name.
    """
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        artist = Artist.objects.filter(pk=request.POST.get('artist')).first()
        name = ArtistName.objects.filter(pk=request.POST.get('name')).first()

        if not artist:
            messages.error(request, "Artist not given")

        if not name:
            messages.error(request, "ArtistName not given")

        if artist and name:
            artist.name = name.name
            artist.save()

        return HttpResponseRedirect(reverse("music:artist-detail", args=[artist.slug]))
