from django.shortcuts   import redirect


class BillRequiredAndExistMixin:
    """
    View mixin that verifies the user has `check_out`, `bills` and selected 
    `reservation_no` exists in the session.

    If `reservations` does not exist in `session`, page will be redirected to
    login page. If selected `reservation_no` does not exist, will raise 
    `ValueError`.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('check_out', {}).get('bills', ''):
            reservation_no = kwargs.get('reservation_no', None)
            reservation = next((resv for resv in request.session['check_out']['bills'] if resv['reservation_no'] == reservation_no), None)
            if reservation_no == 'all' or reservation:
                return super().dispatch(request, *args, **kwargs)
            else:
                raise ValueError('Selected reservation number is not found in current session')
        return redirect('check_out:login')
