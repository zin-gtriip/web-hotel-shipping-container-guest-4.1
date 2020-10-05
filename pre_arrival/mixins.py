from datetime           import datetime as dt
from django.shortcuts   import redirect
from django.utils       import timezone
from django.conf        import settings


class ExpirySessionMixin:
    """
    View mixin that verifies the user has `pre_arrival`, `initial_expiry_date`
    is not expired.
    
    If it does not exist or expired, page will be redirected to login page. This
    mixin must be put on every pre-arrival page except login and complete page.
    """
    
    def dispatch(self, request, *args, **kwargs):
        if request.session.session_key and request.session.get('pre_arrival', {}).get('initial_expiry_date', ''):
            try:
                expiry_date = dt.strptime(request.session['pre_arrival'].get('initial_expiry_date', ''), '%Y-%m-%dT%H:%M:%S.%f%z')
            except:
                expiry_date = None
            if expiry_date and expiry_date >= timezone.now():
                return super().dispatch(request, *args, **kwargs)
        return redirect('pre_arrival:login')


class PageParameterRequiredMixin(ExpirySessionMixin):
    """
    View mixin that verifies the user has `pre_arrival`, `{page_parameter}`.
    Note: `page_parameter` needs to be defined on each view and assigned after 
    form is valid on each form. It also must be same `name` in `urls.py`.

    Inherit from `ExpirySessionMixin` that also validate `initial_expiry_date` 
    in session. If `page_parameter` does not exist in `session`, page will be 
    redirected to page of `page_parameter` value.
    """
    page_parameter = None

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('pre_arrival', {}).get(self.page_parameter, ''):
            return super().dispatch(request, *args, **kwargs)
        if not self.page_parameter:
            return redirect('pre_arrival:login')
        return redirect('pre_arrival:%s' % self.page_parameter)


class ProgressRateContextMixin:
    """
    View mixin which puts progress rate into context of the view.

    This mixin will calculate progress rate based on `PROGRESS_BAR_START_RATE`,
    `PROGRESS_BAR_END_RATE`, and `PRE_ARRIVAL_URLS` length in `settings.py` 
    by dividing averagely.
    This mixin also save previous page into `request` for calculating previous
    page progress bar.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get current url from `request.path`, ex: `/pre_arrival/login/` to get `login`
        current_url = self.request.path.replace('/pre_arrival/', '').split('/')[0]
        # calculate progress rate
        current_url_index = settings.PRE_ARRIVAL_URLS.index(current_url)
        previous_url_index = 0
        if self.request.session.get('pre_arrival', {}).get('previous_url', '') in settings.PRE_ARRIVAL_URLS:
            previous_url_index = settings.PRE_ARRIVAL_URLS.index(self.request.session['pre_arrival']['previous_url']) # get previous url index from `session`
        rate_per_page = (settings.PROGRESS_BAR_END_RATE - settings.PROGRESS_BAR_START_RATE) / (len(settings.PRE_ARRIVAL_URLS) - 1) # -1 to exclude login page
        context['current_page_progress_rate'] = settings.PROGRESS_BAR_START_RATE + (current_url_index * rate_per_page)
        context['previous_page_progress_rate'] = settings.PROGRESS_BAR_START_RATE + (previous_url_index * rate_per_page)
        if current_url_index == 0: # for `login` page
            context['current_page_progress_rate'] = settings.PROGRESS_BAR_START_RATE
            context['previous_page_progress_rate'] = 0
        # save current url to `session` as `previous_url`
        if not 'pre_arrival' in self.request.session:
            self.request.session['pre_arrival'] = {}
        self.request.session['pre_arrival']['previous_url'] = (current_url if current_url != 'login' else '')
        return context
