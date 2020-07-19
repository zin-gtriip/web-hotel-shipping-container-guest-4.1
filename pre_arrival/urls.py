from django.urls    import path
from .views         import *

app_name = 'pre_arrival'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('check_in/data/', CheckInDataView.as_view(), name='check-in-data'),
    path('check_in/login/', CheckInLoginView.as_view(), name='check-in-login'),
    path('check_in/reservation/', CheckInReservationView.as_view(), name='check-in-reservation'),
    path('check_in/passport/', CheckInPassportView.as_view(), name='check-in-passport'),
    path('check_in/detail/', CheckInDetailView.as_view(), name='check-in-detail'),
    path('check_in/other_info', CheckInOtherInfoView.as_view(), name='check-in-other-info'),
    path('check_in/complete', CheckInCompleteView.as_view(), name='check-in-complete'),
]