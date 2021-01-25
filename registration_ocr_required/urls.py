from django.urls    import path
from .views         import *

app_name = 'registration_ocr_required'
urlpatterns = [
    path('', IndexView.as_view(), name='hotel_guest_index'),
    path('registration/', IndexView.as_view(), name='index'),
    path('registration/data/', RegistrationDataView.as_view(), name='data'),
    path('registration/login/', RegistrationLoginView.as_view(), name='login'),
    path('registration/timer_extension/', RegistrationTimerExtensionView.as_view(), name='timer_extension'),
    path('registration/reservation/', RegistrationReservationView.as_view(), name='reservation'),
    path('registration/passport/', RegistrationPassportView.as_view(), name='passport'),
    path('registration/detail/', RegistrationDetailView.as_view(), name='detail'),
    path('registration/extra_passport/', RegistrationExtraPassportView.as_view(), name='extra_passport'),
    path('registration/other_info/', RegistrationOtherInfoView.as_view(), name='other_info'),
    path('registration/complete/', RegistrationCompleteView.as_view(), name='complete'),
]
