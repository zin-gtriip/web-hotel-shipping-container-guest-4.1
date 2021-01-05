from django.urls    import path
from .views         import *

app_name = 'pre_arrival_ocr_required'
urlpatterns = [
    path('pre_arrival/detail/', PreArrivalDetailView.as_view(), name='detail'),
    path('pre_arrival/extra_passport/', PreArrivalOcrRequiredExtraPassportView.as_view(), name='extra_passport'),
]
