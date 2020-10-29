from django.shortcuts   import redirect


class BillRequiredAndExistMixin:
    """
    View mixin that verifies the user has `check_out.bookings` and selected 
    `reservation_no` exists in the session when check-out is not complete.

    If `check_out.bookings` does not exist in `session`, page will be 
    redirected to login page. If selected `reservation_no` does not exist 
    and check-out is not complete, will raise `ValueError`.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('check_out', {}).get('bookings', []):
            reservation_no = kwargs.get('reservation_no', None)
            reservation = next((resv for resv in request.session['check_out']['bookings'] if resv['reservation_no'] == reservation_no), None)
            if reservation_no == 'all' or reservation or request.session.get('check_out', {}).get('complete', None):
                return super().dispatch(request, *args, **kwargs)
            else:
                raise ValueError('Selected reservation number is not found in current session')
        return redirect('check_out:login')
