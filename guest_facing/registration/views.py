from django.conf                import settings
from django.http                import Http404
from django.shortcuts           import render, reverse, redirect
from django.utils               import translation
from django.utils.translation   import gettext, gettext_lazy as _
from django.views.generic       import *
from guest_facing.core.utils    import encrypt, decrypt
from guest_facing.core.views    import IndexView
from guest_facing.core.mixins   import PropertyRequiredMixin, RequestFormKwargsMixin, MobileTemplateMixin, JSONResponseMixin
from .                          import utils
from .forms                     import (RegistrationLoginForm, RegistrationTimerExtensionForm, RegistrationReservationForm, RegistrationGuestListForm,
                                RegistrationDetailForm, RegistrationPassportForm, RegistrationOtherInfoForm, RegistrationCompleteForm)
from .mixins                    import ParameterRequiredMixin, ExpirySessionMixin, ProgressRateContextMixin


class IndexView(IndexView):
    pattern_name = 'registration:data'


class RegistrationDataView(RedirectView):
    pattern_name = 'registration:login'

    def get(self, request, *args, **kwargs):
        request.session['property_id'] = request.GET.get('property', None)
        request.session['app'] = request.GET.get('app', 0)
        request.session['registration'] = {'preload': {}}
        if 'lang' in request.GET: request.session[translation.LANGUAGE_SESSION_KEY] = request.GET.get('lang', 'en')
        if 'auto_login' in request.GET: request.session['registration']['preload']['auto_login'] = request.GET.get('auto_login', 0)
        if 'reservation_no' in request.GET: request.session['registration']['preload']['reservation_no'] = request.GET.get('reservation_no', '')
        if 'arrival_date' in request.GET: request.session['registration']['preload']['arrival_date'] = request.GET.get('arrival_date', '')
        if 'last_name' in request.GET: request.session['registration']['preload']['last_name'] = request.GET.get('last_name', '')
        if 'first_name' in request.GET: request.session['registration']['preload']['first_name'] = request.GET.get('first_name', '')
        if 'nationality' in request.GET: request.session['registration']['preload']['nationality'] = request.GET.get('nationality', '')
        if 'passport_no' in request.GET: request.session['registration']['preload']['passport_no'] = request.GET.get('passport_no', '')
        if 'birth_date' in request.GET: request.session['registration']['preload']['birth_date'] = request.GET.get('birth_date', '')
        return super().get(request, *args, **kwargs)


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
    success_url             = '/registration/guest_list'
    progress_bar_page       = 'reservation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = []
        for reservation in self.request.session['registration'].get('bookings', []):
            reservation = dict(reservation) # create new variable to prevent modification on `request.session`
            reservation['formattedArrivalDate'] = utils.format_display_date(reservation.get('arrivalDate', ''))
            reservation['formattedDepartureDate'] = utils.format_display_date(reservation.get('departureDate', ''))
            room = next((temp for temp in settings.REGISTRATION_ROOM_TYPES if temp['room_type'] == reservation['roomType']), {})
            reservation['roomName'] = room.get('room_name', '')
            reservation['roomImage'] = room.get('room_image', '')
            context['reservations'].append(reservation)
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class RegistrationGuestListView(ParameterRequiredMixin, PropertyRequiredMixin, RequestFormKwargsMixin, ProgressRateContextMixin, FormView):
    template_name           = 'registration/desktop/guest_list.html'
    form_class              = RegistrationGuestListForm
    success_url             = '/registration/other_info'
    parameter_required      = 'reservation'
    progress_bar_page       = 'guest_list'

    def get(self, request, *args, **kwargs):
        self.request.session['registration']['detail'] = {} # initiate and remove unsaved `detail` if any
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        max_guest = int(self.request.session['registration']['reservation'].get('adults', 1)) + int(self.request.session['registration']['reservation'].get('children', 0))
        context['add_guest'] = max_guest > len(self.request.session['registration']['reservation'].get('guestsList', []))
        context['can_submit'] = all([guest.get('is_done', False) for guest in self.request.session['registration']['reservation'].get('guestsList', [])])
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class RegistrationDetailView(PropertyRequiredMixin, RequestFormKwargsMixin, MobileTemplateMixin, ProgressRateContextMixin, UpdateView):
    template_name           = 'registration/desktop/detail.html'
    mobile_template_name    = 'registration/mobile/detail.html'
    form_class              = RegistrationDetailForm
    success_url             = '/registration/guest_list'
    progress_bar_page       = 'guest_list'

    def get_object(self):
        guest_id = decrypt(self.kwargs.get('encrypted_id', '')) # 0 for new guest
        guest = self.request.session['registration'].get('detail', {})
        if guest.get('id', None) != guest_id: # not from `passport` page 
            if guest_id != '0': # existing guest
                guest = next((dict(data) for data in self.request.session['registration']['reservation'].get('guestsList', {}) if data.get('guestID', '') == guest_id or data.get('new_guest_id') == guest_id), {})
            else: # new guest
                guest = {}
                guest['guestID'] = '0'
        if not guest:
            raise Http404('Not found')
        guest['id'] = guest.get('guestID', '0') # assign `id` from `guestID` as identifier
        self.request.session['registration']['detail'] = guest # assigned as separate object for not overwriting `reservation` session
        return self.request.session['registration']['detail']

    def dispatch(self, request, *args, **kwargs):
        max_guest = int(self.request.session['registration']['reservation'].get('adults', 1)) + int(self.request.session['registration']['reservation'].get('children', 0))
        if max_guest <= len(self.request.session['registration']['reservation'].get('guestsList', [])):
            return redirect('registration:guest_list') # redirect to guest list if max guests is exceeded
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ocr_required'] = settings.REGISTRATION_OCR # determine input is editable
        context['bootstrap_datepicker_language'] = translation.get_language()
        if context['bootstrap_datepicker_language'] == 'zh-hans':
            context['bootstrap_datepicker_language'] = 'zh-CN'
        return context

    def get_success_url(self):
        if not self.success_url:
            return super().get_success_url()
        url = self.success_url.format(**self.object)
        if not self.request.POST.get('is_submit', False):
            url = reverse('registration:passport', kwargs={'encrypted_id': self.kwargs.get('encrypted_id', '')})
        return url


