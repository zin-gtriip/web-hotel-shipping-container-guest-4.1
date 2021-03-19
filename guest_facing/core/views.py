from django.conf            import settings
from django.shortcuts       import render
from django.urls            import reverse
from django.views.generic   import *
from .forms                 import *
from .mixins                import *

class IndexView(RedirectView):
    pattern_name = 'admin:index'

    def dispatch(self, request, *args, **kwargs):
        self.request.session.pop('property_id', None)
        return super().dispatch(request, *args, **kwargs)


class CorePropertyView(RequestFormKwargsMixin, FormView):
    template_name   = 'core/desktop/property.html'
    form_class      = GuestBasePropertyForm

    def dispatch(self, request, *args, **kwargs):
        properties = settings.GUEST_ENDPOINT
        if len(properties) == 1: # auto submit
            prop = next(iter(properties), None)
            data = {}
            data['property_id'] = prop.get('id', None)
            form = self.get_form_class()
            form = form(request, data)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = settings.GUEST_ENDPOINT
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        self.success_url = reverse('core:index')
        next_url = self.request.GET.get('next', None)
        if next_url:
            self.success_url = next_url
        return super().get_success_url()
