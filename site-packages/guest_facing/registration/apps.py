from django.apps        import AppConfig
from core.mixins        import DependentAppConfigMixin


class RegistrationConfig(DependentAppConfigMixin, AppConfig):
    name            = 'registration'
    dependencies    = [
        'guest_facing.core',
    ]
