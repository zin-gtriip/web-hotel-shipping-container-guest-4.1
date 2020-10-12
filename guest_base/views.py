from django.shortcuts       import render
from django.views.generic   import RedirectView, TemplateView

class IndexView(RedirectView):
    pattern_name = 'admin:index'

class HTML404View(TemplateView):
    template_name              = 'guest_base/404.html'

    def get(self, request, *args, **kwargs):
        response = super(HTML404View, self).get(request, *args, **kwargs)
        response.status_code = 404
        return response

    def as_error_view(error):
        as_view_fun = error.as_view()

        def view(request):
            response = as_view_fun(request)
            response.render()
            return response

        return view