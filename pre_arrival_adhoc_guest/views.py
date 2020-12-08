from django.shortcuts               import redirect
from django.http                    import HttpResponseRedirect
from django.views.generic           import *
from pre_arrival.mixins             import *
from pre_arrival.views              import PreArrivalPassportView, PreArrivalOtherInfoView
from pre_arrival_all_passport.views import PreArrivalDetailView, PreArrivalAllPassportExtraPassportView
from .forms                         import *


class PreArrivalPassportView(PreArrivalPassportView):

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('pre_arrival', {}).get('reservation', {}).get('preArrivalDone', '0') == '1':
            request.session['pre_arrival']['passport'] = True # mark `passport` is done
            return redirect('pre_arrival_adhoc_guest:guest_list')
        return super().dispatch(request, *args, **kwargs)


class PreArrivalAdhocGuestGuestListView(ParameterRequiredMixin, ProgressRateContextMixin, TemplateView):
    template_name           = 'pre_arrival_adhoc_guest/desktop/guest_list.html'
    parameter_required      = 'passport'
    progress_bar_page       = 'passport'

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('pre_arrival', {}).get('reservation', {}).get('preArrivalDone', '0') != '1':
            return redirect('pre_arrival:passport')
        prefilled = []
        for guest in list(request.session['pre_arrival']['reservation'].get('guestsList', [])):
            if not guest.get('hasLocalRecord', None):
                request.session['pre_arrival']['reservation']['guestsList'].remove(guest) # reset `guestsList` with no new guest
            else:
                prefilled.append(guest) # store additional guests to `session.pre_arrival.detail` that will be used on `pre_arrival_all_passport.forms`
        request.session['pre_arrival']['detail'] = {'prefilled_guest_temp': prefilled}
        return super().dispatch(request, *args, **kwargs)


class PreArrivalDetailView(PreArrivalDetailView):

    def dispatch(self, request, *args, **kwargs):
        # redirect to `guest_list` if `session` has no new added guest
        guests = [guest for guest in request.session['pre_arrival']['reservation'].get('guestsList', []) if guest.get('passportImage', '')]
        if request.session['pre_arrival']['reservation'].get('preArrivalDone', '0') == '1' and not guests:
            return redirect('pre_arrival_adhoc_guest:guest_list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # render extra form formset
        if self.request.POST:
            context['extra'] = PreArrivalDetailExtraFormSet(self.request, self.request.POST)
        else:
            context['extra'] = PreArrivalDetailExtraFormSet(self.request)
        return context


class PreArrivalAllPassportExtraPassportView(PreArrivalAllPassportExtraPassportView):
    form_class = PreArrivalAllPassportExtraPassportForm


class PreArrivalOtherInfoView(PreArrivalOtherInfoView):

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('pre_arrival', {}).get('reservation', {}).get('preArrivalDone', '0') == '1':
            request.session['pre_arrival']['other_info'] = True # mark `other_info` is done
            form = self.get_form()
            form.gateway_post()
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)
