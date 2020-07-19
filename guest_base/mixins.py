from django.conf import settings

class DependentAppConfigMixin(object):
    dependencies = []

    def ready(self):
        if not all(depend in settings.INSTALLED_APPS for depend in self.dependencies):
            raise ValueError('"%s" app depends on %s' % (self.name, ', '.join(self.dependencies)))
        return super().ready()