class RegistrationPassportView(PropertyRequiredMixin, RequestFormKwargsMixin, MobileTemplateMixin, ProgressRateContextMixin, UpdateView):
    template_name           = 'registration/desktop/passport.html'
    mobile_template_name    = 'registration/mobile/passport.html'
    form_class              = RegistrationPassportForm
    success_url             = '/registration/detail/{encrypted_id}'
    progress_bar_page       = 'guest_list'

    def get_object(self):
        guest_id = decrypt(self.kwargs.get('encrypted_id', '')) # 0 for creation
        if self.request.session['registration']['detail'].get('id', None) != guest_id:
            raise Http404('Not found')
        return self.request.session['registration']['detail']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encrypted_id'] = self.kwargs.get('encrypted_id', '')
        return context

    def get_success_url(self):
        if not self.success_url:
            return super().get_success_url()
        url = self.success_url.format(**{'encrypted_id': self.kwargs.get('encrypted_id', '')}) # pass encrypted id
        return url


class RegistrationOtherInfoView(ParameterRequiredMixin, PropertyRequiredMixin, RequestFormKwargsMixin, ProgressRateContextMixin, FormView):
    template_name           = 'registration/desktop/other_info.html'
    form_class              = RegistrationOtherInfoForm
    success_url             = '/registration/complete'
    parameter_required      = 'guest_list'
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
        reservation['formattedArrivalDate'] = utils.format_display_date(reservation.get('arrivalDate', ''))
        reservation['formattedDepartureDate'] = utils.format_display_date(reservation.get('departureDate', ''))
        reservation['mainGuestLastName'] = next(guest.get('lastName', '') for guest in reservation.get('guestsList', []) if guest.get('isMainGuest', '0') == '1')
        room = next((temp for temp in settings.REGISTRATION_ROOM_TYPES if temp['room_type'] == reservation['roomType']), {})
        reservation['roomName'] = room.get('room_name', '')
        reservation['roomImage'] = room.get('room_image', '')
        context['reservation'] = reservation
        context['ios_url'] = settings.APP_IOS_URL
        context['android_url'] = settings.APP_ANDROID_URL
        context['direct_url'] = settings.APP_DIRECT_URL
        return context
