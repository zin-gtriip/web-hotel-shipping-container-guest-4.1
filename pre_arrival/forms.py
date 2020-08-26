import os, base64, datetime
from django                     import forms
from django.conf                import settings
from django.utils               import timezone
from django.utils.translation   import gettext, gettext_lazy as _
from django_countries.fields    import Country, CountryField
from guest_base                 import gateways
from .                          import utilities, samples

class PreArrivalLoginForm(forms.Form):
    reservation_no  = forms.CharField(label=_('Reservation Number'))
    arrival_date    = forms.DateField(label=_('Arrival Date'))
    last_name       = forms.CharField(label=_('Last Name'))

    SUCCESS_CODE    = 500
    ERROR_MESSAGES  = {
        100: _('No matching PMS reservation with given Reservation Number.'),
        101: _('No matching PMS reservation with given Arrival Date.'),
        102: _('No main guest found for this reservation.'),
        103: _('No matching PMS reservation with given Last Name.'),
        200: _('No matching reservation status record.'),
        300: _('No matching pre-arrival time frame record.'),
        400: _('Pre-arrival performed.'),
    }

    def __init__(self, request, *args, **kwargs):
        super(PreArrivalLoginForm, self).__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        self.fields['reservation_no'].initial = self.request.session.get('pre_arrival', {}).get('preload', {}).get('reservation_no')
        self.fields['arrival_date'].initial = self.request.session.get('pre_arrival', {}).get('preload', {}).get('arrival_date')
        self.fields['last_name'].initial = self.request.session.get('pre_arrival', {}).get('preload', {}).get('last_name')

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
        if response.get('overall_status', '') != self.SUCCESS_CODE:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([self.ERROR_MESSAGES.get(response.get('overall_status', 0), _('Unknown error'))])
        
        return self.cleaned_data

    def gateway_post(self):
        data = {
            'reservation_no': self.cleaned_data.get('reservation_no'),
            'arrival_date': self.cleaned_data.get('arrival_date').strftime('%Y-%m-%d'),
            'last_name': self.cleaned_data.get('last_name'),
        }
        return gateways.backend_post('/checkBookingsPreArrival', data)
    
    def save_data(self):
        data = self.gateway_post()
        if not 'pre_arrival' in self.request.session:
            self.request.session['pre_arrival'] = {}
        expiry_duration = gateways.amp('GET', settings.AMP_CONFIG_URL + str(settings.AMP_CONFIG_ID)).get('pre_arrival_session_expiry_duration', settings.PRE_ARRIVAL_AGE)
        expiry_date = (timezone.now() + datetime.timedelta(minutes=expiry_duration)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        self.request.session['pre_arrival'].update({
            'bookings': data.get('data', []),
            'expiry_date': expiry_date,
            'input_reservation_no': self.cleaned_data.get('reservation_no'),
            'input_arrival_date': self.cleaned_data.get('arrival_date').strftime('%Y-%m-%d'),
            'input_last_name': self.cleaned_data.get('last_name'),
        })
        if 'preload' in self.request.session['pre_arrival'] and 'auto_login' in self.request.session['pre_arrival']['preload']:
            self.request.session['pre_arrival']['preload']['auto_login'] = False # set auto login to False


class PreArrivalReservationForm(forms.Form):
    reservation_no = forms.ChoiceField(widget=forms.RadioSelect())

    def __init__(self, request, *args, **kwargs):
        super(PreArrivalReservationForm, self).__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        self.fields['reservation_no'].choices = [(reservation.get('reservationNo', ''), reservation.get('reservationNo', '')) for reservation in self.request.session['pre_arrival'].get('bookings', [])]

    def clean(self):
        super().clean()
        reservation_no = self.cleaned_data.get('reservation_no')

        if not reservation_no:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('No reservation selected.')])
        return self.cleaned_data

    def save_data(self):
        reservation_no = self.cleaned_data.get('reservation_no')
        reservation = next(reservation for reservation in self.request.session['pre_arrival'].get('bookings', []) if reservation.get('reservationNo', '') == reservation_no)
        self.request.session['pre_arrival'].update({'form': reservation})


