import os, base64
from django                     import forms
from django.conf                import settings
from django.utils.translation   import gettext, gettext_lazy as _
from django_countries.fields    import Country
from guest_base                 import gateways


class PreArrivalAllPassportExtraPassportForm(forms.Form):
    passport_file = forms.CharField(widget=forms.HiddenInput())
    
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''

    def clean(self):
        super().clean()
        passport_file = self.cleaned_data.get('passport_file')

        if not passport_file:
            raise forms.ValidationError(_('No image file selected.'))

        # validate based on `scan_type` (`passport` / `nric`)
        saved_file = self.save_file()
        response = self.gateway_ocr(saved_file)
        if 'status' not in response and 'message' not in response:
            if response.get('scan_type', 'passport') == 'passport':
                if response.get('expired', '') != 'false':
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
        response['scan_type'] = scan_type
        return response

    def save(self):
        file_name = self.request.session.session_key +'.png'
        folder_name = os.path.join(settings.BASE_DIR, 'media', 'ocr')
        saved_file = os.path.join(folder_name, file_name)
        with open(saved_file, 'rb') as image_file:
            file_b64_encoded = base64.b64encode(image_file.read())
        ocr = self.gateway_ocr(saved_file)
        extra_guest = {}
        extra_guest['guestID'] = ''
        extra_guest['firstName'] = ocr.get('names', '')
        extra_guest['lastName'] = ocr.get('surname', '')
        extra_guest['nationality'] = Country(ocr.get('nationality', '')).code
        extra_guest['passportNo'] = ocr.get('number', '')
        extra_guest['dob'] = ocr.get('date_of_birth', '')
        extra_guest['passportImage'] = file_b64_encoded.decode()
        self.request.session['pre_arrival']['reservation']['guestsList'].append(extra_guest)
