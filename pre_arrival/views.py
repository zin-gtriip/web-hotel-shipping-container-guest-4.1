from django                     import forms
from django.shortcuts           import render
from django.views.generic       import *
from django.utils               import translation
from django.utils.translation   import gettext, gettext_lazy as _
from guest_base                 import views as GuestBaseViews
from .forms                     import *
from .mixins                    import *
from .utilities                 import *

class IndexView(GuestBaseViews.IndexView):
    pattern_name = 'pre_arrival:check-in-login'


class CheckInDataView(RequestInitializedMixin, RedirectView):
    pattern_name = 'pre_arrival:check-in-login'

    def get_redirect_url(self, *args, **kwargs):
        self.request.session['check_in_data'] = {}
        if 'lang' in self.request.GET: self.request.session[translation.LANGUAGE_SESSION_KEY] = self.request.GET.get('lang', 'en-gb')
        if 'app' in self.request.GET: self.request.session['check_in_data']['app'] = self.request.GET.get('app', False)
        if 'auto_login' in self.request.GET: self.request.session['check_in_data']['auto_login'] = self.request.GET.get('auto_login', False)
        if 'skip_ocr' in self.request.GET: self.request.session['check_in_data']['skip_ocr'] = self.request.GET.get('skip_ocr', False)
        if 'reservation_no' in self.request.GET: self.request.session['check_in_data']['reservation_no'] = self.request.GET.get('reservation_no', False)
        if 'arrival_date' in self.request.GET: self.request.session['check_in_data']['arrival_date'] = self.request.GET.get('arrival_date', False)
        if 'last_name' in self.request.GET: self.request.session['check_in_data']['last_name'] = self.request.GET.get('last_name', False)
        if 'first_name' in self.request.GET: self.request.session['check_in_data']['first_name'] = self.request.GET.get('first_name', False)
        if 'nationality' in self.request.GET: self.request.session['check_in_data']['nationality'] = self.request.GET.get('nationality', False)
        if 'passport_no' in self.request.GET: self.request.session['check_in_data']['passport_no'] = self.request.GET.get('passport_no', False)
        if 'birth_date' in self.request.GET: self.request.session['check_in_data']['birth_date'] = self.request.GET.get('birth_date', False)
        return super().get_redirect_url(*args, **kwargs)


class CheckInLoginView(RequestInitializedMixin, MobileTemplateMixin, FormView):
    template_name           = 'pre_arrival/desktop/login.html'
    form_class              = CheckInLoginForm
    success_url             = '/check_in/reservation'
    mobile_template_name    = 'pre_arrival/mobile/login.html'

    def dispatch(self, request, *args, **kwargs):
        if 'check_in_data' in request.session and request.session['check_in_data'].get('auto_login', False):
            data = {
                'reservation_no': request.session['check_in_data'].get('reservation_no', ''),
                'arrival_date': request.session['check_in_data'].get('arrival_date', ''),
                'last_name': request.session['check_in_data'].get('last_name', ''),
            }
            form = self.get_form_class()
            form = form(request, data)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save_data()
        return super().form_valid(form)


class CheckInReservationView(RequestInitializedMixin, SessionDataRequiredMixin, FormView):
    template_name           = 'pre_arrival/desktop/reservation.html'
    form_class              = CheckInReservationForm
    success_url             = '/check_in/passport'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = []
        for reservation in self.request.session['check_in_details'].get('booking_details', []):
            reservation['formattedArrivalDate'] = format_display_date(reservation.get('arrivalDate', ''))
            reservation['formattedDepartureDate'] = format_display_date(reservation.get('departureDate', ''))
            context['reservations'].append(reservation)
        return context

    def form_valid(self, form):
        form.save_data()
        return super().form_valid(form)


class CheckInPassportView(RequestInitializedMixin, SessionDataRequiredMixin, MobileTemplateMixin, FormView):
    template_name           = 'pre_arrival/desktop/passport.html'
    form_class              = CheckInPassportForm
    success_url             = '/check_in/detail'
    mobile_template_name    = 'pre_arrival/mobile/passport.html'

    def dispatch(self, request, *args, **kwargs):
        if 'check_in_data' in request.session and request.session['check_in_data'].get('skip_ocr', False):
            data = {
                'skip_passport': True
            }
            form = self.get_form_class()
            form = form(request, data)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save_data()
        return super().form_valid(form)


class CheckInDetailView(RequestInitializedMixin, SessionDataRequiredMixin, MobileTemplateMixin, FormView):
    template_name           = 'pre_arrival/desktop/detail.html'
    form_class              = CheckInDetailForm
    success_url             = '/check_in/other_info'
    mobile_template_name    = 'pre_arrival/mobile/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # translation for bootstrap datepicker
        context['bootstrap_datepicker_language'] = translation.get_language()
        if context['bootstrap_datepicker_language'] == 'zh-hans':
            context['bootstrap_datepicker_language'] = 'zh-CN'
        # max extra form
        context['max_extra_form'] = int(self.request.session['check_in_details']['form'].get('adults', 1)) + int(self.request.session['check_in_details']['form'].get('children', 0)) - 1
        # render extra form formset
        additional_guests = [guest for guest in self.request.session['check_in_details']['form'].get('guestsList', []) if guest.get('isMainGuest', 0) == 0]
        CheckInDetailExtraFormSet = forms.formset_factory(CheckInDetailExtraForm, formset=CheckInDetailExtraBaseFormSet, extra=len(additional_guests)) # extra based on `additional_guests` length
        if self.request.POST:
            context['extra'] = CheckInDetailExtraFormSet(self.request, self.request.POST)
        else:
            context['extra'] = CheckInDetailExtraFormSet(self.request)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        extra = self.get_context_data().get('extra')
        if form.is_valid() and extra.is_valid():
            return self.form_valid(form, extra)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, extra):
        form.save_data(extra)
        return super().form_valid(form)


class CheckInOtherInfoView(RequestInitializedMixin, SessionDataRequiredMixin, FormView):
    template_name           = 'pre_arrival/desktop/other_info.html'
    form_class              = CheckInOtherInfoForm
    success_url             = '/check_in/complete'
    
    def form_valid(self, form):
        form.save_data()
        form.gateway_post()
        if form.errors:
            return self.form_invalid(form)
        return super().form_valid(form)


class CheckInCompleteView(RequestInitializedMixin, SessionDataRequiredMixin, TemplateView):
    template_name           = 'pre_arrival/desktop/complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation = self.request.session['check_in_details']['form']
        reservation['formattedArrivalDate'] = format_display_date(reservation.get('arrivalDate', ''))
        reservation['formattedDepartureDate'] = format_display_date(reservation.get('departureDate', ''))
        reservation['mainGuestLastName'] = next(guest.get('lastName', '') for guest in reservation.get('guestsList', []) if guest.get('isMainGuest', 0) == 1)
        context['reservation'] = reservation
        return context
