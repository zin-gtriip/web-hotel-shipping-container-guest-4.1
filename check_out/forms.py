from django                     import forms
from django.utils.translation   import gettext, gettext_lazy as _
from .                          import samples

class CheckOutLoginForm(forms.Form):
    room_no     = forms.CharField(label=_('Room Number'))
    last_name   = forms.CharField(label=_('Last Name'))

    SUCCESS_CODE    = 500

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        self.fields['room_no'].initial = self.request.session.get('check_out', {}).get('preload', {}).get('room_no')
        self.fields['last_name'].initial = self.request.session.get('check_out', {}).get('preload', {}).get('last_name')

    def clean(self):
        super().clean()
        room_no = self.cleaned_data.get('room_no')
        last_name = self.cleaned_data.get('last_name')

        # validate required field
        if not room_no:
            self._errors['room_no'] = self.error_class([_('Enter the required information')])
        if not last_name:
            self._errors['last_name'] = self.error_class([_('Enter the required information')])

        # validate to backend
        response = self.gateway_post()
        if response.get('overall_status', '') != self.SUCCESS_CODE:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([self.ERROR_MESSAGES.get(response.get('overall_status', 0), _('Unknown error'))])
        
        return self.cleaned_data

    def gateway_post(self):
        data = {
            'room_no': self.cleaned_data.get('reservation_no'),
            'last_name': self.cleaned_data.get('last_name'),
        }
        print(data)
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
