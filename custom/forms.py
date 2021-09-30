import os
from datetime                           import datetime as dt
from django                             import forms
from django.conf                        import settings
from django.urls                        import reverse
from django.shortcuts                   import render, redirect
from django.utils.translation           import gettext, gettext_lazy as _
from django_countries.fields            import Country, CountryField
from guest_facing.core                  import gateways
from guest_facing.registration.forms    import RegistrationLoginForm, RegistrationReservationForm, RegistrationDetailForm, RegistrationGuestListForm, RegistrationOtherInfoForm
from guest_facing.registration          import utils

class RegistrationLoginForm(RegistrationLoginForm):

    def save(self):
        super().save()

        # for OTA
        self.request.session['registration']['booker_profile'] = []
        self.request.session['registration']['isBookerRegistered'] = self.response.get('data', {}).get('isBookerRegistered', False)
        self.request.session['registration']['isBookerStaying'] = False

class RegistrationReservationForm(RegistrationReservationForm):
    template_name           = 'registration/desktop/reservation.html'
    booker_stay = forms.CharField(widget=forms.HiddenInput(), required=False)

    def save(self):
        super().save()

        # for OTA
        booker_stay = self.cleaned_data.get('booker_stay')
        # check if booker is already registered in another room
        if self.request.session['registration']['isBookerRegistered'] == False:
            # booker is not registered yet, confirm user whether booker is staying in current room
            if booker_stay == 'no':
                # booker is not staying in current room, remove booker from current reservation guest list
                for guest in self.request.session['registration']['reservation'].get('guestsList', []):
                    if guest.get('isBooker') == True:
                        self.request.session['registration']['booker_profile'] = guest
                        self.request.session['registration']['reservation'].get('guestsList', []).remove(guest)
            elif booker_stay == 'yes':
                # booker is staying in current room, no need to remove booker from current reservation guest list
                count = 0
                self.request.session['registration']['isBookerStaying'] = True
                for guest in self.request.session['registration']['reservation'].get('guestsList', []):
                    if guest.get('isBooker') == True:
                        self.request.session['registration']['booker_profile'] = guest
                        count+=1
                if count == 0:
                    self.request.session['registration']['reservation'].get('guestsList', []).append(self.request.session['registration']['booker_profile'])
        else:
            # booker is already registered, remove booker from current reservation guest list
            for guest in self.request.session['registration']['reservation'].get('guestsList', []):
                if guest.get('isBooker') == True:
                    self.request.session['registration']['booker_profile'] = guest
                    if guest.get('hasLocalRecord') == False:
                        # remove the booker guest only if the booker guest was not registered in this room
                        self.request.session['registration']['reservation'].get('guestsList', []).remove(guest)

class RegistrationGuestListForm(RegistrationGuestListForm):

    def gateway_post(self):
        main_guest = next((guest for guest in self.request.session['registration']['reservation'].get('guestsList', []) if guest.get('isMainGuest') == True), {})
        guest_email = main_guest.get('email', '')
        is_subscribe = main_guest.get('emailSubscription', '')
        for guest in self.request.session['registration']['reservation'].get('guestsList', []):
            guest.update({'email': guest_email,'emailSubscription': is_subscribe})

        self.request.session['registration']['other_info'] = True # mark `other info` page as done
        data = self.request.session['registration']['reservation']
        email = utils.prepare_email(dict(self.request.session['registration']['reservation'])) # create new variable to prevent modification on `request.session`
        data['userInputNumber'] = self.request.session['registration'].get('input_reservation_no', '')
        data = {**data, **email} # add email data
        response = gateways.guest_endpoint('post', '/submitWebRegistration', self.request.session.get('property_id', ''), data)
        if response.get('statusCode', '') == '5002':
            # get existing reservation from backend
            new_booking_data = {}
            new_booking_data['reservationNo'] = self.request.session['registration'].get('input_reservation_no', '')
            new_booking_data['arrivalDate'] = self.request.session['registration'].get('input_arrival_date', '')
            new_booking_data['lastName'] = self.request.session['registration'].get('input_last_name', '')
            new_booking_data['reservationType'] = self.request.session['registration'].get('reservation_type', '')
            new_booking_response = gateways.guest_endpoint('post', '/checkWebRegistration', self.request.session.get('property_id', ''), new_booking_data)
            new_booking = new_booking_response.get('data', {}).get('data', [])
            self.request.session['registration']['bookings'] = [reservation for reservation in new_booking if reservation.get('pmsNo') != self.request.session['registration'].get('reservation', {}).get('pmsNo', '')]

            # for OTA
            self.request.session['registration']['booker_profile'] = []
            self.request.session['registration']['isBookerRegistered'] = new_booking_response.get('data', {}).get('isBookerRegistered', False)
            self.request.session['registration']['isBookerStaying'] = False
        else:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([response.get('message', _('Unknown error'))])

