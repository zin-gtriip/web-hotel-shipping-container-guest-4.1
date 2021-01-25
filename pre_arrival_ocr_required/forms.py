import os, base64
from django                     import forms
from django.conf                import settings
from django.utils.translation   import gettext, gettext_lazy as _
from django_countries.fields    import Country
from core                       import gateways
from pre_arrival                import utils
from pre_arrival.forms          import *


class PreArrivalLoginForm(PreArrivalLoginForm):
    pass


class PreArrivalTimerExtensionForm(PreArrivalTimerExtensionForm):
    pass


class PreArrivalReservationForm(PreArrivalReservationForm):
    pass


class PreArrivalPassportForm(PreArrivalPassportForm):
    pass


class PreArrivalDetailForm(PreArrivalDetailForm):

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        # store additional guests to temp in session because `guestsList` will be saved with no additional guests
        if not self.request.session['pre_arrival'].get('detail', None):
            prefilled = [guest for guest in self.request.session['pre_arrival']['reservation'].get('guestsList', []) if guest.get('isMainGuest', '0') != '1']
            self.request.session['pre_arrival']['detail'] = {'prefilled_guest_temp': prefilled}
        
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
                'passportImage': form.cleaned_data.get('passport_file'),
            })

        # update with session `guestList` data, in case there are other fields in session `guestList`
        updated_guests = []
        for guest in guests:
            if guest.get('guestID', '0') != '0': # update prefilled guest only
                reservation_guest = next((guest_temp for guest_temp in self.request.session['pre_arrival']['reservation'].get('guestsList', []) if guest_temp.get('guestID', '') == guest.get('guestID', '')), {})
                reservation_guest.update(guest)
                updated_guests.append(reservation_guest)
            else:
                updated_guests.append(guest)
        self.request.session['pre_arrival']['reservation']['guestsList'] = updated_guests # replace with whole new list
        self.request.session['pre_arrival'].pop('ocr', None) # remove ocr after save detail


class PreArrivalDetailExtraForm(PreArrivalDetailExtraForm):
    passport_file = forms.CharField(widget=forms.HiddenInput(), required=False)


class PreArrivalDetailExtraBaseFormSet(PreArrivalDetailExtraBaseFormSet):

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        # populate additional guests that only have passport image
        prefilled = []
        for guest in self.request.session['pre_arrival']['reservation'].get('guestsList', []):
            if guest.get('isMainGuest', '0') == '0' and guest.get('passportImage', ''):
                prefilled.append({
                    'guest_id': guest.get('guestID', ''),
                    'first_name': guest.get('firstName', ''),
                    'last_name': guest.get('lastName', ''),
                    'nationality': guest.get('nationality', ''),
                    'passport_no': guest.get('passportNo', ''),
                    'birth_date': guest.get('dob', ''),
                    'passport_file': guest.get('passportImage', ''),
                })
        self.initial = prefilled

    def clean(self):
        super().clean()
        if self.request.POST.get('form_type', '') == 'submit':
            max_guest = int(self.request.session['pre_arrival']['reservation'].get('adults', 1)) + int(self.request.session['pre_arrival']['reservation'].get('children', 0)) - 1
            if len(self.forms) > max_guest:
                self._non_form_errors = self.error_class([_('You have exceeded the number of additional guests.')])


# initiate formset, for one2many field
PreArrivalDetailExtraFormSet = forms.formset_factory(PreArrivalDetailExtraForm, formset=PreArrivalDetailExtraBaseFormSet)


class PreArrivalExtraPassportForm(forms.Form):
    passport_file = forms.CharField(widget=forms.HiddenInput())
    
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''

    def clean(self):
        super().clean()
        passport_file = self.cleaned_data.get('passport_file')

        if not passport_file:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('No image file selected.')])

        # validate based on `scan_type` (`passport` / `nric`)
        saved_file = self.save_file()
        response = self.gateway_ocr(saved_file)
        if 'status' not in response and 'message' not in response:
            if response.get('scan_type', 'passport') == 'passport':
                if response.get('expired', '') != 'false':
                    self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('Your passport has expired, please capture / upload a valid passport photo to proceed')])
        else:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([response.get('message', _('Unknown error'))])
            
        # remove saved file if fail
        if self._errors:
            os.remove(saved_file)

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
        if 'status' in response or 'message' in response:
            scan_type = 'nric'
            response = gateways.ocr(saved_file, 'nric')
        response['scan_type'] = scan_type
        return response

    def save(self):
        # prepare for ocr
        file_name = self.request.session.session_key +'.png'
        folder_name = os.path.join(settings.BASE_DIR, 'media', 'ocr')
        saved_file = os.path.join(folder_name, file_name)
        with open(saved_file, 'rb') as image_file:
            file_b64_encoded = base64.b64encode(image_file.read())
        ocr = self.gateway_ocr(saved_file)
        os.remove(saved_file) # remove saved file after got response

        # parse dob
        dob = utils.parse_ocr_date(ocr.get('date_of_birth', ''))
        if dob:
            date_format = settings.DATE_INPUT_FORMATS[0] if settings.DATE_INPUT_FORMATS else '%Y-%m-%d'
            dob = dob.strftime(date_format)
        
        # get data from additional guests temp in session
        extra_guest = next((guest for guest in self.request.session['pre_arrival']['detail'].get('prefilled_guest_temp', []) if not guest.get('passportImage', '')), {})
        extra_guest['guestID'] = extra_guest.get('guestID', '0')
        extra_guest['firstName'] = ocr.get('names', '').title()
        extra_guest['lastName'] = ocr.get('surname', '').title()
        extra_guest['nationality'] = Country(ocr.get('nationality', '')).code
        extra_guest['passportNo'] = ocr.get('number', '')
        extra_guest['dob'] = dob
        extra_guest['passportImage'] = file_b64_encoded.decode()
        self.request.session['pre_arrival']['reservation']['guestsList'].append(extra_guest)


class PreArrivalOtherInfoForm(PreArrivalOtherInfoForm):
    pass


class PreArrivalCompleteForm(PreArrivalCompleteForm):
    pass
