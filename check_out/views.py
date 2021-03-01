from django.conf                import settings
from django.contrib             import messages
from django.http                import Http404
from django.shortcuts           import render
from django.utils               import translation
from django.utils.translation   import gettext, gettext_lazy as _
from django.views.generic       import *
from guest_base                 import views as GuestBaseViews, gateways
from guest_base.mixins          import PropertyRequiredMixin, RequestFormKwargsMixin, MobileTemplateMixin
from .                          import samples
from .forms                     import *
from .mixins                    import *


class IndexView(GuestBaseViews.IndexView):
    pattern_name = 'check_out:data'


class CheckOutDataView(RedirectView):
    pattern_name = 'check_out:login'

    def get_redirect_url(self, *args, **kwargs):
        self.request.session['property_id'] = self.request.GET.get('property', None)
        self.request.session['app'] = self.request.GET.get('app', 0)
        self.request.session['check_out'] = {'preload': {}}
        if 'lang' in self.request.GET: self.request.session[translation.LANGUAGE_SESSION_KEY] = self.request.GET.get('lang', 'en')
        if 'auto_login' in self.request.GET: self.request.session['check_out']['preload']['auto_login'] = self.request.GET.get('auto_login', 0)
        if 'reservation_no' in self.request.GET: self.request.session['check_out']['preload']['reservation_no'] = self.request.GET.get('reservation_no', '')
        if 'last_name' in self.request.GET: self.request.session['check_out']['preload']['last_name'] = self.request.GET.get('last_name', '')
        if 'room_no' in self.request.GET: self.request.session['check_out']['preload']['room_no'] = self.request.GET.get('room_no', '')
        return super().get_redirect_url(*args, **kwargs)


class CheckOutLoginView(PropertyRequiredMixin, RequestFormKwargsMixin, MobileTemplateMixin, FormView):
    template_name           = 'check_out/desktop/login.html'
    mobile_template_name    = 'check_out/mobile/login.html'
    form_class              = CheckOutLoginForm
    success_url             = '/check_out/bill/{reservation_no}'

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('check_out', {}).get('preload', {}).get('auto_login', 0):
            request.session['check_out']['preload']['auto_login'] = 0 # set auto login to False to prevent using `preload` data again
            data = {}
            data['reservation_no'] = request.session.get('check_out', {}).get('preload', {}).get('reservation_no', '')
            data['last_name'] = request.session.get('check_out', {}).get('preload', {}).get('last_name', '')
            data['room_no'] = request.session.get('check_out', {}).get('preload', {}).get('room_no', '')
            form = self.get_form_class()
            form = form(request, data)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        if not self.success_url:
            return super().get_success_url()
        url = self.success_url.format(**{'reservation_no': 'all'})
        return url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get('form', None)
        if self.request.session.get('app', 0) and self.request.session.get('check_out', {}).get('preload', {}).get('last_name', '') and (form and not form.is_bound):
            context['skip_last_name'] = True
        return context
    

class CheckOutBillView(BillRequiredAndExistMixin, PropertyRequiredMixin, RequestFormKwargsMixin, UpdateView):
    template_name           = 'check_out/desktop/bill.html'
    form_class              = CheckOutBillForm
    success_url             = '/check_out/bill/all'

    def gateway_post(self, reservations_no):
        data = {'reservation_no': reservations_no}
        response = gateways.guest_endpoint('/billsForCheckOut', self.request.session.get('property_id', ''), data)
        return response.get('data', {})

    def get_object(self, queryset=None):
        reservation_no = self.kwargs.get('reservation_no', None)
        reservations_no = [reservation_no]
        if reservation_no == 'all':
            reservations_no = [resv['reservation_no'] for resv in self.request.session['check_out'].get('bills', []) if resv.get('reservation_no', '')]
        obj = self.gateway_post(reservations_no)
        obj['id'] = reservation_no # set `reservation_no` as unique identifier
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['gst_no'] = settings.GST_NO
        context['business_no'] = settings.BUSINESS_NO
        context['currency_symbol'] = settings.CURRENCY_SYMBOL
        return context

    def form_valid(self, form):
        data = super().form_valid(form)
        if self.request.session['check_out'].get('complete', None):
            messages.add_message(self.request, messages.SUCCESS, _("All Guests have been successfully checked out.\n\nWe hope you enjoy your stay with us, and we'll see you again soon!"))
        else:
            reservation = next((temp for temp in self.object.get('reservation_info') if temp.get('reservation_no', '') == self.object.get('id', None)), {})
            guest_name = reservation.get('first_name', '') +' '+ reservation.get('last_name', '')
            guests_left = [temp.get('first_name', '') +' '+ temp.get('last_name', '') for temp in self.request.session['check_out'].get('bills', [])]
            names_left = '\n- '.join(guests_left)
            messages.add_message(self.request, messages.SUCCESS, _('We have checked-out the guest:\n- %(name)s\n\nOther guests left to check-out:\n- %(names_left)s') % {'name': guest_name, 'names_left': names_left})
        return data

    def get_success_url(self):
        url = self.success_url
        if len(self.request.session['check_out'].get('bills', [])) == 1: # redirect to last bill if left 1 bill to check-out
            bill = next(iter(self.request.session['check_out'].get('bills', [])), None)
            url = '/check_out/bill/%(reservation_no)s' % {'reservation_no': bill.get('reservation_no', 'all')}
        return url


class CheckOutComplete(TemplateView):
    template_name           = 'check_out/desktop/complete.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('check_out', {}).get('complete', None):
            return redirect('check_out:login')
        return super().dispatch(request, *args, **kwargs)
