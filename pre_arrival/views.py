from django.shortcuts           import render
from django.views.generic       import *
from django.utils               import translation
from django.utils.translation   import gettext, gettext_lazy as _
from guest_base                 import views as GuestBaseViews
from guest_base.mixins          import RequestFormKwargsMixin, MobileTemplateMixin, JSONResponseMixin
from .forms                     import *
from .mixins                    import *
from .utilities                 import *


class IndexView(GuestBaseViews.IndexView):
    pattern_name = 'pre_arrival:data'


class PreArrivalDataView(RedirectView):
    pattern_name = 'pre_arrival:login'

    def get_redirect_url(self, *args, **kwargs):
        self.request.session['pre_arrival'] = {'preload': {}}
        self.request.session['app'] = self.request.GET.get('app', 0)
        if 'lang' in self.request.GET: self.request.session[translation.LANGUAGE_SESSION_KEY] = self.request.GET.get('lang', 'en')
        if 'auto_login' in self.request.GET: self.request.session['pre_arrival']['preload']['auto_login'] = self.request.GET.get('auto_login', 0)
        if 'skip_ocr' in self.request.GET: self.request.session['pre_arrival']['preload']['skip_ocr'] = self.request.GET.get('skip_ocr', 0)
        if 'reservation_no' in self.request.GET: self.request.session['pre_arrival']['preload']['reservation_no'] = self.request.GET.get('reservation_no', '')
        if 'arrival_date' in self.request.GET: self.request.session['pre_arrival']['preload']['arrival_date'] = self.request.GET.get('arrival_date', '')
        if 'last_name' in self.request.GET: self.request.session['pre_arrival']['preload']['last_name'] = self.request.GET.get('last_name', '')
        if 'first_name' in self.request.GET: self.request.session['pre_arrival']['preload']['first_name'] = self.request.GET.get('first_name', '')
        if 'nationality' in self.request.GET: self.request.session['pre_arrival']['preload']['nationality'] = self.request.GET.get('nationality', '')
        if 'passport_no' in self.request.GET: self.request.session['pre_arrival']['preload']['passport_no'] = self.request.GET.get('passport_no', '')
        if 'birth_date' in self.request.GET: self.request.session['pre_arrival']['preload']['birth_date'] = self.request.GET.get('birth_date', '')
        return super().get_redirect_url(*args, **kwargs)


class PreArrivalLoginView(RequestFormKwargsMixin, MobileTemplateMixin, ProgressRateContextMixin, FormView):
    template_name           = 'pre_arrival/desktop/login.html'
    mobile_template_name    = 'pre_arrival/mobile/login.html'
    form_class              = PreArrivalLoginForm
    success_url             = '/pre_arrival/reservation'

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('pre_arrival', {}).get('preload', {}).get('auto_login', 0):
            data['reservation_no'] = request.session.get('pre_arrival', {}).get('preload', {}).get('reservation_no', '')
            data['arrival_date'] = request.session.get('pre_arrival', {}).get('preload', {}).get('arrival_date', '')
            data['last_name'] = request.session.get('pre_arrival', {}).get('preload', {}).get('last_name', '')
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


class PreArrivalTimerExtensionView(JSONResponseMixin, RequestFormKwargsMixin, FormView):
    form_class              = PreArrivalTimerExtensionForm

    def form_valid(self, form):
        form.save()
        self.json_data = {'pre_arrival_extended_expiry_date': self.request.session['pre_arrival'].get('extended_expiry_date', '')}
        self.json_status = 'success'
        return self.render_to_json_response(self.get_context_data())

    def form_invalid(self, form):
        self.json_errors = form.errors
        self.json_status = 'error'
        return self.render_to_json_response(self.get_context_data())


class PreArrivalReservationView(ExpirySessionMixin, RequestFormKwargsMixin, ProgressRateContextMixin, FormView):
    template_name           = 'pre_arrival/desktop/reservation.html'
    form_class              = PreArrivalReservationForm
    success_url             = '/pre_arrival/passport'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = []
        for reservation in self.request.session['pre_arrival'].get('bookings', []):
            reservation['formattedArrivalDate'] = format_display_date(reservation.get('arrivalDate', ''))
            reservation['formattedDepartureDate'] = format_display_date(reservation.get('departureDate', ''))
            room = next((temp for temp in settings.ROOM_TYPES if temp['room_type'] == reservation['roomType']), {})
            reservation['roomName'] = room.get('room_name', '')
            reservation['roomImage'] = room.get('room_image', '')
            context['reservations'].append(reservation)
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PreArrivalPassportView(PageParameterRequiredMixin, RequestFormKwargsMixin, MobileTemplateMixin, ProgressRateContextMixin, FormView):
    template_name           = 'pre_arrival/desktop/passport.html'
    mobile_template_name    = 'pre_arrival/mobile/passport.html'
    form_class              = PreArrivalPassportForm
    success_url             = '/pre_arrival/detail'
    page_parameter          = 'reservation'

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('pre_arrival', {}).get('preload', {}).get('skip_ocr', False):
            data['skip_passport'] = True
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


class PreArrivalDetailView(PageParameterRequiredMixin, RequestFormKwargsMixin, MobileTemplateMixin, ProgressRateContextMixin, FormView):
    template_name           = 'pre_arrival/desktop/detail.html'
    mobile_template_name    = 'pre_arrival/mobile/detail.html'
    form_class              = PreArrivalDetailForm
    success_url             = '/pre_arrival/other_info'
    page_parameter          = 'passport'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # translation for bootstrap datepicker
        context['bootstrap_datepicker_language'] = translation.get_language()
        if context['bootstrap_datepicker_language'] == 'zh-hans':
            context['bootstrap_datepicker_language'] = 'zh-CN'
        # max extra form
        context['max_extra_form'] = int(self.request.session['pre_arrival']['reservation'].get('adults', 1)) + int(self.request.session['pre_arrival']['reservation'].get('children', 0)) - 1
        # render extra form formset
        if self.request.POST:
            context['extra'] = PreArrivalDetailExtraFormSet(self.request, self.request.POST)
        else:
            context['extra'] = PreArrivalDetailExtraFormSet(self.request)
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


class PreArrivalOtherInfoView(PageParameterRequiredMixin, RequestFormKwargsMixin, ProgressRateContextMixin, FormView):
    template_name           = 'pre_arrival/desktop/other_info.html'
    form_class              = PreArrivalOtherInfoForm
    success_url             = '/pre_arrival/complete'
    page_parameter          = 'detail'
    
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


class PreArrivalCompleteView(PageParameterRequiredMixin, RequestFormKwargsMixin, ProgressRateContextMixin, FormView):
    template_name           = 'pre_arrival/desktop/complete.html'
    form_class              = PreArrivalCompleteForm
    success_url             = '/pre_arrival/reservation'
    page_parameter          = 'other_info'
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation = self.request.session['pre_arrival']['reservation']
        reservation['formattedArrivalDate'] = format_display_date(reservation.get('arrivalDate', ''))
        reservation['formattedDepartureDate'] = format_display_date(reservation.get('departureDate', ''))
        reservation['mainGuestLastName'] = next(guest.get('lastName', '') for guest in reservation.get('guestsList', []) if guest.get('isMainGuest', '0') == '1')
        room = next(temp for temp in settings.ROOM_TYPES if temp['room_type'] == reservation['roomType'])
        reservation['roomName'] = room['room_name']
        reservation['roomImage'] = room['room_image']
        context['reservation'] = reservation
        return context
