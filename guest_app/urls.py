from django.urls    import path
from .views         import *

app_name = 'guest_app'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('check_in/data/', CheckInDataView.as_view(), name='check-in-data'),
    path('check_in/login/', CheckInLoginView.as_view(), name='check-in-login'),
    path('check_in/reservation/', CheckInReservationView.as_view(), name='check-in-reservation'),
    path('check_in/passport/', CheckInPassportView.as_view(), name='check-in-passport'),
    path('check_in/detail/', CheckInDetailView.as_view(), name='check-in-detail'),
]