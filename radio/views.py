from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic import TemplateView
from datetime import datetime, date
from radio.models import Radio, Play
from dateutil.relativedelta import relativedelta


class IndexView(TemplateView):
    template_name = 'radio/index.html'


class StatsView(TemplateView):
    template_name = 'radio/stats.html'
    radio = None

    def get_month_year(self):
        today = date.today()
        default = [today.year, today.month]

        try:
            year = int(self.request.GET.get('year'))
            month = int(self.request.GET.get('month'))
        except:
            return default

        if year < 2000 or year > today.year or month < 1 or month > 12:
            return default

        return [year, month]

    def dispatch(self, *args, **kwargs):
        radio_slug = self.kwargs.get('radio_slug')
        if radio_slug:
            self.radio = get_object_or_404(Radio, slug=radio_slug)

        self.year, self.month = self.get_month_year()
        self.start = date(self.year, self.month, 1)
        self.end = self.start + relativedelta(months=1)

        return super(StatsView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        qs = Play.objects.all().values('artist', 'title').annotate(count=Count('*'))

        if self.radio:
            qs = qs.filter(radio=self.radio)

        # Limit to one month
        qs = qs.filter(timestamp__date__gte=self.start)
        qs = qs.filter(timestamp__date__lt=self.end)

        top_plays = qs.order_by('-count')[:20]
        bottom_plays = qs.order_by('count')[:20]

        context = super(StatsView, self).get_context_data(**kwargs)
        context.update({
            "radio": self.radio,
            "radios": Radio.objects.all().order_by("name"),
            "top_plays": top_plays,
            "bottom_plays": bottom_plays,
            "month": self.month,
            "year": self.year,
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
            'radios': Radio.objects.all(),
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
