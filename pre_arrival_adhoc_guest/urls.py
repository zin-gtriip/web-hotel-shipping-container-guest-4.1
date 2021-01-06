from django.urls    import path
from .views         import *

app_name = 'pre_arrival_adhoc_guest'
urlpatterns = [
    path('pre_arrival/passport/', PreArrivalPassportView.as_view(), name='passport'),
    path('pre_arrival/guest_list/', PreArrivalGuestListView.as_view(), name='guest_list'),
    path('pre_arrival/detail/', PreArrivalDetailView.as_view(), name='detail'),
    path('pre_arrival/extra_passport/', PreArrivalExtraPassportView.as_view(), name='extra_passport'),
    path('pre_arrival/other_info/', PreArrivalOtherInfoView.as_view(), name='other_info'),
]
