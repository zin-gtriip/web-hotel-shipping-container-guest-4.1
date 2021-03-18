import os, base64, datetime
from django                     import forms
from django.conf                import settings
from django.template.loader     import render_to_string
from django.utils               import timezone
from django.utils.translation   import gettext, gettext_lazy as _
from django_countries.fields    import Country, CountryField
from guest_facing.core          import gateways, utils as core_utils
from .                          import utils, samples

class RegistrationLoginForm(forms.Form):
    reservation_no  = forms.CharField(label=_('Reservation Number'))
    arrival_date    = forms.DateField(label=_('Arrival Date'))
    last_name       = forms.CharField(label=_('Last Name'))

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        self.response = {}
        self.fields['reservation_no'].initial = self.request.session.get('registration', {}).get('preload', {}).get('reservation_no')
        self.fields['arrival_date'].initial = self.request.session.get('registration', {}).get('preload', {}).get('arrival_date')
        self.fields['last_name'].initial = self.request.session.get('registration', {}).get('preload', {}).get('last_name')

    def clean(self):
        super().clean()
        reservation_no = self.cleaned_data.get('reservation_no')
        arrival_date = self.cleaned_data.get('arrival_date')
        last_name = self.cleaned_data.get('last_name')

        # validate required field
        if not reservation_no:
            self._errors['reservation_no'] = self.error_class([_('Enter the required information')])
        if not arrival_date:
            self._errors['arrival_date'] = self.error_class([_('Enter the required information')])
        if not last_name:
            self._errors['last_name'] = self.error_class([_('Enter the required information')])

        # validate to backend
        response = self.gateway_post()
        if response.get('overall_status', '') != 500:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([response.get('overall_status', '')])
        return self.cleaned_data

    def gateway_post(self):
        data = {}
        data['reservation_no'] = self.cleaned_data.get('reservation_no')
        data['arrival_date'] = self.cleaned_data.get('arrival_date').strftime('%Y-%m-%d')
        data['last_name'] = self.cleaned_data.get('last_name')
        self.response = gateways.guest_endpoint('/checkBookingsPreArrival', self.request.session.get('property_id', ''), data)
        return self.response
    
    def save(self):
        response = self.response
        preload_data = dict(self.request.session.get('registration', {}).get('preload', {})) # get and store preload because session will be cleared
        self.request.session['registration'] = {} # clear session data
        self.request.session['registration']['preload'] = preload_data # restore preload data
        self.request.session['registration']['bookings'] = response.get('data', [])
        self.request.session['registration']['input_reservation_no'] = self.cleaned_data.get('reservation_no')
        self.request.session['registration']['input_arrival_date'] = self.cleaned_data.get('arrival_date').strftime('%Y-%m-%d')
        self.request.session['registration']['input_last_name'] = self.cleaned_data.get('last_name')
        config = gateways.amp_endpoint('/getConfigVariables') or {} # get config variables
        expiry_duration = config.get('prearrival_session_duration_minutes', settings.REGISTRATION_SESSION_AGE_INITIAL)
        initial_expiry_date = (timezone.now() + datetime.timedelta(minutes=expiry_duration)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        self.request.session['registration']['initial_expiry_date'] = initial_expiry_date
        self.request.session['registration']['initial_expiry_duration'] = expiry_duration # will be popped after pass to templates
        if 'preload' in self.request.session['registration'] and 'auto_login' in self.request.session['registration']['preload']:
            self.request.session['registration']['preload']['auto_login'] = 0 # set auto login to False


class RegistrationTimerExtensionForm(forms.Form):
    token_id = forms.CharField()

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean(self):
        super().clean()
        token_id = self.cleaned_data.get('token_id')

        if not token_id:
            self._errors['token_id'] = self.error_class([_('Token ID is missing.')])
        else:
            session_key = self.request.session.session_key
            initial_expiry_date = self.request.session.get('registration', {}).get('initial_expiry_date', '')
            if core_utils.decrypt(token_id) != (session_key + initial_expiry_date):
                self._errors['token_id'] = self.error_class([_('Token ID is not correct.')])
        return self.cleaned_data

    def save(self):
        initial_expiry_date = self.request.session['registration'].get('initial_expiry_date', '')
        initial_expiry_date = datetime.datetime.strptime(initial_expiry_date, '%Y-%m-%dT%H:%M:%S.%f%z')
        config = gateways.amp_endpoint('/getConfigVariables', self.request.session.get('property_id', '')) or {} # get config variables
        extend_duration = config.get('prearrival_session_extend_duration_minutes', settings.REGISTRATION_SESSION_AGE_EXTEND)
        extended_expiry_date = (initial_expiry_date + datetime.timedelta(minutes=extend_duration)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        self.request.session['registration']['extended_expiry_date'] = extended_expiry_date
        self.request.session['registration']['extended_expiry_duration'] = extend_duration # will be popped after pass to templates


class RegistrationReservationForm(forms.Form):
    reservation_no = forms.ChoiceField(widget=forms.RadioSelect())

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        self.fields['reservation_no'].choices = [(reservation.get('reservationNo', ''), reservation.get('reservationNo', '')) for reservation in self.request.session['registration'].get('bookings', [])]

    def clean(self):
        super().clean()
        reservation_no = self.cleaned_data.get('reservation_no')

        if not reservation_no:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('No reservation selected.')])
        return self.cleaned_data

    def save(self):
        reservation_no = self.cleaned_data.get('reservation_no')
        reservation = next(reservation for reservation in self.request.session['registration'].get('bookings', []) if reservation.get('reservationNo', '') == reservation_no)
        self.request.session['registration']['reservation'] = reservation # also working as variable to prevent page jump


