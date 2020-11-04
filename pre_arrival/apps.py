from django.apps        import AppConfig
from guest_base.mixins  import DependentAppConfigMixin


class PreArrivalConfig(DependentAppConfigMixin, AppConfig):
    name            = 'pre_arrival'
    version         = '1.0.1'
    dependencies    = [
        'guest_base.apps.GuestBaseConfig',
    ]
