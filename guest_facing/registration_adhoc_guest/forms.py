import os, base64
from django                                         import forms
from django.conf                                    import settings
from django.utils.translation                       import gettext, gettext_lazy as _
from django_countries.fields                        import Country
from guest_facing.registration                      import utils
from guest_facing.registration_ocr_required.forms   import *


class RegistrationLoginForm(RegistrationLoginForm):
    pass


class RegistrationTimerExtensionForm(RegistrationTimerExtensionForm):
    pass


class RegistrationReservationForm(RegistrationReservationForm):
    pass


class RegistrationPassportForm(RegistrationPassportForm):
    pass


class RegistrationDetailForm(RegistrationDetailForm):
    pass


class RegistrationDetailExtraForm(RegistrationDetailExtraForm):
    has_record = forms.BooleanField(widget=forms.HiddenInput(), required=False)


class RegistrationDetailExtraBaseFormSet(RegistrationDetailExtraBaseFormSet):

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        # populate additional guests that only have passport image
        prefilled = []
        for guest in self.request.session['registration']['reservation'].get('guestsList', []):
            if guest.get('isMainGuest', '0') == '0' and (guest.get('passportImage', '') or guest.get('hasLocalRecord', '0') == '1'):
                prefilled.append({
                    'guest_id': guest.get('guestID', ''),
                    'has_record': guest.get('hasLocalRecord', '0'),
                    'first_name': guest.get('firstName', ''),
                    'last_name': guest.get('lastName', ''),
                    'nationality': guest.get('nationality', ''),
                    'passport_no': guest.get('passportNo', ''),
                    'birth_date': guest.get('dob', ''),
                    'passport_file': guest.get('passportImage', ''),
                })
        self.initial = prefilled


# initiate formset, for one2many field
RegistrationDetailExtraFormSet = forms.formset_factory(RegistrationDetailExtraForm, formset=RegistrationDetailExtraBaseFormSet)


class RegistrationExtraPassportForm(RegistrationExtraPassportForm):
    
    def save(self):
        # prepare for ocr
        file_name = self.request.session.session_key +'.png'
        folder_name = os.path.join(settings.BASE_DIR, 'media', 'ocr')
        saved_file = os.path.join(folder_name, file_name)
        with open(saved_file, 'rb') as image_file:
            file_b64_encoded = base64.b64encode(image_file.read())
        ocr = self.response
        os.remove(saved_file) # remove saved file after got response

        # parse dob
        dob = utils.parse_ocr_date(ocr.get('date_of_birth', ''))
        if dob:
            date_format = settings.DATE_INPUT_FORMATS[0] if settings.DATE_INPUT_FORMATS else '%Y-%m-%d'
            dob = dob.strftime(date_format)
        
        # get data from additional guests temp in session, check if first login from `passportImage`, if relogin from `hasLocalRecord`
        extra_guest = next((guest for guest in self.request.session['registration']['detail'].get('prefilled_guest_temp', []) if not guest.get('passportImage', '') and guest.get('hasLocalRecord', '0') == '0'), {})
        extra_guest['guestID'] = extra_guest.get('guestID', '0')
        extra_guest['firstName'] = ocr.get('names', '').title()
        extra_guest['lastName'] = ocr.get('surname', '').title()
        extra_guest['nationality'] = Country(ocr.get('nationality', '')).code
        extra_guest['passportNo'] = ocr.get('number', '')
        extra_guest['dob'] = dob
        extra_guest['passportImage'] = file_b64_encoded.decode()
        self.request.session['registration']['reservation']['guestsList'].append(extra_guest)


class RegistrationOtherInfoForm(RegistrationOtherInfoForm):
    
    def gateway_post(self):
        super().gateway_post()
        registered_reservation_no = self.request.session['registration'].get('reservation', {}).get('reservationNo', '')
        registered_reservation = next((reservation for reservation in self.request.session['registration']['bookings'] if reservation.get('reservationNo', '') == registered_reservation_no), {})
        if registered_reservation:
            self.request.session['registration']['bookings'].remove(registered_reservation) # remove just registered reservation to prevent "Next Registration" displayed on complete page


class RegistrationCompleteForm(RegistrationCompleteForm):
    pass
