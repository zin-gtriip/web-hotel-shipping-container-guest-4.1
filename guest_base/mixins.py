from django.conf import settings

class DependentAppConfigMixin:
    """
    A app mixin that verifies dependencies of an app.
    """

    dependencies = []

    def ready(self):
        if not all(depend in settings.INSTALLED_APPS for depend in self.dependencies):
            raise ValueError('"%s" app depends on %s' % (self.name, ', '.join(self.dependencies)))
        return super().ready()
