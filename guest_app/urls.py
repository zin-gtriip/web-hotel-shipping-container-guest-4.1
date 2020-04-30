from django.urls    import path
from .views         import *

app_name = 'guest_app'
urlpatterns = [
    path('checkin/login/', CheckInLoginView.as_view(), name='checkin-login'),
    path('checkin/passport/', CheckInPassportView.as_view(), name='checkin-passport'),
    path('checkin/detail/', CheckInDetailView.as_view(), name='checkin-detail'),
]