class RegistrationPassportForm(forms.Form):
    passport_file = forms.CharField(widget=forms.HiddenInput(), required=False)
    skip_passport = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    error_messages = {
        'Incorrect API key': _('Incorrect API key'),
        'Invalid passport image.': _('Invalid passport image.'),
        'Invalid passport image. MRZ Code is invalid.': _('Invalid passport image. MRZ Code is invalid.'),
        'Invalid passport image. Please make sure your passport page area is not blocked.': _('Invalid passport image. Please make sure your passport page area is not blocked.'),
        'Image file is too big.': _('Image file is too big.'),
        'Error scanning image. Please try again later.': _('Error scanning image. Please try again later.'),
        'Invalid NRIC image.': _('Invalid NRIC image.'),
    }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        self.response = {}

    def clean(self):
        super().clean()
        passport_file = self.cleaned_data.get('passport_file')
        skip_passport = self.cleaned_data.get('skip_passport')

        if not skip_passport and not passport_file:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('No image file selected.')])

        # validate based on `scan_type` (`passport` / `nric`)
        if not skip_passport:
            saved_file = self.save_file()
            response = self.gateway_ocr(saved_file)
            if 'status' not in response and 'message' not in response:
                if response.get('scan_type', 'passport') == 'passport':
                    if response.get('expired', '') == 'false':
                        config = gateways.amp_endpoint('/getConfigVariables', self.request.session.get('property_id', '')) or {} # get config variables
                        age_limit = config.get('prearrival_adult_min_age_years', settings.REGISTRATION_ADULT_AGE_LIMIT)
                        if utils.calculate_age(utils.parse_ocr_date(response.get('date_of_birth', ''))) <= age_limit:
                            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('You must be at least %(age)s years of age to proceed with your registration.') % {'age': age_limit}])
                    else:
                        self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('Your passport has expired, please capture / upload a valid passport photo to proceed')])
            else:
                response_message = response.get('message', _('Unknown error'))
                self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([self.error_messages.get(response_message, response_message)])
            # remove saved file if fail
            if self._errors:
                os.remove(saved_file)

        return self.cleaned_data

    def save_file(self):
        # save passport file using `session_key` as file name
        file_name = self.request.session.session_key +'.png'
        folder_ocr = os.path.join(settings.BASE_DIR, 'media', 'ocr')
        if not os.path.exists(folder_ocr):
            folder_media = os.path.join(settings.BASE_DIR, 'media')
            if not os.path.exists(folder_media):
                os.mkdir(folder_media)
            os.mkdir(folder_ocr)
        saved_file = os.path.join(folder_ocr, file_name)
        file_data = base64.b64decode(self.cleaned_data.get('passport_file'))
        with open(saved_file, 'wb') as f:
            f.write(file_data)
        return saved_file

    def gateway_ocr(self, saved_file):
        scan_type = 'passport'
        response = gateways.ocr(saved_file, 'passport')
        if 'status' in response or 'message' in response:
            scan_type = 'nric'
            response = gateways.ocr(saved_file, 'nric')
        response['scan_type'] = scan_type
        self.response = response
        return self.response

    def save(self):
        main_guest = next((guest for guest in self.request.session['registration']['reservation'].get('guestsList', []) if guest.get('isMainGuest', '0') == '1'), {})
        if self.cleaned_data.get('skip_passport'):
            main_guest.update({'passportImage': ''})
            self.request.session['registration'].pop('ocr', None)
        else:
            file_name = self.request.session.session_key +'.png'
            folder_name = os.path.join(settings.BASE_DIR, 'media', 'ocr')
            saved_file = os.path.join(folder_name, file_name)
            with open(saved_file, 'rb') as image_file:
                file_b64_encoded = base64.b64encode(image_file.read())
            main_guest.update({'passportImage': file_b64_encoded.decode()})
            self.request.session['registration']['ocr'] = self.response
            os.remove(saved_file) # remove saved file
        self.request.session['registration']['passport'] = True # variable to prevent page jump


