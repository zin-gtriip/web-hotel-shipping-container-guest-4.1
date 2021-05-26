import os, base64, datetime
from datetime                   import datetime as dt
from django                     import forms
from django.conf                import settings
from django.utils               import timezone
from django.utils.translation   import gettext, gettext_lazy as _
from django_countries.fields    import Country, CountryField
from captcha                    import fields as captchaField, widgets as captchaWidget
from guest_facing.core          import gateways
from guest_facing.core.utils    import decrypt
from .                          import utils


class RegistrationLoginForm(forms.Form):
    reservation_no  = forms.CharField(label=_('Reservation Number'), required=False)
    arrival_date    = forms.DateField(label=_('Arrival Date'), required=False)
    last_name       = forms.CharField(label=_('Last Name'), required=False)
    recaptcha       = captchaField.ReCaptchaField(widget=captchaWidget.ReCaptchaV2Invisible)

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
        recaptcha = self.cleaned_data.get('recaptcha')

        # validate required field
        if not reservation_no:
            self._errors['reservation_no'] = self.error_class([_('Enter the required information')])
        if not arrival_date:
            self._errors['arrival_date'] = self.error_class([_('Enter the required information')])
        if not last_name:
            self._errors['last_name'] = self.error_class([_('Enter the required information')])
        if not recaptcha:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class(['recaptcha'])
        # validate to backend
        if not self.errors:
            response = self.gateway_post()
            if response.get('statusCode', '') != '5001':
                self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([response.get('statusCode', '')])
        return self.cleaned_data

    def gateway_post(self):
        data = {}
        data['reservationNo'] = self.cleaned_data.get('reservation_no')
        data['arrivalDate'] = self.cleaned_data.get('arrival_date').strftime('%Y-%m-%d')
        data['lastName'] = self.cleaned_data.get('last_name')
        self.response = gateways.guest_endpoint('post', '/checkWebRegistration', self.request.session.get('property_id', ''), data)
        return self.response
    
    def save(self):
        response = self.response
        preload_data = dict(self.request.session.get('registration', {}).get('preload', {})) # get and store preload because session will be cleared
        self.request.session['registration'] = {} # clear session data
        self.request.session['registration']['preload'] = preload_data # restore preload data
        self.request.session['registration']['bookings'] = response.get('data', {}).get('data', [])
        self.request.session['registration']['input_reservation_no'] = self.cleaned_data.get('reservation_no')
        self.request.session['registration']['input_arrival_date'] = self.cleaned_data.get('arrival_date').strftime('%Y-%m-%d')
        self.request.session['registration']['input_last_name'] = self.cleaned_data.get('last_name')
        config = gateways.amp_endpoint('get', '/configVariables', self.request.session.get('property_id', '')) or {}
        expiry_duration = config.get('data', {}).get('prearrivalSessionDurationMinutes', settings.REGISTRATION_SESSION_AGE_INITIAL)
        initial_expiry_date = (timezone.now() + datetime.timedelta(minutes=expiry_duration)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        self.request.session['registration']['initial_expiry_date'] = initial_expiry_date
        self.request.session['registration']['initial_expiry_duration'] = expiry_duration # will be popped after pass to templates
        if 'preload' in self.request.session['registration'] and 'auto_login' in self.request.session['registration']['preload']:
            self.request.session['registration']['preload']['auto_login'] = 0 # set auto login to False


class RegistrationTimerExtensionForm(forms.Form):
    token_id = forms.CharField(required=False)

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
            if decrypt(token_id) != (session_key + initial_expiry_date):
                self._errors['token_id'] = self.error_class([_('Token ID is not correct.')])
        return self.cleaned_data

    def save(self):
        initial_expiry_date = self.request.session['registration'].get('initial_expiry_date', '')
        initial_expiry_date = datetime.datetime.strptime(initial_expiry_date, '%Y-%m-%dT%H:%M:%S.%f%z')
        config = gateways.amp_endpoint('get', '/configVariables', self.request.session.get('property_id', '')) or {} # get config variables
        extend_duration = config.get('data', {}).get('prearrivalSessionExtendDurationMinutes', settings.REGISTRATION_SESSION_AGE_EXTEND)
        extended_expiry_date = (initial_expiry_date + datetime.timedelta(minutes=extend_duration)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        self.request.session['registration']['extended_expiry_date'] = extended_expiry_date
        self.request.session['registration']['extended_expiry_duration'] = extend_duration # will be popped after pass to templates


class RegistrationReservationForm(forms.Form):
    reservation_no = forms.ChoiceField(widget=forms.RadioSelect(), required=False)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        self.fields['reservation_no'].choices = [(reservation.get('pmsNo', ''), reservation.get('pmsNo', '')) for reservation in self.request.session['registration'].get('bookings', [])]

    def clean(self):
        super().clean()
        reservation_no = self.cleaned_data.get('reservation_no')

        if not reservation_no:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('No reservation selected.')])
        return self.cleaned_data

    def save(self):
        reservation_no = self.cleaned_data.get('reservation_no')
        reservation = next(reservation for reservation in self.request.session['registration'].get('bookings', []) if reservation.get('pmsNo', '') == reservation_no)
        self.request.session['registration']['reservation'] = reservation # also working as variable to prevent page jump


