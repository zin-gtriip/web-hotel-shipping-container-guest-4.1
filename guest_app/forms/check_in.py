import os
import base64
from django                     import forms
from django.utils.translation   import gettext, gettext_lazy as _
from django.conf                import settings
from guest_app                  import gateways, utilities, samples

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
        self.request.session.flush()
        self.request.session.create() # for creating `session_key`
        self.request.session.set_expiry(settings.CHECK_IN_SESSION_AGE)
        self.request.session['check_in_data'] = {'booking_details': data}


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
        folder_name = os.path.join(settings.BASE_DIR, 'upload')
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        saved_file = os.path.join(folder_name, file_name)
        file_data = base64.b64decode(self.cleaned_data.get('passport_file'))
        with open(saved_file, 'wb') as f:
            f.write(file_data)

        # send to ocr scanning
        scan_type = 'passport'
        response = samples.ocr_data # gateways.ocr(saved_file, 'passport')
        if 'status' in response or 'message' in response:
            scan_type = 'nric'
            response = gateways.ocr(saved_file, 'nric')

        # validation based on `scan_type` (`passport` / `nric`)
        if 'status' not in response and 'message' not in response:
            if scan_type == 'passport':
                if response.get('expired', '') == 'false':
                    if utilities.calculate_age(response.get('date_of_birth', '')) <= settings.PASSPORT_AGE_LIMIT:
                        self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('You must be at least %(age)s years of age to proceed with your registration.') % {'age': settings.PASSPORT_AGE_LIMIT}])
                else:
                    self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('Your passport has expired, please capture / upload a valid passport photo to proceed')])
        else:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([response['message'] or _('Unknown error')])
        return response

    def set_session(self, data):
        if data is not None:
            self.request.session['check_in_data'].update({'passport_ocr': data})
            self.request.session.save()


class CheckInDetailForm(forms.Form):

    def __init__(self, request, *args, **kwargs):
        super(CheckInDetailForm, self).__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
