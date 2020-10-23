from django.shortcuts       import redirect
from django.views.generic   import *
from guest_base.mixins      import RequestFormKwargsMixin, MobileTemplateMixin
from pre_arrival            import views as PreArrivalView
from pre_arrival.mixins     import *
from .forms                 import *


class PreArrivalDetailView(PreArrivalView.PreArrivalDetailView):
    form_class = PreArrivalDetailForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # render extra form formset
        if self.request.POST:
            context['extra'] = PreArrivalDetailExtraFormSet(self.request, self.request.POST)
        else:
            context['extra'] = PreArrivalDetailExtraFormSet(self.request)
        return context
    
    def form_valid(self, form, extra):
        form.save(extra)
        if self.request.POST.get('form_type', '') == 'add_guest':
            return redirect('pre_arrival_all_passport:extra_passport')
        return super().form_valid(form, extra)


class PreArrivalAllPassportExtraPassportView(ParameterRequiredMixin, RequestFormKwargsMixin, MobileTemplateMixin, ProgressRateContextMixin, FormView):
    template_name           = 'pre_arrival_all_passport/desktop/extra_passport.html'
    mobile_template_name    = 'pre_arrival_all_passport/mobile/extra_passport.html'
    form_class              = PreArrivalAllPassportExtraPassportForm
    success_url             = '/pre_arrival/detail'
    parameter_required      = 'passport'
    progress_bar_page       = 'detail'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        guest_id = self.request.GET.get('guest_id', None)
        kwargs.update(guest_id=guest_id)
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
