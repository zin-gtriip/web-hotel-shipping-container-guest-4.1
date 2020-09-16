from django.urls    import path
from .views         import *

app_name = 'check_out'
urlpatterns = [
    path('check_out/', IndexView.as_view(), name='index'),
    path('check_out/data/', CheckOutDataView.as_view(), name='data'),
    path('check_out/login/', CheckOutLoginView.as_view(), name='login'),
    path('check_out/bill/<str:reservation_no>', CheckOutBillView.as_view(), name='bill'),
]
