from django.conf                import settings
from django.contrib             import messages
from django.http                import Http404
from django.shortcuts           import render
from django.utils               import translation
from django.utils.translation   import gettext, gettext_lazy as _
from django.views.generic       import *
from guest_base                 import views as GuestBaseViews
from guest_base.mixins          import RequestFormKwargsMixin, MobileTemplateMixin
from .                          import samples
from .forms                     import *
from .mixins                    import *


class IndexView(GuestBaseViews.IndexView):
    pattern_name = 'check_out:data'


class CheckOutDataView(RedirectView):
    pattern_name = 'check_out:login'

    def get_redirect_url(self, *args, **kwargs):
        self.request.session['check_out'] = {'preload': {}}
        self.request.session['app'] = self.request.GET.get('app', False) if 'app' in self.request.GET else False
        if 'lang' in self.request.GET: self.request.session[translation.LANGUAGE_SESSION_KEY] = self.request.GET.get('lang', 'en')
        if 'auto_login' in self.request.GET: self.request.session['check_out']['preload']['auto_login'] = self.request.GET.get('auto_login', False)
        if 'reservation_no' in self.request.GET: self.request.session['check_out']['preload']['reservation_no'] = self.request.GET.get('reservation_no', '')
        if 'room_no' in self.request.GET: self.request.session['check_out']['preload']['room_no'] = self.request.GET.get('room_no', '')
        return super().get_redirect_url(*args, **kwargs)


class CheckOutLoginView(RequestFormKwargsMixin, MobileTemplateMixin, FormView):
    template_name           = 'check_out/desktop/login.html'
    mobile_template_name    = 'check_out/mobile/login.html'
    form_class              = CheckOutLoginForm
    success_url             = '/check_out/bill/{reservation_no}'

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('check_out', {}).get('preload', {}).get('auto_login', False):
            data = {
                'reservation_no': request.session.get('check_out', {}).get('preload', {}).get('reservation_no', ''),
                'room_no': request.session.get('check_out', {}).get('preload', {}).get('room_no', ''),
            }
            form = self.get_form_class()
            form = form(request, data)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save_data()
        return super().form_valid(form)

    def get_success_url(self):
        if not self.success_url:
            return super().get_success_url()
        url = self.success_url.format(**{'reservation_no': 'all'})
        return url
    

class CheckOutBillView(RequestFormKwargsMixin, BillRequiredAndExistMixin, UpdateView):
    template_name           = 'check_out/desktop/bill.html'
    form_class              = CheckOutBillForm
    success_url             = '/check_out/bill/{reservation_no}'

    def gateway_post(self, reservations_no):
        if not reservations_no:
            raise ValueError('No reservation number is provided')
        data = {'reservation_no': reservations_no}
        response = gateways.backend_post('/billsForCheckOut', data)
        if response.get('status_code', '') == 500:
            bill = response.get('data', {})
        else:
            raise Http404('No matching entries with the Reservation No. found')
        return bill

    def get_object(self, queryset=None):
        reservation_no = self.kwargs.get('reservation_no', None)
        reservations_no = [reservation_no]
        if reservation_no == 'all':
            reservations_no = [resv['reservation_no'] for resv in self.request.session['check_out'].get('bills', []) if resv.get('reservation_no', '')]
        obj = self.gateway_post(reservations_no)
        reservation_info = obj.get('reservation_info', [])
        if len(reservation_info) == 1:
            reservation = next(iter(reservation_info), {})
            obj.update(**reservation)
        elif len(reservation_info) > 1:
            reservations_no = [reservation.get('reservation_no', '') for reservation in reservation_info]
            rooms_no = [reservation.get('room_no', '') for reservation in reservation_info]
            arrivals_date = [reservation.get('arrival_date', '') for reservation in reservation_info]
            departures_date = [reservation.get('departure_date', '') for reservation in reservation_info]
            obj['reservation_no'] = ','.join(reservations_no)
            obj['room_no'] = ','.join(list(set(rooms_no))) # `set` is for removing duplicate value
            obj['arrival_date'] = ','.join(list(set(arrivals_date)))
            obj['departure_date'] = ','.join(list(set(departures_date)))
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['gst_no'] = settings.GST_NO
        context['business_no'] = settings.BUSINESS_NO
        context['currency_symbol'] = settings.CURRENCY_SYMBOL
        return context

    def form_valid(self, form):
        data = super().form_valid(form)
        guest_name = self.object.get('first_name', '') +' '+ self.object.get('last_name', '')
        if len(self.object.get('reservation_no', '').split(',')) > 1:
            guest_name = 'All Guests'
        messages.add_message(self.request, messages.SUCCESS, _('%(name)s have been successfully checked out.') % {'name': guest_name})
        return data

    def get_success_url(self):
        if not self.success_url:
            return super().get_success_url()
        url = self.success_url.format(**{'reservation_no': self.kwargs.get('reservation_no', None)})
        return url
