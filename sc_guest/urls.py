"""sc_guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('guest/', include('custom.urls')),
    path('guest/', include('guest_facing.registration.urls')),
    path('guest/', include('guest_facing.check_out.urls')),
    path('guest/', include('guest_facing.chat.urls')),
    path('guest/', include('guest_facing.core.urls')),
    
    path('guest/admin/', admin.site.urls),
    path('guest/i18n/', include('django.conf.urls.i18n')),
    path('guest/jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
