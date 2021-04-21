from django.apps                import AppConfig
from guest_facing.core.mixins   import DependentAppConfigMixin


class RegistrationConfig(DependentAppConfigMixin, AppConfig):
    name            = 'guest_facing.registration'
    dependencies    = [
        'guest_facing.core',
    ]