class RegistrationDetailForm(forms.Form):
    guest_id    = forms.CharField(widget=forms.HiddenInput())
    first_name  = forms.CharField(label=_('First Name'))
    last_name   = forms.CharField(label=_('Last Name'))
    passport_no = forms.CharField(label=_('Passport Number'))
    nationality = CountryField(blank_label=_('[Select Country]')).formfield(label=_('Nationality'))
    birth_date  = forms.DateField(label=_('Date of Birth'))

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        # from backend
        main_guest = next((guest for guest in self.request.session['registration']['reservation'].get('guestsList', []) if guest.get('isMainGuest', '0') == '1'), {})
        guest_id = main_guest.get('guestID', 0)
        first_name = main_guest.get('firstName', '')
        last_name = main_guest.get('lastName', '')
        passport_no = main_guest.get('passportNo', '')
        nationality = main_guest.get('nationality', 'SG')
        birth_date = main_guest.get('dob', '')
        # from `preload`
        first_name = self.request.session.get('registration', {}).get('preload', {}).get('first_name', first_name)
        passport_no = self.request.session.get('registration', {}).get('preload', {}).get('passport_no', passport_no)
        nationality = self.request.session.get('registration', {}).get('preload', {}).get('nationality', nationality)
        birth_date = self.request.session.get('registration', {}).get('preload', {}).get('birth_date', birth_date)
        # from `ocr`
        first_name = self.request.session.get('registration', {}).get('ocr', {}).get('names', first_name)
        passport_no = self.request.session.get('registration', {}).get('ocr', {}).get('number', passport_no)
        nationality = Country(self.request.session.get('registration', {}).get('ocr', {}).get('nationality', '')).code or nationality
        birth_date = utils.parse_ocr_date(self.request.session.get('registration', {}).get('ocr', {}).get('date_of_birth', '')) or birth_date
        # assign
        self.fields['guest_id'].initial = guest_id
        self.fields['first_name'].initial = first_name.title()
        self.fields['last_name'].initial = last_name
        self.fields['passport_no'].initial = passport_no
        self.fields['nationality'].initial = nationality
        self.fields['birth_date'].initial = birth_date
    
    def clean(self):
        super().clean()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        nationality = self.cleaned_data.get('nationality')
        passport_no = self.cleaned_data.get('passport_no')
        birth_date = self.cleaned_data.get('birth_date')
        
        # validate required field
        if not first_name:
            self._errors['first_name'] = self.error_class([_('Enter the required information')])
        if not last_name:
            self._errors['last_name'] = self.error_class([_('Enter the required information')])
        if not nationality:
            self._errors['nationality'] = self.error_class([_('Enter the required information')])
        if not passport_no:
            self._errors['passport_no'] = self.error_class([_('Enter the required information')])
        if not birth_date:
            self._errors['birth_date'] = self.error_class([_('Enter the required information')])
        else:
            config = gateways.amp_endpoint('/getConfigVariables', self.request.session.get('property_id', '')) or {} # get config variables
            age_limit = config.get('prearrival_adult_min_age_years', settings.REGISTRATION_ADULT_AGE_LIMIT)
            if utils.calculate_age(birth_date) <= age_limit:
                self._errors['birth_date'] = self.error_class([_('Main guest has to be %(age)s and above.') % {'age': age_limit}])
        return self.cleaned_data

    def save(self, extra):
        guests = [{
            'guestID': self.cleaned_data.get('guest_id'),
            'firstName': self.cleaned_data.get('first_name'),
            'lastName': self.cleaned_data.get('last_name'),
            'nationality': self.cleaned_data.get('nationality'),
            'passportNo': self.cleaned_data.get('passport_no'),
            'dob': self.cleaned_data.get('birth_date').strftime('%Y-%m-%d'),
        }]
        for form in extra.forms:
            guests.append({
                'guestID': form.cleaned_data.get('guest_id'),
                'firstName': form.cleaned_data.get('first_name'),
                'lastName': form.cleaned_data.get('last_name'),
                'nationality': form.cleaned_data.get('nationality'),
                'passportNo': form.cleaned_data.get('passport_no'),
                'dob': form.cleaned_data.get('birth_date').strftime('%Y-%m-%d'),
            })

        # update with session `guestList` data, in case there are other fields in session `guestList`
        updated_guests = []
        for guest in guests:
            if guest.get('guestID', '0') != '0': # update prefilled guest only
                reservation_guest = next((guest_temp for guest_temp in self.request.session['registration']['reservation'].get('guestsList', []) if guest_temp.get('guestID', '') == guest.get('guestID', '')), {})
                reservation_guest.update(guest)
                updated_guests.append(reservation_guest)
            else:
                updated_guests.append(guest)
        self.request.session['registration']['reservation']['guestsList'] = updated_guests # replace with whole new list
        self.request.session['registration'].pop('ocr', None) # remove ocr after save detail
        self.request.session['registration']['detail'] = True # variable to prevent page jump


