from django.views.generic import DetailView, TemplateView
from loaders.models import Outage, LoaderFailure
from radioscraper.mixins import UserIsStaffMixin


class IndexView(UserIsStaffMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        active_outages = (
            Outage.objects
            .filter(end__isnull=True)
            .select_related("radio")
        )

        context = super().get_context_data(**kwargs)
        context.update({
            "active_outages": active_outages
        })
        return context


class OutageDetailView(UserIsStaffMixin, DetailView):
    template_name = "dashboard/outage_detail.html"
    model = Outage

    def get_context_data(self, **kwargs):
        failures = self.object.failures.order_by("-timestamp")[:20]
        has_more = len(failures) < self.object.failure_count

        context = super().get_context_data(**kwargs)
        context.update({
            "failures": failures,
            "has_more": has_more,
        })
        return context


class FailureDetailView(UserIsStaffMixin, DetailView):
    template_name = "dashboard/failure_detail.html"
    model = LoaderFailure
    context_object_name = "failure"
