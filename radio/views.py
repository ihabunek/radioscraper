from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from urllib.parse import urlencode

from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, TemplateView, RedirectView

from radio.models import Radio, Play
from radio.utils.stats import get_song_stats, get_artist_stats, get_most_played_artists


def get_year_month(request):
    today = date.today()
    default = [today.year, today.month]

    try:
        year = int(request.GET.get('year'))
        month = int(request.GET.get('month'))
    except:
        return default

    if year < 2000 or year > today.year or month < 1 or month > 12:
        return default

    return [year, month]


def stats_url(path, year, month, radio=None):
    if month < 1:
        month = 12
        year = year - 1

    if month > 12:
        month = 1
        year = year + 1

    today = date.today()
    if year < 2017 or year > today.year or (year == today.year and month > today.month):
        return None

    query = urlencode({
        "year": year,
        "month": month,
        "radio": radio,
    })

    return "{}?{}".format(path, query)


def prev_next_links(path, year, month, radio=None):
    return {
        "prev_month": stats_url(path, year, month - 1, radio),
        "next_month": stats_url(path, year, month + 1, radio),
        "prev_year": stats_url(path, year - 1, month, radio),
        "next_year": stats_url(path, year + 1, month, radio),
    }


class StatsRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        year, month = get_year_month(self.request)
        radio = self.request.GET.get("radio", "").strip()

        return "{}?{}".format(
            reverse("radio:stats", args=[radio] if radio else []),
            urlencode({"year": year, "month": month})
        )


class RadioStatsView(TemplateView):
    template_name = 'radio/radio_stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = self.kwargs.get('radio_slug')
        radio = get_object_or_404(Radio, slug=slug)

        year, month = get_year_month(self.request)
        start = date(year, month, 1)
        end = start + relativedelta(months=1)
        play_count = radio.plays(start, end).count()

        context.update({
            "radio": radio,
            "month": month,
            "year": year,
            "play_count": play_count,
        })

        context.update(
            prev_next_links(self.request.path, year, month, radio.slug)
        )

        if play_count > 0:
            context.update({
                "song_stats": get_song_stats(start, end, radio.id),
                "artist_stats": get_artist_stats(start, end, radio.id),
                "most_played_songs": radio.most_played_songs(start, end)[:30],
                "most_played_artists": get_most_played_artists(radio, start, end)[:30],
                "most_played_daily": radio.most_played_daily(start, end).first()
            })

        return context


class StatsView(TemplateView):
    template_name = 'radio/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        year, month = get_year_month(self.request)
        start = date(year, month, 1)
        end = start + relativedelta(months=1)

        plays = Play.objects.month(year, month)
        play_count = plays.count()

        context.update({
            "month": month,
            "year": year,
            "play_count": play_count,
        })

        context.update(
            prev_next_links(self.request.path, year, month)
        )

        if play_count > 0:
            most_played_songs = (plays
                .values('artist_name', 'title')
                .annotate(count=Count('*'))
                .order_by('-count'))[:30]

            context.update({
                "song_stats": get_song_stats(start, end),
                "artist_stats": get_artist_stats(start, end),
                "most_played_songs": most_played_songs,
                "most_played_artists": get_most_played_artists(None, start, end)[:30],
            })

        return context


class PlaysView(ListView):
    template_name = 'radio/plays.html'
    queryset = Play.objects.all().order_by("-timestamp").prefetch_related('radio', 'artist')
    context_object_name = 'plays'
    paginate_by = 100

    def _parse_date(self, value):
        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except:
            return None

    def dispatch(self, *args, **kwargs):
        self.artist_name = self.request.GET.get('artist_name')
        self.title = self.request.GET.get('title')
        self.radio = self.request.GET.get('radio')
        self.start = self._parse_date(self.request.GET.get('start'))
        self.end = self._parse_date(self.request.GET.get('end'))

        return super(PlaysView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PlaysView, self).get_context_data(**kwargs)
        context.update({
            'radio': self.radio,
            'artist_name': self.artist_name,
            'title': self.title,
            'start': self.start,
            'end': self.end,
        })
        return context

    def get_queryset(self):
        qs = super(PlaysView, self).get_queryset()

        if self.radio:
            qs = qs.filter(radio__slug=self.radio)

        if self.artist_name:
            qs = qs.filter(artist_name__iunaccent__iexact=self.artist_name)

        if self.title:
            qs = qs.filter(title__iunaccent__iexact=self.title)

        if self.start:
            qs = qs.filter(timestamp__gte=self.start)

        if self.end:
            qs = qs.filter(timestamp__lt=self.end + relativedelta(days=1))

        return qs
