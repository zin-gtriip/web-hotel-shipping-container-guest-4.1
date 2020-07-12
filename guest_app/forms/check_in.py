import os
import base64
from django                     import forms
from django.utils.translation   import gettext, gettext_lazy as _
from django.conf                import settings
from django_countries.fields    import Country, CountryField
from guest_app                  import gateways, utilities, samples

class CheckInLoginForm(forms.Form):
    reservation_no  = forms.CharField(label=_('Reservation Number'))
    arrival_date    = forms.DateField(label=_('Arrival Date'))
    last_name       = forms.CharField(label=_('Last Name'))

    def __init__(self, request, *args, **kwargs):
        super(CheckInLoginForm, self).__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        if 'check_in_data' in self.request.session:
            self.fields['reservation_no'].initial = self.request.session['check_in_data'].get('reservation_no')
            self.fields['arrival_date'].initial = self.request.session['check_in_data'].get('arrival_date')
            self.fields['last_name'].initial = self.request.session['check_in_data'].get('last_name')

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
        return self.cleaned_data

    def gateway_post(self):
        data = {
            'confirmation_number': self.cleaned_data.get('reservation_no'),
            'arrival_date': self.cleaned_data.get('arrival_date'),
            'last_name': self.cleaned_data.get('last_name'),
        }
        response = samples.get_data(data) #gateways.post('/booking/get_booking', data)
        if response.get('status', '') != 'success':
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([response['message'] or _('Unknown error')])
        return response
    
    def set_session(self, data):
        self.request.session['check_in_details'] = {'booking_details': data}
        self.request.session.set_expiry(settings.CHECK_IN_SESSION_AGE)
        if 'check_in_data' in self.request.session and 'auto_login' in self.request.session['check_in_data']:
            self.request.session['check_in_data']['auto_login'] = False # set auto login to False


class CheckInReservationForm(forms.Form):
    reservation = forms.ChoiceField(widget=forms.RadioSelect())

    def __init__(self, request, *args, **kwargs):
        super(CheckInReservationForm, self).__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        self.fields['reservation'].choices = [(reservation.get('identifier', ''), reservation.get('room_type', '')) for reservation in self.request.session['check_in_details']['booking_details'].get('reservations', [])]

    def clean(self):
        super().clean()
        reservation = self.cleaned_data.get('reservation')

        if not reservation:
            raise forms.ValidationError(_('No reservation selected.'))
        return self.cleaned_data

    def set_session(self):
        reservation = self.cleaned_data.get('reservation')
        self.request.session['check_in_details'].update({'form': {'reservation': reservation}})
        self.request.session.save()


class CheckInPassportForm(forms.Form):
    passport_file = forms.CharField(widget=forms.HiddenInput(), required=False)
    skip_passport = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    
    def __init__(self, request, *args, **kwargs):
        super(CheckInPassportForm, self).__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''

    def clean(self):
        super().clean()
        passport_file = self.cleaned_data.get('passport_file')
        skip_passport = self.cleaned_data.get('skip_passport')

        if not skip_passport and not passport_file:
            raise forms.ValidationError(_('No image file selected.'))
        return self.cleaned_data

    def gateway_ocr(self):
        if self.cleaned_data.get('skip_passport'):
            return

        # save passport file using `session_key` as file name
        file_name = self.request.session.session_key +'.png'
        folder_name = os.path.join(settings.BASE_DIR, 'media', 'ocr')
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        saved_file = os.path.join(folder_name, file_name)
        file_data = base64.b64decode(self.cleaned_data.get('passport_file'))
        with open(saved_file, 'wb') as f:
            f.write(file_data)

        # send to ocr scanning
        scan_type = 'passport'
        response = gateways.ocr(saved_file, 'passport')
        # if 'status' in response or 'message' in response:
        #     scan_type = 'nric'
        #     response = gateways.ocr(saved_file, 'nric')

        # validation based on `scan_type` (`passport` / `nric`)
        if 'status' not in response and 'message' not in response:
            if scan_type == 'passport':
                if response.get('expired', '') == 'false':
                    if utilities.calculate_age(utilities.parse_ocr_date(response.get('date_of_birth', ''))) <= settings.PASSPORT_AGE_LIMIT:
                        self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('You must be at least %(age)s years of age to proceed with your registration.') % {'age': settings.PASSPORT_AGE_LIMIT}])
                else:
                    self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('Your passport has expired, please capture / upload a valid passport photo to proceed')])
        else:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([response['message'] or _('Unknown error')])
        return response

    def set_session(self, data):
        if data is not None:
            self.request.session['check_in_details'].update({'passport_ocr': data})
            self.request.session.save()


