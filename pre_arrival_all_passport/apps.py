from django.apps import AppConfig
from guest_base.mixins  import DependentAppConfigMixin


class PreArrivalAllPassportConfig(AppConfig):
    name            = 'pre_arrival_all_passport'
    version         = '1.3.5'
    dependencies    = [
        'pre_arrival.apps.PreArrivalConfig',
    ]