class PreArrivalPassportForm(forms.Form):
    passport_file = forms.CharField(widget=forms.HiddenInput(), required=False)
    skip_passport = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    
    def __init__(self, request, *args, **kwargs):
        super(PreArrivalPassportForm, self).__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''

    def clean(self):
        super().clean()
        passport_file = self.cleaned_data.get('passport_file')
        skip_passport = self.cleaned_data.get('skip_passport')

        if not skip_passport and not passport_file:
            raise forms.ValidationError(_('No image file selected.'))

        # validate based on `scan_type` (`passport` / `nric`)
        if not skip_passport:
            saved_file = self.save_file()
            response = self.gateway_ocr(saved_file)
            if 'status' not in response and 'message' not in response:
                if response.get('scan_type', 'passport') == 'passport':
                    if response.get('expired', '') == 'false':
                        if utilities.calculate_age(utilities.parse_ocr_date(response.get('date_of_birth', ''))) <= settings.PASSPORT_AGE_LIMIT:
                            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('You must be at least %(age)s years of age to proceed with your registration.') % {'age': settings.PASSPORT_AGE_LIMIT}])
                    else:
                        self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('Your passport has expired, please capture / upload a valid passport photo to proceed')])
            else:
                self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([response.get('message', _('Unknown error'))])

        return self.cleaned_data

    def save_file(self):
        # save passport file using `session_key` as file name
        file_name = self.request.session.session_key +'.png'
        folder_name = os.path.join(settings.BASE_DIR, 'media', 'ocr')
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        saved_file = os.path.join(folder_name, file_name)
        file_data = base64.b64decode(self.cleaned_data.get('passport_file'))
        with open(saved_file, 'wb') as f:
            f.write(file_data)
        return saved_file

    def gateway_ocr(self, saved_file):
        scan_type = 'passport'
        response = gateways.ocr(saved_file, 'passport')
        # if 'status' in response or 'message' in response:
        #     scan_type = 'nric'
        #     response = gateways.ocr(saved_file, 'nric')
        response.update({'scan_type': scan_type})
        return response

    def save_data(self):
        main_guest = next((guest for guest in self.request.session['pre_arrival']['form'].get('guestsList', []) if guest.get('isMainGuest', '0') == '1'), {})
        if self.cleaned_data.get('skip_passport'):
            main_guest.update({'passportImage': ''})
        else:
            file_name = self.request.session.session_key +'.png'
            folder_name = os.path.join(settings.BASE_DIR, 'media', 'ocr')
            saved_file = os.path.join(folder_name, file_name)
            with open(saved_file, 'rb') as image_file:
                file_b64_encoded = base64.b64encode(image_file.read())
            main_guest.update({'passportImage': file_b64_encoded.decode()})
            self.request.session['pre_arrival'].update({'ocr': self.gateway_ocr(saved_file)})


class PreArrivalDetailForm(forms.Form):
    guest_id    = forms.CharField(widget=forms.HiddenInput())
    first_name  = forms.CharField(label=_('First Name'))
    last_name   = forms.CharField(label=_('Last Name'))
    passport_no = forms.CharField(label=_('Passport Number'))
    nationality = CountryField(blank_label=_('[Select Country]')).formfield(label=_('Nationality'))
    birth_date  = forms.DateField(label=_('Date of Birth'))

    def __init__(self, request, *args, **kwargs):
        super(PreArrivalDetailForm, self).__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        # from backend
        main_guest = next((guest for guest in self.request.session['pre_arrival']['form'].get('guestsList', []) if guest.get('isMainGuest', '0') == '1'), {})
        guest_id = main_guest.get('guestID', 0)
        first_name = main_guest.get('firstName', '')
        last_name = main_guest.get('lastName', '')
        passport_no = main_guest.get('passportNo', '')
        nationality = main_guest.get('nationality', 'SG')
        birth_date = main_guest.get('dob', '')
        # from `preload`
        first_name = self.request.session.get('pre_arrival', {}).get('preload', {}).get('first_name', first_name)
        passport_no = self.request.session.get('pre_arrival', {}).get('preload', {}).get('passport_no', passport_no)
        nationality = self.request.session.get('pre_arrival', {}).get('preload', {}).get('nationality', nationality)
        birth_date = self.request.session.get('pre_arrival', {}).get('preload', {}).get('birth_date', birth_date)
        # from `ocr`
        first_name = self.request.session.get('pre_arrival', {}).get('ocr', {}).get('names', first_name)
        passport_no = self.request.session.get('pre_arrival', {}).get('ocr', {}).get('number', passport_no)
        nationality = Country(self.request.session.get('pre_arrival', {}).get('ocr', {}).get('nationality', '')).code or nationality
        birth_date = utilities.parse_ocr_date(self.request.session.get('pre_arrival', {}).get('ocr', {}).get('date_of_birth', '')) or birth_date
        # assign
        self.fields['guest_id'].initial = guest_id
        self.fields['first_name'].initial = first_name
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
            if utilities.calculate_age(birth_date) <= settings.PASSPORT_AGE_LIMIT:
                self._errors['birth_date'] = self.error_class([_('Main guest has to be %(age)s and above.') % {'age': settings.PASSPORT_AGE_LIMIT}])
        return self.cleaned_data

    def save_data(self, extra):
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

        for guest in guests:
            booking_details_guest = next((guest_temp for guest_temp in self.request.session['pre_arrival']['form'].get('guestsList', []) if guest_temp.get('guestID', '') == guest.get('guestID', '')), {})
            if booking_details_guest:
                booking_details_guest.update(guest)
            else:
                self.request.session['pre_arrival']['form']['guestsList'].append(guest)