class RegistrationDetailExtraForm(forms.Form):
    guest_id = forms.CharField(widget=forms.HiddenInput())
    first_name = forms.CharField(label=_('First Name'))
    last_name = forms.CharField(label=_('Last Name'))
    nationality = CountryField(blank_label=_('[Select Country]')).formfield(label=_('Nationality'))
    passport_no = forms.CharField(label=_('Passport Number'))
    birth_date = forms.DateField(label=_('Date of Birth'))

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''

    def clean(self):
        super().clean()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        nationality = self.cleaned_data.get('nationality')
        passport_no = self.cleaned_data.get('passport_no')
        birth_date = self.cleaned_data.get('birth_date')

        if not first_name:
            self._errors['first_name'] = self.error_class([_('Enter the required information')])
        if not last_name:
            self._errors['last_name'] = self.error_class([_('Enter the required information')])
        if not nationality:
            self._errors['nationality'] = self.error_class([_('Enter the required information')])
        if not passport_no:
            self._errors['passport_no'] = self.error_class([_('Enter the required information')])
        if not birth_date:
            self._errors['birth_date'] = self.error_class([_('Enter the required information')])
        return self.cleaned_data


class RegistrationDetailExtraBaseFormSet(forms.BaseFormSet):
    
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        # populate additional guests
        prefilled = []
        for guest in self.request.session['registration']['reservation'].get('guestsList', []):
            if guest.get('isMainGuest', '0') == '0':
                prefilled.append({
                    'guest_id': guest.get('guestID', ''),
                    'first_name': guest.get('firstName', ''),
                    'last_name': guest.get('lastName', ''),
                    'nationality': guest.get('nationality', ''),
                    'passport_no': guest.get('passportNo', ''),
                    'birth_date': guest.get('dob', ''),
                })
        self.extra = 0 # number of empty extra form to be populated
        self.initial = prefilled

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['request'] = self.request
        return kwargs

    def clean(self):
        super().clean()
        adult, max_adult = 1, int(self.request.session['registration']['reservation'].get('adults', 1))
        config = gateways.amp_endpoint('/getConfigVariables', self.request.session.get('property_id', '')) or {} # get config variables
        age_limit = config.get('prearrival_adult_min_age_years', settings.REGISTRATION_ADULT_AGE_LIMIT)
        for form in self.forms:
            if utils.calculate_age(form.cleaned_data.get('birth_date')) > age_limit:
                adult += 1
        if adult > max_adult:
            self._non_form_errors = self.error_class([_('You have exceeded the number of adults.')])


# initiate formset, for one2many field
RegistrationDetailExtraFormSet = forms.formset_factory(RegistrationDetailExtraForm, formset=RegistrationDetailExtraBaseFormSet)


