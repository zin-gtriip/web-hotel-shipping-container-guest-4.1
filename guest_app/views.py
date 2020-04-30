from django.shortcuts           import render, redirect
from django.views.generic.edit  import FormView
from .forms.check_in            import *
from .mixins                    import *

class CheckInLoginView(RequestInitializedMixin, FormView):
    template_name   = 'check_in/login.html'
    form_class      = CheckInLoginForm
    success_url     = '/checkin/passport'

    def form_valid(self, form):
        form.set_session()
        return super().form_valid(form)


class CheckInPassportView(RequestInitializedMixin, SessionDataRequiredMixin, FormView):
    template_name   = 'check_in/passport.html'
    form_class      = CheckInPassportForm
    success_url     = '/checkin/detail'


class CheckInDetailView(RequestInitializedMixin, SessionDataRequiredMixin, FormView):
    template_name   = 'check_in/detail.html'
    form_class      = CheckInDetailForm
    # success_url     = '/checkin/detail'
