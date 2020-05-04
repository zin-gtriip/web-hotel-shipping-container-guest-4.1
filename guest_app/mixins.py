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
    Generic form view mixin verifies that the user has `checkin_data`
    in `request.session`.
    This mixin works similar like `LoginRequiredMixin` and must be put
    on every check-in page except login
    """
    checkin_login_url   = 'guest_app:checkin-login'
    checkout_login_url  = 'guest_app:checkout-login'

    def dispatch(self, request, *args, **kwargs):
        if request.session.session_key:
            if ('/checkin' in request.path and 'checkin_data' in request.session) or ('/checkout' in request.path and 'checkout_data' in request.session):
                return super(SessionDataRequiredMixin, self).dispatch(request, *args, **kwargs)
        if '/checkin' in request.path:
            return redirect(self.checkin_login_url)
        else:
            return redirect(self.checkout_login_url)
        return redirect('guest_app:index')