class RegistrationGuestListForm(forms.Form):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''

    def clean(self):
        super().clean()
        max_guest = int(self.request.session['registration']['reservation'].get('adults', 1)) + int(self.request.session['registration']['reservation'].get('children', 0))
        if max_guest < len(self.request.session['registration']['reservation'].get('guestsList', [])):
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('You have exceeded the number of guests.')])
        return self.cleaned_data

    def save(self):
        self.request.session['registration']['guest_list'] = True

    def gateway_post(self):
        self.request.session['registration']['other_info'] = True # mark `other info` page as done
        data = self.request.session['registration']['reservation']
        email = utils.prepare_email(dict(self.request.session['registration']['reservation'])) # create new variable to prevent modification on `request.session`
        data['userInputNumber'] = self.request.session['registration'].get('input_reservation_no', '')
        data = {**data, **email} # add email data
        response = gateways.guest_endpoint('post', '/submitWebRegistration', self.request.session.get('property_id', ''), data)
        if response.get('statusCode', '') == '5002':
            # get existing reservation from backend
            new_booking_data = {}
            new_booking_data['reservationNo'] = self.request.session['registration'].get('input_reservation_no', '')
            new_booking_data['arrivalDate'] = self.request.session['registration'].get('input_arrival_date', '')
            new_booking_data['lastName'] = self.request.session['registration'].get('input_last_name', '')
            new_booking_response = gateways.guest_endpoint('post', '/checkWebRegistration', self.request.session.get('property_id', ''), new_booking_data)
            new_booking = new_booking_response.get('data', {}).get('data', [])
            self.request.session['registration']['bookings'] = [reservation for reservation in new_booking if reservation.get('pmsNo') != self.request.session['registration'].get('reservation', {}).get('pmsNo', '')]
        else:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([response.get('message', _('Unknown error'))])


