from django.conf                import settings
from django.shortcuts           import render
from django.utils               import translation
from django.utils.translation   import gettext, gettext_lazy as _
from django.views.generic       import *
from guest_facing.core.views    import IndexView
from guest_facing.core.mixins   import PropertyRequiredMixin, RequestFormKwargsMixin, MobileTemplateMixin, JSONResponseMixin
from .forms                     import *
from .mixins                    import *
from .utils                     import *

class IndexView(IndexView):
    pattern_name = 'registration:data'


class RegistrationDataView(RedirectView):
    pattern_name = 'registration:login'

    def get_redirect_url(self, *args, **kwargs):
        self.request.session['property_id'] = self.request.GET.get('property', None)
        self.request.session['app'] = self.request.GET.get('app', 0)
        self.request.session['registration'] = {'preload': {}}
        if 'lang' in self.request.GET: self.request.session[translation.LANGUAGE_SESSION_KEY] = self.request.GET.get('lang', 'en')
        if 'auto_login' in self.request.GET: self.request.session['registration']['preload']['auto_login'] = self.request.GET.get('auto_login', 0)
        if 'reservation_no' in self.request.GET: self.request.session['registration']['preload']['reservation_no'] = self.request.GET.get('reservation_no', '')
        if 'arrival_date' in self.request.GET: self.request.session['registration']['preload']['arrival_date'] = self.request.GET.get('arrival_date', '')
        if 'last_name' in self.request.GET: self.request.session['registration']['preload']['last_name'] = self.request.GET.get('last_name', '')
        if 'first_name' in self.request.GET: self.request.session['registration']['preload']['first_name'] = self.request.GET.get('first_name', '')
        if 'nationality' in self.request.GET: self.request.session['registration']['preload']['nationality'] = self.request.GET.get('nationality', '')
        if 'passport_no' in self.request.GET: self.request.session['registration']['preload']['passport_no'] = self.request.GET.get('passport_no', '')
        if 'birth_date' in self.request.GET: self.request.session['registration']['preload']['birth_date'] = self.request.GET.get('birth_date', '')
        return super().get_redirect_url(*args, **kwargs)


class RegistrationLoginView(PropertyRequiredMixin, RequestFormKwargsMixin, MobileTemplateMixin, ProgressRateContextMixin, FormView):
    template_name           = 'registration/desktop/login.html'
    mobile_template_name    = 'registration/mobile/login.html'
    form_class              = RegistrationLoginForm
    success_url             = '/registration/reservation'
    progress_bar_page       = 'login'

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('registration', {}).get('preload', {}).get('auto_login', 0):
            request.session['registration']['preload']['auto_login'] = 0 # set auto login to False to prevent using `preload` data again
            data = {}
            data['reservation_no'] = request.session.get('registration', {}).get('preload', {}).get('reservation_no', '')
            data['arrival_date'] = request.session.get('registration', {}).get('preload', {}).get('arrival_date', '')
            data['last_name'] = request.session.get('registration', {}).get('preload', {}).get('last_name', '')
            form = self.get_form_class()
            form = form(request, data)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get('form', None)
        if self.request.session.get('app', 0) and self.request.session.get('registration', {}).get('preload', {}).get('reservation_no', '') and (form and not form.is_bound):
            context['skip_reservation_no'] = True
        return context


class RegistrationTimerExtensionView(PropertyRequiredMixin, JSONResponseMixin, RequestFormKwargsMixin, FormView):
    form_class              = RegistrationTimerExtensionForm

    def form_valid(self, form):
        form.save()
        self.json_data['registration_extended_expiry_date'] = self.request.session['registration'].get('extended_expiry_date', '')
        self.json_data['registration_extended_expiry_duration'] = self.request.session['registration'].pop('extended_expiry_duration', '')
        self.json_status = 'success'
        return self.render_to_json_response(self.get_context_data())

    def form_invalid(self, form):
        self.json_errors = form.errors
        self.json_status = 'error'
        return self.render_to_json_response(self.get_context_data())


