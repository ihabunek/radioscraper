from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic import TemplateView

from radio.models import Radio, Play


class IndexView(TemplateView):
    template_name = 'radio/index.html'


class StatsView(TemplateView):
    template_name = 'radio/stats.html'
    radio = None

    def dispatch(self, *args, **kwargs):
        radio_slug = self.kwargs.get('radio_slug')
        if radio_slug:
            self.radio = get_object_or_404(Radio, slug=radio_slug)

        return super(StatsView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        qs = Play.objects.all().values('artist', 'title').annotate(count=Count('*'))

        if self.radio:
            qs = qs.filter(radio=self.radio)

        top_plays = qs.order_by('-count')[:20]
        bottom_plays = qs.order_by('count')[:20]

        context = super(StatsView, self).get_context_data(**kwargs)
        context.update({
            "radio": self.radio,
            "radios": Radio.objects.all().order_by("name"),
            "top_plays": top_plays,
            "bottom_plays": bottom_plays,
        })
        return context


class PlaysView(ListView):
    template_name = 'radio/plays.html'
    queryset = Play.objects.all().order_by("-timestamp").prefetch_related('radio')
    context_object_name = 'plays'
    paginate_by = 100

    def dispatch(self, *args, **kwargs):
        self.artist = self.request.GET.get('artist')
        self.title = self.request.GET.get('title')
        self.radio = self.request.GET.get('radio')

        return super(PlaysView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PlaysView, self).get_context_data(**kwargs)
        context.update({
            'radios': Radio.objects.all(),
            'radio': self.radio,
            'artist': self.artist,
            'title': self.title,
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

        return qs