class RegistrationOtherInfoForm(forms.Form):
    arrival_time        = forms.ChoiceField(label=_('Time of Arrival'))
    special_requests    = forms.CharField(label=_('Special Requests'), required=False)
    email               = forms.EmailField(label=_('Email'), label_suffix='*')
    is_subscribe        = forms.BooleanField(label=_('Is Subscribe'), required=False)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        self.fields['arrival_time'].choices = utils.generate_arrival_time()
        self.fields['arrival_time'].initial = utils.parse_arrival_time(self.request.session['registration']['reservation'].get('eta', ''))
        self.fields['special_requests'].initial = self.request.session['registration']['reservation'].get('comments', '')
        main_guest = next((guest for guest in self.request.session['registration']['reservation'].get('guestsList', []) if guest.get('isMainGuest', '0') == '1'), {})
        self.fields['email'].initial = main_guest.get('email', '')
        self.fields['is_subscribe'].initial = True if main_guest.get('emailSubscription', '1') == '1' else False

    def clean(self):
        super().clean()
        arrival_time = self.cleaned_data.get('arrival_time')
        email = self.cleaned_data.get('email')

        if not arrival_time:
            self._errors['arrival_time'] = self.error_class([_('Enter the required information')])
        if not email:
            self._errors['email'] = self.error_class([_('Enter the required information')])

        return self.cleaned_data

    def save(self):
        arrival_time = self.cleaned_data.get('arrival_time')
        special_requests = self.cleaned_data.get('special_requests')
        email = self.cleaned_data.get('email')
        is_subscribe = self.cleaned_data.get('is_subscribe')

        main_guest = next((guest for guest in self.request.session['registration']['reservation'].get('guestsList', []) if guest.get('isMainGuest', '0') == '1'), {})
        main_guest.update({
            'email': email,
            'emailSubscription': is_subscribe and '1' or '0',
        })
        self.request.session['registration']['reservation']['eta'] = arrival_time + ':00.000'
        self.request.session['registration']['reservation']['comments'] = special_requests
        self.request.session['registration']['other_info'] = True # variable to prevent page jump

    def prepare_email(self):
        context = dict(self.request.session['registration']['reservation']) # create new variable to prevent modification on `request.session`
        context['formattedArrivalDate'] = utils.format_display_date(context.get('arrivalDate', ''))
        context['formattedDepartureDate'] = utils.format_display_date(context.get('departureDate', ''))
        main_guest = next(guest for guest in context.get('guestsList', []) if guest.get('isMainGuest', '0') == '1')
        context['mainGuestFirstName'] = main_guest.get('firstName', '')
        context['mainGuestLastName'] = main_guest.get('lastName', '')
        room = next((temp for temp in settings.REGISTRATION_ROOM_TYPES if temp['room_type'] == context['roomType']), {})
        context['roomName'] = room.get('room_name', '')
        context['roomImage'] = settings.HOST_URL + room.get('room_image', '')
        context['hotelName'] = settings.HOTEL_NAME
        context['staticURL'] = settings.HOST_URL + settings.STATIC_IMAGE_URL
        context['iOSURL'] = settings.APP_IOS_URL
        context['androidURL'] = settings.APP_ANDROID_URL
        data = {}
        template = settings.REGISTRATION_COMPLETE_EMAIL or os.path.join(settings.BASE_DIR, 'registration', 'templates', 'registration', 'email', 'complete.html')
        data['title'] = _('Pre-Check-In Complete - %(hotel_name)s - Reservation #%(reservation_no)s') % {'hotel_name': settings.HOTEL_NAME, 'reservation_no': context.get('reservationNo', '')}
        data['html'] = render_to_string(template, context)
        return data

    def gateway_post(self):
        data = self.request.session['registration']['reservation']
        email = self.prepare_email()
        data['customerInputNumber'] = self.request.session['registration'].get('input_reservation_no', '')
        data = {**data, **email} # add email data
        response = gateways.guest_endpoint('/processGuestsPreArrival', self.request.session.get('property_id', ''), data)
        if response.get('success', '') == 'true':
            # get existing reservation from backend
            new_booking_data = {}
            new_booking_data['reservation_no'] = self.request.session['registration'].get('input_reservation_no', '')
            new_booking_data['arrival_date'] = self.request.session['registration'].get('input_arrival_date', '')
            new_booking_data['last_name'] = self.request.session['registration'].get('input_last_name', '')
            new_booking_response = gateways.guest_endpoint('/checkBookingsPreArrival', self.request.session.get('property_id', ''), new_booking_data)
            self.request.session['registration']['bookings'] = new_booking_response.get('data', [])
        else:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([response.get('message', _('Unknown error'))])


class RegistrationCompleteForm(forms.Form):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean(self):
        super().clean()
        if not self.request.session['registration'].get('bookings', []):
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('There is no reservation can be done for registration')])
        return self.cleaned_data

    def save(self):
        # reset data on session using `REGISTRATION_PROGRESS_BAR_PAGES`
        for page in settings.REGISTRATION_PARAMETER_REQUIRED_PAGES or list():
            self.request.session['registration'].pop(page, None)
        config = gateways.amp_endpoint('/getConfigVariables', self.request.session.get('property_id', '')) or {} # get config variables
        expiry_duration = config.get('prearrival_session_duration_minutes', settings.REGISTRATION_SESSION_AGE_INITIAL)
        initial_expiry_date = (timezone.now() + datetime.timedelta(minutes=expiry_duration)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        self.request.session['registration']['initial_expiry_date'] = initial_expiry_date
        self.request.session['registration']['initial_expiry_duration'] = expiry_duration # will be popped after pass to templates
        self.request.session['registration'].pop('extended_expiry_date', None)
