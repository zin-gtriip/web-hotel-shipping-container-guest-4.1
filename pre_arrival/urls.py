from django.urls    import path
from .views         import *

app_name = 'pre_arrival'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('pre_arrival/data/', PreArrivalDataView.as_view(), name='data'),
    path('pre_arrival/login/', PreArrivalLoginView.as_view(), name='login'),
    path('pre_arrival/reservation/', PreArrivalReservationView.as_view(), name='reservation'),
    path('pre_arrival/passport/', PreArrivalPassportView.as_view(), name='passport'),
    path('pre_arrival/detail/', PreArrivalDetailView.as_view(), name='detail'),
    path('pre_arrival/other_info', PreArrivalOtherInfoView.as_view(), name='other-info'),
    path('pre_arrival/complete', PreArrivalCompleteView.as_view(), name='complete'),
]