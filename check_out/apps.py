from django.apps        import AppConfig
from guest_base.mixins  import DependentAppConfigMixin


class CheckOutConfig(DependentAppConfigMixin, AppConfig):
    name            = 'check_out'
    version         = '1.0.5'
    dependencies    = [
        'guest_base.apps.GuestBaseConfig',
    ]
