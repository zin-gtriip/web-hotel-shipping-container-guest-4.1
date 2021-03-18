from django.conf        import settings
from django.http        import JsonResponse
from django.shortcuts   import redirect
from django.urls        import reverse

class DependentAppConfigMixin:
    """
    App mixin that verifies dependencies of an app.
    """

    dependencies = []

    def ready(self):
        if not all(depend in settings.INSTALLED_APPS for depend in self.dependencies):
            raise ValueError('"%s" app depends on "%s"' % (self.name, ', '.join(self.dependencies)))
        return super().ready()


class PropertyRequiredMixin:
    """
    View mixin that validates `property` in session. If it does not, page will
    be redirected to `GuestBasePropertyView` to let user to select property.
    """

    def dispatch(self, request, *args, **kwargs):
        if 'property_id' in request.session and request.session['property_id']:
            return super().dispatch(request, *args, **kwargs)
        return redirect(reverse('guest_base:property') + '?next=' + request.path)


class RequestFormKwargsMixin:
    """
    View mixin which puts the request into the form kwargs.

    Note: Using this mixin requires you to pop the `request` kwarg
    out of the dict in the super of your form's `__init__`.
    """

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(request=self.request)
        return kwargs


class MobileTemplateMixin:
    """
    View mixin that replace `template_name` with mobile template.

    This mixin uses `django_user_agents` plugin to indicate if `user_agent` is
    mobile. And will check view is accessed from app through session. If one of 
    them is fulfilled `mobile_template_name` will be used if it is provided.
    """
    mobile_template_name = None

    def get_template_names(self):
        if self.request.session.get('app', False) or not self.request.user_agent.is_pc:
            if self.mobile_template_name:
                return [self.mobile_template_name]
        return super().get_template_names()


class JSONResponseMixin:
    """
    A view mixin that can be used to render a JSON response.
    """

    json_status = None
    json_errors = []
    json_data   = {}

    def render_to_json_response(self, context, **response_kwargs):
        """ Returns a JSON response, transforming 'context' to make the payload. """
        return JsonResponse(self.get_json_data(context), **response_kwargs)

    def get_json_data(self, context):
        """ Returns an object that will be serialized as JSON by json.dumps(). """
        data = self.json_data
        data['status'] = self.json_status or 'error'
        data['errors'] = self.json_errors
        return data
