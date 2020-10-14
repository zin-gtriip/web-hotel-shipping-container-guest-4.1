from django.shortcuts       import render
from django.views.generic   import RedirectView, TemplateView

class IndexView(RedirectView):
    pattern_name = 'admin:index'