class RegistrationReservationView(ExpirySessionMixin, PropertyRequiredMixin, RequestFormKwargsMixin, ProgressRateContextMixin, FormView):
    template_name           = 'registration/desktop/reservation.html'
    form_class              = RegistrationReservationForm
    success_url             = '/registration/passport'
    progress_bar_page       = 'reservation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = []
        for reservation in self.request.session['registration'].get('bookings', []):
            reservation = dict(reservation) # create new variable to prevent modification on `request.session`
            reservation['formattedArrivalDate'] = format_display_date(reservation.get('arrivalDate', ''))
            reservation['formattedDepartureDate'] = format_display_date(reservation.get('departureDate', ''))
            room = next((temp for temp in settings.REGISTRATION_ROOM_TYPES if temp['room_type'] == reservation['roomType']), {})
            reservation['roomName'] = room.get('room_name', '')
            reservation['roomImage'] = room.get('room_image', '')
            context['reservations'].append(reservation)
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class RegistrationPassportView(ParameterRequiredMixin, PropertyRequiredMixin, RequestFormKwargsMixin, MobileTemplateMixin, ProgressRateContextMixin, FormView):
    template_name           = 'registration/desktop/passport.html'
    mobile_template_name    = 'registration/mobile/passport.html'
    form_class              = RegistrationPassportForm
    success_url             = '/registration/detail'
    parameter_required      = 'reservation'
    progress_bar_page       = 'passport'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class RegistrationDetailView(ParameterRequiredMixin, PropertyRequiredMixin, RequestFormKwargsMixin, MobileTemplateMixin, ProgressRateContextMixin, FormView):
    template_name           = 'registration/desktop/detail.html'
    mobile_template_name    = 'registration/mobile/detail.html'
    form_class              = RegistrationDetailForm
    success_url             = '/registration/other_info'
    parameter_required      = 'passport'
    progress_bar_page       = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # translation for bootstrap datepicker
        context['bootstrap_datepicker_language'] = translation.get_language()
        if context['bootstrap_datepicker_language'] == 'zh-hans':
            context['bootstrap_datepicker_language'] = 'zh-CN'
        # max extra form
        context['max_extra_form'] = int(self.request.session['registration']['reservation'].get('adults', 1)) + int(self.request.session['registration']['reservation'].get('children', 0)) - 1
        # render extra form formset
        if self.request.POST:
            context['extra'] = RegistrationDetailExtraFormSet(self.request, self.request.POST)
        else:
            context['extra'] = RegistrationDetailExtraFormSet(self.request)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        extra = self.get_context_data().get('extra')
        if form.is_valid() and extra.is_valid():
            return self.form_valid(form, extra)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, extra):
        form.save(extra)
        return super().form_valid(form)


class RegistrationOtherInfoView(ParameterRequiredMixin, PropertyRequiredMixin, RequestFormKwargsMixin, ProgressRateContextMixin, FormView):
    template_name           = 'registration/desktop/other_info.html'
    form_class              = RegistrationOtherInfoForm
    success_url             = '/registration/complete'
    parameter_required      = 'detail'
    progress_bar_page       = 'other_info'
    
    def form_valid(self, form):
        form.save()
        form.gateway_post()
        if form.errors:
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tnc_link'] = settings.TNC_LINK
        context['privacy_link'] = settings.PRIVACY_LINK
        return context


class RegistrationCompleteView(ParameterRequiredMixin, PropertyRequiredMixin, RequestFormKwargsMixin, ProgressRateContextMixin, FormView):
    template_name           = 'registration/desktop/complete.html'
    form_class              = RegistrationCompleteForm
    success_url             = '/registration/reservation'
    parameter_required      = 'other_info'
    progress_bar_page       = 'complete'
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation = dict(self.request.session['registration']['reservation']) # create new variable to prevent modification on `request.session`
        reservation['formattedArrivalDate'] = format_display_date(reservation.get('arrivalDate', ''))
        reservation['formattedDepartureDate'] = format_display_date(reservation.get('departureDate', ''))
        reservation['mainGuestLastName'] = next(guest.get('lastName', '') for guest in reservation.get('guestsList', []) if guest.get('isMainGuest', '0') == '1')
        room = next((temp for temp in settings.REGISTRATION_ROOM_TYPES if temp['room_type'] == reservation['roomType']), {})
        reservation['roomName'] = room.get('room_name', '')
        reservation['roomImage'] = room.get('room_image', '')
        context['reservation'] = reservation
        context['ios_url'] = settings.APP_IOS_URL
        context['android_url'] = settings.APP_ANDROID_URL
        context['direct_url'] = settings.APP_DIRECT_URL
        return context
