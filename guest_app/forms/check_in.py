import os
import base64
from django                     import forms
from django.utils.translation   import gettext, gettext_lazy as _
from django.core.cache          import caches
from django.conf                import settings
from guest_app                  import gateways, utilities, samples

CACHE = caches['default']

class CheckInLoginForm(forms.Form):
    reservation_no  = forms.CharField(label=_('Reservation Number'))
    arrival_date    = forms.DateField(label=_('Arrival Date'))
    last_name       = forms.CharField(label=_('Last Name'))

    def __init__(self, request, *args, **kwargs):
        super(CheckInLoginForm, self).__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''

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
        # validate from backend
        if reservation_no and arrival_date and last_name:
            data = {
                'confirmation_number': reservation_no,
                'arrival_date': arrival_date,
                'last_name': last_name,
            }
            response = samples.get_data(data) #gateways.post('/booking/get_booking', data)
            CACHE.set('checkin_login_response', response) # save to cache to be used after form is valid

            if response.get('status', '') != 'success':
                raise forms.ValidationError(response.get('message', _('Unknown error')))
        return self.cleaned_data

    def set_session(self):
        self.request.session.flush()
        self.request.session.create() # for creating `session_key`
        self.request.session.set_expiry(settings.CHECKIN_SESSION_AGE)
        self.request.session['checkin_data'] = CACHE.get('checkin_login_response', {})
        CACHE.clear()


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

        if not skip_passport:
            # validate passport_file not empty
            if not passport_file:
                raise forms.ValidationError(_('No image file selected.'))
            
            # save passport file using `session_key` as file name
            file_name = self.request.session.session_key +'.png'
            folder_name = os.path.join(settings.BASE_DIR, 'upload')
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)
            saved_file = os.path.join(folder_name, file_name)
            file_data = base64.b64decode(passport_file)
            with open(saved_file, 'wb') as f:
                f.write(file_data)

            # send to ocr scanning
            scan_type = 'passport'
            response = {'status': 'success', 'expired': 'false', 'date_of_birth': '20/10/1990'} # gateways.ocr(saved_file, 'passport')
            if response.get('status', '') != 'success':
                scan_type = 'nric'
                response = gateways.ocr(saved_file, 'nric')

            # validation based on `scan_type` (`passport` / `nric`)
            if scan_type == 'passport':
                if response.get('expired', '') == 'false':
                    if utilities.calculate_age(response.get('date_of_birth', '')) <= settings.PASSPORT_AGE_LIMIT:
                        raise forms.ValidationError(_('You must be at least %(age)s years of age to proceed with your registration.') % {'age': settings.PASSPORT_AGE_LIMIT})
                else:
                    raise forms.ValidationError(_('Your passport has expired, please capture / upload a valid passport photo to proceed'))

        return self.cleaned_data


class CheckInDetailForm(forms.Form):

    def __init__(self, request, *args, **kwargs):
        super(CheckInDetailForm, self).__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
