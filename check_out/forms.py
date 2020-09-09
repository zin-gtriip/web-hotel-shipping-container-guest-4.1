from django                     import forms
from django.utils.translation   import gettext, gettext_lazy as _
from .                          import samples

class CheckOutLoginForm(forms.Form):
    reservation_no  = forms.CharField(label=_('Reservation Number'))
    room_no         = forms.CharField(label=_('Room Number'))

    SUCCESS_CODE    = 500

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
        if response.get('overall_status', '') != self.SUCCESS_CODE:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([self.ERROR_MESSAGES.get(response.get('overall_status', 0), _('Unknown error'))])
        
        return self.cleaned_data

    def gateway_post(self):
        data = {
            'reservation_no': self.cleaned_data.get('reservation_no'),
            'room_no': self.cleaned_data.get('room_no'),
        }
        return samples.check_out_data #gateways.backend_post('/checkBookingsPreArrival', data)
    
    def save_data(self):
        data = self.gateway_post()
        if not 'check_out' in self.request.session:
            self.request.session['check_out'] = {}
        self.request.session['check_out'].update({
            'bills': data.get('data', []),
        })
        if 'preload' in self.request.session['check_out'] and 'auto_login' in self.request.session['pre_arrival']['preload']:
            self.request.session['check_out']['preload']['auto_login'] = False # set auto login to False
