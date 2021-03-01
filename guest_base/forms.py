from django                     import forms
from django.conf                import settings
from django.utils.translation   import gettext, gettext_lazy as _


class GuestBasePropertyForm(forms.Form):
    property_id = forms.ChoiceField(widget=forms.RadioSelect())

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''
        self.fields['property_id'].choices = [(prop.get('id', ''), prop.get('description', '')) for prop in settings.GUEST_ENDPOINT or []]

    def clean(self):
        super().clean()
        property_id = self.cleaned_data.get('property_id')
        if not property_id:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('No property selected.')])
        else:
            prop_data = next((prop for prop in settings.GUEST_ENDPOINT or [] if prop.get('id', '') == property_id), None)
            if not prop_data:
                self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('No property selected.')])
        return self.cleaned_data

    def save(self):
        property_id = self.cleaned_data.get('property_id')
        self.request.session['property_id'] = property_id
        if 'pre_arrival' in self.request.session and 'preload' in self.request.session['pre_arrival'] and 'property_id' in self.request.session['pre_arrival']['preload']:
            self.request.session['pre_arrival']['preload'].pop('property_id', None)
        if 'check_out' in self.request.session and 'preload' in self.request.session['check_out'] and 'property_id' in self.request.session['check_out']['preload']:
            self.request.session['check_out']['preload'].pop('property_id', None)
    