class PreArrivalDetailExtraForm(forms.Form):
    guest_id = forms.CharField(widget=forms.HiddenInput())
    first_name = forms.CharField(label=_('First Name'))
    last_name = forms.CharField(label=_('Last Name'))
    nationality = CountryField(blank_label='[Select Country]').formfield(label=_('Nationality'))
    passport_no = forms.CharField(label=_('Passport Number'))
    birth_date = forms.DateField(label=_('Date of Birth'))

    def __init__(self, request, *args, **kwargs):
        super(PreArrivalDetailExtraForm, self).__init__(*args, **kwargs)
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

class PreArrivalDetailExtraBaseFormSet(forms.BaseFormSet):
    
    def __init__(self, request, *args, **kwargs):
        super(PreArrivalDetailExtraBaseFormSet, self).__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        # populate additional guests
        additional_guests = []
        for guest in self.request.session['pre_arrival']['form'].get('guestsList', []):
            if guest.get('isMainGuest', '0') == '0':
                additional_guests.append({
                    'guest_id': guest.get('guestID', ''),
                    'first_name': guest.get('firstName', ''),
                    'last_name': guest.get('lastName', ''),
                    'nationality': guest.get('nationality', ''),
                    'passport_no': guest.get('passportNo', ''),
                    'birth_date': guest.get('dob', ''),
                })
        self.extra = 0 # number of empty extra form to be populated
        self.initial = additional_guests

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['request'] = self.request
        return kwargs

    def clean(self):
        super().clean()
        adult, max_adult = 1, int(self.request.session['pre_arrival']['form'].get('adults', 1))
        age_limit = gateways.amp('GET', settings.AMP_CONFIG_URL + str(settings.AMP_CONFIG_ID)).get('pre_arrival_adult_minimum_age', settings.DETAIL_FORM_AGE_LIMIT)
        for form in self.forms:
            if utilities.calculate_age(form.cleaned_data.get('birth_date')) > settings.DETAIL_FORM_AGE_LIMIT:
                adult += 1
        if adult > max_adult:
            self._non_form_errors = self.error_class([_('You have exceeded the number of adults.')])

# extra based on `additional_guests` length which is declared by `total_form_count()`
PreArrivalDetailExtraFormSet = forms.formset_factory(PreArrivalDetailExtraForm, formset=PreArrivalDetailExtraBaseFormSet)


class PreArrivalOtherInfoForm(forms.Form):
    arrival_time        = forms.ChoiceField(label=_('Time of Arrival'))
    special_requests    = forms.CharField(label=_('Special Requests'), required=False)
    email               = forms.EmailField(label=_('Email'))
    is_subscribe        = forms.BooleanField(label=_('Is Subscribe'), required=False)

    def __init__(self, request, *args, **kwargs):
        super(PreArrivalOtherInfoForm, self).__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        self.fields['arrival_time'].choices = utilities.generate_arrival_time()
        self.fields['arrival_time'].initial = utilities.parse_arrival_time(self.request.session['pre_arrival']['form'].get('eta', ''))
        self.fields['special_requests'].initial = self.request.session['pre_arrival']['form'].get('comments', '')
        main_guest = next((guest for guest in self.request.session['pre_arrival']['form'].get('guestsList', []) if guest.get('isMainGuest', '0') == '1'), {})
        self.fields['email'].initial = main_guest.get('email', '')
        self.fields['is_subscribe'].initial = main_guest.get('emailSubscription', '')

    def clean(self):
        super().clean()
        arrival_time = self.cleaned_data.get('arrival_time')
        email = self.cleaned_data.get('email')

        if not arrival_time:
            self._errors['arrival_time'] = self.error_class([_('Enter the required information')])
        if not email:
            self._errors['email'] = self.error_class([_('Enter the required information')])

        return self.cleaned_data

    def save_data(self):
        arrival_time = self.cleaned_data.get('arrival_time')
        special_requests = self.cleaned_data.get('special_requests')
        email = self.cleaned_data.get('email')
        is_subscribe = self.cleaned_data.get('is_subscribe')

        main_guest = next((guest for guest in self.request.session['pre_arrival']['form'].get('guestsList', []) if guest.get('isMainGuest', '0') == '1'), {})
        main_guest.update({
            'email': email,
            'emailSubscription': is_subscribe and '1' or '0',
        })
        self.request.session['pre_arrival']['form'].update({
            'eta': arrival_time + ':00.000',
            'comments': special_requests,
        })

    def gateway_post(self):
        data = self.request.session['pre_arrival']['form']
        data['customerInputNumber'] = self.request.session['pre_arrival'].get('input_reservation_no', '')
        response = gateways.backend_post('/processGuestsPreArrival', data)
        if response.get('success', '') == 'true':
            # get existing reservation from backend
            new_booking_data = {
                'reservation_no': self.request.session['pre_arrival'].get('input_reservation_no', ''),
                'arrival_date': self.request.session['pre_arrival'].get('input_arrival_date', ''),
                'last_name': self.request.session['pre_arrival'].get('input_last_name', ''),
            }
            new_booking_response = gateways.backend_post('/checkBookingsPreArrival', new_booking_data)
            self.request.session['pre_arrival'].update({'bookings': new_booking_response.get('data', [])})
        else:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([response.get('message', _('Unknown error'))])
