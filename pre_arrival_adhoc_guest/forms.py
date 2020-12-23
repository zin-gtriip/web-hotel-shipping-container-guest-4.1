from django                         import forms
from pre_arrival.forms              import PreArrivalOtherInfoForm
from pre_arrival_all_passport.forms import *


class PreArrivalDetailExtraForm(PreArrivalDetailExtraForm):
    has_record = forms.BooleanField(widget=forms.HiddenInput(), required=False)


class PreArrivalDetailExtraBaseFormSet(PreArrivalDetailExtraBaseFormSet):

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        # populate additional guests that only have passport image
        prefilled = []
        for guest in self.request.session['pre_arrival']['reservation'].get('guestsList', []):
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
PreArrivalDetailExtraFormSet = forms.formset_factory(PreArrivalDetailExtraForm, formset=PreArrivalDetailExtraBaseFormSet)


class PreArrivalAllPassportExtraPassportForm(PreArrivalAllPassportExtraPassportForm):
    
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
        dob = utilities.parse_ocr_date(ocr.get('date_of_birth', ''))
        if dob:
            date_format = settings.DATE_INPUT_FORMATS[0] if settings.DATE_INPUT_FORMATS else '%Y-%m-%d'
            dob = dob.strftime(date_format)
        
        # get data from additional guests temp in session, check if first login from `passportImage`, if relogin from `hasLocalRecord`
        extra_guest = next((guest for guest in self.request.session['pre_arrival']['detail'].get('prefilled_guest_temp', []) if not guest.get('passportImage', '') and guest.get('hasLocalRecord', '0') == '0'), {})
        extra_guest['guestID'] = extra_guest.get('guestID', '0')
        extra_guest['firstName'] = ocr.get('names', '').title()
        extra_guest['lastName'] = ocr.get('surname', '').title()
        extra_guest['nationality'] = Country(ocr.get('nationality', '')).code
        extra_guest['passportNo'] = ocr.get('number', '')
        extra_guest['dob'] = dob
        extra_guest['passportImage'] = file_b64_encoded.decode()
        self.request.session['pre_arrival']['reservation']['guestsList'].append(extra_guest)


class PreArrivalOtherInfoForm(PreArrivalOtherInfoForm):
    
    def gateway_post(self):
        super().gateway_post()
        registered_reservation_no = self.request.session['pre_arrival'].get('reservation', {}).get('reservationNo', '')
        registered_reservation = next((reservation for reservation in self.request.session['pre_arrival']['bookings'] if reservation.get('reservationNo', '') == registered_reservation_no), {})
        if registered_reservation:
            self.request.session['pre_arrival']['bookings'].remove(registered_reservation) # remove just registered reservation to prevent "Next Registration" displayed on complete page
