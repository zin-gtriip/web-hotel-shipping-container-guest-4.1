from django.apps import AppConfig
from guest_base.mixins  import DependentAppConfigMixin


class PreArrivalOcrRequired(AppConfig):
    name            = 'pre_arrival_ocr_required'
    version         = '1.3.1'
    dependencies    = [
        'pre_arrival.apps.PreArrivalConfig',
    ]
