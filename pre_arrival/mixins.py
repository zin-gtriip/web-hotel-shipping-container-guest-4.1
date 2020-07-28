from datetime           import datetime as dt
from django.shortcuts   import redirect
from django.utils       import timezone
from django.conf        import settings

class RequestInitializedMixin(object):
    """
    View mixin which puts the request into the form kwargs.

    Note: Using this mixin requires you to pop the `request` kwarg
    out of the dict in the super of your form's `__init__`.
    """

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(request=self.request)
        return kwargs


class SessionDataRequiredMixin(object):
    """
    View mixin that verifies the user has `pre_arrival`, `expiry_date`
    is not expired.
    
    If it does not exist or expired, page will be redirected to login page. This
    mixin must be put on every pre-arrival page except login and complete page.
    """
    
    def dispatch(self, request, *args, **kwargs):
        if request.session.session_key and request.session.get('pre_arrival', {}).get('expiry_date', ''):
            try:
                expiry_date = dt.strptime(request.session['pre_arrival'].get('expiry_date', ''), '%Y-%m-%d %H:%M:%S.%f%z')
            except:
                expiry_date = None
            if expiry_date and expiry_date >= timezone.now():
                return super().dispatch(request, *args, **kwargs)
        return redirect('pre_arrival:login')


class ProgressRateInitializedMixin(object):
    """
    View mixin which puts progress rate into context of the view.

    This mixin will calculate progress rate based on `PRE_ARRIVAL_START_PROGRESS_BAR`,
    `PRE_ARRIVAL_END_PROGRESS_BAR`, and `PRE_ARRIVAL_URLS` length in `settings.py` 
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
        rate_per_page = (settings.PRE_ARRIVAL_END_PROGRESS_BAR - settings.PRE_ARRIVAL_START_PROGRESS_BAR) / (len(settings.PRE_ARRIVAL_URLS) - 1) # -1 to exclude login page
        context['current_page_progress_bar'] = settings.PRE_ARRIVAL_START_PROGRESS_BAR + (current_url_index * rate_per_page)
        context['previous_page_progress_bar'] = settings.PRE_ARRIVAL_START_PROGRESS_BAR + (previous_url_index * rate_per_page)
        if current_url_index == 0: # for `login` page
            context['current_page_progress_bar'] = settings.PRE_ARRIVAL_START_PROGRESS_BAR
            context['previous_page_progress_bar'] = 0
        # save current url to `session` as `previous_url`
        if not 'pre_arrival' in self.request.session:
            self.request.session['pre_arrival'] = {}
        self.request.session['pre_arrival'].update({'previous_url': (current_url if current_url != 'login' else '')})
        self.request.session.save()
        return context


class MobileTemplateMixin(object):
    """
    View mixin that replace `template_name` with mobile template.

    This mixin uses `django_user_agents` plugin to indicate if `user_agent` is
    mobile. And will check view is accessed from app through `preload`
    session. If one of them is fulfilled `mobile_template_name` will be used
    if it is provided.
    """
    mobile_template_name = None

    def get_template_names(self):
        if (self.request.session.get('pre_arrival', {}).get('preload', {}).get('app', False)) or not self.request.user_agent.is_pc:
            if self.mobile_template_name:
                return [self.mobile_template_name]
        return super().get_template_names()