class RegistrationDetailForm(RegistrationDetailForm):

    def save(self):
        self.instance['firstName'] = self.cleaned_data.get('first_name')
        self.instance['lastName'] = self.cleaned_data.get('last_name')
        self.instance['nationality'] = self.cleaned_data.get('nationality')
        self.instance['gender'] = self.cleaned_data.get('gender')
        self.instance['idNo'] = self.cleaned_data.get('id_no')
        self.instance['dob'] = self.cleaned_data.get('birth_date').strftime('%Y-%m-%d') if self.cleaned_data.get('birth_date') else ''
        self.instance['is_overwrite'] = self.cleaned_data.get('is_overwrite')
        if self.cleaned_data.get('is_submit', False):
            if self.instance.get('guestId', 0) != 0 or self.instance.get('new_guest_id', None): # existing guest
                if self.instance.get('guestId', 0) != 0:
                    guest = next((data for data in self.request.session['registration']['reservation'].get('guestsList', []) if data.get('guestId', None) == self.instance.get('id', 0)), {})
                else:
                    guest = next((data for data in self.request.session['registration']['reservation'].get('guestsList', []) if data.get('new_guest_id', '') == self.instance.get('new_guest_id', None)), {})
                guest['firstName'] = self.instance.get('firstName', '')
                guest['lastName'] = self.instance.get('lastName', '')
                guest['nationality'] = self.instance.get('nationality', '')
                guest['nationalityThreeLetters'] = Country(self.instance.get('nationality')).alpha3
                guest['gender'] = self.instance.get('gender', '')
                guest['idNo'] = self.instance.get('idNo', '')
                guest['dob'] = self.instance.get('dob', '')
                guest['idImage'] = self.instance.get('idImage', '')
                guest['idType'] = self.instance.get('idType', '')
                if not self.instance.get('new_guest_id', None):
                    guest['new_guest_id'] = 0
                guest['age'] = utils.calculate_age(dt.strptime(self.instance.get('dob', ''), '%Y-%m-%d'))
                guest['is_done'] = True
            else: # new guest
                guest = {}
                guest['guestId'] = self.instance.get('guestId', 0)
                guest['firstName'] = self.instance.get('firstName', '')
                guest['lastName'] = self.instance.get('lastName', '')
                guest['nationality'] = self.instance.get('nationality', '')
                guest['nationalityThreeLetters'] = Country(self.instance.get('nationality')).alpha3
                guest['gender'] = self.instance.get('gender', '')
                guest['idNo'] = self.instance.get('idNo', '')
                guest['dob'] = self.instance.get('dob', '')
                guest['idImage'] = self.instance.get('idImage', '')
                guest['idType'] = self.instance.get('idType', '')
                guest['new_guest_id'] = 'new%s' % len([data for data in self.request.session['registration']['reservation'].get('guestsList', []) if data.get('guestId', 0) == 0])
                guest['age'] = utils.calculate_age(dt.strptime(self.instance.get('dob', ''), '%Y-%m-%d'))
                guest['is_done'] = True
                self.request.session['registration']['reservation']['guestsList'].append(guest)
        return self.instance

