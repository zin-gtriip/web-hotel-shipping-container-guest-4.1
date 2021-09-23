from django.conf                            import settings
from django.contrib                         import messages
from django.shortcuts                       import render, redirect
from django.urls                            import reverse
from django.utils                           import translation
from django.utils.translation               import gettext, gettext_lazy as _
from django.views.generic                   import *
from guest_facing.registration.views        import RegistrationLoginView, RegistrationReservationView, RegistrationGuestListView, RegistrationDetailView, RegistrationGuestListView, RegistrationOtherInfoView, RegistrationCompleteView
from guest_facing.chat.views                import *
from .forms                                 import *
from guest_facing.core.mixins               import RequestFormKwargsMixin, PropertyRequiredMixin, MobileTemplateMixin
from guest_facing.registration.mixins       import *

class RegistrationLoginView(RegistrationLoginView):
    form_class           = RegistrationLoginForm

class RegistrationReservationView(RegistrationReservationView):
    template_name           = 'registration/desktop/reservation.html'
    form_class              = RegistrationReservationForm

class RegistrationGuestListView(RegistrationGuestListView):
    form_class              = RegistrationGuestListForm
    success_url             = '/guest/registration/main_guest'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        max_guest = int(self.request.session['registration']['reservation'].get('adults', 1)) + int(self.request.session['registration']['reservation'].get('children', 0))
        context['add_guest'] = max_guest > len(self.request.session['registration']['reservation'].get('guestsList', []))
        if len(self.request.session['registration']['reservation'].get('guestsList', [])) == 0:
            context['can_submit'] = False
        else:
            context['can_submit'] = all([guest.get('is_done', False) or guest.get('hasLocalRecord', False) for guest in self.request.session['registration']['reservation'].get('guestsList', [])])
        return context

class RegistrationDetailView(RegistrationDetailView):
    form_class              = RegistrationDetailForm

class RegistrationMainGuestView(ParameterRequiredMixin, PropertyRequiredMixin, RequestFormKwargsMixin, ProgressRateContextMixin, FormView):
    template_name           = 'registration/desktop/main_guest.html'
    form_class              = RegistrationMainGuestForm
    success_url             = '/guest/registration/other_info'
    parameter_required      = 'guest_list'
    progress_bar_page       = 'guest_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        config = gateways.amp_endpoint('get', '/configVariables', self.request.session.get('property_id', '')) or {} # get config variables
        context['age_limit'] = config.get('data', {}).get('prearrivalAdultMinAgeYears', settings.REGISTRATION_ADULT_AGE_LIMIT)
        return context

    def form_valid(self, form):
        form.save()
        if form.errors:
            return self.form_invalid(form)
        return super().form_valid(form)
