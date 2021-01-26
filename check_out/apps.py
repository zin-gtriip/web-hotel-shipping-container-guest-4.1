from django.apps        import AppConfig
from core.mixins        import DependentAppConfigMixin


class CheckOutConfig(DependentAppConfigMixin, AppConfig):
    name            = 'check_out'
    version         = '1.3.5'
    dependencies    = [
        'core.apps.CoreConfig',
    ]
