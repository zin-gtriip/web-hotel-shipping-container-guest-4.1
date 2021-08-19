from django                     import forms
from django.conf                import settings
from django.utils.translation   import gettext, gettext_lazy as _
from captcha                    import fields as captchaField, widgets as captchaWidget
from guest_facing.core          import gateways


class CheckOutLoginForm(forms.Form):
    reservation_no  = forms.CharField(label=_('Reservation Number'), required=False)
    last_name       = forms.CharField(label=_('Last Name'), required=False)
    room_no         = forms.CharField(label=_('Room Number'))

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        self.response = {}
        self.fields['reservation_no'].initial = self.request.session.get('check_out', {}).get('preload', {}).get('reservation_no')
        self.fields['last_name'].initial = self.request.session.get('check_out', {}).get('preload', {}).get('last_name')
        self.fields['room_no'].initial = self.request.session.get('check_out', {}).get('preload', {}).get('room_no')
        # add `recaptcha` when not auto login
        if not self.request.session.get('check_out', {}).get('preload', {}).get('auto_login', 0):
            self.fields['recaptcha'] = captchaField.ReCaptchaField(widget=captchaWidget.ReCaptchaV2Invisible)

    def clean(self):
        super().clean()
        reservation_no = self.cleaned_data.get('reservation_no')
        last_name = self.cleaned_data.get('last_name')
        room_no = self.cleaned_data.get('room_no')
        recaptcha = self.cleaned_data.get('recaptcha')

        # validate required field
        if not reservation_no and not last_name:
            self._errors['reservation_no'] = self.error_class([_('Enter the required information')])
            self._errors['last_name'] = self.error_class([_('Enter the required information')])
        if not room_no:
            self._errors['room_no'] = self.error_class([_('Enter the required information')])
        # validate `recaptcha` when not auto login
        if not self.request.session.get('check_out', {}).get('preload', {}).get('auto_login', 0) and not recaptcha:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class(['recaptcha'])
        # validate to backend
        if not self.errors:
            response = self.gateway_post()
            if response.get('statusCode', '') != '5011':
                self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([response.get('status_code', 0)])
        return self.cleaned_data

    def gateway_post(self):
        data = {}
        data['reservationNo'] = self.cleaned_data.get('reservation_no', None)
        data['lastName'] = self.cleaned_data.get('last_name', None)
        data['roomNo'] = self.cleaned_data.get('room_no')
        self.response = gateways.guest_endpoint('post', '/signInCheckOut', self.request.session.get('property_id', ''), data)
        return self.response
    
    def save(self):
        data = self.response
        preload_data = dict(self.request.session.get('check_out', {}).get('preload', {})) # get and store preload because session will be cleared
        self.request.session['check_out'] = {} # clear session data
        self.request.session['check_out']['preload'] = preload_data # restore preload data
        self.request.session['check_out']['bookings'] = data.get('data', {}).get('data', [])
        self.request.session['check_out']['bills'] = data.get('data', {}).get('data', [])
        self.request.session['check_out']['input_reservation_no'] = self.cleaned_data.get('reservation_no')
        self.request.session['check_out']['input_last_name'] = self.cleaned_data.get('last_name')
        self.request.session['check_out']['input_room_no'] = self.cleaned_data.get('room_no')
        if 'preload' in self.request.session['check_out'] and 'auto_login' in self.request.session['check_out']['preload']:
            self.request.session['check_out']['preload']['auto_login'] = 0 # set auto login to False


class CheckOutBillForm(forms.Form):
    reservation_no  = forms.ChoiceField(label=_('Reservation Number'))

    def __init__(self, instance, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = instance
        self.request = request
        self.label_suffix = ''
        # populate choices
        self.fields['reservation_no'].choices = []
        for reservation in self.request.session['check_out'].get('bills', []):
            self.fields['reservation_no'].choices.append((reservation.get('pmsNo', ''), reservation.get('firstName', '') + ' ' + reservation.get('lastName', '')))
        # set initial
        self.fields['reservation_no'].initial = self.instance.get('id', '')

    def clean(self):
        super().clean()
        reservation_no = self.cleaned_data.get('reservation_no', '')
        
        if not reservation_no:
            self._errors['reservation_no'] = self.error_class([_('Enter the required information')])
        return self.cleaned_data

    def gateway_post(self):
        reservation_info = self.instance.get('reservationInfo', [])
        data = {'reservationInfo': reservation_info}
        return gateways.guest_endpoint('post', '/postCheckOut', self.request.session.get('property_id', ''), data)

    def save(self):
        response = self.gateway_post()
        if response.get('statusCode', '') == '5013':
            # get existing reservation from backend
            if response.get('reservationNoLeft', []):
                new_guest_data = {}
                new_guest_data['reservationNo'] = next(iter(response.get('reservationNoLeft', [])), '')
                new_guest_data['lastName'] = ''
                new_guest_data['roomNo'] = self.request.session['check_out'].get('input_room_no')
                new_guest_response = gateways.guest_endpoint('post', '/signInCheckOut', self.request.session.get('property_id', ''), new_guest_data)
                self.request.session['check_out']['bills'] = new_guest_response.get('data', {}).get('data', [])
                if not new_guest_response.get('data', {}).get('data', []):
                    self.request.session['check_out']['complete'] = True
            else:
                self.request.session['check_out']['complete'] = True
        else:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([response.get('message', _('Unknown error'))])
        return self.instance
