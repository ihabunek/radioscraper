from django.views.generic import TemplateView

from radio.models import Radio


class IndexView(TemplateView):
    template_name = 'ui/index.html'

    def get_context_data(self, **kwargs):
        radios = (Radio.objects.active()
            .order_by('name')
            .prefetch_related('first_play', 'last_play'))

        context = super().get_context_data(**kwargs)
        context.update({
            "radios": radios
        })
        return context
