from django.urls    import path
from .views         import *

app_name = 'chat'
urlpatterns = [
    path('chat/', IndexView.as_view(), name='index'),
    path('chat/channel/', ChatChannelView.as_view(), name='channel'),
    path('chat/message/', ChatMessageView.as_view(), name='message'),
]
