from django.urls    import path
from .views         import *

app_name = 'custom'
urlpatterns = [
    path('registration/login/', RegistrationLoginView.as_view(), name='login'),
    path('registration/reservation/', RegistrationReservationView.as_view(), name='reservation'),
    path('registration/guest_list/', RegistrationGuestListView.as_view(), name='guest_list'),
    path('registration/detail/<str:encrypted_id>/', RegistrationDetailView.as_view(), name='detail'),
    path('registration/main_guest/', RegistrationMainGuestView.as_view(), name='main_guest'),
    path('registration/other_info/', RegistrationOtherInfoView.as_view(), name='other_info'),
]