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
    Generic form view mixin verifies that the user has `check_in_details`
    and `check_out_details` in `request.session`.
    This mixin works similar like `LoginRequiredMixin` and must be put
    on every check-in page except login
    """
    check_in_login_url   = 'guest_app:check-in-login'
    check_out_login_url  = 'guest_app:check-out-login'

    def dispatch(self, request, *args, **kwargs):
        if request.session.session_key:
            if ('/check_in' in request.path and 'check_in_details' in request.session) or ('/check_out' in request.path and 'check_out_details' in request.session):
                return super(SessionDataRequiredMixin, self).dispatch(request, *args, **kwargs)
        if '/check_in' in request.path:
            return redirect(self.check_in_login_url)
        elif '/check_out' in request.path:
            return redirect(self.check_out_login_url)
        return redirect('guest_app:index')