class RegistrationDetailForm(forms.Form):
    first_name = forms.CharField(label=_('First Name'), required=False)
    last_name = forms.CharField(label=_('Last Name'), required=False)
    id_no = forms.CharField(label=_('Passport Number'), required=False)
    nationality = CountryField(blank_label=_('[Select Country]')).formfield(label=_('Nationality'), required=False)
    birth_date = forms.DateField(label=_('Date of Birth'), required=False)
    is_overwrite = forms.BooleanField(initial=True, required=False)
    is_submit = forms.BooleanField(initial=True, required=False)

    def __init__(self, instance, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = instance
        self.request = request
        self.label_suffix = ''
        # from backend
        first_name = self.instance.get('firstName', '')
        last_name = self.instance.get('lastName', '')
        id_no = self.instance.get('idNo', '')
        nationality = self.instance.get('nationality', 'SG')
        birth_date = self.instance.get('dob', '')
        # from `preload`
        if self.instance.get('isMainGuest', False):
            first_name = self.request.session.get('registration', {}).get('preload', {}).get('first_name', first_name)
            id_no = self.request.session.get('registration', {}).get('preload', {}).get('id_no', id_no)
            nationality = self.request.session.get('registration', {}).get('preload', {}).get('nationality', nationality)
            birth_date = self.request.session.get('registration', {}).get('preload', {}).get('birth_date', birth_date)
        # from `ocr`
        if self.instance.get('is_overwrite', False):
            first_name = self.request.session.get('registration', {}).get('ocr', {}).get('first_name', first_name)
            if self.instance.get('guestId', 0) == 0:
                last_name = self.request.session.get('registration', {}).get('ocr', {}).get('last_name', last_name)
            id_no = self.request.session.get('registration', {}).get('ocr', {}).get('number', id_no)
            nationality = Country(self.request.session.get('registration', {}).get('ocr', {}).get('nationality', '')).code or nationality
            birth_date = self.request.session.get('registration', {}).get('ocr', {}).get('date_of_birth', birth_date)
        # assign
        self.fields['first_name'].initial = first_name.title()
        self.fields['last_name'].initial = last_name
        self.fields['id_no'].initial = id_no
        self.fields['nationality'].initial = nationality
        self.fields['birth_date'].initial = birth_date
    
    def clean(self):
        super().clean()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        nationality = self.cleaned_data.get('nationality')
        id_no = self.cleaned_data.get('id_no')
        birth_date = self.cleaned_data.get('birth_date')
        is_submit = self.cleaned_data.get('is_submit')
        config = gateways.amp_endpoint('get', '/configVariables', self.request.session.get('property_id', '')) or {} # get config variables
        
        if is_submit:
            if not first_name:
                self._errors['first_name'] = self.error_class([_('Enter the required information')])
            if not last_name:
                self._errors['last_name'] = self.error_class([_('Enter the required information')])
            if not nationality:
                self._errors['nationality'] = self.error_class([_('Enter the required information')])
            if not id_no:
                self._errors['id_no'] = self.error_class([_('Enter the required information')])
            if not birth_date:
                self._errors['birth_date'] = self.error_class([_('Enter the required information')])
            else:
                age_limit = config.get('data', {}).get('prearrivalAdultMinAgeYears', settings.REGISTRATION_ADULT_AGE_LIMIT)
                is_adult = utils.calculate_age(birth_date) > age_limit
                # validate main guest age limit
                if self.instance.get('isMainGuest', False) and not is_adult:
                    self._errors['birth_date'] = self.error_class([_('Main guest has to be %(age)s and above.') % {'age': age_limit}])
                # validate adult no
                max_adult = int(self.request.session['registration']['reservation'].get('adults', 1))
                adult = is_adult and 1 or 0
                for guest in self.request.session['registration']['reservation'].get('guestsList', []):
                    if guest.get('guestId') != self.instance.get('guestId') or guest.get('new_guest_id') != self.instance.get('new_guest_id'): # not current instance
                        if utils.calculate_age(dt.strptime(guest.get('dob', ''), '%Y-%m-%d')) > age_limit: # is adult
                            adult += 1
                if max_adult < adult:
                    self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('You have exceeded the number of adults.')])
            if config.get('data', {}).get('enableOcr', settings.REGISTRATION_OCR) and (not self.instance.get('idImage') or not self.instance.get('idType')):
                self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('You need to upload passport image.')])
        return self.cleaned_data

    def save(self):
        self.instance['firstName'] = self.cleaned_data.get('first_name')
        self.instance['lastName'] = self.cleaned_data.get('last_name')
        self.instance['nationality'] = self.cleaned_data.get('nationality')
        self.instance['idNo'] = self.cleaned_data.get('id_no')
        self.instance['dob'] = self.cleaned_data.get('birth_date').strftime('%Y-%m-%d') if self.cleaned_data.get('birth_date') else ''
        self.instance['is_overwrite'] = self.cleaned_data.get('is_overwrite')
        if self.cleaned_data.get('is_submit', False):
            if self.instance.get('guestId', 0) != 0 or self.instance.get('new_guest_id', None): # existing guest
                guest = next((data for data in self.request.session['registration']['reservation'].get('guestsList', []) if data.get('guestId', None) == self.instance.get('id', 0) or data.get('new_guest_id', '') == self.instance.get('new_guest_id', None)), {})
                guest['firstName'] = self.instance.get('firstName', '')
                guest['lastName'] = self.instance.get('lastName', '')
                guest['nationality'] = self.instance.get('nationality', '')
                guest['nationalityThreeLetters'] = Country(self.instance.get('nationality')).alpha3
                guest['idNo'] = self.instance.get('idNo', '')
                guest['dob'] = self.instance.get('dob', '')
                guest['idImage'] = self.instance.get('idImage', '')
                guest['idType'] = self.instance.get('idType', '')
                guest['is_done'] = True
            else: # new guest
                guest = {}
                guest['guestId'] = self.instance.get('guestId', 0)
                guest['firstName'] = self.instance.get('firstName', '')
                guest['lastName'] = self.instance.get('lastName', '')
                guest['nationality'] = self.instance.get('nationality', '')
                guest['nationalityThreeLetters'] = Country(self.instance.get('nationality')).alpha3
                guest['idNo'] = self.instance.get('idNo', '')
                guest['dob'] = self.instance.get('dob', '')
                guest['idImage'] = self.instance.get('idImage', '')
                guest['idType'] = self.instance.get('idType', '')
                guest['new_guest_id'] = 'new%s' % len([data for data in self.request.session['registration']['reservation'].get('guestsList', []) if data.get('guestId', 0) == 0])
                guest['is_done'] = True
                self.request.session['registration']['reservation']['guestsList'].append(guest)
        return self.instance


