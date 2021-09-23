from django.urls    import path
from .views         import *

app_name = 'custom'
urlpatterns = [
    path('registration/guest_list/', RegistrationGuestListView.as_view(), name='guest_list'),
    path('registration/main_guest/', RegistrationMainGuestView.as_view(), name='main_guest'),
]