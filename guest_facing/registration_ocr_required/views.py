from django.shortcuts                   import redirect
from django.views.generic               import *
from guest_facing.core.mixins           import RequestFormKwargsMixin, MobileTemplateMixin
from guest_facing.registration.mixins   import *
from guest_facing.registration.views    import *
from .forms                             import *


class IndexView(IndexView):
    pass


class RegistrationDataView(RegistrationDataView):
    pass


class RegistrationLoginView(RegistrationLoginView):
    pass


class RegistrationTimerExtensionView(RegistrationTimerExtensionView):
    pass


class RegistrationReservationView(RegistrationReservationView):
    pass


class RegistrationPassportView(RegistrationPassportView):
    pass


class RegistrationDetailView(RegistrationDetailView):
    form_class = RegistrationDetailForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # render extra form formset
        if self.request.POST:
            context['extra'] = RegistrationDetailExtraFormSet(self.request, self.request.POST)
        else:
            context['extra'] = RegistrationDetailExtraFormSet(self.request)
        return context
    
    def form_valid(self, form, extra):
        form.save(extra)
        if self.request.POST.get('form_type', '') == 'add_guest':
            return redirect('registration_ocr_required:extra_passport')
        return super().form_valid(form, extra)


class RegistrationExtraPassportView(ParameterRequiredMixin, RequestFormKwargsMixin, MobileTemplateMixin, ProgressRateContextMixin, FormView):
    template_name           = 'registration/desktop/extra_passport.html'
    mobile_template_name    = 'registration/mobile/extra_passport.html'
    form_class              = RegistrationExtraPassportForm
    success_url             = '/registration/detail'
    parameter_required      = 'passport'
    progress_bar_page       = 'detail'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class RegistrationOtherInfoView(RegistrationOtherInfoView):
    pass


class RegistrationCompleteView(RegistrationCompleteView):
    pass
