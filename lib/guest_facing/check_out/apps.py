from django.apps                import AppConfig
from guest_facing.core.mixins   import DependentAppConfigMixin


class CheckOutConfig(DependentAppConfigMixin, AppConfig):
    name            = 'check_out'
    dependencies    = [
        'guest_facing.core',
    ]
