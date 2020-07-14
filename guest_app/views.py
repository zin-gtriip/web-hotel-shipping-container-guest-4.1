from django.shortcuts           import render, redirect
from django.views.generic       import RedirectView, FormView
from django.utils               import translation
from .forms.check_in            import *
from .mixins                    import *

class IndexView(RedirectView):
    pattern_name = 'guest_app:check-in-login'


class CheckInDataView(RequestInitializedMixin, RedirectView):
    pattern_name = 'guest_app:check-in-login'

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
    template_name           = 'desktop/check_in/login.html'
    form_class              = CheckInLoginForm
    success_url             = '/check_in/reservation'
    mobile_template_name    = 'mobile/check_in/login.html'

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
        data = form.gateway_post()
        if form.errors:
            return self.form_invalid(form)
        form.save_data(data)
        return super().form_valid(form)


class CheckInReservationView(RequestInitializedMixin, SessionDataRequiredMixin, FormView):
    template_name           = 'desktop/check_in/reservation.html'
    form_class              = CheckInReservationForm
    success_url             = '/check_in/passport'

    def form_valid(self, form):
        form.save_data()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'reservations': self.request.session['check_in_details']['booking_details'].get('reservations', [])})
        return context


class CheckInPassportView(RequestInitializedMixin, SessionDataRequiredMixin, MobileTemplateMixin, FormView):
    template_name           = 'desktop/check_in/passport.html'
    form_class              = CheckInPassportForm
    success_url             = '/check_in/detail'
    mobile_template_name    = 'mobile/check_in/passport.html'

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
        form.gateway_ocr()
        if form.errors:
            return self.form_invalid(form)
        form.save_data()
        return super().form_valid(form)


class CheckInDetailView(RequestInitializedMixin, SessionDataRequiredMixin, MobileTemplateMixin, FormView):
    template_name           = 'desktop/check_in/detail.html'
    form_class              = CheckInDetailForm
    # success_url             = '/check_in/detail'
    mobile_template_name    = 'mobile/check_in/detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # translation for bootstrap datepicker
        data['bootstrap_datepicker_language'] = translation.get_language()
        if data['bootstrap_datepicker_language'] == 'zh-hans':
            data['bootstrap_datepicker_language'] = 'zh-CN'
        # max extra form
        data['max_extra_form'] = int(self.request.session['check_in_details']['booking_details'].get('adult_number', 0)) + int(self.request.session['check_in_details']['booking_details'].get('child_number', 0)) - 1
        # render extra form formset
        if self.request.POST:
            data['extra'] = CheckInDetailExtraFormSet(self.request, self.request.POST)
        else:
            data['extra'] = CheckInDetailExtraFormSet(self.request)
        return data

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
