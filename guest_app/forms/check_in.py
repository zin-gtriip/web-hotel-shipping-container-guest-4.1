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

        # validate to backend
        response = self.gateway_post()
        if response.get('status', '') != 'success':
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([response['message'] or _('Unknown error')])

        return self.cleaned_data

    def gateway_post(self):
        data = {
            'confirmation_number': self.cleaned_data.get('reservation_no'),
            'arrival_date': self.cleaned_data.get('arrival_date'),
            'last_name': self.cleaned_data.get('last_name'),
        }
        return samples.get_data(data) #gateways.post('/booking/get_booking', data)
    
    def save_data(self):
        data = self.gateway_post()
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

    def save_data(self):
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
        if self.cleaned_data.get('skip_passport'):
            self.request.session['check_in_details']['form'].update({'passport_image': ''})
        else:
            file_name = self.request.session.session_key +'.png'
            folder_name = os.path.join(settings.BASE_DIR, 'media', 'ocr')
            saved_file = os.path.join(folder_name, file_name)
            self.request.session['check_in_details']['form'].update({'passport_image': saved_file})
            self.request.session['check_in_details'].update({'ocr_details': self.gateway_ocr(saved_file)})
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
        if 'check_in_details' in self.request.session and 'ocr_details' in self.request.session['check_in_details']:
            first_name = self.request.session['check_in_details']['ocr_details'].get('names', first_name)
            passport_no = self.request.session['check_in_details']['ocr_details'].get('number', passport_no)
            nationality = Country(self.request.session['check_in_details']['ocr_details'].get('nationality', '')).code or nationality
            birth_date = utilities.parse_ocr_date(self.request.session['check_in_details']['ocr_details'].get('date_of_birth', '')) or birth_date
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
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        nationality = self.cleaned_data.get('nationality')
        passport_no = self.cleaned_data.get('passport_no')
        birth_date = self.cleaned_data.get('birth_date').strftime('%Y-%m-%d')
        additional_guests = []

        for form in extra.forms:
            additional_guests.append({
                'first_name': form.cleaned_data.get('first_name'),
                'last_name': form.cleaned_data.get('last_name'),
                'nationality': form.cleaned_data.get('nationality'),
                'passport_no': form.cleaned_data.get('passport_no'),
                'birth_date': form.cleaned_data.get('birth_date').strftime('%Y-%m-%d'),
            })

        self.request.session['check_in_details']['form'].update({
            'first_name': first_name,
            'last_name': last_name,
            'nationality': nationality,
            'passport_no': passport_no,
            'birth_date': birth_date,
            'additional_guests': additional_guests,
        })
        self.request.session.save()


class CheckInDetailExtraForm(forms.Form):
    first_name = forms.CharField(label=_('First Name'))
    last_name = forms.CharField(label=_('Last Name'))
    nationality = CountryField(blank_label='[Select Country]').formfield(label=_('Nationality'))
    passport_no = forms.CharField(label=_('Passport Number'))
    birth_date = forms.DateField(label=_('Date of Birth'))

    def __init__(self, request, *args, **kwargs):
        super(CheckInDetailExtraForm, self).__init__(*args, **kwargs)
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

class CheckInDetailExtraBaseFormSet(forms.BaseFormSet):
    
    def __init__(self, request, *args, **kwargs):
        super(CheckInDetailExtraBaseFormSet, self).__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['request']= self.request
        return kwargs

    def clean(self):
        super().clean()
        adult, max_adult = 1, int(self.request.session['check_in_details']['booking_details'].get('adult_number', 0))
        for form in self.forms:
            if utilities.calculate_age(form.cleaned_data.get('birth_date')) > settings.DETAIL_FORM_AGE_LIMIT:
                adult += 1
        if adult > max_adult:
            self._non_form_errors = self.error_class([_('You have exceeded the number of adults.')])
    
CheckInDetailExtraFormSet = forms.formset_factory(CheckInDetailExtraForm, formset=CheckInDetailExtraBaseFormSet, extra=1)


class CheckInOtherInfoForm(forms.Form):
    arrival_time = forms.ChoiceField(label=_('Time of Arrival'))
    special_requests = forms.CharField(label=_('Special Requests'), required=False)
    email = forms.EmailField(label=_('Email'))
    is_subscribe = forms.BooleanField(label=_('Is Subscribe'), required=False)

    def __init__(self, request, *args, **kwargs):
        super(CheckInOtherInfoForm, self).__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        self.fields['arrival_time'].choices = utilities.generate_time_arrival()

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

        self.request.session['check_in_details']['form'].update({
            'arrival_time': arrival_time,
            'special_requests': special_requests,
            'email': email,
            'is_subscribe': is_subscribe,
        })
        self.request.session.save()

    def gateway_post(self):
        data = self.request.session['check_in_details']['form']
        response = samples.send_data(data) #gateways.post('/booking/submit_details', data)
        if response.get('status', '') == 'success':
            self.request.session.set_expiry(settings.SESSION_COOKIE_AGE) # reset session expiry time
        else:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([response.get('message', _('Unknown error'))])
