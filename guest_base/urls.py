from django.urls    import path
from .views         import *

app_name = 'guest_base'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('property/', GuestBasePropertyView.as_view(), name='property'),
]