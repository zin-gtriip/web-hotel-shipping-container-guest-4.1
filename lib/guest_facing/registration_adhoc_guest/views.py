from django.shortcuts                               import redirect
from django.http                                    import HttpResponseRedirect
from django.views.generic                           import *
from guest_facing.registration                      import utils
from guest_facing.registration.mixins               import *
from guest_facing.registration_ocr_required.views   import *
from .forms                                         import *


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

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('registration', {}).get('reservation', {}).get('preArrivalDone', '0') == '1':
            request.session['registration']['passport'] = True # mark `passport` is done
            return redirect('registration_adhoc_guest:guest_list')
        return super().dispatch(request, *args, **kwargs)


class RegistrationGuestListView(ParameterRequiredMixin, ProgressRateContextMixin, TemplateView):
    template_name           = 'registration/desktop/guest_list.html'
    parameter_required      = 'passport'
    progress_bar_page       = 'passport'

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('registration', {}).get('reservation', {}).get('preArrivalDone', '0') != '1':
            return redirect('registration:passport')
        prefilled = []
        for guest in list(request.session['registration']['reservation'].get('guestsList', [])):
            if guest.get('passportImage', ''): # use `passportImage` to determine if guest is newly added
                request.session['registration']['reservation']['guestsList'].remove(guest) # reset `guestsList` with no new guest
            else:
                prefilled.append(guest) # store additional guests to `session.registration.detail` that will be used on `registration_ocr_required.forms`
        request.session['registration']['detail'] = {'prefilled_guest_temp': prefilled}
        return super().dispatch(request, *args, **kwargs)


class RegistrationDetailView(RegistrationDetailView):

    def dispatch(self, request, *args, **kwargs):
        # redirect to `guest_list` if `session` has no new added guest
        guests = [guest for guest in request.session['registration']['reservation'].get('guestsList', []) if guest.get('passportImage', '')] # use `passportImage` to determine if guest is newly added
        if request.session['registration']['reservation'].get('preArrivalDone', '0') == '1' and not guests:
            return redirect('registration_adhoc_guest:guest_list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # render extra form formset
        if self.request.POST:
            context['extra'] = RegistrationDetailExtraFormSet(self.request, self.request.POST)
        else:
            context['extra'] = RegistrationDetailExtraFormSet(self.request)
        return context


class RegistrationExtraPassportView(RegistrationExtraPassportView):
    form_class = RegistrationExtraPassportForm


class RegistrationOtherInfoView(RegistrationOtherInfoView):
    form_class = RegistrationOtherInfoForm

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('registration', {}).get('reservation', {}).get('preArrivalDone', '0') == '1':
            data = {}
            data['arrival_time'] = utils.parse_arrival_time(self.request.session['registration']['reservation'].get('eta', ''))
            data['special_requests'] = request.session.get('registration', {}).get('reservation', {}).get('comments', '')
            main_guest = next((guest for guest in self.request.session['registration']['reservation'].get('guestsList', []) if guest.get('isMainGuest', '0') == '1'), {})
            data['email'] = main_guest.get('email', '')
            data['is_subscribe'] = main_guest.get('emailSubscription', True)
            form = self.get_form_class()
            form = form(request, data)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return super().dispatch(request, *args, **kwargs)


class RegistrationCompleteView(RegistrationCompleteView):
    pass
