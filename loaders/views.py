from django.views.generic import ListView, DetailView

from loaders.models import LoaderFailure
from django.contrib.auth.mixins import AccessMixin


class AdminAccessMixin(AccessMixin):
    """Allows access to admins"""

    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return self.handle_no_permission()
        return super(AdminAccessMixin, self).dispatch(request, *args, **kwargs)


class FailureListView(AdminAccessMixin, ListView):
    model = LoaderFailure
    context_object_name = 'failures'
    paginate_by = 100
    ordering = ['-timestamp']


class FailureDetailView(AdminAccessMixin, DetailView):
    model = LoaderFailure
    context_object_name = 'failure'
