from datetime           import datetime as dt
from django.shortcuts   import redirect
from django.utils       import timezone
from django.conf        import settings


class ExpirySessionMixin:
    """
    View mixin that verifies the user has `pre_arrival`, `initial_expiry_date`
    or 'extended_expiry_date' is not expired.
    
    If it does not exist or expired, page will be redirected to login page. This
    mixin must be put on every pre-arrival page except login and complete page.
    """
    
    def dispatch(self, request, *args, **kwargs):
        if request.session.session_key and (request.session['pre_arrival'].get('initial_expiry_date', '') or request.session['pre_arrival'].get('extended_expiry_date', '')):
            expiry_date = request.session['pre_arrival'].get('extended_expiry_date', '') or request.session['pre_arrival'].get('initial_expiry_date', '')
            try:
                expiry_date = dt.strptime(expiry_date, '%Y-%m-%dT%H:%M:%S.%f%z')
            except:
                expiry_date = None
            if expiry_date and expiry_date >= timezone.now():
                return super().dispatch(request, *args, **kwargs)
        return redirect('pre_arrival:login')


class ParameterRequiredMixin(ExpirySessionMixin):
    """
    View mixin that verifies the user has `pre_arrival`, `{parameter_required}`.
    Note: `parameter_required` needs to be defined on each view and assigned after 
    form is valid on each form. It also must be same `name` in `urls.py`.

    Inherit from `ExpirySessionMixin` that also validate `initial_expiry_date` 
    in session. If `parameter_required` does not exist in `session`, page will be 
    redirected to page of `parameter_required` value.
    """
    parameter_required = None

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('pre_arrival', {}).get(self.parameter_required, ''):
            return super().dispatch(request, args, kwargs)
        if not self.parameter_required:
            return redirect('pre_arrival:login')
        return redirect('/pre_arrival/%s/' % self.parameter_required)


class ProgressRateContextMixin:
    """
    View mixin which save progress rate into `pre_arrival` in `request.session`.

    This mixin is using `progress_bar_page` defined on every view to to calculate
    current page progress rate. This mixin also will save previous page progress
    rate for animating progress bar.
    Note: `progress_bar_page` must be defined on every view otherwise progress
    rate value will be same like first page
    """

    progress_bar_page = None

    def dispatch(self, request, *args, **kwargs):
        if not 'pre_arrival' in request.session:
            request.session['pre_arrival'] = {}
        page_index = settings.PRE_ARRIVAL_PROGRESS_BAR_PAGES.index(self.progress_bar_page) if self.progress_bar_page in settings.PRE_ARRIVAL_PROGRESS_BAR_PAGES else 0
        if page_index == 0:
            request.session['pre_arrival']['previous_progress_rate'] = 0
            request.session['pre_arrival']['current_progress_rate'] = settings.PRE_ARRIVAL_PROGRESS_BAR_START_RATE
        else:
            request.session['pre_arrival']['previous_progress_rate'] = request.session['pre_arrival'].get('current_progress_rate', settings.PRE_ARRIVAL_PROGRESS_BAR_START_RATE)
            request.session['pre_arrival']['current_progress_rate'] = settings.PRE_ARRIVAL_PROGRESS_BAR_START_RATE + (page_index * settings.PRE_ARRIVAL_PROGRESS_BAR_RATE_PER_PAGE)
        return super().dispatch(request, *args, **kwargs)