class RegistrationMainGuestForm(forms.Form):
    main_guest_id = forms.ChoiceField(widget=forms.RadioSelect(), required=False)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''

        choices = []
        for guest in self.request.session['registration'].get('reservation', []).get('guestsList', []):
            if guest.get('guestId', 0) == 0:
                choices.append((guest.get('new_guest_id', ''), guest.get('new_guest_id', '')))
            else:
                choices.append((str(guest.get('guestId', '')),str(guest.get('guestId', ''))))
        self.fields['main_guest_id'].choices = choices

    def clean(self):
        super().clean()
        main_guest_id = self.cleaned_data.get('main_guest_id')

        if not main_guest_id:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('Main guest is not selected.')])
        return self.cleaned_data

    def save(self):
        main_guest_id = self.cleaned_data.get('main_guest_id')
        # save main guest
        booker_guest = self.request.session['registration']['booker_profile']
        main_guest = next((guest for guest in self.request.session['registration']['reservation'].get('guestsList', []) if guest.get('isMainGuest', False)), {})

        for guest in self.request.session['registration']['reservation'].get('guestsList', []):
            if self.request.session['registration']['reservation'].get('preArrivalDone', True) == True:
                guest.update({'email': main_guest.get('email', ''),'emailSubscription': main_guest.get('emailSubscription', False)})
            else:
                guest.update({'email': booker_guest.get('email', ''),'emailSubscription': booker_guest.get('emailSubscription', False)})

            if guest.get('new_guest_id', '') == main_guest_id or str(guest.get('guestId', )) == main_guest_id:
                guest['isMainGuest'] = True

                # update the room's main guest as a booker guest
                # multiple rooms > when booker guest is not staying in any of the room
                # single room > when booker is not staying in the room
                if len(self.request.session['registration']['bookings']) == 1 and self.request.session['registration']['isBookerRegistered'] == False and self.request.session['registration']['isBookerStaying'] == False:
                    print('guest profile replaced with booker guest')
                    guest['guestId'] = booker_guest['guestId']
                    guest['lastName'] = booker_guest['lastName']
                    guest['isBooker'] = True
            else:
                guest['isMainGuest'] = False
        self.request.session['registration']['main_guest'] = True

class RegistrationOtherInfoForm(RegistrationOtherInfoForm):

    def save(self):
        arrival_time = self.cleaned_data.get('arrival_time')
        special_requests = self.cleaned_data.get('special_requests')
        email = self.cleaned_data.get('email')
        is_subscribe = self.cleaned_data.get('is_subscribe')

        for guest in self.request.session['registration']['reservation'].get('guestsList', []):
            guest.update({'email': email,'emailSubscription': is_subscribe})

        self.request.session['registration']['reservation']['eta'] = arrival_time + ':00'
        self.request.session['registration']['reservation']['comments'] = special_requests
        self.request.session['registration']['other_info'] = True # variable to prevent page jump

    def gateway_post(self):
        data = self.request.session['registration']['reservation']
        email = utils.prepare_email(dict(self.request.session['registration']['reservation'])) # create new variable to prevent modification on `request.session`
        data['userInputNumber'] = self.request.session['registration'].get('input_reservation_no', '')
        data = {**data, **email} # add email data
        response = gateways.guest_endpoint('post', '/submitWebRegistration', self.request.session.get('property_id', ''), data)
        print('submitWebRegistration',response)
        if response.get('statusCode', '') == '5002':
            # get existing reservation from backend
            new_booking_data = {}
            new_booking_data['reservationNo'] = self.request.session['registration'].get('input_reservation_no', '')
            new_booking_data['arrivalDate'] = self.request.session['registration'].get('input_arrival_date', '')
            new_booking_data['lastName'] = self.request.session['registration'].get('input_last_name', '')
            new_booking_response = gateways.guest_endpoint('post', '/checkWebRegistration', self.request.session.get('property_id', ''), new_booking_data)
            new_booking = new_booking_response.get('data', {}).get('data', [])
            self.request.session['registration']['bookings'] = [reservation for reservation in new_booking if reservation.get('pmsNo') != self.request.session['registration'].get('reservation', {}).get('pmsNo', '')]

            # for OTA
            self.request.session['registration']['booker_profile'] = []
            self.request.session['registration']['isBookerRegistered'] = new_booking_response.get('data', {}).get('isBookerRegistered', False)
            self.request.session['registration']['isBookerStaying'] = False
        else:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([response.get('message', _('Unknown error'))])

