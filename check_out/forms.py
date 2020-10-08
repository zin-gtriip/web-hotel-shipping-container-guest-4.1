from django                     import forms
from django.utils.translation   import gettext, gettext_lazy as _
from guest_base                 import gateways
from .                          import samples

class CheckOutLoginForm(forms.Form):
    reservation_no  = forms.CharField(label=_('Reservation Number'))
    room_no         = forms.CharField(label=_('Room Number'))

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        self.fields['reservation_no'].initial = self.request.session.get('check_out', {}).get('preload', {}).get('reservation_no')
        self.fields['room_no'].initial = self.request.session.get('check_out', {}).get('preload', {}).get('room_no')

    def clean(self):
        super().clean()
        reservation_no = self.cleaned_data.get('reservation_no')
        room_no = self.cleaned_data.get('room_no')

        # validate required field
        if not reservation_no:
            self._errors['reservation_no'] = self.error_class([_('Enter the required information')])
        if not room_no:
            self._errors['room_no'] = self.error_class([_('Enter the required information')])

        # validate to backend
        response = self.gateway_post()
        if response.get('status_code', '') != 500:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('We were unable to retrieve your reservation from our database.')])
        
        return self.cleaned_data

    def gateway_post(self):
        data = {}
        data['reservation_no'] = self.cleaned_data.get('reservation_no')
        data['room_no'] = self.cleaned_data.get('room_no')
        return gateways.backend_post('/signInForCheckOut', data)
    
    def save(self):
        data = self.gateway_post()
        if not 'check_out' in self.request.session:
            self.request.session['check_out'] = {}
        self.request.session['check_out']['bills'] = data.get('data', [])
        self.request.session['check_out']['input_reservation_no'] = self.cleaned_data.get('reservation_no')
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
        reservations_no = [reservation.get('reservation_no', '') for reservation in self.request.session['check_out'].get('bills', [])]
        self.fields['reservation_no'].choices = [('all', 'All Guests')]
        for reservation in self.request.session['check_out'].get('bills', []):
            self.fields['reservation_no'].choices.append((reservation.get('reservation_no', ''), reservation.get('first_name', '') + ' ' + reservation.get('last_name', '')))
        # set initial
        self.fields['reservation_no'].initial = self.instance.get('id', '')

    def clean(self):
        reservation_no = self.cleaned_data.get('reservation_no', '')
        if not reservation_no:
            self._errors['reservation_no'] = self.error_class([_('Enter the required information')])
        return self.cleaned_data

    def gateway_post(self):
        reservation_info = self.instance.get('reservation_info', [])
        data = {'reservation_info': reservation_info}
        return gateways.backend_post('/postCheckOut', data)

    def save(self):
        response = self.gateway_post()
        if response.get('status_code', '') != 500:
            raise Exception(response.get('message', _('Unknown error')))
        return self.instance
