from django.apps        import AppConfig
from core.mixins        import DependentAppConfigMixin


class RegistrationConfig(DependentAppConfigMixin, AppConfig):
    name            = 'registration'
    version         = '1.3.5'
    dependencies    = [
        'core.apps.CoreConfig',
    ]
