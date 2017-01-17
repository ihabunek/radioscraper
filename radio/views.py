from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView

from radio.models import Radio, Play
from radio.utils.stats import get_repeated_plays


class IndexView(TemplateView):
    template_name = 'radio/index.html'


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


class RadioStatsView(TemplateView):
    template_name = 'radio/radio_stats.html'

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('radio_slug')
        radio = get_object_or_404(Radio, slug=slug)

        year, month = get_year_month(self.request)
        start = date(year, month, 1)
        end = start + relativedelta(months=1)

        context = super().get_context_data(**kwargs)
        context.update({
            "repeated": get_repeated_plays(start, end, radio.id),
            "play_count": radio.plays(start, end).count(),
            "radio": radio,
            "month": month,
            "year": year,
            "most_played_songs": radio.most_played_songs(start, end)[:30],
            "most_played_artists": radio.most_played_artists(start, end)[:30],
            "most_played_daily": radio.most_played_daily(start, end).first()
        })
        return context


class StatsView(TemplateView):
    template_name = 'radio/stats.html'

    def get_context_data(self, **kwargs):
        year, month = get_year_month(self.request)
        start = date(year, month, 1)
        end = start + relativedelta(months=1)

        top_plays = (Play.objects.all()
            .values('artist', 'title')
            .annotate(count=Count('*'))
            .filter(timestamp__date__gte=start)
            .filter(timestamp__date__lt=end)
            .order_by('-count'))[:20]

        context = super().get_context_data(**kwargs)
        context.update({
            "repeated": get_repeated_plays(start, end),
            "top_plays": top_plays,
            "month": month,
            "year": year,
        })
        return context


class PlaysView(ListView):
    template_name = 'radio/plays.html'
    queryset = Play.objects.all().order_by("-timestamp").prefetch_related('radio')
    context_object_name = 'plays'
    paginate_by = 100

    def _parse_date(self, value):
        try:
            return datetime.strptime(value, "%d.%m.%Y")
        except:
            return None

    def dispatch(self, *args, **kwargs):
        self.artist = self.request.GET.get('artist')
        self.title = self.request.GET.get('title')
        self.radio = self.request.GET.get('radio')
        self.start = self._parse_date(self.request.GET.get('start'))
        self.end = self._parse_date(self.request.GET.get('end'))

        return super(PlaysView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PlaysView, self).get_context_data(**kwargs)
        context.update({
            'radio': self.radio,
            'artist': self.artist,
            'title': self.title,
            'start': self.start,
            'end': self.end,
        })
        return context

    def get_queryset(self):
        qs = super(PlaysView, self).get_queryset()

        if self.radio:
            qs = qs.filter(radio__slug=self.radio)

        if self.artist:
            qs = qs.filter(artist__unaccent__iexact=self.artist)

        if self.title:
            qs = qs.filter(title__unaccent__iexact=self.title)

        if self.start:
            qs = qs.filter(timestamp__date__gte=self.start)

        if self.end:
            qs = qs.filter(timestamp__date__lte=self.end)

        return qs