class RegistrationOcrForm(forms.Form):
    ocr_file = forms.CharField(widget=forms.HiddenInput(), required=False)

    error_messages = {
        'Incorrect API key': _('Incorrect API key'),
        'Invalid passport image.': _('Invalid passport image.'),
        'Invalid passport image. MRZ Code is invalid.': _('Invalid passport image. MRZ Code is invalid.'),
        'Invalid passport image. Please make sure your passport page area is not blocked.': _('Invalid passport image. Please make sure your passport page area is not blocked.'),
        'Image file is too big.': _('Image file is too big.'),
        'Error scanning image. Please try again later.': _('Error scanning image. Please try again later.'),
        'Invalid NRIC image.': _('Invalid NRIC image.'),
    }

    def __init__(self, instance, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = instance
        self.request = request
        self.label_suffix = ''
        self.response = {}
        self.file = None
        self.request.session['registration']['ocr'] = {} # initiate `ocr`

    def clean(self):
        super().clean()
        ocr_file = self.cleaned_data.get('ocr_file')

        if not ocr_file:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('No image file selected.')])
        else:
            # validate based on `scan_type` (`passport` / `nric`)
            self.save_file()
            self.gateway_ocr()
            if self.response.get('success'):
                result = self.response.get('result', {})
                if result.get('document_type', 'passport') == 'passport' and not result.get('expired'):
                    self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('Your passport has expired, please capture / upload a valid passport photo to proceed')])
            else:
                response_message = self.response.get('errorMessage', _('Unknown error'))
                self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([self.error_messages.get(response_message, response_message)])
            
            if self._errors: # remove saved file if fail
                os.remove(self.file)

        return self.cleaned_data

    def save_file(self):
        file_name = self.request.session.session_key +'.png' # save ocr file using `session_key` as file name
        folder_ocr = os.path.join(settings.BASE_DIR, 'media', 'ocr')
        if not os.path.exists(folder_ocr):
            folder_media = os.path.join(settings.BASE_DIR, 'media')
            if not os.path.exists(folder_media):
                os.mkdir(folder_media)
            os.mkdir(folder_ocr)
        saved_file = os.path.join(folder_ocr, file_name)
        file_data = base64.b64decode(self.cleaned_data.get('ocr_file'))
        with open(saved_file, 'wb') as f:
            f.write(file_data)
        self.file = saved_file

    def gateway_ocr(self):
        self.response = gateways.ocr(self.file)

    def save(self):
        with open(self.file, 'rb') as image_file:
            file_b64_encoded = base64.b64encode(image_file.read())
        self.instance['idImage'] = file_b64_encoded.decode()
        self.instance['idType'] = 'PASSPORT' if self.response.get('result', {}).get('document_type') == 'passport' else 'IC'
        self.request.session['registration']['ocr'] = self.response.get('result', {})
        return self.instance


