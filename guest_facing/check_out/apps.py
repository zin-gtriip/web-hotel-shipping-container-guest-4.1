from django.apps                import AppConfig
from guest_facing.core.mixins   import DependentAppConfigMixin


class CheckOutConfig(DependentAppConfigMixin, AppConfig):
    name            = 'guest_facing.check_out'
    dependencies    = [
        'guest_facing.core',
    ]
