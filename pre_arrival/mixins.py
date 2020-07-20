from django.shortcuts		    import render, redirect

class RequestInitializedMixin(object):
    """
    Generic form view mixin which puts the request into the form kwargs.

    Note: Using this mixin requires you to pop the `request` kwarg
    out of the dict in the super of your form's `__init__`.
    """

    def get_form_kwargs(self):
        kwargs = super(RequestInitializedMixin, self).get_form_kwargs()
        kwargs.update(request=self.request)
        return kwargs


class SessionDataRequiredMixin(object):
    """
    Generic form view mixin that verifies the user has `pre_arrival`
    and `bookings` in `request.session`.

    This mixin works similar like `LoginRequiredMixin` and must be put
    on every check-in page except login
    """
    def dispatch(self, request, *args, **kwargs):
        if request.session.session_key and '/check_in' in request.path and request.session.get('pre_arrival', {}).get('bookings', {}):
            return super(SessionDataRequiredMixin, self).dispatch(request, *args, **kwargs)
        return redirect('pre_arrival:index')


class MobileTemplateMixin(object):
    """
    Generic form view mixin that replace `template_name` with mobile template.

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
