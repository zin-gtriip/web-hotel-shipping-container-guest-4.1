from django.urls    import path
from .views         import (IndexView, RegistrationDataView, RegistrationLoginView, RegistrationTimerExtensionView,
                    RegistrationReservationView, RegistrationGuestListView, RegistrationDetailView, RegistrationOcrView,
                    RegistrationOtherInfoView, RegistrationCompleteView)

app_name = 'registration'
urlpatterns = [
    path('', IndexView.as_view(), name='sc_guest_index'),
    path('registration/', IndexView.as_view(), name='index'),
    path('registration/data/', RegistrationDataView.as_view(), name='data'),
    path('registration/login/', RegistrationLoginView.as_view(), name='login'),
    path('registration/timer_extension/', RegistrationTimerExtensionView.as_view(), name='timer_extension'),
    path('registration/reservation/', RegistrationReservationView.as_view(), name='reservation'),
    path('registration/guest_list/', RegistrationGuestListView.as_view(), name='guest_list'),
    path('registration/detail/<str:encrypted_id>/', RegistrationDetailView.as_view(), name='detail'),
    path('registration/ocr/<str:encrypted_id>/', RegistrationOcrView.as_view(), name='ocr'),
    path('registration/other_info/', RegistrationOtherInfoView.as_view(), name='other_info'),
    path('registration/complete/', RegistrationCompleteView.as_view(), name='complete'),
]