class RegistrationOtherInfoForm(forms.Form):
    arrival_time        = forms.ChoiceField(label=_('Time of Arrival'), required=False)
    special_requests    = forms.CharField(label=_('Special Requests'), required=False)
    email               = forms.EmailField(label=_('Email'), required=False)
    is_subscribe        = forms.BooleanField(label=_('Is Subscribe'), required=False)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        self.fields['arrival_time'].choices = utils.generate_arrival_time()
        self.fields['arrival_time'].initial = utils.parse_arrival_time(self.request.session['registration']['reservation'].get('eta', ''))
        self.fields['special_requests'].initial = self.request.session['registration']['reservation'].get('comments', '')
        main_guest = next((guest for guest in self.request.session['registration']['reservation'].get('guestsList', []) if guest.get('isMainGuest', False)), {})
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

        main_guest = next((guest for guest in self.request.session['registration']['reservation'].get('guestsList', []) if guest.get('isMainGuest', False)), {})
        main_guest.update({'email': email,'emailSubscription': is_subscribe})
        self.request.session['registration']['reservation']['eta'] = arrival_time + ':00'
        self.request.session['registration']['reservation']['comments'] = special_requests
        self.request.session['registration']['other_info'] = True # variable to prevent page jump

    def gateway_post(self):
        data = self.request.session['registration']['reservation']
        email = utils.prepare_email(dict(self.request.session['registration']['reservation'])) # create new variable to prevent modification on `request.session`
        data['userInputNumber'] = self.request.session['registration'].get('input_reservation_no', '')
        data = {**data, **email} # add email data
        response = gateways.guest_endpoint('post', '/submitWebRegistration', self.request.session.get('property_id', ''), data)
        if response.get('statusCode', '') == '5002':
            # get existing reservation from backend
            new_booking_data = {}
            new_booking_data['reservationNo'] = self.request.session['registration'].get('input_reservation_no', '')
            new_booking_data['arrivalDate'] = self.request.session['registration'].get('input_arrival_date', '')
            new_booking_data['lastName'] = self.request.session['registration'].get('input_last_name', '')
            new_booking_response = gateways.guest_endpoint('post', '/checkWebRegistration', self.request.session.get('property_id', ''), new_booking_data)
            new_booking = new_booking_response.get('data', {}).get('data', [])
            self.request.session['registration']['bookings'] = [reservation for reservation in new_booking if reservation.get('pmsNo') != self.request.session['registration'].get('reservation', {}).get('pmsNo', '')]
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
        config = gateways.amp_endpoint('get', 'configVariables', self.request.session.get('property_id', '')) or {} # get config variables
        expiry_duration = config.get('data', {}).get('prearrivalSessionDurationMinutes', settings.REGISTRATION_SESSION_AGE_INITIAL)
        initial_expiry_date = (timezone.now() + datetime.timedelta(minutes=expiry_duration)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        self.request.session['registration']['initial_expiry_date'] = initial_expiry_date
        self.request.session['registration']['initial_expiry_duration'] = expiry_duration # will be popped after pass to templates
        self.request.session['registration'].pop('extended_expiry_date', None)