class CheckInDetailForm(forms.Form):
    first_name = forms.CharField(label=_('First Name'))
    last_name = forms.CharField(label=_('Last Name'))
    passport_no = forms.CharField(label=_('Passport Number'))
    nationality = CountryField(blank_label=_('[Select Country]')).formfield(label=_('Nationality'))
    birth_date = forms.DateField(label=_('Date of Birth'))

    def __init__(self, request, *args, **kwargs):
        super(CheckInDetailForm, self).__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''

        first_name = self.request.session['check_in_details']['booking_details'].get('first_name', '')
        last_name = self.request.session['check_in_details']['booking_details'].get('last_name', '')
        passport_no = self.request.session['check_in_details']['booking_details'].get('passport_no', '')
        nationality = self.request.session['check_in_details']['booking_details'].get('nationality', 'SG')
        birth_date = self.request.session['check_in_details']['booking_details'].get('birth_date', '')
        if 'check_in_data' in self.request.session:
            first_name = self.request.session['check_in_data'].get('first_name', first_name)
            passport_no = self.request.session['check_in_data'].get('passport_no', passport_no)
            nationality = self.request.session['check_in_data'].get('nationality', nationality)
            birth_date = self.request.session['check_in_data'].get('birth_date', birth_date)
        if 'check_in_details' in self.request.session and 'passport_ocr' in self.request.session['check_in_details']:
            first_name = self.request.session['check_in_details']['passport_ocr'].get('names', first_name)
            passport_no = self.request.session['check_in_details']['passport_ocr'].get('number', passport_no)
            nationality = Country(self.request.session['check_in_details']['passport_ocr'].get('nationality', '')).code or nationality
            birth_date = utilities.parse_ocr_date(self.request.session['check_in_details']['passport_ocr'].get('date_of_birth', '')) or birth_date
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
                self._errors['birth_date'] = self.error_class([_('You must be at least %(age)s years of age to proceed with your registration.') % {'age': settings.PASSPORT_AGE_LIMIT}])
        return self.cleaned_data


class CheckInDetailExtraForm(forms.Form):
    is_valid = forms.BooleanField(widget=forms.HiddenInput())
    first_name = forms.CharField(label=_('First Name'))
    last_name = forms.CharField(label=_('Last Name'))
    nationality = CountryField(blank_label='[Select Country]').formfield(label=_('Nationality'))
    passport_no = forms.CharField(label=_('Passport Number'))
    birth_date = forms.DateField(label=_('Date of Birth'))

    def clean(self):
        super().clean()
        is_valid = self.cleaned_data.get('is_valid')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        nationality = self.cleaned_data.get('nationality')
        passport_no = self.cleaned_data.get('passport_no')
        birth_date = self.cleaned_data.get('birth_date')

        if is_valid and not first_name:
            self._errors['first_name'] = self.error_class([_('Enter the required information')])
        if is_valid and not last_name:
            self._errors['last_name'] = self.error_class([_('Enter the required information')])
        if is_valid and not nationality:
            self._errors['nationality'] = self.error_class([_('Enter the required information')])
        if is_valid and not passport_no:
            self._errors['passport_no'] = self.error_class([_('Enter the required information')])
        if is_valid and not birth_date:
            self._errors['birth_date'] = self.error_class([_('Enter the required information')])
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(CheckInDetailExtraForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
    
CheckInDetailExtraFormSet = forms.formset_factory(CheckInDetailExtraForm, extra=1)
