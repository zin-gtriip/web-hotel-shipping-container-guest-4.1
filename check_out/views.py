from django.shortcuts           import render
from django.views.generic       import *
from django.utils               import translation
from django.utils.translation   import gettext, gettext_lazy as _
from guest_base                 import views as GuestBaseViews
from guest_base.mixins          import RequestFormKwargsMixin, MobileTemplateMixin
from .forms                     import *


class IndexView(GuestBaseViews.IndexView):
    pattern_name = 'check_out:data'


class CheckOutDataView(RedirectView):
    pattern_name = 'check_out:login'

    def get_redirect_url(self, *args, **kwargs):
        self.request.session['check_out'] = {'preload': {}}
        self.request.session['app'] = self.request.GET.get('app', False) if 'app' in self.request.GET else False
        if 'lang' in self.request.GET: self.request.session[translation.LANGUAGE_SESSION_KEY] = self.request.GET.get('lang', 'en')
        if 'auto_login' in self.request.GET: self.request.session['check_out']['preload']['auto_login'] = self.request.GET.get('auto_login', False)
        if 'room_no' in self.request.GET: self.request.session['check_out']['preload']['room_no'] = self.request.GET.get('room_no', '')
        if 'last_name' in self.request.GET: self.request.session['check_out']['preload']['last_name'] = self.request.GET.get('last_name', '')
        return super().get_redirect_url(*args, **kwargs)


class CheckOutLoginView(RequestFormKwargsMixin, MobileTemplateMixin, FormView):
    template_name           = 'check_out/desktop/login.html'
    mobile_template_name    = 'check_out/mobile/login.html'
    form_class              = CheckOutLoginForm
    # success_url             = '/check_out/bill'

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('check_out', {}).get('preload', {}).get('auto_login', False):
            data = {
                'room_no': request.session.get('check_out', {}).get('preload', {}).get('room_no', ''),
                'last_name': request.session.get('check_out', {}).get('preload', {}).get('last_name', ''),
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
