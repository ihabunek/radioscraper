from django.db.models import Count
from django.views.generic import TemplateView
from radio.models import Radio, Play


class IndexView(TemplateView):
    template_name = 'radio/index.html'

    def get_context_data(self, **kwargs):
        top_plays = Play.objects.all().values('artist', 'title') \
            .annotate(count=Count('*')).order_by('-count')[:20]

        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            "radios": Radio.objects.all(),
            "top_plays": top_plays,
        })
        return context
