from django.apps        import AppConfig
from guest_base.mixins  import DependentAppConfigMixin


class CheckOutConfig(DependentAppConfigMixin, AppConfig):
    name            = 'check_out'
    version         = '1.1.2'
    dependencies    = [
        'guest_base.apps.GuestBaseConfig',
    ]
