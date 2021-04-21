from django.apps import AppConfig
from guest_base.mixins  import DependentAppConfigMixin


class PreArrivalAdhocGuestConfig(AppConfig):
    name            = 'pre_arrival_adhoc_guest'
    version         = '1.4.3'
    dependencies    = [
        'pre_arrival.apps.PreArrivalConfig',
        'pre_arrival_all_passport.apps.PreArrivalAllPassportConfig',
    ]
