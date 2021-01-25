from django.apps        import AppConfig
from core.mixins        import DependentAppConfigMixin


class PreArrivalConfig(DependentAppConfigMixin, AppConfig):
    name            = 'pre_arrival'
    version         = '1.3.4'
    dependencies    = [
        'core.apps.CoreConfig',
    ]
