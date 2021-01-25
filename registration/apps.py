from django.apps        import AppConfig
from core.mixins        import DependentAppConfigMixin


class RegistrationConfig(DependentAppConfigMixin, AppConfig):
    name            = 'registration'
    version         = '1.3.4'
    dependencies    = [
        'core.apps.CoreConfig',
    ]
